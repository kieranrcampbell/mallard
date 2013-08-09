#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch


"""

from mallard.gui.mframe import MFrame


import sys
# import wxversion
# wxversion.select(wxversion.getInstalled()[0])

import wx

def start():
    # application variables
    size = (960, 770)
    title = "Mallard - Data Acquisition for CRIS"


    app = wx.App()
    frame = MFrame(None, mtitle = title, msize = size)
    app.MainLoop()

    
    
if __name__ == "__main__":
    start()



    


