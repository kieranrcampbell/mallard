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
    def __init__(self, settings, callbackFunc):
        self.settings = settings
        self.settings.sanitise() # don't want things to go wrong here
        self.callbackFunc = callbackFunc # to report data to


    def createTask(self):
        # constants
        self.timeout = 100.0
        
        self.maxRate = 1000.0

        # create task handles
        countTaskHandle = TaskHandle(0)
        writeTaskHandle = TaskHandle(0)

        # create tasks
        DAQmxCreateTask("", byref(countTaskHandle))
        DAQmxCreateTask("", byref(writeTaskHandle))

        # configure channels
        DAQmxCreateCICountEdgesChan(countTaskHandle, 
                                    self.settings.inputChannel, "",
                                    DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
        DAQmxCfgSampClkTiming(countTaskHandle, self.settings.clockChannel,
                              self.maxRate, DAQmx_Val_Rising, 
                              DAQmx_Val_ContSamps, 1)

        DAQmxCreateAOVoltageChan(writeTaskHandle, 
                                 self.settings.outputChannel
                                 "", self.settings.voltageMin,
                                 self.settings.voltageMax,
                                 DAQmx_Val_Volts, None)

        # start tasks
        DAQmxStartTask(countTaskHandle)
        DAQmxStartTask(writeTaskHandle)


    def acquire(self):
        """
        Main acquire loop
        """
        data = uInt32(0) # the counter
        
        # set initial voltage
        voltage = vMin
        DAQmxWriteAnalogScalarF64(writeTaskHandle, True, self.timeout,
                                  voltage, None)

        # begin acquisition loop
        for i in range(scans):
            for j in range(intervalsPerScan):
                DAQmxReadCounterScalarU32(countTaskHandle, self.timeout,
                                          byref(data), None)
                self.callbackFunc(voltage, data)
                voltage = j * voltsPerInterval
                DAQmxWriteAnalogScalarF64(writeTaskHandle, 
                                          True, self.timeout,
                                          voltage, None)


    def stopTasks(self):
        """
        Halts current tasks
        """
        DAQmxStopTask(countTaskHandle)
        DAQmxStopTask(writeTaskHandle)
    



    
    
