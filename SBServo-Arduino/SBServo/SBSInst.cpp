/*
 * SBSInst.cpp
 * SB Serial Servo Instruction Control
 * Date: 01/01/2020
 * Author: SB Components
 */

#include <stddef.h>
#include "SBSInst.h"

SBSInst::SBSInst()
{
	Level = 1;//All instructions except the broadcast command return a response
	Error = 0;
}

SBSInst::SBSInst(u8 End)
{
	Level = 1;
	this->End = End;
	Error = 0;
}

SBSInst::SBSInst(u8 End, u8 Level)
{
	this->Level = Level;
	this->End = End;
	Error = 0;
}

// 1 16-bit split into 2 8 digits
//DataL，DataH
void SBSInst::Host2SBS(u8 *DataL, u8* DataH, u16 Data)
{
	if(End){
		*DataL = (Data>>8);
		*DataH = (Data&0xff);
	}else{
		*DataH = (Data>>8);
		*DataL = (Data&0xff);
	}
}

//2 8-digit combinations for 1 16-digit number
//DataL，DataH
u16 SBSInst::SBS2Host(u8 DataL, u8 DataH)
{
	u16 Data;
	if(End){
		Data = DataL;
		Data<<=8;
		Data |= DataH;
	}else{
		Data = DataH;
		Data<<=8;
		Data |= DataL;
	}
	return Data;
}

void SBSInst::writeBuf(u8 ID, u8 MemAddr, u8 *nDat, u8 nLen, u8 Fun)
{
	u8 msgLen = 2;
	u8 bBuf[6];
	u8 CheckSum = 0;
	bBuf[0] = 0xff;
	bBuf[1] = 0xff;
	bBuf[2] = ID;
	bBuf[4] = Fun;
	if(nDat){
		msgLen += nLen + 1;
		bBuf[3] = msgLen;
		bBuf[5] = MemAddr;
		writeSBS(bBuf, 6);
		
	}else{
		bBuf[3] = msgLen;
		writeSBS(bBuf, 5);
	}
	CheckSum = ID + msgLen + Fun + MemAddr;
	u8 i = 0;
	if(nDat){
		for(i=0; i<nLen; i++){
			CheckSum += nDat[i];
		}
		writeSBS(nDat, nLen);
	}
	writeSBS(~CheckSum);
}

//write command
//Servo ID，MemAddr，Data Input，Write length
int SBSInst::genWrite(u8 ID, u8 MemAddr, u8 *nDat, u8 nLen)
{
	rFlushSBS();
	writeBuf(ID, MemAddr, nDat, nLen, INST_WRITE);
	wFlushSBS();
	return Ack(ID);
}

//Asynchronous write instruction
//Servo ID，MemAddr, Data Input，Write Length
int SBSInst::regWrite(u8 ID, u8 MemAddr, u8 *nDat, u8 nLen)
{
	rFlushSBS();
	writeBuf(ID, MemAddr, nDat, nLen, INST_REG_WRITE);
	wFlushSBS();
	return Ack(ID);
}

//Asynchronous write execution instruction
//Servo ID
int SBSInst::RegWriteAction(u8 ID)
{
	rFlushSBS();
	writeBuf(ID, 0, NULL, 0, INST_REG_ACTION);
	wFlushSBS();
	return Ack(ID);
}

//Synchronous Write Instruction
//params: Servo ID [] array, ID array length, Memory Address, write Data, write Length
void SBSInst::syncWrite(u8 ID[], u8 IDN, u8 MemAddr, u8 *nDat, u8 nLen)
{
	rFlushSBS();
	u8 mesLen = ((nLen+1)*IDN+4);
	u8 Sum = 0;
	u8 bBuf[7];
	bBuf[0] = 0xff;
	bBuf[1] = 0xff;
	bBuf[2] = 0xfe;
	bBuf[3] = mesLen;
	bBuf[4] = INST_SYNC_WRITE;
	bBuf[5] = MemAddr;
	bBuf[6] = nLen;
	writeSBS(bBuf, 7);

	Sum = 0xfe + mesLen + INST_SYNC_WRITE + MemAddr + nLen;
	u8 i, j;
	for(i=0; i<IDN; i++){
		writeSBS(ID[i]);
		writeSBS(nDat+i*nLen, nLen);
		Sum += ID[i];
		for(j=0; j<nLen; j++){
			Sum += nDat[i*nLen+j];
		}
	}
	writeSBS(~Sum);
	wFlushSBS();
}

int SBSInst::writeByte(u8 ID, u8 MemAddr, u8 bDat)
{
	rFlushSBS();
	writeBuf(ID, MemAddr, &bDat, 1, INST_WRITE);
	wFlushSBS();
	return Ack(ID);
}

int SBSInst::writeWord(u8 ID, u8 MemAddr, u16 wDat)
{
	u8 bBuf[2];
	Host2SBS(bBuf+0, bBuf+1, wDat);
	rFlushSBS();
	writeBuf(ID, MemAddr, bBuf, 2, INST_WRITE);
	wFlushSBS();
	return Ack(ID);
}

//Read Instruction
//params: Servo ID, Memory Address, return data nData, data length nLen
int SBSInst::Read(u8 ID, u8 MemAddr, u8 *nData, u8 nLen)
{
	rFlushSBS();
	writeBuf(ID, MemAddr, &nLen, 1, INST_READ);
	wFlushSBS();
	if(!checkHead()){
		return 0;
	}
	u8 bBuf[4];
	Error = 0;
	if(readSBS(bBuf, 3)!=3){
		return 0;
	}
	int Size = readSBS(nData, nLen);
	if(Size!=nLen){
		return 0;
	}
	if(readSBS(bBuf+3, 1)!=1){
		return 0;
	}
	u8 calSum = bBuf[0]+bBuf[1]+bBuf[2];
	u8 i;
	for(i=0; i<Size; i++){
		calSum += nData[i];
	}
	calSum = ~calSum;
	if(calSum!=bBuf[3]){
		return 0;
	}
	Error = bBuf[2];
	return Size;
}

//Read 1 Byte
int SBSInst::readByte(u8 ID, u8 MemAddr)
{
	u8 bDat;
	int Size = Read(ID, MemAddr, &bDat, 1);
	if(Size!=1){
		return -1;
	}else{
		return bDat;
	}
}

//Read a Word
int SBSInst::readWord(u8 ID, u8 MemAddr)
{	
	u8 nDat[2];
	int Size;
	u16 wDat;
	Size = Read(ID, MemAddr, nDat, 2);
	if(Size!=2)
		return -1;
	wDat = SBS2Host(nDat[0], nDat[1]);
	return wDat;
}

//Ping command, 
//return: servo ID
int	SBSInst::Ping(u8 ID)
{
	rFlushSBS();
	writeBuf(ID, 0, NULL, 0, INST_PING);
	wFlushSBS();
	Error = 0;
	if(!checkHead()){
		return -1;
	}
	u8 bBuf[4];
	if(readSBS(bBuf, 4)!=4){
		return -1;
	}
	if(bBuf[0]!=ID && ID!=0xfe){
		return -1;
	}
	if(bBuf[1]!=2){
		return -1;
	}
	u8 calSum = ~(bBuf[0]+bBuf[1]+bBuf[2]);
	if(calSum!=bBuf[3]){
		return -1;			
	}
	Error = bBuf[2];
	return bBuf[0];
}

int SBSInst::checkHead()
{
	u8 bDat;
	u8 bBuf[2] = {0, 0};
	u8 Cnt = 0;
	while(1){
		if(!readSBS(&bDat, 1)){
			return 0;
		}
		bBuf[1] = bBuf[0];
		bBuf[0] = bDat;
		if(bBuf[0]==0xff && bBuf[1]==0xff){
			break;
		}
		Cnt++;
		if(Cnt>10){
			return 0;
		}
	}
	return 1;
}

int	SBSInst::Ack(u8 ID)
{
	Error = 0;
	if(ID!=0xfe && Level){
		if(!checkHead()){
			return 0;
		}
		u8 bBuf[4];
		if(readSBS(bBuf, 4)!=4){
			return 0;
		}
		if(bBuf[0]!=ID){
			return 0;
		}
		if(bBuf[1]!=2){
			return 0;
		}
		u8 calSum = ~(bBuf[0]+bBuf[1]+bBuf[2]);
		if(calSum!=bBuf[3]){
			return 0;			
		}
		Error = bBuf[2];
	}
	return 1;
}
