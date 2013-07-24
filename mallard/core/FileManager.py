#!/usr/bin/python

"""
Manages file storage, retrieval and parsing

kieran.renfrew.campbell@cern.ch


"""

import numpy as np
from SessionSettings import SessionSettings
from DataManager import DataManager

class FileManager:
    """
    Manages all writing of files, both data and settings
    """
    
    def __init__(self, settings):
        
        self.settings = settings
        
    def changeSettings(self, settings):
        """
        Changes the current settings being
        written to file
        """
        self.settings = settings

    def constructHeader(self, integrated):
        """
        Constructs the header for the csv file given
        self.settings
        if integrated = True, add 'volts,count,ai' to
        header
        """
        header = []
        d = self.settings.__dict__
        for k in d:
            header.append(",".join((k,str(d[k]))))
        
        if integrated = True:
            header.append('voltage,count,ai')
        return "\n".join(header) + "\n"

    def writeCapture(self, rawCountData, rawAIData, integratedData):
        """
        """
        filename = self.getName(self.settings.filename)
        h = self.constructHeader(True)

        # integrated count
        f = filename + ".integrated.csv"
        np.savetxt(f, integratedData, delimiter=",",
                   header = h,
                   fmt = "%f,%i")

        h = self.constructHeader(False)
        # raw count
        f = filename + ".raw.count.csv"
        np.savetxt(f, rawCountData, delimiter=",",
                   header = h,
                   fmt = "%f,%i")

        # raw AI
        f = filename + ".raw.ai.csv"
        np.savetxt(f, rawAIData, delimiter=",",
                   header = h,
                   fmt = "%f,%i")
        

        
        
    def getName(self, s):
        """
        Parses filenames of the format
        [somepath]mycapture.integrated.csv
        [somepath]mycapture.raw.volts.csv
        [somepath]mycapture.raw.counts.csv
        to just return "[somepath]mycapture", or
        -1 if there's an error
        """
        s = s.split(".csv")[0].split(".")
        fName = None

        if s[-1] is "integrated":
            fName = '.'.join(s[:-1])

        elif s[-1] is "raw":
            fName = '.'.join(s[:-2])

        else:
            # file in wrong format, throw error
            return -1

        return fName


    def loadData(self, fileName, dmanager):
        """
        Loads voltages and count from fileName.
        Notice any of the three will do, just need to 
        get the others.
        """
        data = np.loadtxt(fileName, delimiter=",")
        dmanager.setData( (data.T[0], data.T[1]) )

    def getSettings(self, fileName):
        """
        Loads settings from the first lines
        of the data file
        """
        s = SessionSettings() # template
        d = s.__dict__ # get all the fields needed

        f = open(fileName, 'r')

        for line in f:
            if line[0] is '#':
                a = line[2:].strip().split(",")
                if len(a) > 1 and a[0] in d:
                    d[a[0]] = a[1]

        s.sanitise()
        return s
