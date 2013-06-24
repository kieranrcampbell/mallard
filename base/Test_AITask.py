#!/usr/bin/python


from AITask import AITask
from numpy import *
from math import pi
import sys

if __name__ == "__main__":
    
    channel = "Dev1/ai0"
    print("Reading from " + channel)

    import time
    testAI = AITask(channels=[ channel ])
    testAI.start()
    time.sleep(1)
    for i in xrange(5):
        print testAI.read()
    testAI.stop()
