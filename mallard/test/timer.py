#!/usr/bin/python

from PyDAQmx import *
from PyDAQmx.DAQmxConstants import *
from PyDAQmx.DAQmxFunctions import *

import numpy as np

if __name__ == "__main__":

    # constants
    timout = 100.0

    vMin = 0.0
    vMax = 5.0
    intervalsPerScan = 1000
    scans = 5
    voltsPerInterval = (vMax - vMin) / intervalsPerScan

    counterChannel = "Dev1/ctr1"
    clockChannel = "/Dev1/PFI1"
    aoChannel = "/Dev1/ao0"

    maxRate = 1000.0

    # create task handles
    countTaskHandle = TaskHandle(0)
    writeTaskHandle = TaskHandle(0)

    # create tasks
    DAQmxCreateTask("", byref(countTaskHandle))
    DAQmxCreateTask("", byref(writeTaskHandle))

    # configure channels
    DAQmxCreateCICountEdgesChan(countTaskHandle, counterChannel, "",
                                DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
    DAQmxCfgSampClkTiming(countTaskHandle, clockChannel, maxRate,
                          DAQmx_Val_Rising, DAQmx_Val_ContSamps, 1)

    DAQmxCreateAOVoltageChan(writeTaskHandle, aoChannel, "", vMin, vMax,
                             DAQmx_Val_Volts, None)

    # start tasks
    DAQmxStartTask(countTaskHandle)
    DAQmxStartTask(writeTaskHandle)

    data = uInt32(0) # the counter

    combinedData = np.zeros((scans, intervalsPerScan), dtype=uInt32)

    # begin acquisition loop
    for i in range(scans):
        for j in range(intervalsPerScan):
            DAQmxReadCounterScalarU32(countTaskHandle, timout,
                                      byref(data), None)
            combinedData[i][j] = data.value
            voltage = j * voltsPerInterval
            DAQmxWriteAnalogScalarF64(writeTaskHandle, True, timout,
                                      voltage, None)


    # end tasks
    DAQmxStopTask(countTaskHandle)
    DAQmxStopTask(writeTaskHandle)
    
    print combinedData


    
    
