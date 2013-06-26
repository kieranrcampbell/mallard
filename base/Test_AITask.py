#!/usr/bin/python


from AITask import AITask

from math import pi
from pylab import *
from multiprocessing import Process
from numpy import *

import sys


if __name__ == "__main__":
    
    channel = "Dev1/ai8"
    print("Reading from " + channel)

    # samples from each read
    samples = 100

    # create task and start
    testAI = AITask(channels=[ channel ], samplesPerChan = samples)
    testAI.start()

#    X = arange(samples)
    data = array( [0] )

    
    # for i in xrange(20):
    #     print ("Capture " + str(i) )
    #     read_data = testAI.read()
    #     print read_data
    #     data = concatenate( [data, read_data] )
    data = testAI.read(100)
    print data
    print "shape: " + str(data.shape)
    testAI.stop()
#    plot1, = plot(data)
    show()



