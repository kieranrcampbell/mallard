#!/usr/bin/python

"""

Created when the user wishes to set up a capture. 
Interfaces between the physical device, data buffer
and gui.

kieran.renfrew.campbell@cern.ch


"""

from cInterface import cInterface
from DataManager import DataManager
from SessionSettings import SessionSettings

class CaptureSession:
    """
    Interfaces between card, gui and data buffers
    """    
    def __init__(self):
        print ('Capture session created')

        self.dmanager = DataManager() # stores and manages data from the card

        # set up c interface and provide callback function
        # in data manager
        self.interface = cInterface(self.dmanager.dataCallback)

        self.settings = SessionSettings()



    def setName(self, name):
        """
        Change the name of the current session
        """
        self.settings.name = name

    def getName(self):
        return self.settings.name
