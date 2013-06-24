#!/usr/bin/python

"""
Generic task for communicating with National Instruments hardware.
Based on original by Quentin Smith <quentin@mit.ed>
"""

import ctypes
import ctypes.util
import atexit
import re

__author__ = "Kieran Campbell <kieran.renfrew.campbell@cern.ch>"
 

uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong

float64 = ctypes.c_double
int32 = ctypes.c_long

TaskHandle = uInt32

DAQmx_Val_Volts = 10348

DAQmx_Val_GroupByScanNumber = 1
DAQmx_Val_RSE = 10083
DAQmx_Val_Rising = 10280

DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_ContSamps = 10123


class NITask(object):
    def __init__(self):

        self.lvrtdark = ctypes.CDLL(ctypes.util.find_library("lvrtdark"), 
                        mode=ctypes.RTLD_GLOBAL)

        f = ctypes.util.find_library("nidaqmxbase")
        if not f:
            print "Could not find nidaqmxbase library"
            sys.exit(0)

        self.nidaq = ctypes.CDLL( f, 
                    mode=ctypes.RTLD_GLOBAL)

        atexit.register(self.cleanup)
        
	self.taskHandle = TaskHandle(0)

    def CHK(self, err):
        """Check the return code of a NIDAQmx Base library call and throw
        an exception if it indicates failure."""
        if err < 0:
            buf_size = 2048
            buf = ctypes.create_string_buffer('\000' * buf_size)
            self.nidaq.DAQmxBaseGetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))

    def start(self):
        self.CHK(self.nidaq.DAQmxBaseStartTask(self.taskHandle))

    def stop(self):
        self.CHK(self.nidaq.DAQmxBaseStopTask(self.taskHandle))
	
    def cleanup(self):
        print "Cleaning up "+str(self)
        if self.taskHandle:
            self.stop()
            self.CHK(self.nidaq.DAQmxBaseClearTask(self.taskHandle))
    __del__ = cleanup



    @staticmethod
    def chanNumber(chanList):
        """Returns the number of channels in a channel specification or None if the list is malformed."""
        chanNum = 0
        chanMatch = re.compile("Dev(\d+)/\w+(\d+)(:\d+)?")
        for chan in chanList:
            m = chanMatch.match(chan)
            if m is None:
                return None
            start = m.group(2)
            end = m.group(3)
            if end is not None:
                chanNum += (int(end)-int(start)+1)
            else:
                chanNum += 1
            return chanNum
        
