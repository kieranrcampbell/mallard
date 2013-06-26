#!/usr/bin/python


"""
Generic task for communicating with National Instruments hardware.
Based on original by Quentin Smith <quentin@mit.ed>

"""

from NITask import *

import ctypes
import numpy

__author__ = "Kieran Campbell <kieran.renfrew.campbell@cern.ch>"

class AITask(NITask):
    def __init__(self, min=-10.0, max=10.0,
		 channels=["Dev1/ai0", "Dev1/ai1", "Dev1/ai2", "Dev1/ai3", "Dev1/ai4", "Dev1/ai5", "Dev1/ai6", "Dev1/ai7"],
		 clockSource="OnboardClock", sampleRate=200,
		 samplesPerChan=8, totalSamples=None,
		 timeout=10.0):
        NITask.__init__(self)
        
        self.min = min
	self.max = max
	self.channels = channels
	self.clockSource = clockSource
	self.sampleRate = sampleRate
	self.samplesPerChan = samplesPerChan
	self.totalSamples = totalSamples
	self.timeout = timeout

	self.numChan = NITask.chanNumber(channels)

	if self.numChan is None:
	    raise ValueError("Channel specification is invalid")

        chan = ", ".join(self.channels)
	
	self.CHK(
            self.nidaq.DAQmxBaseCreateTask("",ctypes.byref(self.taskHandle)))
	self.CHK(self.nidaq.DAQmxBaseCreateAIVoltageChan(self.taskHandle, 
                                                         chan, 
                                                         "", 
                                                         DAQmx_Val_RSE, 
                                                         float64(self.min),
                                                         float64(self.max),
                                                         DAQmx_Val_Volts, 
                                                         None))
        if self.totalSamples:
            self.CHK(self.nidaq.DAQmxBaseCfgSampClkTiming(self.taskHandle, self.clockSource, float64(self.sampleRate), DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, uInt64(self.totalSamples)))
        
        else:
            self.CHK(
                self.nidaq.DAQmxBaseCfgSampClkTiming(self.taskHandle, 
                                                     self.clockSource, 
                                                     float64(self.sampleRate), 
                                                     DAQmx_Val_Rising, 
                                                     DAQmx_Val_ContSamps, 
                                                     uInt64(self.samplesPerChan)))

    def read(self, samplesPerChan=None):
        if samplesPerChan is None:
	    samplesPerChan = self.samplesPerChan
	
        data = numpy.zeros((samplesPerChan,self.numChan),dtype=numpy.float64)
	nRead = int32()
	self.CHK(self.nidaq.DAQmxBaseReadAnalogF64(self.taskHandle,
                                                   int32(samplesPerChan),
                                                   float64(self.timeout),
                                                   DAQmx_Val_GroupByScanNumber,
                                                   data.ctypes.data,
                                                   samplesPerChan*self.numChan,
                                                   ctypes.byref(nRead),None))
	print "Acquired %d samples for %d channels." % (nRead.value, self.numChan)
        if nRead.value != samplesPerChan:
            print "Expected %d samples! Attempting to resize." % samplesPerChan
            data.resize((nRead.value, self.numChan))
	return data
