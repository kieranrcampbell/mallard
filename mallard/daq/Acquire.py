#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

This is the only non-oo module in the package.
When we use multiprocessing to fork, we have to
be able to pickle whatever function we send, which can't
be done with class instance methods, so this is the replacement.


"""


from PyDAQmx import *
from PyDAQmx.DAQmxConstants import *
from PyDAQmx.DAQmxFunctions import *

from multiprocessing import Pipe

def acquire(settings, queue):
    settings.sanitise() # don't want things to go wrong here

    # constants
    timeout = 100.0 # arbitrary - change in future
    maxRate = 1000.0

    # create task handles
    countTaskHandle = TaskHandle(0)
    aoTaskHandle = TaskHandle(0)
    aiTaskHandle = TaskHandle(0)

    # create tasks
    DAQmxCreateTask("", byref(countTaskHandle))
    DAQmxCreateTask("", byref(aoTaskHandle))
    DAQmxCreateTask("", byref(aiTaskHandle))

    # configure channels
    DAQmxCreateCICountEdgesChan(countTaskHandle, 
                                settings.counterChannel, "",
                                DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
    DAQmxCfgSampClkTiming(countTaskHandle, 
                          settings.clockChannel,
                          maxRate, DAQmx_Val_Rising, 
                          DAQmx_Val_ContSamps, 1)

    DAQmxCreateAOVoltageChan(aoTaskHandle, 
                             settings.aoChannel,
                             "", settings.voltageMin,
                             settings.voltageMax,
                             DAQmx_Val_Volts, None)

    DAQmxCreateAIVoltageChan(aiTaskHandle,
                             settings.aiChannel, "",
                             DAQmx_Val_RSE, -10.0, 10.0,
                             DAQmx_Val_Volts, None)

    # start tasks
    DAQmxStartTask(countTaskHandle)
    DAQmxStartTask(aoTaskHandle)
    DAQmxStartTask(aiTaskHandle)

    lastCount = uInt32(0)
    countData = uInt32(0) # the counter
    aiData = float64(0)

    # set initial voltage
    aoVoltage = settings.voltageMin

    voltsPerInterval = (settings.voltageMax - \
                        settings.voltageMin) \
                       / float(settings.intervalsPerScan - 1)


    DAQmxWriteAnalogScalarF64(aoTaskHandle, True, 
                              timeout,
                              aoVoltage, None)

    # begin acquisition loop
    for i in range(settings.scans):
        for j in range(settings.intervalsPerScan):

            DAQmxReadCounterScalarU32(countTaskHandle, 
                                      timeout,
                                      byref(countData), None)
            DAQmxReadAnalogScalarF64(aiTaskHandle, timeout,
                                     byref(aiData), None)

            aoVoltage = j * voltsPerInterval
            DAQmxWriteAnalogScalarF64(aoTaskHandle, 
                                      True, timeout,
                                      aoVoltage, None)

            # callbackFunc(i, j, countData.value - lastCount.value,
            #                   aiData.value)
            c = countData.value - lastCount.value
            queue.put( (i, j, c, aiData.value) )

            lastCount.value = countData.value
 

    """
    Halts current tasks
    """
    DAQmxStopTask(countTaskHandle)
    DAQmxStopTask(aoTaskHandle)
    DAQmxStopTask(aiTaskHandle)

    DAQmxClearTask(countTaskHandle)
    DAQmxClearTask(aoTaskHandle)
    DAQmxClearTask(aiTaskHandle)



    
    
