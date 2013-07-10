#!/usr/bin/python

"""
Manages file storage, retrieval and parsing

kieran.renfrew.campbell@cern.ch


"""

import numpy as np
from SessionSettings import SessionSettings

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

    def constructHeader(self):
        """
        Constructs the header for the csv file given
        self.settings
        """
        header = []
        d = self.settings.__dict__
        for k in d:
            header.append(",".join((k,str(d[k]))))
        
        header.append('voltage,count')
        return "\n".join(header) + "\n"

    def writeCapture(self,volts, counts):
        """
        Writes the capture to fileName.
        Note volts, counts should be numpy arrays
        """
        data = np.column_stack((volts, counts))
        np.savetxt(self.settings.filename, data, delimiter=",",
                   header = self.constructHeader(),
                   fmt = "%f %i")
        
    def loadData(self, fileName):
        """
        Loads voltages and counts
        from fileName.
        Returns a tuple (voltage, count)
        """
        data = np.loadtxt(fileName, delimiter=",")
        return (data.T[0], data.T[1])

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
