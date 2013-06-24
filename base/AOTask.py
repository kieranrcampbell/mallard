#!/usr/bin/python


"""
Generic task for communicating with National Instruments hardware.
Based on original by Quentin Smith <quentin@mit.ed>

"""

from NITask import *

import ctypes
import numpy

__author__ = "Kieran Campbell <kieran.renfrew.campbell@cern.ch>"

class AOTask(NITask):
    def __init__(self, min=0.0, max=5.0,
		 channels=["Dev/ao0"],
		 timeout=10.0):
        NITask.__init__(self)
        
        self.min = min
	self.max = max
	self.channels = channels
	self.timeout = timeout

	self.numChan = NITask.chanNumber(channels)

	if self.numChan is None:
	    raise ValueError("Channel specification is invalid")

        chan = ", ".join(self.channels)
	
	super(AOTask, self).CHK(self.nidaq.DAQmxBaseCreateTask("",ctypes.byref(self.taskHandle)))

	super(AOTask, self).CHK(self.nidaq.DAQmxBaseCreateAOVoltageChan(self.taskHandle, chan, "", float64(self.min), float64(self.max), DAQmx_Val_Volts, None))


    def write(self, data):
	nWritten = int32()
        data = data.astype(numpy.float64)
	self.CHK(self.nidaq.DAQmxBaseWriteAnalogF64(self.taskHandle,
                                                    int32(1), int32(0),
                                                    float64(self.timeout),
                                                    DAQmx_Val_GroupByScanNumber,
                                                    data.ctypes.data,
                                                    ctypes.byref(nWritten),None))
        if nWritten.value != self.numChan:
            print "Expected to write %d samples!" % self.numChan


