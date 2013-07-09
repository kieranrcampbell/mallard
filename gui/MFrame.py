#!/usr/bin/python

"""
wxFrame test 
"""

import wx
import matplotlib
import pylab

from CapturePane import CapturePane
from CaptureNotebook import CaptureNotebook


matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar



class MFrame(wx.Frame):
    """

    Main frame class for the Mallard
    data acquisition project

    kieran.renfrew.campbell@cern.ch

    """

    def __init__(self, parent, mtitle, msize):
        super(MFrame, self).__init__(parent, 
                                     title = mtitle,
                                     size = msize)

        # class variables
        self.panel = None
        self.notebook = None

        self.InitUI()


    def InitUI(self):
        """
        UI initialisation
        """
        self.createMenu()
        self.createPanel()
        self.Centre()
        self.Show()

    def createMenu(self):
        """
        Add top menubar
        """
        # menu stuff
        menubar = wx.MenuBar()

        # File menu
        fileMenu = wx.Menu()
        fileNewCapture = fileMenu.Append(wx.ID_NEW, "New Capture",
                                         "New Capture")
        fileSaveCapture = fileMenu.Append(wx.ID_SAVE, "Save Capture",
                                          "Save Capture")
        fileOpenCapture = fileMenu.Append(wx.ID_ANY, 'Open Capture',
                                          'Open existing capture')
        fileQuitItem = fileMenu.Append(wx.ID_EXIT,
                                       'Quit', 'Quit Application')
        
        menubar.Append(fileMenu, '&File')


        # capture menu
        captureMenu = wx.Menu()
        captureSettings = captureMenu.Append(wx.ID_ANY, "Settings",
                                          "Current Capture Settings")
        menubar.Append(captureMenu, '&Capture')

        changeName = captureMenu.Append(wx.ID_ANY, "Rename session",
                                        "Rename current session")

        self.SetMenuBar(menubar)

        # Graph menu
        graphMenu = wx.Menu()
        menubar.Append(graphMenu, '&Graph')

        # file events
        self.Bind(wx.EVT_MENU, self.onNew, fileNewCapture)
        self.Bind(wx.EVT_MENU, self.onSave, fileSaveCapture)
        self.Bind(wx.EVT_MENU, self.onCaptureOpen, fileOpenCapture)
        self.Bind(wx.EVT_MENU, self.onQuit, fileQuitItem)

        # capture menu events
        self.Bind(wx.EVT_MENU, self.onCaptureSettings,
                  captureSettings)
        self.Bind(wx.EVT_MENU, self.onChangeName, changeName)

    def createPanel(self):
        """
        Creates main notebook
        """
        self.panel = wx.Panel(self)
        self.notebook = CaptureNotebook(self.panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, flag = wx.ALL | wx.EXPAND, border=5)
        self.notebook.addTab("new")
        self.panel.SetSizer(sizer)
        self.Layout()

        
    # begin event functions
    def onNew(self, event):
        """
        User has indicated new capture
        """
        self.notebook.addTab("New tab")

    def onSave(self, event):
        """
        User has indicated capture save
        """
        print ('Save capture')

    def onCaptureOpen(self, event):
        """
        Called to open an existing capture
        """
        
    def onQuit(self, event):
        """
        Called to exit program
        """
        self.Close()

    def onCaptureSettings(self, event):
        """
        Called to edit a given capture's settings
        """
        if self.notebook.GetPageCount() == 0:
            wx.MessageBox('No open captures', 'Error',
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.notebook.getOpenTab().changeSettings()

    def onChangeName(self, event):
        name = self.notebook.getOpenTab().session.getName()
        dlg = wx.TextEntryDialog(
            self, 'Enter new name', 'Rename', name)

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            self.notebook.getOpenTab().session.setName(name)
            self.notebook.SetPageText(
                self.notebook.GetSelection(), name )




