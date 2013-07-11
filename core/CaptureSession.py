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
from gui.Graph import Graph

class CaptureSession:
    """
    Interfaces between card, gui and data buffers
    """    
    def __init__(self):
        self.settings = SessionSettings()
        self.fileManager = FileManager(self.settings)
        self.dmanager = DataManager(self.settings) 
        self.hasData = False # no data currently loaded

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
        # load data
        self.fileManager.loadData(path, self.dmanager)
        self.hasData = True

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

    def startCapture(self):
        self.settings.sanitise()
        self.dmanager = DataManager(self.settings) 

        # set up c interface and provide callback function
        # in data manager
        self.interface = cInterface(self.dmanager.dataCallback,
                                    self.settings)

        self.interface.acquire()
        self.dmanager.combineCounts()
        print "Finished capture"


        self.hasData = True

    def createGraphFromSession(self):
        g = Graph(self.dmanager.getData())
        
