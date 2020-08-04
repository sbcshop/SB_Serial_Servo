/*
 * Serial.h
 * SB Servo Serial Communication
 * Date: 01/01/2020
 * Author: SB Components
 */

#ifndef _SERIAL_H
#define _SERIAL_H

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include "SBSInst.h"

class Serial : public SBSInst
{
public:
	Serial();
	Serial(u8 End);
	Serial(u8 End, u8 Level);

protected:
	virtual int writeSBS(unsigned char *nDat, int nLen);	// Output n Bytes
	virtual int readSBS(unsigned char *nDat, int nLen);	// Read Input
	virtual int writeSBS(unsigned char bDat);	// 1 Byte Output
	virtual void rFlushSBS();//
	virtual void wFlushSBS();//
public:
	unsigned long int IOTimeOut;	// Input/Output Timeout
	HardwareSerial *pSerial;	//Pointer to Serial Port
	int Err;
public:
	virtual int getErr(){  return Err;  }
};

#endif