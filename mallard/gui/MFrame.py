#!/usr/bin/python

"""

Main frame of Mallard application.

kieran.renfrew.campbell@cern.ch


"""

import wx
import matplotlib
import pylab

from CapturePane import CapturePane
from CaptureNotebook import CaptureNotebook



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

        self.sb = self.CreateStatusBar()

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
        fileSaveCaptureAs = fileMenu.Append(wx.ID_SAVE, "Save Capture As...",
                                          "Save Capture As")

        fileCloseCapture = fileMenu.Append(wx.ID_ANY, 'Close Capture',
                                           'Close current capture')

        fileMenu.AppendSeparator()
        fileLoadSettings = fileMenu.Append(wx.ID_ANY, 
                                           'Load settings from existing capture',
                                           'Load settings into capture')
        fileMenu.AppendSeparator()
        
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
        showGraph = graphMenu.Append(wx.ID_ANY, "Show graph", "Show graph")
        clearGraph = graphMenu.Append(wx.ID_ANY, "Clear all", "Clear all")

        menubar.Append(graphMenu, '&Graph')

        # file events
        self.Bind(wx.EVT_MENU, self.onNew, fileNewCapture)
        self.Bind(wx.EVT_MENU, self.onSave, fileSaveCapture)
        self.Bind(wx.EVT_MENU, self.onSaveAs, fileSaveCaptureAs)
        self.Bind(wx.EVT_MENU, self.onClose, fileCloseCapture)
        self.Bind(wx.EVT_MENU, self.onLoadSettings, fileLoadSettings)
        self.Bind(wx.EVT_MENU, self.onQuit, fileQuitItem)

        # capture menu events
        self.Bind(wx.EVT_MENU, self.onCaptureSettings,
                  captureSettings)
        self.Bind(wx.EVT_MENU, self.onChangeName, changeName)

        # graph events
        self.Bind(wx.EVT_MENU, self.onShowGraph, showGraph)
        self.Bind(wx.EVT_MENU, self.onClearGraph, clearGraph)

    def createPanel(self):
        """
        Creates main notebook
        """
        self.panel = wx.Panel(self)
        self.notebook = CaptureNotebook(self.panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, flag = wx.ALL | wx.EXPAND, border=5)
        self.panel.SetSizer(sizer)
        self.Layout()

        
    # begin event functions
    def onNew(self, event):
        """
        User has indicated new capture
        """
        self.notebook.addTab("New tab", self.setSBText)

    def onSave(self, event):
        """
        User has indicated capture save
        """
        if self.assertOpenCapture():

            if self.notebook.getOpenSession().settings.filename \
                    is "":
                self.onSaveAs(event)
        
            else:
                self.notebook.getOpenSession().saveSession()

    def onSaveAs(self, event):
        """
        Save capture as specific name
        """
        if self.assertOpenCapture():

            name = self.notebook.getOpenSession().settings.name
            saveFileDialog = wx.FileDialog(self, "Save As", "", 
                                           name + '.csv',
                                           "CSV files (*.csv)|*.csv",
                                           wx.FD_SAVE)
            if saveFileDialog.ShowModal() == wx.ID_OK:
                path = saveFileDialog.GetPath()
                self.notebook.getOpenSession().saveSessionAs(path)
                                       


    def onClose(self, event):
        """
        Called to close an open capture
        """
        if self.assertOpenCapture():
            self.notebook.closeTab()

        
    def onLoadSettings(self, event):
        """
        Loads settings only from open file
        """
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "CSV files (*.csv)|*.csv",
                                       wx.FD_OPEN)
        if openFileDialog.ShowModal() == wx.ID_OK:
            path = openFileDialog.GetPath()

            self.notebook.addTab("")
            self.notebook.getLastTab().loadSettingsFromFile(path)

            self.notebook.SetPageText(
                self.notebook.GetSelection(), 
                self.notebook.getLastTab().session.getName() )


    def onQuit(self, event):
        """
        Called to exit program
        """
        self.Close()

    def onCaptureSettings(self, event):
        """
        Called to edit a given capture's settings
        """
        if self.assertOpenCapture():
            self.notebook.getOpenTab().changeSettings()

    def onShowGraph(self, event):
        if self.assertOpenCapture():
            if not self.notebook.getOpenSession().hasData:
                wx.MessageBox('No open captures', 'Error',
                              wx.OK | wx.ICON_INFORMATION)
                return

            self.notebook.getOpenSession().createGraphFromSession()

    def onClearGraph(self, event):
        self.notebook.getOpenSession().clearGraph()

    def onChangeName(self, event):

        if self.assertOpenCapture():
            name = self.notebook.getOpenSession().getName()
            dlg = wx.TextEntryDialog(
                self, 'Enter new name', 'Rename', name)

            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                self.notebook.getOpenSession().setName(name)
                self.notebook.SetPageText(
                    self.notebook.GetSelection(), name )


    def assertOpenCapture(self):
        """
        Makes sure there exists a CapturePane
        to perform action on
        """
        if len(self.notebook.getTabList()) == 0:
            wx.MessageBox('No open captures', 'Error',
                          wx.OK | wx.ICON_INFORMATION)
            return False

        return True

    def setSBText(self, text):
        """
        Sets the text on the status bar
        """
        self.sb.SetStatusText(text)
