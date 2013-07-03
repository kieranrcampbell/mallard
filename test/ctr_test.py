#!/usr/bin/python

"""
Testing daqtriggerbase library for multiple, 
trigger-driven acqusition.
kieran.renfrew.campbell@cern.ch
"""

import ctypes
import ctypes.util
import numpy as np
import sys

from ctypes import *
from pylab import *

data_count = []
prev_count = 0

"""
Function called when data is received.
"""
def data_callback(data):
    global data_count, prev_count

    data_count.append(data - prev_count)
    prev_count = data

    # global all_data
    # global data_points
    # data_array = np.fromiter(data, dtype=np.float64, count=length)
    # all_data = np.hstack([all_data, data_array])
    # data_points += length

"""
Plot all data captured
"""
def plot_data(data):
    X = np.arange( len(data) )
    plot(X, data)
    show()

if __name__ == "__main__":
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
    cb_func = CB_CALLBACK_TYPE(data_callback)

    
    # acquire data
    daqtriggerbase.acquire(cb_func)

    # print count


    data = array(data_count)
    plot_data(data)
