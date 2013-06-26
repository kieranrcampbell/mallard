/*

  Data acquisition for ISOLDE.
  kieran.renfrew.campbell@cern.ch

 */


#include "NIDAQmxBase.h"
#include "daq_trigger_base.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define DAQmxErrChk(functionCall) { if( DAQmxFailed(error=(functionCall)) ) { goto Error; } }

#define samplesPerRead 10

/*
  channel: channel for analogue data acquisition (eg "/Dev1/ai8")
  sampleRate: rate for analogue data acquisition
  triggerSource: channel for the trigger (eg "/Dev1/PFI0")
  noTriggers: number of triggers to record data for. If -1 loop is infinite */  
void setParameters(char* channel, float64 sampleRate, 
		   char* triggerSource, int noTriggers) {

  strcpy (userData.channel, channel);
  strcpy(userData.triggerSource, triggerSource);

  userData.sampleRate = sampleRate;
  userData.noTriggers = noTriggers;
}

void printAllInfo(void) {
  printf("Channel: %s \n", userData.channel);
  printf("Trigger source: %s \n", userData.triggerSource);
  printf("Sample rate: %d \n", userData.sampleRate);
  printf("Numer of triggers: %d \n", userData.noTriggers);
}

void acquire(void)
{
    // Task parameters
    int32       error = 0;
    TaskHandle  taskHandle = 0;
    char        errBuff[2048]={'\0'};
    int32       i;
    time_t      startTime;

    // Channel parameters

    float64     min = -10.0;
    float64     max = 10.0;

    // Timing parameters
    char        clockSource[] = "OnboardClock";
    uInt64      samplesPerChan = samplesPerRead; // only using 1 channel
    
    // Triggering parameters
    uInt32      triggerSlope = DAQmx_Val_RisingSlope;

    // Data read parameters
    #define     bufferSize (uInt32)samplesPerRead
    float64     data[bufferSize];
    int32       pointsToRead = bufferSize;
    int32       pointsRead;
    float64     timeout = 10.0;
    int32       totalRead = 0;


    char taskCreate[] = "Creating base task\n";
    char voltageCreate[] = "Creating voltage channel\n";
    char configTiming[] = "Configuring device timing\n";
    char configTrig[] = "Configuring rising edge trigger\n";
    char startingTask[] = "Starting daq task\n";

    int count = 0;
    
    startTime = time(NULL);

    /* create the task */
    printf(taskCreate);
    DAQmxErrChk (DAQmxBaseCreateTask("",&taskHandle));

       /* create voltage channel */
    printf(voltageCreate);
    DAQmxErrChk (DAQmxBaseCreateAIVoltageChan(taskHandle,
					      userData.channel,"",
					      DAQmx_Val_Cfg_Default,
					      min,max,
					      DAQmx_Val_Volts,NULL));

    /* configure sampe timing */
    printf(configTiming);
    DAQmxErrChk (DAQmxBaseCfgSampClkTiming(taskHandle,
					   clockSource,
					   userData.sampleRate,
					   DAQmx_Val_Rising,
					   DAQmx_Val_FiniteSamps,
					   samplesPerChan));

    /* configure the trigger */
    printf(configTrig);
    DAQmxErrChk (DAQmxBaseCfgDigEdgeStartTrig(taskHandle,
					      userData.triggerSource,
					      triggerSlope));

    startTime = time(NULL);
 
    /* Loop for desired number of triggers or infinitely if set to -1 */
    for(; count < userData.noTriggers || userData.noTriggers == -1; ++count) 
      {
      	DAQmxErrChk (DAQmxBaseStartTask(taskHandle));

        DAQmxErrChk (DAQmxBaseReadAnalogF64(taskHandle,
					    pointsToRead,
					    timeout,
					    DAQmx_Val_GroupByScanNumber,
					    data,
					    bufferSize,
					    &pointsRead,NULL));

        totalRead += pointsRead;
        printf("Acquired %ld samples. Total %ld\n",pointsRead,totalRead);
	printf("Time acquired %f \n", time);

        for (i = 0; i < bufferSize; ++i)   {
	  printf ("data[%ld] = %f\n", i, data[i]); 
	} 

	printf("Pass: %i \n", count);

	DAQmxErrChk (DAQmxBaseStopTask(taskHandle));
	DAQmxErrChk (DAQmxBaseCfgDigEdgeStartTrig(taskHandle,
						  userData.triggerSource,
						  triggerSlope));

    }

    /* stop & delete task */
    DAQmxErrChk (DAQmxBaseStopTask(taskHandle));
    DAQmxErrChk (DAQmxBaseClearTask(taskHandle));

    printf("\nAcquired %ld total samples.\n",totalRead);

Error:
    if( DAQmxFailed(error) )
        DAQmxBaseGetExtendedErrorInfo(errBuff,2048);
    if(taskHandle != 0) {
        DAQmxBaseStopTask (taskHandle);
        DAQmxBaseClearTask (taskHandle);
    }
    if( DAQmxFailed(error) )
		printf ("DAQmxBase Error %ld: %s\n", error, errBuff);
    
}

/* int main(void) { */

/*   /\* Testing *\/ */
/*   printf("Setting parameters\n"); */
/*   setParameters("/Dev1/ai8", 1000, "/Dev1/PFI0", 10); */


/*   printf("Beginning acquire\n"); */
/*   acquire(); */

/* } */

