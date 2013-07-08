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

count = 0
voltage = 0

"""
Function called when data is received.
"""
def data_callback(data):
    global data_count, prev_count, count, voltage

    data_count.append(data - prev_count)
    prev_count = data

    count += 1

    # write voltage every 100 clock cycles
    if count % 100 == 0:
        count = 0
        voltage += 0.03



    # global all_data
    # global data_points
    # data_array = np.fromiter(data, dtype=np.float64, count=length)
    # all_data = np.hstack([all_data, data_array])
    # data_points += length

def py_get_voltage( cnt ):
    """
    Returns voltage to be set
    """
    return voltage



"""
Plot all data captured
"""
def plot_data(data):
    X = np.arange( len(data) )
    plot(X, data)
    show()

if __name__ == "__main__":
    global data_count

    print "Importing libraries..."
    # import 2 required shared libraries
    ctypes.CDLL(ctypes.util.find_library("lvrtdark"), 
                mode=ctypes.RTLD_GLOBAL)
    ctypes.CDLL(ctypes.util.find_library("nidaqmxbase"),
                mode=ctypes.RTLD_GLOBAL)

    # import our library
    daqtriggerbase = ctypes.CDLL("libcdaq.so", 
                                 mode=ctypes.RTLD_GLOBAL)
    print "Done"


    # set all functions to void
    daqtriggerbase.setParameters.restype = None
    daqtriggerbase.printAllInfo.restype = None
    daqtriggerbase.acquire.restype = None
    daqtriggerbase.writeVoltage.restype = None

    # set up user settings
    readChannel = "/Dev1/ctr1" # virtual counter channel
    writeChannel = "/Dev1/ao0"
    report = c_bool(True) # report data back to python
    report_every = c_int(1)
    
    # set parameters
    daqtriggerbase.setParameters(readChannel, writeChannel,
                                 report, report_every)
    # check parameters set correctly
    daqtriggerbase.printAllInfo()

    # initialise callback function
    CB_CALLBACK_TYPE = CFUNCTYPE(None, c_uint)
    cb_func = CB_CALLBACK_TYPE(data_callback)

    CB_RETVOLTAGE_TYPE = CFUNCTYPE(c_double, c_uint)
    rv_func = CB_RETVOLTAGE_TYPE(py_get_voltage)
    
    # acquire data
    daqtriggerbase.acquire(cb_func, rv_func)

    # print count


    data = array(data_count)
    global count
    print('Total callbacks: ' + str(count))

#    plot_data(data)

