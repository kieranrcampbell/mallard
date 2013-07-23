#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

For changing settings

"""

import wx
from mallard.core import *

class SettingsDialog(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.SetTitle("Edit Settings")
        self.InitUI()
        self.SetSize((300, 420))


    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        gs = wx.GridSizer(5, 2, 5, 5)


        # texts
        label6 = wx.StaticText(self, label="Counter channel",
                               style = wx.ALIGN_LEFT | wx.ALL)
        label7 = wx.StaticText(self, label="AO channel",
                               style = wx.ALIGN_LEFT | wx.ALL)

        label8 = wx.StaticText(self, label="AI channel",
                               style = wx.ALIGN_LEFT | wx.ALL)

        label9 = wx.StaticText(self, label="Clock channel",
                               style = wx.ALIGN_LEFT | wx.ALL)

        label1 = wx.StaticText(self, label="Clock cycles per voltage: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label2 = wx.StaticText(self, label="Min voltage: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label3 = wx.StaticText(self, label="Max voltage: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label4 = wx.StaticText(self, label="Intervals per scan: ",
                              style = wx.ALIGN_LEFT | wx.ALL)
        label5 = wx.StaticText(self, label="Scans: ",
                              style = wx.ALIGN_LEFT | wx.ALL)

        # text boxes
        self.txt6 = wx.TextCtrl(self, size=(100,30), id=-1)
        self.txt7 = wx.TextCtrl(self, size=(100,30), id=-1)
        self.txt8 = wx.TextCtrl(self, size=(100,30), id=-1)
        self.txt9 = wx.TextCtrl(self, size=(100,30), id=-1)
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
                      (label8, 0, wx.ALIGN_LEFT),
                      (self.txt8, 0, wx.ALIGN_RIGHT),
                      (label9, 0, wx.ALIGN_LEFT),
                      (self.txt9, 0, wx.ALIGN_RIGHT),
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
        self.txt6.SetValue(str(self.settings.counterChannel))
        self.txt7.SetValue(str(self.settings.aoChannel))
        self.txt8.SetValue(str(self.settings.aiChannel))
        self.txt9.SetValue(str(self.settings.clockChannel))
        self.txt1.SetValue(str(self.settings.clockCyclesPerVoltage))
        self.txt2.SetValue(str(self.settings.voltageMin))
        self.txt3.SetValue(str(self.settings.voltageMax))
        self.txt4.SetValue(str(self.settings.intervalsPerScan))
        self.txt5.SetValue(str(self.settings.scans))


    def onOk(self, event):
        # do self settings here
        self.settings.counterChannel = self.txt6.GetValue()
        self.settings.aoChannel = self.txt7.GetValue()
        self.settings.aiChannel = self.txt8.GetValue()
        self.settings.clockChannel = self.txt9.GetValue()
        self.settings.clockCyclesPerVoltage = self.txt1.GetValue()
        self.settings.voltageMin = self.txt2.GetValue()
        self.settings.voltageMax = self.txt3.GetValue()
        self.settings.intervalsPerScan = self.txt4.GetValue()
        self.settings.scans = self.txt5.GetValue()

        self.Destroy()

    def onCancel(self, event):
        self.Destroy()

    def getSettings(self):
        return self.settings
