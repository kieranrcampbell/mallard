#!/usr/bin/python

"""
Individual page in the capture notebook

kieran.renfrew.campbell@cern.ch
"""


import wx

from core import CaptureSession
from core.SessionSettings import SessionSettings
from SettingsDialog import SettingsDialog


class CapturePane(wx.Panel):
    """ 
    Represents an individual tab in CaptureNotebook
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent,
                          id = wx.ID_ANY)

        # main session that does all analysis
        self.session = CaptureSession()
        self.createPanel()

    def createPanel(self):
        """
        Creates main panel
        """

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # upper (display) box
        self.upperBox = wx.BoxSizer(wx.HORIZONTAL)
        self.settingsSizer = wx.GridSizer(2, 1, 5, 5)
        self.createDisplayBox()

        # control box
        self.bottomControlBox = wx.BoxSizer(wx.HORIZONTAL)
        self.startButton = wx.Button(self, label='Start Capture',
                                     size=(120, 30))
        self.startButton.Bind(wx.EVT_BUTTON, self.onStartCapture)
        self.bottomControlBox.Add(self.startButton, 1,
                                  flag = wx.ALL | wx.ALIGN_BOTTOM | \
                                      wx.ALIGN_RIGHT, border = 10)
 

        # add all sizers
        self.vbox.Add(self.upperBox, 
                      flag = wx.ALL ,
                      border = 10)

        self.vbox.Add(self.bottomControlBox,
                      flag = wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT,
                      border = 10)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)


    
    def createDisplayBox(self):
        """ 
        Creates the upper settings & graph display
        """
        self.settingsBox = wx.ListBox(self, -1, size=(200, 180))

        self.settingsButton = wx.Button(self, label='Edit',
                                        size=(80, 30))

        self.settingsButton.Bind(wx.EVT_BUTTON, self.btnChangeSettings)

        self.settingsSizer.AddMany( [ (self.settingsBox, 0, wx.ALIGN_LEFT),
                                      (self.settingsButton, 0, 
                                       wx.ALIGN_LEFT ) ] )

        self.setSettings()

        self.upperBox.Add(self.settingsSizer,
                          flag = wx.ALL | wx.ALIGN_TOP | wx.ALIGN_LEFT\
                              | wx.EXPAND,
                          border = 10)



    def onStartCapture(self, event):
        """
        Begin data capture
        """
        self.session.startCapture()
        self.session.createGraphFromSession()


    def changeSettings(self):
        """
        Called to change settings in
        a particular tab
        """
        sdlg = SettingsDialog(None)
        sdlg.setTextFields(self.session.settings)
                        
        sdlg.ShowModal()
        sdlg.Destroy()
        self.session.settings = sdlg.getSettings()
        self.setSettings()

    def loadSessionFromFile(self, path):
        """
        Loads an entire session (settings + data)
        from a file
        """
        self.loadSettingsFromFile(path)

    def loadSettingsFromFile(self, path):
        """
        Loads just the settings from file
        """
        self.session.loadSession(path)
        self.setSettings()



    def btnChangeSettings(self, event):
        self.changeSettings()

    def getSession(self):
        """
        Returns the main CaptureSession running
        """
        return self.session

    def setSettings(self):
        """
        Creates the appropriate session settings in the listbox
        """
        self.settingsBox.Clear()
        
        self.settingsBox.Insert("Input channel: " + \
                                    str(self.session.settings.inputChannel),
                                0)

        self.settingsBox.Insert("Output channel: " + \
                                    str(self.session.settings.outputChannel),  1)

        self.settingsBox.Insert("Cycles per volt: " + \
                                    str(self.session.settings.clockCyclesPerVoltage), 
                                2)
        
        self.settingsBox.Insert( "Voltage min: " + \
                                     str(self.session.settings.voltageMin),
                                 3)

        self.settingsBox.Insert( "Voltage max: " + \
                                     str(self.session.settings.voltageMax),
                                 4)

        self.settingsBox.Insert( "Intervals per sweep: " + \
                                     str(self.session.settings.intervalsPerSweep), 
                                 5)

        self.settingsBox.Insert( "Sweeps: " + \
                                     str(self.session.settings.sweeps), 
                                 6)
        

