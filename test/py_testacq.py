#!/usr/bin/python

"""
Testing daqtriggerbase library for multiple, 
trigger-driven acqusition.
kieran.renfrew.campbell@cern.ch
"""

import ctypes
import ctypes.util
from ctypes import *


if __name__ == "__main__":
    # import 2 required shared libraries
    ctypes.CDLL(ctypes.util.find_library("lvrtdark"), 
                mode=ctypes.RTLD_GLOBAL)
    ctypes.CDLL(ctypes.util.find_library("nidaqmxbase"),
                mode=ctypes.RTLD_GLOBAL)

    # import our library
    daqtriggerbase = ctypes.CDLL("libdaqtriggerbase.so", 
                                 mode=ctypes.RTLD_GLOBAL)

    # set all functions to void
    daqtriggerbase.setParameters.restype = None
    daqtriggerbase.printAllInfo.restype = None
    daqtriggerbase.acquire.restype = None

    # set up user settings
    sampleRate = c_double(1000)
    noTriggers = c_ulong(10)
    channel = "/Dev1/ai8"
    triggerSource = "/Dev1/PFI0"
    
    # set parameters
    daqtriggerbase.setParameters(channel, sampleRate,
                                 triggerSource, noTriggers)

    # check parameters set correctly
    daqtriggerbase.printAllInfo()

    # acquire data
    daqtriggerbase.acquire()
