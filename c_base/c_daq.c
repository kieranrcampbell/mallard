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




void acquire(void (*pyCallbackFunc)(uInt32),
	     double (*pyVoltFunc)(uInt32)) {
  // Task parameters
  int32       error = 0;
  //  TaskHandle  taskHandle = 0;
  char        errBuff[2048]={'\0'};
  time_t      startTime;

  // Data read parameters
  uInt32      data;
  float64     timeout = 5.0;

  // Channel parameters
  float64     min = 0.0;
  float64     max = 5.0;

  // Task parameters
  //  memcpy(writeParams.gerrBuff, '\0', 1);

  // Data write parameters
  TaskHandle taskHandle = 0;

  float64 voltage = 0.0;
  float64 newVoltage = 0.0;

  writeParams.gtimeout = 10.0;
  writeParams.taskHandle = 0;
  writeParams.samplesPerChan = 1;

  // counter stuff
  DAQmxErrChk (DAQmxBaseCreateTask("",&taskHandle));
  DAQmxErrChk (DAQmxBaseCreateCICountEdgesChan(taskHandle,
					       userData.readChannel,"",
					       DAQmx_Val_Falling,0,
					       DAQmx_Val_CountUp));
  DAQmxErrChk (DAQmxBaseStartTask(taskHandle));
  gRunning = 1;

  // analogue output stuff
  DAQmxErrChk(DAQmxBaseCreateTask("", &writeParams.taskHandle));
  DAQmxErrChk(DAQmxBaseCreateAOVoltageChan(writeParams.taskHandle, 
					   userData.writeChannel,
					   "",min,max,
					   DAQmx_Val_Volts,NULL));
  DAQmxErrChk(DAQmxBaseStartTask(writeParams.taskHandle));



  // The loop will quit after 10 seconds
  startTime = time(NULL);
  while( gRunning && time(NULL)<startTime+10 ) {
    DAQmxErrChk (DAQmxBaseReadCounterScalarU32(taskHandle,
					       timeout,&data,NULL));

    /* callback to python */
    if(userData.contReport)
      pyCallbackFunc(data);

    float64 gdata = 1.7;
    uInt32 cnt = 0;
    newVoltage = pyVoltFunc(cnt);
    if(newVoltage != voltage) {
      printf("voltage: %f \n", newVoltage);

      voltage = newVoltage;
      DAQmxErrChk(DAQmxBaseWriteAnalogF64(writeParams.taskHandle,
					  writeParams.samplesPerChan,0,
					  writeParams.gtimeout,
					  DAQmx_Val_GroupByChannel,
					  &voltage,
					  &writeParams.gpointsWritten,
					  NULL));


    }

  }



 Error:
  puts("");
  
  if( DAQmxFailed(error) )
    DAQmxBaseGetExtendedErrorInfo(errBuff,2048);
  if( taskHandle!=0 ) {
    DAQmxBaseStopTask(taskHandle);
    DAQmxBaseClearTask(taskHandle);
  }
  if( writeParams.taskHandle!=0 ) {
    DAQmxBaseStopTask(writeParams.taskHandle);
    DAQmxBaseClearTask(writeParams.taskHandle);
  }


  if( DAQmxFailed(error) )
    printf ("DAQmxBase Error %ld: %s\n", error, errBuff);

}

void setParameters(char* readChannel, char* writeChannel, 
		   _Bool contReport, int reportEvery) {
  strcpy (userData.readChannel, readChannel);
  strcpy (userData.writeChannel, writeChannel);
  
  userData.contReport = contReport;
  userData.reportEvery = reportEvery; 

}

void printAllInfo(void) {
  printf("Write Channel: %s \n", userData.writeChannel);
  printf("Read Channel: %s \n", userData.readChannel);
  printf("Continous reporting: %d \n", userData.contReport);
  printf("Report every: %ud \n", userData.reportEvery);
}


