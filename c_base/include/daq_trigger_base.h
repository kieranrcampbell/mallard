/*

  Data acquisition for ISOLDE.
  kieran.renfrew.campbell@cern.ch

 */

#ifndef DAQ_TRIGGER_BASE_H
#define DAQ_TRIGGER_BASE_H


/*
  Defines all parameters which need to be passed to here at runtime
  by the user (using python)
*/

struct UserData {
  char channel[256]; // analogue input channel
  float64 sampleRate; // rate at which each sample is read
  char triggerSource[256]; // input channel for the trigger

  /*
    Number of triggers to listen and record data for.
    Note this number is not guaranteed if the rate is
    set too fast
  */
  int noTriggers; 

  /* more will be added in future */

} userData;

/*
  channel: channel for analogue data acquisition (eg "/Dev1/ai8")
  sampleRate: rate for analogue data acquisition
  triggerSource: channel for the trigger (eg "/Dev1/PFI0")
  noTriggers: number of triggers to record data for. If -1 loop is infinite */  
void setParameters(char* channel, float64 sampleRate, 
		   char* triggerSource, int noTriggers);


void printAllInfo(void);

/* Begins data acquisition */
void acquire(void);


#endif
