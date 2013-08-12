#!/usr/bin/python

"""

Main frame of Mallard application.

kieran.renfrew.campbell@cern.ch


"""

import wx
import matplotlib
import pylab

from capturepane import CapturePane
from capturenotebook import CaptureNotebook
from settingsdialog import GlobalSettingsDialog

from mallard.core.session import GlobalSession


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

        self.globalSession = GlobalSession()
        self.globalSession.statusCallback = self.setSBText

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


        fileLoadSettings = fileMenu.Append(wx.ID_ANY, 
                                           'Load settings from existing capture',
                                           'Load settings into capture')
        fileMenu.AppendSeparator()
        filePreferences = fileMenu.Append(wx.ID_ANY,
                                          "Preferences",
                                          "Global Settings")

        fileMenu.AppendSeparator()
        
        fileQuitItem = fileMenu.Append(wx.ID_EXIT,
                                       'Quit', 'Quit Application')
        
        menubar.Append(fileMenu, '&File')


        # capture menu
        captureMenu = wx.Menu()
        captureSettings = captureMenu.Append(wx.ID_ANY, "Settings",
                                          "Current Capture Settings")
        captureKill = captureMenu.Append(wx.ID_ANY, "Kill Capture",
                                         "Kill Running Capture")
        menubar.Append(captureMenu, '&Capture')

        changeName = captureMenu.Append(wx.ID_ANY, "Rename session",
                                        "Rename current session")

        self.SetMenuBar(menubar)

        # Graph menu
        graphMenu = wx.Menu()
        clearGraph = graphMenu.Append(wx.ID_ANY, "Clear all", "Clear all")

        menubar.Append(graphMenu, '&Graph')

        # Help menu
        helpMenu = wx.Menu()
        docMenu = helpMenu.Append(wx.ID_ANY, "Documentation", "Show documentation")
        aboutMenu = helpMenu.Append(wx.ID_ANY, "About", "About")

        menubar.Append(helpMenu, '&Help')

        # file events
        self.Bind(wx.EVT_MENU, self.onNew, fileNewCapture)
        self.Bind(wx.EVT_MENU, self.onSave, fileSaveCapture)
        self.Bind(wx.EVT_MENU, self.onSaveAs, fileSaveCaptureAs)
        self.Bind(wx.EVT_MENU, self.onClose, fileCloseCapture)
        self.Bind(wx.EVT_MENU, self.onLoadSettings, fileLoadSettings)
        self.Bind(wx.EVT_MENU, self.onPreferences, filePreferences)
        self.Bind(wx.EVT_MENU, self.onQuit, fileQuitItem)

        # capture menu events
        self.Bind(wx.EVT_MENU, self.onCaptureSettings,
                  captureSettings)
        self.Bind(wx.EVT_MENU, self.onChangeName, changeName)
        self.Bind(wx.EVT_MENU, self.onKillCapture, captureKill)

        # graph events
        self.Bind(wx.EVT_MENU, self.onClearGraph, clearGraph)

        # help events
        self.Bind(wx.EVT_MENU, self.onDocumentation, docMenu)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutMenu)

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
        self.notebook.addTab(self.globalSession)

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

                name = self.notebook.getOpenSession().settings.name
                self.notebook.SetPageText(
                    self.notebook.GetSelection(), name  )

                                       


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


    def onPreferences(self, event):
        """
        User selects to edit global preferences
        """
        sdlg = GlobalSettingsDialog(None)
        sdlg.setSettings(self.globalSession.getSettings())
        sdlg.ShowModal()
        self.globalSession.setSettings(sdlg.getSettings())

        
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


    def onKillCapture(self, event):

        if self.assertOpenCapture():
            if self.notebook.getOpenSession().isCapturing():
                self.notebook.getOpenSession().killCapture()

            else:
                wx.MessageBox('No capture in progress', 'Error',
                              wx.OK | wx.ICON_INFORMATION)

    def onAbout(self, event):
        """
        When user clicks help -> about
        """
        description = "Data Acquisition for CRIS. Created as part of the \n Cern summer student programme 2013."

        info = wx.AboutDialogInfo()


        info.SetName('Mallard for CRIS')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetWebSite('http://kieranrcampbell.github.io/mallard/')
        info.AddDeveloper('Kieran R Campbell')

        wx.AboutBox(info)

    def onDocumentation(self, event):
        """
        When user clicks help -> documentation
        """
        # os.filestart("doc.pdf")
        

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


    def displayError(self, msg):
        """
        Displays msg as an error message in a pop up box
        """
        wx.MessageBox(str(msg), 'Error',
                      wx.OK | wx.ICON_INFORMATION)

    def guiExceptHook(self, type, value, tb):
        """
        Exception hook for main program
        """
        self.displayError(type + value)
