#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

SessionSettings

Stores the settings for a given capture session.


"""


class SessionSettings:

    def __init__(self):    
        # number of onboard clock cycles to record for per volt div
        self.clockCyclesPerVoltage = 200

        # minimum voltage
        self.voltageMin = 0

        # maximum voltage
        self.voltageMax = 5

        # number of voltages to record for per scan
        self.intervalsPerScan = 50

        self.scans = 1
        
        self.counterChannel = "/Dev1/ctr1" # corresponds to PFI3
        
        self.aoChannel = "/Dev1/ao0"

        self.aiChannel = "/Dev1/ai2"

        self.clockChannel = "/Dev1/PFI1"

        self.name = "new_capture" # name of session

        self.filename = "" # file name

    def sanitise(self):
        """ 
        Makes sure the ints are ints and
        the strings are strings, as reading from
        file normally makes everything a string
        """
        self.clockCyclesPerVoltage = int(self.clockCyclesPerVoltage)
        self.voltageMin = int(self.voltageMin)
        self.voltageMax = int(self.voltageMax)
        self.intervalsPerScan = int(self.intervalsPerScan)
        self.scans = int(self.scans)
        self.counterChannel = str(self.counterChannel)
        self.aoChannel = str(self.aoChannel)
        self.name = str(self.name)
        self.filename = str(self.filename)
        self.clockChannel = str(self.clockChannel)




class GlobalSettings:
    """
    Represents the global application settings
    """

    def __init__(self):

        # graph style constants
        self._GRAPH_HIST = 0
        self._GRAPH_LINE = 1
        self._GRAPH_DOT = 2

        # averaging
        self._NORMALISED = 0 # mean displayed is the true mean
        self._CUMULATIVE = 1 # mean displayed is cumulative


        # the three global parameters
        self.countGraphStyle = self._GRAPH_DOT
        self.voltGraphStyle = self._GRAPH_DOT
        self.meanStyle = self._NORMALISED
