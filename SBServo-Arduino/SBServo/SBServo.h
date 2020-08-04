/*
 * SBServo.h
 * SB Servo Arduino Interface Library
 * Date: 01/01/2020
 * Author: SB Components
 */

#ifndef _SBSERVO_H
#define _SBSERVO_H

//-------Baud Rate--------
#define	SBS_1M 0
#define	SBS_0_5M 1
#define	SBS_250K 2
#define	SBS_128K 3
#define	SBS_115200 4
#define	SBS_76800	5
#define	SBS_57600	6
#define	SBS_38400	7

//	Memory Address
//-------EPROM(Read only)--------
#define SBS_VERSION_L 3
#define SBS_VERSION_H 4

//-------EPROM(Read And write)--------
#define SBS_ID 5
#define SBS_BAUD_RATE 6
#define SBS_MIN_ANGLE_LIMIT_L 9
#define SBS_MIN_ANGLE_LIMIT_H 10
#define SBS_MAX_ANGLE_LIMIT_L 11
#define SBS_MAX_ANGLE_LIMIT_H 12
#define SBS_CW_DEAD 26
#define SBS_CCW_DEAD 27

//-------SRAM(Read & Write)--------
#define SBS_TORQUE_ENABLE 40
#define SBS_GOAL_POSITION_L 42
#define SBS_GOAL_POSITION_H 43
#define SBS_GOAL_TIME_L 44
#define SBS_GOAL_TIME_H 45
#define SBS_GOAL_SPEED_L 46
#define SBS_GOAL_SPEED_H 47
#define SBS_LOCK 48

//-------SRAM(Read Only)--------
#define SBS_PRESENT_POSITION_L 56
#define SBS_PRESENT_POSITION_H 57
#define SBS_PRESENT_SPEED_L 58
#define SBS_PRESENT_SPEED_H 59
#define SBS_PRESENT_LOAD_L 60
#define SBS_PRESENT_LOAD_H 61
#define SBS_PRESENT_VOLTAGE 62
#define SBS_PRESENT_TEMPERATURE 63
#define SBS_MOVING 66
#define SBS_PRESENT_CURRENT_L 69
#define SBS_PRESENT_CURRENT_H 70

#include "Serial.h"

class SBServo : public Serial
{
public:
	SBServo();
	SBServo(u8 End);
	SBServo(u8 End, u8 Level);
	virtual int WritePos(u8 ID, u16 Position, u16 Time, u16 Speed = 0);	// Write Position of a single Servo 
	virtual int RegWritePos(u8 ID, u16 Position, u16 Time, u16 Speed = 0);	// Asynchronous Write Servo Position
	virtual void SyncWritePos(u8 ID[], u8 IDN, u16 Position[], u16 Time[], u16 Speed[]);	// Write Position for multiple Servos
	virtual int PWMMode(u8 ID);	// PWM output Mode
	virtual int WritePWM(u8 ID, s16 pwmOut);	// PWM output Mode Instruction
	virtual int EnableTorque(u8 ID, u8 Enable);	// Torque control
	virtual int unLockEprom(u8 ID);	// EEPROM Unlock
	virtual int LockEprom(u8 ID);	// EEPROM Lock
	virtual int FeedBack(int ID);	// Feedback Servo Information
	virtual int ReadPos(int ID);	// Read Position
	virtual int ReadSpeed(int ID);	// Read Speed
	virtual int ReadLoad(int ID);	// Read Torque
	virtual int ReadVoltage(int ID);	// Read Voltage
	virtual int ReadTemperature(int ID);	// Read Temperature
	virtual int ReadMove(int ID);	// Read Servo moving 
	virtual int ReadCurrent(int ID);	// Read Current
private:
	u8 Mem[SBS_PRESENT_CURRENT_H-SBS_PRESENT_POSITION_L+1];
};

#endif