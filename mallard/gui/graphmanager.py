#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch


"""

from pylab import *

#from mallard.core.session import GlobalSession

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
        from mallard.core.session import GlobalSession

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
        self.calcLineStyles()

        self.clearPlot()

        # set labels (again)
        self.countSubplot.set_xlabel("Volts (V)")
        self.countSubplot.set_ylabel("Count")

        self.aiSubplot.set_xlabel("Volts (V)")
        self.aiSubplot.set_ylabel("Measured Volts (V)")


        if self.countLineStyle == 'hist':
            self.countSubplot.step(voltage[:len(counts)], counts,'r',
                                   voltage, oldCounts, 'k')
        else:
            self.countSubplot.plot(voltage[:len(counts)], counts, 
                                   'r' + self.countLineStyle, 
                                   voltage, oldCounts, 
                                   'k' + self.countLineStyle)

        if self.voltLineStyle == 'hist':
            self.aiSubplot.step(voltage[:len(ai)], ai,'r',
                                voltage, oldAi, 'k')
        else:
            self.aiSubplot.plot(voltage[:len(ai)], ai,
                                'r' + self.voltLineStyle,
                                voltage, oldAi, 
                                'k' + self.voltLineStyle)

        self.canvas.draw()

    def calcLineStyles(self):
        """
        Creates the correct text lines
        from the globalSession settings
        """

        settings = self.globalSession.getSettings()

        self.countLineStyle = ''
        if settings.countGraphStyle == settings._GRAPH_DOT:
            self.countLineStyle = 'o'
        if settings.countGraphStyle == settings._GRAPH_HIST:
            self.countLineStyle = 'hist'

        if settings.voltGraphStyle == settings._GRAPH_DOT:
            self.voltLineStyle = 'o'
        if settings.voltGraphStyle == settings._GRAPH_HIST:
            self.voltLineStyle = 'hist'
        
    def clearPlot(self):
        self.countSubplot.clear()
        self.aiSubplot.clear()
