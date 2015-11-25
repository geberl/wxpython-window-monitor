# -*- coding: utf-8 -*-
__author__ = 'guenther@eberl.se'

# Import program components / modules from python standard library / non-standard modules.
import database
import mainframe
import wx

import logging
import logging.config
import os
import sys


class WxWindowMonitor(wx.App):
    def __init__(self):
        super(WxWindowMonitor, self).__init__()

        # Logging config on base-module level.
        logger = logging.getLogger(__name__)
        logging.config.fileConfig(r'logging_to_terminal.ini', disable_existing_loggers=False)
        # logging.config.fileConfig(r'logging_to_file.ini', disable_existing_loggers=False)
        # logging.config.fileConfig(r'logging_to_terminal_and_file.ini', disable_existing_loggers=False)

        # For sqlite: Check if database file exists, otherwise create.
        if database.database_config['type'] == 'sqlite':
            if not os.path.isfile(database.database_config['filename']):
                logger.info('Creating new sqlite database file ...')
                database.create_all_tables()
        elif database.database_config['type'] == 'postgresql':
            pass
        else:
            logger.error('Unsupported database type: "%s".' % database.database_config['type'])
            return

        # Show GUI.
        logger.debug('Loading GUI ...')
        self.frame = mainframe.MainFrame(None)
        self.SetTopWindow(self.frame)
        self.frame.Show()


if __name__ == '__main__':
    # Create object.
    app = WxWindowMonitor()

    # Loop.
    app.MainLoop()

    # Exit with default exit code 0.
    sys.exit()
