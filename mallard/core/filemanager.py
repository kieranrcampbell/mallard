#!/usr/bin/python

"""
Manages file storage, retrieval and parsing

kieran.renfrew.campbell@cern.ch


"""

import numpy as np
from settings import SessionSettings


import os.path

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
        
        if (integrated):
            header.append('voltage,count,ai')
        return "\n".join(header) + "\n"

    def writeCapture(self, rawCountData, rawAIData, integratedData):
        """
        Saves the captures to the 3 files
        """
        filename = self.getName(self.settings.filename)
        filename = str(filename)

        sessionName = filename.split("\\")[-1]
        if self.settings.name == "new_capture":
            self.settings.name = sessionName

        h = self.constructHeader(True)

        # integrated count
        f = filename + ".integrated.csv"

        np.savetxt(f, integratedData, delimiter=",",
                   header = h,
                   fmt = "%f,%i,%f")

        h = self.constructHeader(False)
        # raw count
        f = filename + ".raw.counts.csv"

        np.savetxt(f, rawCountData, delimiter=",",
                   header = h)

        # raw AI
        f = filename + ".raw.ai.csv"
        np.savetxt(f, rawAIData, delimiter=",",
                   header = h)
        

        
        
    def getName(self, path):
        """
        Parses filenames of the format
        [somepath]mycapture.integrated.csv
        [somepath]mycapture.raw.volts.csv
        [somepath]mycapture.raw.counts.csv
        to just return "[somepath]mycapture", or
        -1 if there's an error
        """
        s = path.split(".csv")[0].split(".")

        print str(s)

        if len(s) > 1:
            if s[-1] == "integrated":
                return '.'.join(s[:-1])

        if len(s) > 2:
            if s[-2] == "raw":
                return '.'.join(s[:-2])

        else:
            # file in wrong format, throw error
            return path.split(".csv")[0]

        return fName



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
