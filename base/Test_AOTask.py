#!/usr/bin/python


from AOTask import AOTask
from numpy import *
from math import pi
import sys

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print ("Please enter a voltage")
        sys.exit(0)

    voltage = sys.argv[1]
    
    print ("Generate steady voltage across a01 at: " + voltage)
    output_channel = "Dev1/ao1"

    # create a numpy array of 512 in sin shape
    data = array( [voltage] )

    # initialise write task
    task = AOTask(channels=[output_channel])
    task.start()


    print ("Writing data")
    task.write( data )

    task.stop()
