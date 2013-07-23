#!/usr/bin/python

"""
Individual page in the capture notebook

kieran.renfrew.campbell@cern.ch
"""


import wx
import matplotlib
import numpy as np
from pylab import *

matplotlib.interactive( True )

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg 
from matplotlib.backends.backend_wxagg import \
    NavigationToolbar2WxAgg as NavigationToolbar


from mallard.core.SessionSettings import SessionSettings
from mallard.core.CaptureSession import CaptureSession 
from GraphManager import GraphManager
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
        self.subplot = None

        self.createPanel()

        self.graphManager = GraphManager(self.subplot, self.canvas)
        self.session.registerGraphManager(self.graphManager)


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
                                       wx.ALIGN_LEFT | wx.ALIGN_TOP ) ] )

        self.setSettings()
        self.createGraphBox()

        self.upperBox.Add(self.settingsSizer,
                          flag = wx.ALL | wx.ALIGN_TOP | wx.ALIGN_LEFT\
                              | wx.EXPAND,
                          border = 10)
        self.upperBox.Add(self.graphBoxSizer,
                          flag = wx.ALL | wx.ALIGN_TOP | wx.ALIGN_LEFT\
                              | wx.EXPAND,
                          border = 10)

    def createGraphBox(self):
        """
        Creates box to display update graph in
        """
        self.graphBox = wx.StaticBox(self, -1, "Graph")
        self.graphBoxSizer = wx.StaticBoxSizer(self.graphBox, wx.VERTICAL)
        
        self.graphPanel = wx.Panel(self, wx.ID_ANY)
        self.figure = Figure((7,5), None)
        self.canvas = FigureCanvasWxAgg(self.graphPanel,
                                        -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        gvbox = wx.BoxSizer(wx.VERTICAL)
        gvbox.Add(self.canvas, flag = wx.ALIGN_TOP)
        gvbox.Add(self.toolbar, flag = wx.EXPAND)
        self.graphPanel.SetSizer(gvbox)

        self.graphBoxSizer.Add(self.graphPanel, flag = wx.ALL | \
                                   wx.ALIGN_TOP | wx.ALIGN_LEFT,
                               border = 10 )
        

        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_xlabel('Volts (V)')
        self.subplot.set_ylabel('Count')
        print "subplot type: " + str(self.subplot)


    def onStartCapture(self, event):
        """
        Begin data capture
        """
        self.graphManager.clearPlot()
        self.session.startCapture()



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
        
        self.settingsBox.Insert("Counter channel: " + \
                                str(self.session.settings.counterChannel),
                                0)

        self.settingsBox.Insert("AO channel: " + \
                                str(self.session.settings.aoChannel),  1)

        self.settingsBox.Insert("AI channel: " + \
                                str(self.session.settings.aiChannel), 2)
        
        self.settingsBox.Insert("Clock channel: " + \
                                str(self.session.settings.clockChannel), 3)


        self.settingsBox.Insert("Cycles per volt: " + \
                                str(self.session.settings.clockCyclesPerVoltage), 
                                4)
        
        self.settingsBox.Insert( "Voltage min: " + \
                                 str(self.session.settings.voltageMin),
                                 5)

        self.settingsBox.Insert( "Voltage max: " + \
                                 str(self.session.settings.voltageMax),
                                 6)

        self.settingsBox.Insert( "Intervals per scan: " + \
                                 str(self.session.settings.intervalsPerScan), 
                                 7)

        self.settingsBox.Insert( "Scans: " + \
                                 str(self.session.settings.scans), 
                                 8)
        
