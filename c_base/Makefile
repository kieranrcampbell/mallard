nilibs=-lnidaqmxbase
includes=-I./include
flags= -O2 -m32
cc=gcc

build_files = daq_trigger_base.c
      
all : $(build_files)

% : %.c
	$(cc) $(includes) $(flags) $< $(nilibs) -o $@

clean :
	rm -f $(ao_examples)
