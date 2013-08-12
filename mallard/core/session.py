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
import ConfigParser

import wx


class CaptureSession:
    """
    Interfaces between card, gui and data buffers
    """    
    def __init__(self, globalSession, errorFnc):
        self.settings = SessionSettings()
        self.fileManager = FileManager(self.settings)
        self.dmanager = DataManager(self.settings, 
                                    globalSession,
                                    errorFnc) 

        self.needsSaved = False # captured data that needs saved
        
        # method that updates statusbar
        self.globalSession = globalSession
        
        # method displays error popup
        self.errorFnc = errorFnc
        


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
        self.dmanager.initialise(self.settings, 
                                 self.globalSession,
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


class GlobalSession:
    """
    Mainly to deal with global settings
    """
    
    def __init__(self):
        import os
        
        self.configFile = os.path.join( os.path.expanduser("~"), 
                                        "mallard.ini" )

        self.globalSettings = GlobalSettings()
        self.parseFromFile()

        self.statusCallback = None


    def setSettings(self, settings):
        self.globalSettings = settings
        self.saveToFile()

    def getSettings(self):
        return self.globalSettings

    def parseFromFile(self):
        """
        reads in settings from user config file
        """
        import os

        if os.path.exists(self.configFile):

            config = ConfigParser.ConfigParser()
            config.read(self.configFile)
            
            self.globalSettings.countGraphStyle = \
                        int( config.get("mallard","countGraphStyle") )
            self.globalSettings.voltGraphStyle = \
                        int( config.get("mallard","voltGraphStyle") )
            self.globalSettings.meanStyle = \
                        int( config.get("mallard","meanStyle") )
        
                                                         
                                              

    def saveToFile(self):
        """
        Saves current settings to user file
        """
        config = ConfigParser.ConfigParser()

        config.add_section("mallard")
        config.set("mallard", "countGraphStyle",
                   self.globalSettings.countGraphStyle)
        config.set("mallard", "voltGraphStyle",
                   self.globalSettings.voltGraphStyle)
        config.set("mallard", "meanStyle",
                   self.globalSettings.meanStyle)

        f = open(self.configFile, 'w')
        config.write(f)

