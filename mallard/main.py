#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch


"""

from gui.MFrame import MFrame
import wx


if __name__ == "__main__":
    # application variables
    size = (900, 700)
    title = "Data Acqusition for Isolde"


    app = wx.App()
    frame = MFrame(None, mtitle = title, msize = size)

    app.MainLoop()

    


