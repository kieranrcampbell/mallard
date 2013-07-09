#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

SessionSettings

Stores the settings for a given capture session.


"""

class SessionSettings:

    
    # number of onboard clock cycles to record for per volt div
    clockCyclesPerVoltage = 200

    # minimum voltage
    voltageMin = 0

    # maximum voltage
    voltageMax = 5

    # number of voltages to record for per sweep
    intervalsPerSweep = 100

    sweeps = 5

    inputChannel = "/Dev1/ctr1" # corresponds to PFI3

    outputChannel = "/Dev1/ao0"

    name = "" # name of session


