nilibs=-lnidaqmxbase
includes=-I./include
flags= -O2 -m32
ldflags= -shared
cc=gcc

build_files = daq_trigger_base
      
all : $(build_files)

% : %.c
	$(cc) $(ldflags) $(includes) $(flags) $< $(nilibs) -o $@.so

clean :
	rm -f $(ao_examples)
