/*
 * SBServo.cpp
 * SB Servo Arduino Interface Library
 * Date: 01/01/2020
 * Author: SB Components
 */

#include "SBServo.h"

SBServo::SBServo()
{
	End = 1;
}

SBServo::SBServo(u8 End):Serial(End)
{
}

SBServo::SBServo(u8 End, u8 Level):Serial(End, Level)
{
}

int SBServo::WritePos(u8 ID, u16 Position, u16 Time, u16 Speed)
{
	u8 bBuf[6];
	Host2SBS(bBuf+0, bBuf+1, Position);
	Host2SBS(bBuf+2, bBuf+3, Time);
	Host2SBS(bBuf+4, bBuf+5, Speed);
	
	return genWrite(ID, SBS_GOAL_POSITION_L, bBuf, 6);
}

int SBServo::RegWritePos(u8 ID, u16 Position, u16 Time, u16 Speed)
{
	u8 bBuf[6];
	Host2SBS(bBuf+0, bBuf+1, Position);
	Host2SBS(bBuf+2, bBuf+3, Time);
	Host2SBS(bBuf+4, bBuf+5, Speed);
	
	return regWrite(ID, SBS_GOAL_POSITION_L, bBuf, 6);
}

void SBServo::SyncWritePos(u8 ID[], u8 IDN, u16 Position[], u16 Time[], u16 Speed[])
{
    u8 offbuf[6*IDN];
    for(u8 i = 0; i<IDN; i++){
		u16 T, V;
		if(Time){
			T = Time[i];
		}else{
			T = 0;
		}
		if(Speed){
			V = Speed[i];
		}else{
			V = 0;
		}
        Host2SBS(offbuf+i*6+0, offbuf+i*6+1, Position[i]);
        Host2SBS(offbuf+i*6+2, offbuf+i*6+3, T);
        Host2SBS(offbuf+i*6+4, offbuf+i*6+5, V);
    }
    syncWrite(ID, IDN, SBS_GOAL_POSITION_L, offbuf, 6);
}

int SBServo::PWMMode(u8 ID)
{
	u8 bBuf[4];
	bBuf[0] = 0;
	bBuf[1] = 0;
	bBuf[2] = 0;
	bBuf[3] = 0;
	return genWrite(ID, SBS_MIN_ANGLE_LIMIT_L, bBuf, 4);	
}

int SBServo::WritePWM(u8 ID, s16 pwmOut)
{
	if(pwmOut<0){
		pwmOut = -pwmOut;
		pwmOut |= (1<<10);
	}
	u8 bBuf[2];
	Host2SBS(bBuf+0, bBuf+1, pwmOut);
	
	if(ID==0xfe){
		genWrite(ID, SBS_GOAL_TIME_L, bBuf, 2);
	}else{
		syncWrite(&ID, 1, SBS_GOAL_TIME_L, bBuf, 2);
	}
	return 1;
}

int SBServo::EnableTorque(u8 ID, u8 Enable)
{
	return writeByte(ID, SBS_TORQUE_ENABLE, Enable);
}

int SBServo::unLockEprom(u8 ID)
{
	return writeByte(ID, SBS_LOCK, 0);
}

int SBServo::LockEprom(u8 ID)
{
	return writeByte(ID, SBS_LOCK, 1);
}

int SBServo::FeedBack(int ID)
{
	int nLen = Read(ID, SBS_PRESENT_POSITION_L, Mem, sizeof(Mem));
	if(nLen!=sizeof(Mem)){
		Err = 1;
		return -1;
	}
	Err = 0;
	return nLen;
}
	
int SBServo::ReadPos(int ID)
{
	int Pos = -1;
	if(ID==-1){
		Pos = Mem[SBS_PRESENT_POSITION_L-SBS_PRESENT_POSITION_L];
		Pos <<= 8;
		Pos |= Mem[SBS_PRESENT_POSITION_H-SBS_PRESENT_POSITION_L];
	}else{
		Err = 0;
		Pos = readWord(ID, SBS_PRESENT_POSITION_L);
		if(Pos==-1){
			Err = 1;
		}
	}
	return Pos;
}

int SBServo::ReadSpeed(int ID)
{
	int Speed = -1;
	if(ID==-1){
		Speed = Mem[SBS_PRESENT_SPEED_L-SBS_PRESENT_POSITION_L];
		Speed <<= 8;
		Speed |= Mem[SBS_PRESENT_SPEED_H-SBS_PRESENT_POSITION_L];
	}else{
		Err = 0;
		Speed = readWord(ID, SBS_PRESENT_SPEED_L);
		if(Speed==-1){
			Err = 1;
			return -1;
		}
	}
	if(!Err && (Speed&(1<<15))){
		Speed = -(Speed&~(1<<15));
	}	
	return Speed;
}

int SBServo::ReadLoad(int ID)
{
	int Load = -1;
	if(ID==-1){
		Load = Mem[SBS_PRESENT_LOAD_L-SBS_PRESENT_POSITION_L];
		Load <<= 8;
		Load |= Mem[SBS_PRESENT_LOAD_H-SBS_PRESENT_POSITION_L];
	}else{
		Err = 0;
		Load = readWord(ID, SBS_PRESENT_LOAD_L);
		if(Load==-1){
			Err = 1;
		}
	}
	if(!Err && (Load&(1<<10))){
		Load = -(Load&~(1<<10));
	}	
	return Load;
}

int SBServo::ReadVoltage(int ID)
{
	int Voltage = -1;
	if(ID==-1){
		Voltage = Mem[SBS_PRESENT_VOLTAGE-SBS_PRESENT_POSITION_L];	
	}else{
		Err = 0;
		Voltage = readByte(ID, SBS_PRESENT_VOLTAGE);
		if(Voltage==-1){
			Err = 1;
		}
	}
	return Voltage;
}

int SBServo::ReadTemperature(int ID)
{
	int Temper = -1;
	if(ID==-1){
		Temper = Mem[SBS_PRESENT_TEMPERATURE-SBS_PRESENT_POSITION_L];	
	}else{
		Err = 0;
		Temper = readByte(ID, SBS_PRESENT_TEMPERATURE);
		if(Temper==-1){
			Err = 1;
		}
	}
	return Temper;
}

int SBServo::ReadMove(int ID)
{
	int Move = -1;
	if(ID==-1){
		Move = Mem[SBS_MOVING-SBS_PRESENT_POSITION_L];	
	}else{
		Err = 0;
		Move = readByte(ID, SBS_MOVING);
		if(Move==-1){
			Err = 1;
		}
	}
	return Move;
}

int SBServo::ReadCurrent(int ID)
{
	int Current = -1;
	if(ID==-1){
		Current = Mem[SBS_PRESENT_CURRENT_L-SBS_PRESENT_POSITION_L];
		Current <<= 8;
		Current |= Mem[SBS_PRESENT_CURRENT_H-SBS_PRESENT_POSITION_L];
	}else{
		Err = 0;
		Current = readWord(ID, SBS_PRESENT_CURRENT_L);
		if(Current==-1){
			Err = 1;
			return -1;
		}
	}
	if(!Err && (Current&(1<<15))){
		Current = -(Current&~(1<<15));
	}	
	return Current;
}