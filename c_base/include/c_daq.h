/*

  Data acquisition for ISOLDE.
  kieran.renfrew.campbell@cern.ch

 */

#ifndef DAQ_TRIGGER_BASE_H
#define DAQ_TRIGGER_BASE_H

#include "NIDAQmxBase.h"


/*
  Defines all parameters which need to be passed to here at runtime
  by the user (using python)
*/

struct UserData {
  char channel[256]; // analogue input channel
  _Bool contReport; // send captured data back after each trigger

  int reportEvery; // call back to python every ; not yet implemented

} userData;

/*
  channel: counter channel for digital data acquisition,
  so in this case "Dev1/ctr1" for PFI3

  contReport: continuously reports back to python

  reportEvery: callback to function every n loops

*/
void setParameters(char* channel, _Bool contReport,
		   int reportEvery);


void printAllInfo(void);

/* Begins data acquisition */
void acquire(void (*pyCallbackFunc)(uInt32));
#endif
