#!/usr/bin/python

"""

Created when the user wishes to set up a capture. 
Interfaces between the physical device, data buffer
and gui.

kieran.renfrew.campbell@cern.ch


"""

from mallard.daq.Interface import Interface
from DataManager import DataManager
from SessionSettings import SessionSettings
from FileManager import FileManager


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
        self.settings.filename = path
        self.fileManager.loadData(path, self.dmanager)

        self.hasData = True

    def saveSession(self):
        """
        Save session to current filename
        """
        self.fileManager.writeCapture(self.dmanager.getRawCountData(),
                                      self.dmanager.getRawAIData(),
                                      self.dmanager.getCombinedData())

    def loadData(self, volts, count, ai):
        """
        Loads data in given a previous capture
        """
        

    def saveSessionAs(self, path):
        """
        Save session to new filename
        """
        self.settings.filename = path
        self.saveSession()

    def startCapture(self):
        """
        Need to reinitialise dmanager. Can't rely on
        the fact that self.settings is a pointer as
        need to recalculate stuff like voltage intervals 
        """
        self.settings.sanitise()
        
        self.dmanager.initialise(self.settings) 

        interface = Interface(self.dmanager.dataCallback)    
        interface.createTask(self.settings)
        interface.acquire()

        self.hasData = True

    def registerGraphManager(self, graphManager):
        self.dmanager.registerGraphManager(graphManager)


    def getRange(self):
        """
        Returns the range required for gauge
        """
        self.settings.sanitise()
        return self.settings.scans

        
    def clearGraph(self):
        self.dmanager.graphManager.clearPlot()
