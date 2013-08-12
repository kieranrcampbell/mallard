#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch


"""

from pylab import *

from mallard.core.session import GlobalSession

class GraphManager:
    """
    Handles graph on a given CapturePane
    Note (as with all gui modules) this is essentially
    dumb, it is up to DataManager to tell GraphManager
    what to plot and when
    """

    def __init__(self, countSubplot, aiSubplot, canvas):
        """
        plot should be the subplot
        bound to the canvas
        """
        self.countSubplot = countSubplot
        self.aiSubplot = aiSubplot
        self.canvas = canvas

        # in case the initialisation from datamanager fails
        self.globalSession = GlobalSession() 

        # the line style parameters
        self.countLineStyle = None
        self.voltLineStyle = None
        

    def plot(self, voltage, counts, ai, oldCounts, oldAi ):
        """
        Plots counts & ai against voltage
        """
        self.clearPlot()
        self.countSubplot.set_xlabel("Volts (V)")
        self.countSubplot.set_ylabel("Count")
        self.countSubplot.plot(voltage[:len(counts)], counts, 'ko', 
                               voltage, oldCounts, 'r')

        self.aiSubplot.set_xlabel("Volts (V)")
        self.aiSubplot.set_ylabel("Measured Volts (V)")
        self.aiSubplot.plot(voltage[:len(ai)], ai, '--',
                            voltage, oldAi, 'r')

        self.canvas.draw()

    def calcLineStyles(self):
        settings = self.globalSession.getSettings()
    
        
    def clearPlot(self):
        self.countSubplot.clear()
        self.aiSubplot.clear()
