#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch


"""

from pylab import *

class GraphManager:
    """
    Handles graph on a given CapturePane
    Note (as with all gui modules) this is essentially
    dumb, it is up to DataManager to tell GraphManager
    what to plot and when

    TODO: way too much stuff named 'plot' in this
    """

    def __init__(self, subplot, canvas):
        """
        plot should be the subplot
        bound to the canvas
        """
        self.subplot = subplot
        self.canvas = canvas

    def plot(self, x, y):
 
        self.subplot.clear()
        self.subplot.plot(x, y)
        self.canvas.draw()
