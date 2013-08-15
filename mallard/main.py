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


    # if the stdout disappears to quickly,
    # turn on the redirect flag and open
    # from the command line
    app = wx.App()#redirect=False)
    frame = MFrame(None, mtitle = title, msize = size)
    app.MainLoop()

    
    
if __name__ == "__main__":
    start()



    


