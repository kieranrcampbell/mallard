/*********************************************************************
*
* ANSI C Example program:
*    contAcquire-ExtClk-DigStart.c
*
* Example Category:
*    AI
*
* Description:
*    This example demonstrates how to acquire a continuous amount of
*    data using an external sample clock, started by a digital edge.
*
* Instructions for Running:
*    1. Select the physical channel to correspond to where your
*       signal is input on the DAQ device.
*    2. Enter the minimum and maximum voltage ranges.
*    Note: For better accuracy try to match the Input Ranges to the
*          expected voltage level of the measured signal.
*    3. Select a source for the sample clock.
*    4. Set the approximate Rate of the external clock. This allows
*       the internal characteristics of the acquisition to be as
*       efficient as possible. Also set the Samples to Read.
*    5. Select a source for the digital edge start trigger.
*    6. Select the edge, rising or falling, on which to trigger.
*
* Steps:
*    1. Create a task.
*    2. Create an analog input voltage channel.
*    3. Define the parameters for an External Clock Source.
*       Additionally, define the sample mode to be continuous. The
*       external clock rate is given to allow the internal
*       characteristics of the acquisition to be as efficient as
*       possible.
*    4. Set the parameters for a digital edge start trigger.
*    5. Call the Start function to start the acquisition.
*    6. Read the waveform data in a loop until 10 seconds or an
*       error occurs.
*    7. Call the Clear Task function to clear the Task.
*    8. Display an error if any.
*
* I/O Connections Overview:
*    Make sure your signal input terminal matches the Physical
*    Channel I/O control. Also, make sure that your digital trigger
*    signal is connected to the terminal specified in Trigger Source.
*
* Recommended Use:
*    1. Call Configure and Start functions.
*    2. Call Read function in a loop.
*    3. Call Stop function at the end.
*
*********************************************************************/

#include "NIDAQmxBase.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>

#include <iostream>

#define DAQmxErrChk(functionCall) { if( DAQmxFailed(error=(functionCall)) ) { goto Error; } }

void printTimeElapsed(time_t *startTime);

int main(void)
{
    // Task parameters
    int32       error = 0;
    TaskHandle  taskHandle = 0;
    char        errBuff[2048]={'\0'};
    int32       i;
    time_t      startTime;

    // Channel parameters
    char        chan[] = "Dev1/ai8";
    float64     min = -10.0;
    float64     max = 10.0;

    // Timing parameters
    char        clockSource[] = "OnboardClock";
    uInt64      samplesPerChan = 32;
    float64     sampleRate = 1000.0;

    // Triggering parameters
    char        triggerSource[] = "/Dev1/PFI0";
    uInt32      triggerSlope = DAQmx_Val_RisingSlope;
    uInt32      triggerSamples = 100;

    // Data read parameters
    #define     bufferSize (uInt32)32
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
    DAQmxErrChk (DAQmxBaseCreateAIVoltageChan(taskHandle,chan,"",DAQmx_Val_Cfg_Default,min,max,DAQmx_Val_Volts,NULL));

    /* configure sampe timing */
    printf(configTiming);
    DAQmxErrChk (DAQmxBaseCfgSampClkTiming(taskHandle,clockSource,sampleRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,samplesPerChan));

    /* configure the trigger */
    printf(configTrig);
    DAQmxErrChk (DAQmxBaseCfgDigEdgeStartTrig(taskHandle,triggerSource,triggerSlope));

    /* start the task */
    printf(startingTask);
    //    DAQmxErrChk (DAQmxBaseStartTask(taskHandle));

    // The loop will quit after 10 seconds

    startTime = time(NULL);
    /* time(NULL)<startTime+10 */

    

    while( count < 100) {
      	DAQmxErrChk (DAQmxBaseStartTask(taskHandle));

        DAQmxErrChk (DAQmxBaseReadAnalogF64(taskHandle,pointsToRead,timeout,DAQmx_Val_GroupByScanNumber,data,bufferSize,&pointsRead,NULL));
        totalRead += pointsRead;
        printf("Acquired %ld samples. Total %ld\n",pointsRead,totalRead);

	printf("Time acquired %f \n", time);

	//	std::cout << "Size of data array: " << sizeof(data) << std::endl;
        for (i = 0; i < bufferSize; ++i)   {
	  //	  printf ("data[%ld] = %f\n", i, data[i]); 
	   std::cout << "data[" << i << "] = " << data[i] << std::endl; 
	} 

	printf("Pass: %i \n", count++);


	DAQmxErrChk (DAQmxBaseStopTask(taskHandle));
	DAQmxErrChk (DAQmxBaseCfgDigEdgeStartTrig(taskHandle,triggerSource,triggerSlope));

	
    }

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
    return 0;
}

void printTimeElapsed(time_t *startTime) {
  printf("Time elapsed: %ld \n", time(NULL) - (*startTime));
  (*startTime) = time(NULL);
}
