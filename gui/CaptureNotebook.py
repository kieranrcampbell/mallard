#!/usr/bin/python

"""
Main notebook for holding capture sessions

kieran.renfrew.campbell@cern.ch

"""

import wx

from CapturePane import CapturePane

class CaptureNotebook(wx.Notebook):
    """
    Notebook class
    """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent,
                             id = wx.ID_ANY,
                             style = wx.BK_DEFAULT)
        

        self.tabs = [] # list of open tabs
        

    def addTab(self, title):
        """
        Callback to add a new tab
        """
        tab = CapturePane(self)
        tab.SetBackgroundColour("Gray")
        self.AddPage(tab, title)
        self.SetSelection(self.GetPageCount() - 1)

        tabs.append(tab)

    def getTabList(self):
        return tabs
