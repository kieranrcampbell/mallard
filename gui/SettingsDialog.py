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
        self.SetSize((400, 400))


    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        gs = wx.GridSizer(6, 2, 5, 5)

        # 5 settings so 6 hboxes
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)

        # texts
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
        self.txt1 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt2 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt3 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt4 = wx.TextCtrl(self, size=(50, 30), id=-1)
        self.txt5 = wx.TextCtrl(self, size=(50, 30), id=-1)

        hbox1.Add(label1, flag = wx.ALIGN_LEFT | wx.ALL | wx.EXPAND, border=5)
        hbox1.Add(self.txt1, flag = wx.ALL | wx.EXPAND, border=5)

        hbox2.Add(label2, flag = wx.ALL | wx.EXPAND, border=5)
        hbox2.Add(self.txt2, flag = wx.ALL | wx.EXPAND, border=5)

        hbox3.Add(label3, flag = wx.ALL | wx.EXPAND, border=5)
        hbox3.Add(self.txt3, flag = wx.ALL | wx.EXPAND, border=5)

        hbox4.Add(label4, flag = wx.ALL | wx.EXPAND, border=5)
        hbox4.Add(self.txt4, flag = wx.ALL | wx.EXPAND, border=5)

        hbox5.Add(label5, flag = wx.ALL | wx.EXPAND, border=5)
        hbox5.Add(self.txt5, flag = wx.ALL | wx.EXPAND, border=5)

        btnOk = wx.Button(self, label= "OK", size=(80,30))
        btnCnl = wx.Button(self, label = "Cancel", size=(80,30))

        btnOk.Bind(wx.EVT_BUTTON, self.onOk)
        btnCnl.Bind(wx.EVT_BUTTON, self.onCancel)

        hbox6.Add(btnOk, flag = wx.ALL | wx.EXPAND, border = 5)
        hbox6.Add(btnCnl, flag = wx.ALL | wx.EXPAND, border = 5)

        vbox.Add(hbox1, flag = wx.EXPAND | wx.ALIGN_LEFT, border=5)
        vbox.Add(hbox2, flag = wx.ALL | wx.ALIGN_LEFT, border=5)
        vbox.Add(hbox3, flag = wx.ALL | wx.ALIGN_LEFT, border=5)
        vbox.Add(hbox4, flag = wx.ALL | wx.ALIGN_LEFT, border=5)
        vbox.Add(hbox5, flag = wx.ALL | wx.ALIGN_LEFT, border=5)
        vbox.Add(hbox6, flag = wx.ALL | wx.ALIGN_LEFT, border=5)
        

        self.SetSizer(vbox)
        vbox.Fit(self)

    def setTextFields(self, settings):
        self.settings = settings
        self.txt1.SetValue(str(self.settings.clockCyclesPerVoltage))
        self.txt2.SetValue(str(self.settings.voltageMin))
        self.txt3.SetValue(str(self.settings.voltageMax))
        self.txt4.SetValue(str(self.settings.intervalsPerSweep))
        self.txt5.SetValue(str(self.settings.sweeps))


    def onOk(self, event):
        # do self settings here
        self.Destroy()

    def onCancel(self, event):
        self.Destroy()

    def getSettings(self):
        return self.settings
