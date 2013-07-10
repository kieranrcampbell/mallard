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
from FileManager import FileManager

class CaptureSession:
    """
    Interfaces between card, gui and data buffers
    """    
    def __init__(self):
        self.dmanager = DataManager() # stores and manages data from the card

        # set up c interface and provide callback function
        # in data manager
        self.interface = cInterface(self.dmanager.dataCallback)

        self.settings = SessionSettings()
        self.fileManager = FileManager(self.settings)

    def setName(self, name):
        """
        Change the name of the current session
        """
        self.settings.name = name

    def getName(self):
        return self.settings.name


    def loadSettings(self, path):
        """
        Loads just settings from file
        """
        print "loadsettings called"
        self.settings = self.fileManager.getSettings(path)
        self.settings.filename = ""

    def loadSession(self, path):
        """
        Loads a session from a file
        """
        self.loadSettings(path)

    def saveSession(self):
        """
        Save session to current filename
        """
        self.fileManager.writeCapture(self.dmanager.getVoltage(), 
                                      self.dmanager.getCounts())

    def saveSessionAs(self, path):
        """
        Save session to new filename
        """
        self.settings.filename = path
        self.saveSession()
