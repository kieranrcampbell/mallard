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

        # raw analog input data for all measurements
        self.rawAIData = np.zeros((self.settings.scans,
                                   self.settings.intervalsPerScan),
                                  dtype=float64)

        # raw counter data for all measurements
        self.rawCountData = np.zeros((self.settings.scans,
                                      self.settings.intervalsPerScan),
                                     dtype=uInt32)

        self.voltsPerInterval = \
            (self.settings.voltageMax - self.settings.voltageMin) \
            / float(self.settings.intervalsPerScan)

        # numpy array representing all different voltages
        # scanned over
        self.voltArray =  np.arange( self.settings.voltageMin, 
                                   self.settings.voltageMax, 
                                   self.voltsPerInterval )



    def dataCallback(self, scan, interval, countData, aiData):
        """
        Interval is the voltage interval, so the current
        voltage is interval * self.voltsPerInterval
        coutData: counts from MCP
        aiData: AI reading at that voltage
        """
        self.rawCountData[scan][interval] = countData
        self.rawAIData[scan][interval] = aiData
        self.graphManager.plot(self.voltArray, self.getCombinedCounts())


    def registerGraphManager(self, graphManager):
        """
        Registers a GraphManager for continual
        updating of the graphs
        """
        self.graphManager = graphManager

    def getCombinedCounts(self):
        """
        Returns a numpy array of the counts
        averaged over each scan
        """
        return np.mean(self.rawCountData, axis=0)

    def getCombinedAI(self):
        """
        Returns a numpy array of the AI readings
        averaged over each scan
        """
        return np.mean(self.rawAIData, axis=0)

    def getVoltageArray(self):
        """
        Returns an array of the measured
        voltages
        """
        return self.voltArray

    def getCombinedData(self):
        """
        Returns voltage, counts and ai
        stacked together
        """
        return np.column_stack((self.getVoltageArray(),
                                self.getCombinedCounts(),
                                self.getCombinedAI()))

    def getRawCountData(self):
        return self.rawCountData

    def getRawAIData(self):
        return self.rawAIData
