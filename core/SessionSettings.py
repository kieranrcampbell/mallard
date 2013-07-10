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

        # number of voltages to record for per sweep
        self.intervalsPerSweep = 100

        self.sweeps = 5
        
        self.inputChannel = "/Dev1/ctr1" # corresponds to PFI3
        
        self.outputChannel = "/Dev1/ao0"

        self.name = "" # name of session

        self.filename = "" # file name

    def sanitise(self):
        """ 
        makes sure the ints are ints and
        the strings are strings
        """
        self.clockCyclesPerVoltage = int(self.clockCyclesPerVoltage)
        self.voltageMin = int(self.voltageMin)
        self.voltageMax = int(self.voltageMax)
        self.intervalsPerSweep = int(self.intervalsPerSweep)
        self.sweeps = int(self.sweeps)
        self.inputChannel = str(self.inputChannel)
        self.outputChannel = str(self.outputChannel)
        self.name = str(self.name)
        self.filename = str(self.filename)
