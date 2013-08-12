#!/usr/bin/python

"""
Main notebook for holding capture sessions

kieran.renfrew.campbell@cern.ch

"""

import wx

from capturepane import CapturePane

class CaptureNotebook(wx.Notebook):
    """
    Notebook class
    """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent,
                             id = wx.ID_ANY,
                             style = wx.BK_DEFAULT)
        

        self.tabs = [] # list of open tabs
        

    def addTab(self, globalSession):
        """
        statusCallback is a function to provide
        some status to system - in this case
        the status bar
        """
        tab = CapturePane(self, globalSession)
        self.AddPage(tab, tab.session.getName())
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

    def getOpenTab(self):
        return self.tabs[self.GetSelection()]

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

