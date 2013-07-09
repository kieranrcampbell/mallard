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


class ctr_test:
    def __init__(self):

        self.count = 0

        """
        let's set up some read parameters
        """
        self.clockCyclesPerVoltage = 100
        self.voltageMin = 0
        self.voltageMax = 4
        self.intervalsPerSweep = 50
        self.sweeps = 2

        self.voltsPerInterval = (self.voltageMax - self.voltageMin) \
            / float(self.intervalsPerSweep)

        print "Volts per interval: " + str(self.voltsPerInterval)

        self.dataArray = np.zeros( (self.intervalsPerSweep, ) )
        self.currentVoltage = self.voltageMin
        self.currentSweep = 0

        self.finished = False # tell C we're finished


    def data_callback(self, data):
        """
        Only called back every self.clockCyclesPerVoltage steps
        """
        slot = self.count % self.intervalsPerSweep # which voltage position?
        self.dataArray[slot] += data # add count to correct voltage slot
        
        # could probably be done in more elegant way
        self.currentVoltage = self.voltsPerInterval * \
              (slot + 1)    

        self.count += 1

        if self.count == (self.intervalsPerSweep * self.sweeps):
            # we're done measuring
            self.finished = True

            
    def py_get_voltage(self, cnt ):
        """
        Returns voltage to be set
        """
        return self.currentVoltage
    

    def isFinished(self, cnt):
        return self.finished

    """
    Plot all data captured
    """
    def plot_data(self):
        X = np.arange( self.voltageMin, self.voltageMax, 
                       self.voltsPerInterval)
        plot(X, self.dataArray)
        ylabel('Count')
        xlabel('Voltage (V)')
        show()

    def main(self):

        
        print 'Importing libraries...'
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

        # set up user settings
        readChannel = "/Dev1/ctr1" # virtual self.counter channel
        writeChannel = "/Dev1/ao0"
        report_every = c_int(self.clockCyclesPerVoltage)
    
        # set parameters
        daqtriggerbase.setParameters(readChannel, writeChannel,
                                     report_every)

        # check parameters set correctly
        daqtriggerbase.printAllInfo()

        # initialise callback function
        print "Initialising callback functions..."
        CB_CALLBACK_TYPE = CFUNCTYPE(None, c_uint)
        cb_func = CB_CALLBACK_TYPE(self.data_callback)
        
        CB_RETVOLTAGE_TYPE = CFUNCTYPE(c_double, c_uint)
        rv_func = CB_RETVOLTAGE_TYPE(self.py_get_voltage)
    
        CB_FINISHED_TYPE = CFUNCTYPE(c_bool, c_uint)
        is_done_func = CB_FINISHED_TYPE(self.isFinished)
        print "Done"

        # acquire data
        print "Calling acquire..."
        daqtriggerbase.acquire(cb_func, rv_func, is_done_func)
        print "Done"
        # print self.count


        print('Total callbacks: ' + str(self.count))

        print(self.dataArray)
        self.plot_data()

if __name__ == "__main__":
    c = ctr_test()
    c.main()
