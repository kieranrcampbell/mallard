#!/usr/bin/python

"""

Created when the user wishes to set up a capture. 
Interfaces between the physical device, data buffer
and gui.

kieran.renfrew.campbell@cern.ch


"""

from mallard.daq.Acquire import acquire
from DataManager import DataManager
from SessionSettings import SessionSettings
from FileManager import FileManager

from multiprocessing import Process, Queue

# def acquire(interface, queue):
#     """
#     Needs to be defined to get round
#     pickling difficulties when using multiprocessing
#     """
#     interface.acquire(queue)


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


    def saveSession(self):
        """
        Save session to current filename
        """
        self.fileManager.writeCapture(self.dmanager.getRawCountData(),
                                      self.dmanager.getRawAIData(),
                                      self.dmanager.getCombinedData())


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

        # interface = Interface(self.dmanager.dataCallback)    
        # interface.createTask(self.settings)

        q = Queue()
        captureProcess = Process(target=acquire,
                                 args=(self.settings, q,))
        captureProcess.start()
        
        self.dmanager.dataCallback(q)
        captureProcess.join()

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
