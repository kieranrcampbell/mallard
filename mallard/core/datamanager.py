#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch
DataManager - 
passed data from the card to store & save

"""

import numpy as np

from mallard.gui.graphmanager import GraphManager
from PyDAQmx import *

from multiprocessing import Queue

class DataManager:
    
    def __init__(self, settings, globalSession, errorFnc):
        self.initialise(settings, globalSession, errorFnc)

    def initialise(self, settings, globalSession, errorFnc):
        """
        Need to restart the datamanager, but can't
        create a new object due to memory position
        for callbacks
        statusCallback is a function to provide
        info back to the gui
        """
        self.settings = settings

        # global session and errors
        self.globalSession = globalSession
        self.globalSettings = self.globalSession.getSettings()
        self.errorFnc = errorFnc

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
            / float(self.settings.intervalsPerScan - 1)

        # numpy array representing all different voltages
        # scanned over - nb can't use arange here
        l = []
        for i in range(self.settings.intervalsPerScan):
            l.append(i * self.voltsPerInterval)
        self.voltArray = np.array(l)

        self.lastScan = 0
        self.running = True




    def dataCallback(self, queue):
        """
        Interval is the voltage interval, so the current
        voltage is interval * self.voltsPerInterval
        coutData: counts from MCP
        aiData: AI reading at that voltage
        """
        
        counts = ai = np.zeros((self.settings.intervalsPerScan,))
        scale = 1

        for i in range(self.settings.scans):

            # user has selected to stop capture
            if not self.running:
                msg = 'Stopped by user after ' + str(i) + ' scans'
                self.globalSession.statusCallback(msg)
                break

            oldCounts = counts * scale
            oldAi = ai * scale

            # need to rescale up previous measure
            # defined after first to avoid /0
            if self.globalSettings.meanStyle == \
               self.globalSettings._CUMULATIVE:
                scale = (i+2) / float((i+1))

            for j in range(self.settings.intervalsPerScan):

                (scan, interval, count, ai) = queue.get()
                self.lastScan = scan

                if i != scan or j != interval:
                    self.errorFnc( "Process sync error" )

                self.rawCountData[scan][interval] = count
                self.rawAIData[scan][interval] = ai
        
                # update graphs on gui every 10 points
                if j % 5 is 0 or j is self.settings.intervalsPerScan - 1:
                    
                    # update status bar
                    s = "Scan " + str(i+1) + " of " + \
                        str(self.settings.scans) + "\t Voltage: " + \
                        str(self.voltsPerInterval * interval) + " V"

                    self.globalSession.statusCallback(s)

                    counts = self.getCombinedCounts(scan)
                    ai = self.getCombinedAI(scan)

                    self.graphManager.plot(self.voltArray, counts[:j], 
                                           ai[:j], oldCounts, oldAi)




    def registerGraphManager(self, graphManager):
        """
        Registers a GraphManager for continual
        updating of the graphs
        """
        self.graphManager = graphManager
        self.graphManager.globalSession = self.globalSession


    def getCombinedCounts(self, meanTo):
        """
        Returns a numpy array of the counts
        averaged over each scan
        Sometimes we only want to mean the first meanTo columns
        for displaying on the graph
        """
        if self.globalSettings.meanStyle == \
           self.globalSettings._NORMALISED:
            return np.mean(self.rawCountData[:meanTo+1], axis=0)
        else:
            return np.sum(self.rawCountData[:meanTo+1], axis=0)

    def getCombinedAI(self, meanTo):
        """
        Returns a numpy array of the AI readings
        averaged over each scan
        """
        if self.globalSettings.meanStyle == \
           self.globalSettings._NORMALISED:
            return np.mean(self.rawAIData[:meanTo+1], axis=0)
        else:
            return np.sum(self.rawAIData[:meanTo+1], axis=0)

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
                                self.getCombinedCounts(self.settings.scans),
                                self.getCombinedAI(self.settings.scans)))

    def getRawCountData(self):
        return self.rawCountData

    def getRawAIData(self):
        return self.rawAIData


    def setRawCounts(self, counts):
        self.rawCountData = counts

    def setRawAI(self, ai):
        self.rawAIData = ai


    def loadDataFromFile(self, path, fmanager):
        """
        Loads data from existing file
        """
        (volts, counts, ai) = fmanager.readData(path)

        # we don't actually hold any data in memory, so
        # just graph it
        self.graphManager.plot(volts, counts, ai,
                               counts, ai)


        
    # def clearLastScan(self):
    #     """
    #     Zeros the last scan done when we want to stop the Capture
    #     """
    #     print "Removing last scan, mem loc: " + str(self)
    #     self.rawCountData[self.lastScan] = \
    #                             np.zeros((self.settings.intervalsPerScan,))
    #     self.rawAIData[self.lastScan] = \
    #                             np.zeros((self.settings.intervalsPerScan,))
                                           

    # def graphAll(self):
    #     """
    #     Graphs last data captured if scan
    #     is stopped
    #     """
    #     counts = self.getCombinedCounts(self.lastScan - 1)
    #     ai = self.getCombinedAI(self.lastScan - 1)
        
    #     self.graphManager.plot(self.voltArray, 
    #                            self.rawCountData(self.lastScan - 1),
    #                            self.rawAIData(self.lastScan - 1),
    #                            counts, ai)

