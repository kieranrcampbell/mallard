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
        self.AddPage(tab, title)
        self.SetSelection(self.GetPageCount() - 1)

        self.tabs.append(tab)

    def closeTab(self):
        selected = self.GetSelection()
        self.DeletePage(selected)
        del self.tabs[selected]

    def getTabList(self):
        return self.tabs

    def getOpenSession(self):
        return self.tabs[self.GetSelection()].session

    def getTab(self, n):
        """ 
        Returns the nth tab
        """
        return self.tabs[n]

    def getLastTab(self):
        """
        Returns last tab opened
        """
        return self.tabs[-1]
