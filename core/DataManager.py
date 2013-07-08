#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch
DataManager - 
passed data from the card to store & save

"""

import numpy as np

class DataManager:
    
    def __init__(self):
        self.data = []
        self.prev_count = 0

    def dataCallback(lastData, callback = None):
        """
        Function called when data is received.
        """
        data.append(lastData - prev_count)
        prev_count = lastData
        """
        Plot all data captured
        """
        # def plot_data(data):
        #     X = np.arange( len(data) )
        #     plot(X, data)
        #     show()


    def getData():
        """
        Simply returns previous data list
        """
