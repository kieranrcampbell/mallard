#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

Main interface to C capture backend

"""

import ctypes
import ctypes.util
import numpy as np
import sys

from ctypes import *
from pylab import *

class cInterface:
    """
    Main interface to C backend
    """
    
    def __init__(self, callbackF):
        """
        callbackF should be the callback function
        in DataManager that processes all the data
        """
        self.callback = callbackF

    def acquire():
        global data_count
        
        # import 2 required shared libraries
        ctypes.CDLL(ctypes.util.find_library("lvrtdark"), 
                    mode=ctypes.RTLD_GLOBAL)
        ctypes.CDLL(ctypes.util.find_library("nidaqmxbase"),
                    mode=ctypes.RTLD_GLOBAL)

        # import our library
        daqtriggerbase = ctypes.CDLL("libcdaq.so", 
                                     mode=ctypes.RTLD_GLOBAL)

        # set all functions to void
        daqtriggerbase.setParameters.restype = None
        daqtriggerbase.printAllInfo.restype = None
        daqtriggerbase.acquire.restype = None

        # set up user settings
        channel = "/Dev1/ctr1" # virtual counter channel
        report = c_bool(True) # report data back to python
        report_every = c_int(1)
    
        # set parameters
        daqtriggerbase.setParameters(channel, report, report_every)

        # check parameters set correctly
        daqtriggerbase.printAllInfo()

        # initialise callback function
        CB_CALLBACK_TYPE = CFUNCTYPE(None, c_uint)
        cb_func = CB_CALLBACK_TYPE(self.callback)

    
        # acquire data
        daqtriggerbase.acquire(cb_func)


