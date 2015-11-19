# -*- coding: utf-8 -*-
__author__ = 'guenther@eberl.se'

# Import program components / modules from python standard library / non-standard modules.
import gui
import wx
import database

import logging
import logging.config
import os
import sys
import platform
import datetime
import threading
import time

import psutil
from pywinauto import findwindows
from pywinauto import handleprops


# Logging config on sub-module level.
logger = logging.getLogger(__name__)


class MainFrame(gui.MainFrame):
    def __init__(self, parent):
        gui.MainFrame.__init__(self, parent)
        logger.debug('Running __init__ ...')

        # Bind the "on close" event.
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Remember if user clicked on close while the thread was running.
        self.user_clicked_close = False

        # Bind the monitoring buttons.
        self.ButtonStartMonitoring.Bind(wx.EVT_BUTTON, self.start_monitoring)
        self.ButtonStopMonitoring.Bind(wx.EVT_BUTTON, self.stop_monitoring)
        self.ButtonRunOnce.Bind(wx.EVT_BUTTON, self.run_once)

        # Enable/Disable monitoring buttons correctly.
        self.ButtonStartMonitoring.Enable(True)
        self.ButtonStopMonitoring.Enable(False)
        self.ButtonRunOnce.Enable(True)
        self.DateTimeText.SetLabelText(u'Last action: -')

        # Determine if program is running compiled to *.exe/*.app or from Python interpreter.
        if hasattr(sys, 'frozen'):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(__file__)

        # Set the application icon, unsupported on Mac OS X.
        if platform.system() != 'Darwin':
            ico = wx.Icon(self.application_path + os.sep + 'icon.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

        # Refresh settings.
        self.continue_time_refresh = False
        self.refresh_gui_seconds = 0.25
        self.action_seconds = 10

        # Set the options of the gauge element.
        self.gauge_max_value = 100
        self.Gauge.SetRange(self.gauge_max_value)

    def run_once(self, event):
        logger.debug('Running script once (event Id %i).' % event.GetId())

        self.ButtonStartMonitoring.Enable(False)
        self.ButtonStopMonitoring.Enable(False)
        self.ButtonRunOnce.Enable(False)

        self.refresh_timer()
        process_watch_info = database.query_process_to_monitor()
        self.take_action(process_watch_info)

        self.ButtonStartMonitoring.Enable(True)
        self.ButtonStopMonitoring.Enable(False)
        self.ButtonRunOnce.Enable(True)

    def start_monitoring(self, event):
        logger.debug('Starting to do_monitoring thread/GUI (event Id %i).' % event.GetId())

        # Look in the database what processes should be monitored with details.
        process_watch_info = database.query_process_to_monitor()

        # Enable/Disable monitoring buttons correctly.
        self.ButtonStartMonitoring.Enable(False)
        self.ButtonStopMonitoring.Enable(True)
        self.ButtonRunOnce.Enable(False)

        # Start by doing what happens inside the loop otherwise, since the loop starts with a pause.
        self.refresh_timer()
        self.take_action(process_watch_info)

        # Setup loop exit variable and start thread.
        self.continue_time_refresh = True
        thread_0 = threading.Thread(target=self.do_monitoring, name='refresh time', args=[process_watch_info])
        thread_0.daemon = False
        thread_0.start()

        # Bind the window close event to the stop monitoring function.
        self.Bind(wx.EVT_CLOSE, self.stop_monitoring)

    def do_monitoring(self, process_watch_info):
        gauge_current_value = self.gauge_max_value
        while self.continue_time_refresh is True:
            try:
                # Delay next refresh some seconds.
                time.sleep(self.refresh_gui_seconds)

                # Take action always when the gauge hits 0.
                if gauge_current_value == 0:
                    # Refresh timer.
                    self.refresh_timer()

                    # Actually do the thing that should happen periodically (take screenshot, analyse file, etc.).
                    self.take_action(process_watch_info)

                # Set gauge to refresh value.
                if gauge_current_value <= 0:
                    gauge_current_value = 100
                else:
                    gauge_current_value -= self.gauge_max_value / (self.action_seconds / self.refresh_gui_seconds)
                self.Gauge.SetValue(gauge_current_value)

            except Exception as exc:
                logger.debug(exc)
                time.sleep(self.refresh_gui_seconds)

        # Run loop exit function only after loop finishes its last run.
        wx.CallAfter(self.exit_loop)

    def stop_monitoring(self, event):
        logger.debug('Stopped monitoring thread/GUI (event Id %i).' % event.GetId())

        # Disable all buttons. Only when the loop actually exits the start button is enabled again.
        self.ButtonStartMonitoring.Enable(False)
        self.ButtonStopMonitoring.Enable(False)
        self.ButtonRunOnce.Enable(False)

        # Exit loop in thread on next run. This is the next possibility for a clean exit.
        self.continue_time_refresh = False

        # Check and remember if the user clicked the window close button.
        if event.ClassName == 'wxCloseEvent':
            self.user_clicked_close = True

    def refresh_timer(self):
        # Refresh the line in the GUI where the last run time/date of take_action() is displayed.
        datetime_now = datetime.datetime.now()
        date_string_for_gui = datetime_now.strftime('%Y-%m-%d %H:%M:%S')
        self.DateTimeText.SetLabelText(u'Last action: ' + date_string_for_gui)
        self.MainPanel.Layout()  # needed for correct centered alignment when the date/time string length changes.

    def take_action(self, process_watch_info):
        logger.info('Taking action....')

        # Put info about all open windows into database.
        self.get_window_info()

        # Put info about specifically watched processes into database.
        for process_watch_db_id, process_watch_name in process_watch_info:
            self.get_process_info(process_watch_db_id, process_watch_name)

    @staticmethod
    def get_window_info():
        all_window_handles = findwindows.enum_windows()
        for window_handle in all_window_handles:
            if handleprops.isvisible(window_handle):
                pos_x = handleprops.rectangle(window_handle).left
                pos_y = handleprops.rectangle(window_handle).top
                size_x = handleprops.rectangle(window_handle).width()
                size_y = handleprops.rectangle(window_handle).height()
                title_name = handleprops.text(window_handle)
                class_name = handleprops.classname(window_handle)
                pid = handleprops.processid(window_handle)
                date_time = datetime.datetime.now()

                # Note: Minimized windows have negative pos_x and pos_y values (and smaller sizes).

                window_info = [pos_x, pos_y, size_x, size_y, title_name, class_name, pid, date_time]
                window_db_id = database.create_window_record(window_info)
                logger.info('OpenWindow record created in database (db_id %i).' % window_db_id)

    @staticmethod
    def get_process_info(process_watch_db_id, process_watch_name):
        process_instances = []
        for process in psutil.process_iter():
            try:
                if process.name() == process_watch_name:
                    process_instances.append(process)
            except psutil.Error:
                pass

        if len(process_instances) > 0:
            logger.debug('There are %s instances of process "%s" running.' %
                         (len(process_instances), process_watch_name))
            for n, process_instance in enumerate(process_instances):
                date_time = datetime.datetime.now()
                name = process_instance.name()
                instance = n
                pid = process_instance.pid
                parent_pic = process_instance.ppid()
                status = process_instance.status()
                user_name = process_instance.username()
                create_time = datetime.datetime.fromtimestamp(process_instance.create_time())
                command_line = str(process_instance.cmdline())
                connections = str(process_instance.connections())
                cpu_affinity = str(process_instance.cpu_affinity())
                cpu_percent = process_instance.cpu_percent()
                cpu_times = str(process_instance.cpu_times())
                executable_dir = process_instance.exe()
                io_stats = str(process_instance.io_counters())
                io_niceness = process_instance.ionice()
                memory_info = str(process_instance.memory_info())
                memory_info_extended = str(process_instance.memory_info_ex())
                memory_maps = str(process_instance.memory_maps())
                memory_percent = process_instance.memory_percent()
                num_ctx_switches = str(process_instance.num_ctx_switches())
                num_handles = process_instance.num_handles()
                num_threads = process_instance.num_threads()
                threads = str(process_instance.threads())
                niceness = process_instance.nice()
                open_files = str(process_instance.open_files())

                process_info = [process_watch_db_id, date_time, name, instance, pid, parent_pic, status, user_name,
                                create_time, command_line, connections, cpu_affinity, cpu_percent, cpu_times,
                                executable_dir, io_stats, io_niceness, memory_info, memory_info_extended, memory_maps,
                                memory_percent, num_ctx_switches, num_handles, num_threads, threads, niceness,
                                open_files]
                process_db_id = database.create_process_record(process_info)
                logger.info('Process record created in database (db_id %i).' % process_db_id)
        else:
            logger.warning('There is no instance of process %s running.' % process_watch_name)

    def exit_loop(self):
        # Enable/Disable monitoring buttons correctly.
        self.ButtonStartMonitoring.Enable(True)
        self.ButtonStopMonitoring.Enable(False)
        self.ButtonRunOnce.Enable(True)

        # Reset text and gauge.
        self.Gauge.SetValue(0)
        self.MainPanel.Layout()

        # Rebind window close event to the function that actually closes the window.
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Now close the window if user clicked on close button.
        if self.user_clicked_close:
            self.on_close(wx.CloseEvent)

    def on_close(self, event=None):
        if event:
            logger.debug('Closing GUI while thread was NOT running (event Id %i).')
        else:
            logger.debug('Closing GUI while thread was running.')
        self.Destroy()
