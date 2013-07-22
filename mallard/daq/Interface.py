#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

Example usage:
interface = Interface(self.settings, callbackFunc)
interface.acquire()
interface.stopTasks()

Note - must call interface.stopTasks()
after data acquisition is complete, otherwise
channels will block.

"""


from PyDAQmx import *
from PyDAQmx.DAQmxConstants import *
from PyDAQmx.DAQmxFunctions import *


class Interface:
    """
    Provides physical interface & callback using PyDAQmx
    """
    def __init__(self, callbackFunc):
        self.settings = None

        self.callbackFunc = callbackFunc # to report data to


    def createTask(self, settings):
        self.settings = settings
        self.settings.sanitise() # don't want things to go wrong here

        # constants
        self.timeout = 100.0
        
        self.maxRate = 1000.0

        # create task handles
        self.countTaskHandle = TaskHandle(0)
        self.writeTaskHandle = TaskHandle(0)

        # create tasks
        DAQmxCreateTask("", byref(self.countTaskHandle))
        DAQmxCreateTask("", byref(self.writeTaskHandle))

        # configure channels
        DAQmxCreateCICountEdgesChan(self.countTaskHandle, 
                                    self.settings.counterChannel, "",
                                    DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
        DAQmxCfgSampClkTiming(self.countTaskHandle, self.settings.clockChannel,
                              self.maxRate, DAQmx_Val_Rising, 
                              DAQmx_Val_ContSamps, 1)

        DAQmxCreateAOVoltageChan(self.writeTaskHandle, 
                                 self.settings.aoChannel,
                                 "", self.settings.voltageMin,
                                 self.settings.voltageMax,
                                 DAQmx_Val_Volts, None)

        # start tasks
        DAQmxStartTask(self.countTaskHandle)
        DAQmxStartTask(self.writeTaskHandle)


    def acquire(self):
        """
        Main acquire loop
        """
        data = uInt32(0) # the counter
        
        # set initial voltage
        voltage = vMin
        DAQmxWriteAnalogScalarF64(self.writeTaskHandle, True, self.timeout,
                                  voltage, None)

        # begin acquisition loop
        for i in range(scans):
            for j in range(intervalsPerScan):
                DAQmxReadCounterScalarU32(self.countTaskHandle, 
                                          self.timeout,
                                          byref(data), None)
                self.callbackFunc(voltage, data)
                voltage = j * voltsPerInterval
                DAQmxWriteAnalogScalarF64(self.writeTaskHandle, 
                                          True, self.timeout,
                                          voltage, None)


    def stopTasks(self):
        """
        Halts current tasks
        """
        DAQmxStopTask(self.countTaskHandle)
        DAQmxStopTask(self.writeTaskHandle)
    



    
    
