#!/usr/bin/python

"""
Individual page in the capture notebook

kieran.renfrew.campbell@cern.ch
"""


import wx

class CapturePane(wx.Panel):
    """ 
    Represents an individual page in CaptureNotebook
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent,
                          id = wx.ID_ANY)


    def createPanel(self):
        """
        Creates main panel
        """
        self.panel = wx.Panel(self)

        # as per example, create mpl Figure and FigCanvas objects
        self.dpi = 100
        self.fig = Figure((10.0, 7.0), dpi = self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.axes = self.fig.add_subplot(111)

        self.axes.grid(True)
        # bind pick event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Data capture', size=10)

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, -1, wx.LEFT | wx.TOP | wx.GROW)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def drawFigure(self):
        """
        Draws plot(s)
        """
        x = y = range(4)
        self.axes.plot(x, y)
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


    def changeSettings(self):
        """
        Called to change settings in
        a particular tab
        """
        print "Trying to change settings"
