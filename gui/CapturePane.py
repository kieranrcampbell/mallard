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
#        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        # # as per example, create mpl Figure and FigCanvas objects
        # self.dpi = 100
        # self.fig = Figure((10.0, 7.0), dpi = self.dpi)
        # self.canvas = FigCanvas(self.panel, -1, self.fig)

        # self.axes = self.fig.add_subplot(111)

        # self.axes.grid(True)
        # # bind pick event for clicking on one of the bars
        # self.canvas.mpl_connect('pick_event', self.on_pick)

        # self.axes.set_axis_bgcolor('black')
        # self.axes.set_title('Data capture', size=10)

        # pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        # pylab.setp(self.axes.get_yticklabels(), fontsize=8)
#        self.vbox.Add(self.canvas, -1, wx.LEFT | wx.TOP | wx.GROW)

        # upper (display) box
        self.upperBox = wx.BoxSizer(wx.HORIZONTAL)
        self.settingsSizer = wx.BoxSizer(wx.VERTICAL)
        self.createDisplayBox()

        # control box
        self.bottomControlBox = wx.BoxSizer(wx.HORIZONTAL)
        self.startButton = wx.Button(self, label='Start Capture',
                                     size=(120, 30))
        self.startButton.Bind(wx.EVT_BUTTON, self.onStartCapture)
        self.bottomControlBox.Add(self.startButton, 1,
                                  flag = wx.ALIGN_RIGHT, border = 10)
 

        # add all sizers
        self.vbox.Add(self.upperBox, 
                      flag = wx.ALL |wx.ALIGN_LEFT | wx.ALIGN_TOP,
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

        self.settingsSizer.Add(self.settingsBox, 1, 
                               wx.ALL | wx.ALIGN_LEFT, 5)
        self.settingsSizer.Add(self.settingsButton, 1,
                               wx.ALL | wx.ALIGN_LEFT, 5)
        self.setSettings(self.session.settings)

        self.upperBox.Add(self.settingsSizer,
                          flag = wx.ALL | wx.ALIGN_TOP | wx.ALIGN_LEFT,
                          border = 10)

    def drawFigure(self):
        """
        Draws plot(s)
        """
        x = y = range(4)
        self.axes.plot(x, y)
        self.canvas.draw()
        
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        dlg = wx.MessageDialog(
            self, 
            msg, 
            "Click!",
            wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal() 
        dlg.Destroy()        


    def onStartCapture(self, event):
        """
        Begin data capture
        """
        print "Beginning capture"
    def changeSettings(self):
        """
        Called to change settings in
        a particular tab
        """
        sdlg = SettingsDialog(None)
        sdlg.setTextFields(self.session.settings)
                        
        sdlg.ShowModal()
        sdlg.Destroy()

    def btnChangeSettings(self, event):
        self.changeSettings()

    def getSession(self):
        """
        Returns the main CaptureSession running
        """
        return self.session

    def setSettings(self, settings):
        """
        Creates the appropriate session settings in the listbox
        """
        self.settingsBox.Insert("Cycles per volt: " + \
                                       str(settings.clockCyclesPerVoltage), 0)
        self.settingsBox.Insert( "Voltage min: " + \
                                       str(settings.voltageMin), 1)
        self.settingsBox.Insert( "Voltage max: " + \
                                       str(settings.voltageMax), 2)
        self.settingsBox.Insert( "Intervals per sweep: " + \
                                       str(settings.intervalsPerSweep), 3)
        self.settingsBox.Insert( "Sweeps: " + \
                                       str(settings.intervalsPerSweep), 4)
                                   

