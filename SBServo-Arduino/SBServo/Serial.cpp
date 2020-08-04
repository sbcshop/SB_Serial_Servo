/*
 * Serial.cpp
 * SB Servo Serial Communication
 * Date: 01/01/2020
 * Author: SB Components
 */


#include "Serial.h"

Serial::Serial()
{
	IOTimeOut = 100;
	pSerial = NULL;
}

Serial::Serial(u8 End):SBSInst(End)
{
	IOTimeOut = 100;
	pSerial = NULL;
}

Serial::Serial(u8 End, u8 Level):SBSInst(End, Level)
{
	IOTimeOut = 100;
	pSerial = NULL;
}

int Serial::readSBS(unsigned char *nDat, int nLen)
{
	int Size = 0;
	int ComData;
	unsigned long t_begin = millis();
	unsigned long t_user;
	while(1){
		ComData = pSerial->read();
		if(ComData!=-1){
			if(nDat){
				nDat[Size] = ComData;
			}
			Size++;
			t_begin = millis();
		}
		if(Size>=nLen){
			break;
		}
		t_user = millis() - t_begin;
		if(t_user>IOTimeOut){
			break;
		}
	}
	return Size;
}

int Serial::writeSBS(unsigned char *nDat, int nLen)
{
	if(nDat==NULL){
		return 0;
	}
	return pSerial->write(nDat, nLen);
}

int Serial::writeSBS(unsigned char bDat)
{
	return pSerial->write(&bDat, 1);
}

void Serial::rFlushSBS()
{
	while(pSerial->read()!=-1);
}

void Serial::wFlushSBS()
{
}