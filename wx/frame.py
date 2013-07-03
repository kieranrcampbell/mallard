#!/usr/bin/python

"""
wxFrame test 
"""

import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar



class MFrame(wx.Frame):
    
    def __init__(self, parent, mtitle, msize):
        super(MFrame, self).__init__(parent, 
                                     title = mtitle,
                                     size = msize)
        self.InitUI()


    def InitUI(self):
        
        self.createMenu()
        self.createPanel()
        self.drawFigure()

        self.Centre()
        self.Show()

    """
    Add top menubar
    """
    def createMenu(self):
        # menu stuff
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()

        fileQuitItem = fileMenu.Append(wx.ID_EXIT,
                                       'Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onQuit, fileQuitItem)


    """
    Creates main panel
    """
    def createPanel(self):
        self.panel = wx.Panel(self)

        # as per example, create mpl Figure and FigCanvas objects
        self.dpi = 100
        self.fig = Figure((6.0, 5.0), dpi = self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.axes = self.fig.add_subplot(111)


        # bind pick event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    """
    Draws plot
    """
    def drawFigure(self):
        x = y = range(4)
        self.axes.plot(x,y)
        self.canvas.draw()
        
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        dlg = wx.MessageDialog(
            self, 
            msg, 
            "Click!",
            wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal() 
        dlg.Destroy()        

        
    
    """
    Called to exit program
    """
    def onQuit(self, e):
        self.Close()



"""
Program starts here
"""
if __name__ == "__main__":
    # application variables
    size = (700, 600)
    title = "Data Acqusition for Isolde"


    app = wx.App()

    frame = MFrame(None, mtitle = title, msize = size)


    app.MainLoop()

