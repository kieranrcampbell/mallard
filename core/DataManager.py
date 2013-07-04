#!/usr/bin/python

"""

kieran.renfrew.campbell@cern.ch
DataManager - 
passed data from the card to store & save

"""

import numpy as np

class DataManager:
    
    def __init__(self):
        print "Data manager initialised"


    def dataCallback(data):
        """
        Function called when data is received.
        """

        """
        Plot all data captured
        """
        def plot_data(data):
            X = np.arange( len(data) )
            plot(X, data)
            show()

