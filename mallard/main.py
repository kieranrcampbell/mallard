#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch


"""

from mallard.gui.mframe import MFrame

import wx

if __name__ == "__main__":
    # application variables
    size = (960, 770)
    title = "Mallard - Data Acquisition for CRIS"


    app = wx.App()

    frame = MFrame(None, mtitle = title, msize = size)

    app.MainLoop()

    


