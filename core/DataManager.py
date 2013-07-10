#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch
DataManager - 
passed data from the card to store & save

"""

import numpy as np

class DataManager:
    
    def __init__(self):
        self.voltage = None
        self.counts = None

    def dataCallback(self, data):
        """
        Call back after counts
        """

    def setData(self, voltage, counts):
        self.voltage = voltage
        self.counts = counts

    def getData(self):
        """
        Returns voltage and counts column_stacked
        """
        return np.column_stack((self.getVoltage(), 
                                self.getCounts()))

    def getVoltage(self):
        if self.voltage == None:
            return np.zeros( (1,1) )
        return self.voltage

    def getCounts(self):
        if self.counts == None:
            return np.zeros( (1,1) )
        return self.counts


