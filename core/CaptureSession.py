#!/usr/bin/python

"""

Created when the user wishes to set up a capture. 
Interfaces between the physical device, data buffer
and gui.

kieran.renfrew.campbell@cern.ch


"""

from cInterface import cInterface
from DataManager import DataManager


class CaptureSession:
    """
    Interfaces between card, gui and data buffers
    """    
    def __init__(self):
        print ('Capture session created')

        self.dmanager = DataManager() # stores and manages data from the card
        
        # set up c interface and provide callback function
        # in data manager
        self.interface = cInterface(self.DataManager.dataCallback)
