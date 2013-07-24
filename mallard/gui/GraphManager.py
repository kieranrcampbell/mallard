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

    def __init__(self, countSubplot, aiSubplot, canvas):
        """
        plot should be the subplot
        bound to the canvas
        """
        self.countSubplot = countSubplot
        self.aiSubplot = aiSubplot
        self.canvas = canvas

    def plot(self, voltage, counts, ai ):
        """
        Plots counts & ai against voltage
        """
        self.clearPlot()
        self.countSubplot.set_xlabel("Volts (V)")
        self.countSubplot.set_ylabel("Count")
        self.countSubplot.plot(voltage, counts, 'bo')

        self.aiSubplot.set_xlabel("Volts (V)")
        self.aiSubplot.set_ylabel("Measured Volts (V)")
        self.aiSubplot.plot(voltage, ai, 'k')

        self.canvas.draw()


        
    def clearPlot(self):
        self.countSubplot.clear()
        self.aiSubplot.clear()
