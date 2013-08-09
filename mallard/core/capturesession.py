#!/usr/bin/python

"""

Created when the user wishes to set up a capture. 
Interfaces between the physical device, data buffer
and gui.

kieran.renfrew.campbell@cern.ch


"""

from mallard.daq.acquire import acquire
from datamanager import DataManager
from settings import SessionSettings, GlobalSettings
from filemanager import FileManager

from threading import Thread
from multiprocessing import Process, Queue


import wx


class CaptureSession:
    """
    Interfaces between card, gui and data buffers
    """    
    def __init__(self, statusCallback, errorFnc):
        self.settings = SessionSettings()
        self.fileManager = FileManager(self.settings)
        self.dmanager = DataManager(self.settings, statusCallback,
                                    errorFnc) 

        self.needsSaved = False # captured data that needs saved
        
        # method that updates statusbar
        self.statusCallback = statusCallback
        
        # method displays error popup
        self.errorFnc = errorFnc
        
        self.globalSettings = GlobalSettings()


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
        self.settings = self.fileManager.getSettings(path)
        self.settings.filename = ""


    def saveSession(self):
        """
        Save session to current filename
        """
        self.fileManager.writeCapture(self.dmanager.getRawCountData(),
                                      self.dmanager.getRawAIData(),
                                      self.dmanager.getCombinedData())
        self.needsSaved = False


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
        
        # reinitialise data manager to do things like voltage calcs
        self.dmanager.initialise(self.settings, self.statusCallback,
                                 self.errorFnc) 

        # queue for passing data between acquisition and dmanager
        q = Queue()

        # set up acquisition process and start
        self.captureProcess = Process(target=acquire,
                                 args=(self.settings, q, ))
        self.captureProcess.start()

        # set up data capture process and start
        self.dAcqThread = Thread(target=self.dmanager.dataCallback, 
                                 args=(q,))
        self.dAcqThread.start()

        self.needsSaved = True

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

    def killCapture(self):
        """
        Kills running capture. Program's behaviour
        may become undefined
        """
        try:
            self.captureProcess.terminate()
        except:
            self.errorFnc("Could not stop capture process")

        try:
            self.dAcqThread._Thread_stop()
        except:
            self.errorFnc("Could not stop data manager thread")

    def isCapturing(self):
        """
        Returns true if capturing is in progress
        """
        return self.captureProcess.is_alive()

    def setGlobalSettings(self, settings):
        self.globalSettings = settings
