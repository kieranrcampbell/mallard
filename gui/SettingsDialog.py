#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

For changing settings

"""

import wx
from core.SessionSettings import SessionSettings

class SettingsDialog(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.SetTitle("Edit Settings")
        self.InitUI()
        self.SetSize((300, 350))


    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        gs = wx.GridSizer(5, 2, 5, 5)


        # texts
        label6 = wx.StaticText(self, label="Input channel",
                               style = wx.ALIGN_LEFT | wx.ALL)
        label7 = wx.StaticText(self, label="Output channel",
                               style = wx.ALIGN_LEFT | wx.ALL)

        label1 = wx.StaticText(self, label="Clock cycles per voltage: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label2 = wx.StaticText(self, label="Min voltage: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label3 = wx.StaticText(self, label="Max voltage: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label4 = wx.StaticText(self, label="Intervals per sweep: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label5 = wx.StaticText(self, label="Sweeps: ",
                              style = wx.ALIGN_LEFT | wx.ALL)

        # text boxes
        self.txt6 = wx.TextCtrl(self, size=(100,30), id=-1)
        self.txt7 = wx.TextCtrl(self, size=(100,30), id=-1)
        self.txt1 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt2 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt3 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt4 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt5 = wx.TextCtrl(self, size=(50, 30), id=-1)

        # buttons
        btnOk = wx.Button(self, label= "OK", size=(80,30))
        btnCnl = wx.Button(self, label = "Cancel", size=(80,30))

        btnOk.Bind(wx.EVT_BUTTON, self.onOk)
        btnCnl.Bind(wx.EVT_BUTTON, self.onCancel)

        gs.AddMany( [ (label6, 0, wx.ALIGN_LEFT),
                      (self.txt6, 0, wx.ALIGN_RIGHT),
                      (label7, 0, wx.ALIGN_LEFT),
                      (self.txt7, 0, wx.ALIGN_RIGHT),
                      (label1, 0, wx.ALIGN_LEFT),
                      (self.txt1, 0, wx.ALIGN_RIGHT),
                      (label2, 0, wx.ALIGN_LEFT),
                      (self.txt2, 0, wx.ALIGN_RIGHT),
                      (label3, 0, wx.ALIGN_LEFT),
                      (self.txt3, 0, wx.ALIGN_RIGHT),
                      (label4, 0, wx.ALIGN_LEFT),
                      (self.txt4, 0, wx.ALIGN_RIGHT),
                      (label5, 0, wx.ALIGN_LEFT),
                      (self.txt5, 0, wx.ALIGN_RIGHT) ] )                     

        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(btnOk, 1, wx.ALL | wx.ALIGN_RIGHT)
        btnBox.Add(btnCnl, 1, wx.ALL | wx.ALIGN_RIGHT)

        vbox.Add(gs, border=10, flag=wx.EXPAND | wx.ALL)
        vbox.Add(btnBox, border=10, flag= wx.ALL)

        self.SetSizer(vbox)
        vbox.Fit(self)

    def setTextFields(self, settings):
        self.settings = settings
        self.txt6.SetValue(str(self.settings.inputChannel))
        self.txt7.SetValue(str(self.settings.outputChannel))
        self.txt1.SetValue(str(self.settings.clockCyclesPerVoltage))
        self.txt2.SetValue(str(self.settings.voltageMin))
        self.txt3.SetValue(str(self.settings.voltageMax))
        self.txt4.SetValue(str(self.settings.intervalsPerSweep))
        self.txt5.SetValue(str(self.settings.sweeps))


    def onOk(self, event):
        # do self settings here
        self.settings.inputChannel = self.txt6.GetValue()
        self.settings.outputChannel = self.txt7.GetValue()
        self.settings.clockCyclesPerVoltage = self.txt1.GetValue()
        self.settings.voltageMin = self.txt2.GetValue()
        self.settings.voltageMax = self.txt3.GetValue()
        self.settings.intervalsPerSweep = self.txt4.GetValue()
        self.settings.sweeps = self.txt5.GetValue()

        self.Destroy()

    def onCancel(self, event):
        self.Destroy()

    def getSettings(self):
        return self.settings
