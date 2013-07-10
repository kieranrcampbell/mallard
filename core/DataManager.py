#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch
DataManager - 
passed data from the card to store & save

"""

import numpy as np

class DataManager:
    
    def __init__(self, settings):
        self.settings = settings
        self.countArrayList = [] # list of arrays of each count

        self.voltsPerInterval = \
            (self.settings.voltageMax - self.settings.voltageMin) \
            / float(self.settings.intervalsPerSweep)

        self.voltage = self.voltArray()
        self.counts = None

    def dataCallback(self, data):
        """
        Call back after counts
        """
        self.countArrayList.append(data)

    def getData(self):
        """
        Returns voltage and counts column_stacked
        """
        return np.column_stack((self.getVoltage(), 
                                self.getCounts()))

    def getVoltage(self):
        return self.voltage

    def getCounts(self):
        if not self.countArrayList:
            return np.zeros( int(self.settings.intervalsPerSweep) )
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
        self.counts = np.zeros(self.settings.intervalsPerSweep)
        for c in self.countArrayList:
            self.counts = np.add(c, self.counts)
