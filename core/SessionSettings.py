#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

SessionSettings

Stores the settings for a given capture session.


"""

class SessionSettings:

    
    # number of onboard clock cycles to record for per volt div
    clockCyclesPerVoltage = 0

    # minimum voltage
    voltageMin = 0

    # maximum voltage
    voltageMax = 0

    # number of voltages to record for per sweep
    intervalsPerSweep = 0

    sweeps = 0


