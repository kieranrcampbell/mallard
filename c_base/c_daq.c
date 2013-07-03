/*********************************************************************
 *   Data acquisition for ISOLDE.
 *    kieran.renfrew.campbell@cern.ch


 * set running on digital counter channel
 * eg Dev1/ctr1
 */


#include "c_daq.h"
#include <stdio.h>
#include <time.h>
#include <string.h>

#define DAQmxErrChk(functionCall) { if( DAQmxFailed(error=(functionCall)) ) { goto Error; } }

static int gRunning;




void acquire(void (*pyCallbackFunc)(uInt32)) {
  // Task parameters
  int32       error = 0;
  TaskHandle  taskHandle = 0;
  char        errBuff[2048]={'\0'};
  time_t      startTime;

  // Data read parameters
  uInt32      data;
  float64     timeout = 5.0;
  int count = 0;


  DAQmxErrChk (DAQmxBaseCreateTask("",&taskHandle));
  DAQmxErrChk (DAQmxBaseCreateCICountEdgesChan(taskHandle,
					       userData.channel,"",
					       DAQmx_Val_Falling,0,
					       DAQmx_Val_CountUp));
  DAQmxErrChk (DAQmxBaseStartTask(taskHandle));
  gRunning = 1;
  // The loop will quit after 10 seconds
  startTime = time(NULL);
  while( gRunning && time(NULL)<startTime+10 ) {
    DAQmxErrChk (DAQmxBaseReadCounterScalarU32(taskHandle,
					       timeout,&data,NULL));

    /* callback to python */
    if(userData.contReport)
      pyCallbackFunc(data);

    //printf("\rCount: %ld / %d \n",data, ++count);
  }

 Error:
  puts("");
  if( DAQmxFailed(error) )
    DAQmxBaseGetExtendedErrorInfo(errBuff,2048);
  if( taskHandle!=0 ) {
    DAQmxBaseStopTask(taskHandle);
    DAQmxBaseClearTask(taskHandle);
  }
  if( DAQmxFailed(error) )
    printf ("DAQmxBase Error %ld: %s\n", error, errBuff);

}

void setParameters(char* channel, _Bool contReport,
		   int reportEvery) {
  strcpy (userData.channel, channel);
  
  userData.contReport = contReport;
  userData.reportEvery = reportEvery; 

}

void printAllInfo(void) {
  printf("Channel: %s \n", userData.channel);
  printf("Continous reporting: %d \n", userData.contReport);
  printf("Report every: %ud \n", userData.reportEvery);
}
