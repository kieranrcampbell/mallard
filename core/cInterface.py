#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch

Main interface to C capture backend

"""


import ctypes
import ctypes.util
import numpy as np
import os, sys



from ctypes import *
from pylab import *


from FileManager import FileManager 
from SessionSettings import SessionSettings


class cInterface:
    def __init__(self, callback_func, settings):

        self.settings = settings
        self.dmcallback_func = callback_func

        self.count = 0
        self.voltsPerInterval = \
            (self.settings.voltageMax - self.settings.voltageMin) \
            / float(self.settings.intervalsPerSweep)

        self.dataArray = np.zeros( (self.settings.intervalsPerSweep, ) )
        self.currentVoltage = self.settings.voltageMin
        self.currentSweep = 0

        self.finished = False # tell C we're finished


    def data_callback(self, data):
        """
        Only called back every self.settings.clockCyclesPerVoltage steps
        (ie after measuring at a given voltage)
        """
        # which voltage position?
        slot = self.count % self.settings.intervalsPerSweep 

        if slot == 0:
            # finished one sweep, so send the data back to dataManager
            self.dmcallback_func(self.dataArray)
            self.dataArray = np.zeros( (self.settings.intervalsPerSweep, ) )

        self.dataArray[slot] = data # add count to correct voltage slot
        
        # could probably be done in more elegant way
        self.currentVoltage = self.voltsPerInterval * \
              (slot + 1)    

        self.count += 1

        if self.count == (self.settings.intervalsPerSweep * self.settings.sweeps):
            # we're done measuring
            self.finished = True

            
    def py_get_voltage(self, cnt ):
        """
        Returns voltage to be set
        """
        return self.currentVoltage
    

    def isFinished(self, cnt):
        return self.finished


    def acquire(self):

        
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
        readChannel = self.settings.inputChannel#virtual self.counter channel
        writeChannel = self.settings.outputChannel
        report_every = c_int(self.settings.clockCyclesPerVoltage)
    
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


