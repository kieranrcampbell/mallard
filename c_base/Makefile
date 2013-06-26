nilibs=-lnidaqmxbase
includes=-I./include
flags1= -c -Wall -fPIC
ldflags= -shared
cc=gcc

output=libdaqtriggerbase
target = daq_trigger_base

srcs= daq_trigger_base.c eltime.c
objects= $(srcs:.c=.o)

      
all : 
	$(cc)  $(includes) $(flags1) $(srcs) $(nilibs) 
	$(cc) $(ldflags) -o $(output).so $(objects)

clean :
	rm -f $(target).o $(target).so
