nilibs=-lnidaqmxbase
includes=-I./include
flags1= -c -Wall -fPIC
ldflags= -shared
cc=gcc
output=libdaqtriggerbase

target = daq_trigger_base
      
all : 
	$(cc)  $(includes) $(flags1) $(target).c $(nilibs) 
	$(cc) $(ldflags) -o $(output).so $(target).o

clean :
	rm -f $(target).o $(target).so
