#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch
DataManager - 
passed data from the card to store & save

"""

import numpy as np

from mallard.gui.GraphManager import GraphManager

class DataManager:
    
    def __init__(self, settings):
        self.initialise(settings)

    def initialise(self, settings):
        """
        Need to restart the datamanager, but can't
        create a new object due to memory position
        for callbacks
        """
        self.settings = settings
        self.countArrayList = [] # list of arrays of each count

        self.voltsPerInterval = \
            (self.settings.voltageMax - self.settings.voltageMin) \
            / float(self.settings.intervalsPerScan)

        self.voltage = self.voltArray()
        self.counts = None


    def dataCallback(self, data):
        """
        Call back after counts
        """
        print "locd: " + str(self)
        self.countArrayList.append(data)
        self.combineCounts()
        self.graphManager.plot(self.voltage, self.counts)

    def setData(self, (volts, count)):
        """
        Sets voltage and counts given
        the voltage and count
        """
        self.voltage = volts
        self.counts = count

    def getData(self):
        """
        Returns voltage and counts column_stacked
        """
        return np.column_stack((self.getVoltage(), 
                                self.getCounts()))

    def getVoltage(self):
        return self.voltage

    def getCounts(self):
        return self.counts

    def voltArray(self):
        """
        Calculates the step voltages assuming uniformity
        """
        return np.arange( self.settings.voltageMin, 
                          self.settings.voltageMax, 
                          self.voltsPerInterval )

    def combineCounts(self):
        """
        Adds all the counts at a given voltage
        together into self.counts
        """
        self.counts = np.zeros(self.settings.intervalsPerScan)
        for c in self.countArrayList:
            self.counts = np.add(c, self.counts)


    def registerGraphManager(self, graphManager):
        """
        Registers a GraphManager for continual
        updating of the graphs
        """
        self.graphManager = graphManager
        print "loc: " + str(self)




