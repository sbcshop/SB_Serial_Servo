/*
 * SBSInst.h
 * SB Serial Servo Instruction 
 * Date: 01/01/2020
 * Author: SB Components
 */

#ifndef _SBSINST_H
#define _SBSINST_H

typedef	char s8;
typedef	unsigned char u8;	
typedef	unsigned short u16;	
typedef	short s16;
typedef	unsigned long u32;	
typedef	long s32;

#define INST_PING 0x01
#define INST_READ 0x02
#define INST_WRITE 0x03
#define INST_REG_WRITE 0x04
#define INST_REG_ACTION 0x05
#define INST_SYNC_WRITE 0x83

class SBSInst{
public:
	SBSInst();
	SBSInst(u8 End);
	SBSInst(u8 End, u8 Level);
	int genWrite(u8 ID, u8 MemAddr, u8 *nDat, u8 nLen);	// Write Instruction
	int regWrite(u8 ID, u8 MemAddr, u8 *nDat, u8 nLen);	// Asynchronous Write Instruction
	int RegWriteAction(u8 ID = 0xfe);	// Asynchronous Write Execute Instruction
	void syncWrite(u8 ID[], u8 IDN, u8 MemAddr, u8 *nDat, u8 nLen);	//Synchronous Write Instruction
	int writeByte(u8 ID, u8 MemAddr, u8 bDat);	//Write Single Byte
	int writeWord(u8 ID, u8 MemAddr, u16 wDat);	//Write 2 Bytes
	int Read(u8 ID, u8 MemAddr, u8 *nData, u8 nLen);	//Read Instruction
	int readByte(u8 ID, u8 MemAddr);	// Read 1 Byte
	int readWord(u8 ID, u8 MemAddr);	// Read 2 Bytes
	int Ping(u8 ID);	// Ping Instrucution
public:
	u8 Level;	// Return Level
	u8 End;
	u8 Error;	// Status
protected:
	virtual int writeSBS(unsigned char *nDat, int nLen) = 0;
	virtual int readSBS(unsigned char *nDat, int nLen) = 0;
	virtual int writeSBS(unsigned char bDat) = 0;
	virtual void rFlushSBS() = 0;
	virtual void wFlushSBS() = 0;
protected:
	void writeBuf(u8 ID, u8 MemAddr, u8 *nDat, u8 nLen, u8 Fun);
	void Host2SBS(u8 *DataL, u8* DataH, u16 Data);	// Word to bytes
	u16	SBS2Host(u8 DataL, u8 DataH);	// Bytes to Word
	int	Ack(u8 ID);	// Return
	int checkHead();	// Frame Header Detection
};
#endif
