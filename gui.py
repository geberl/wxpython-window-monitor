# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Window Monitor"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 300,55 ), wx.DefaultSize )
		
		MainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.MainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.MainPanel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.MainPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.MainPanel.SetMinSize( wx.Size( 250,100 ) )
		
		PanelSizer = wx.BoxSizer( wx.VERTICAL )
		
		MonitoringSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ButtonStartMonitoring = wx.Button( self.MainPanel, wx.ID_ANY, _(u"Start"), wx.DefaultPosition, wx.DefaultSize, 0 )
		MonitoringSizer.Add( self.ButtonStartMonitoring, 1, wx.ALL, 5 )
		
		self.ButtonStopMonitoring = wx.Button( self.MainPanel, wx.ID_ANY, _(u"Stop"), wx.DefaultPosition, wx.DefaultSize, 0 )
		MonitoringSizer.Add( self.ButtonStopMonitoring, 1, wx.ALL, 5 )
		
		self.ButtonRunOnce = wx.Button( self.MainPanel, wx.ID_ANY, _(u"Run once"), wx.DefaultPosition, wx.DefaultSize, 0 )
		MonitoringSizer.Add( self.ButtonRunOnce, 1, wx.ALL, 5 )
		
		
		PanelSizer.Add( MonitoringSizer, 1, wx.EXPAND, 5 )
		
		TimeSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.DateTimeText = wx.StaticText( self.MainPanel, wx.ID_ANY, _(u"?"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.DateTimeText.Wrap( -1 )
		TimeSizer.Add( self.DateTimeText, 1, wx.ALIGN_CENTER_HORIZONTAL, 50 )
		
		
		PanelSizer.Add( TimeSizer, 0, wx.EXPAND, 5 )
		
		self.Gauge = wx.Gauge( self.MainPanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
		self.Gauge.SetValue( 0 ) 
		self.Gauge.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
		self.Gauge.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		PanelSizer.Add( self.Gauge, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.MainPanel.SetSizer( PanelSizer )
		self.MainPanel.Layout()
		PanelSizer.Fit( self.MainPanel )
		MainSizer.Add( self.MainPanel, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 0 )
		
		
		self.SetSizer( MainSizer )
		self.Layout()
		MainSizer.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

