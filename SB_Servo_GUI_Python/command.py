#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file

Author: SB Components
Website: shop.sb-components.co.uk
Oct 2019
"""

from checksum import CheckSum

Start_Byte = 0xFF
Ping_Instruction = 1
Read_Instruction = 2
Write_Instruction = 3
Reg_Write_Instruction = 4
Action_Instruction = 5
Syc_Write_Instruction = 0x83
Reset_Instruction = 6

#  EEPROM
A_Software_Version = 3  # 0x03
A_ID = 5
A_Baud = 6
A_Return_delay = 7  # 0x07
A_Answer_Status = 8  # 0x08
A_MinAngleLimit = 9  # 0x09
A_MaxAngleLimit = 11  # 0x0B
A_MaxTempLimit = 13  # 0x0D
A_MaxInVoltage = 14  # 0x0E
A_MinInVoltage = 15  # 0x0F
A_MaxTorque = 16  # 0x10
A_Proportional = 21  # 0x15
A_Derivative = 22  # 0x16
A_Integral = 23  # 0x17
A_MinPWM = 24  # 0x18

#  RAM
A_TorqueSwitch = 40  # 0x28
A_TargetPos_H = 42  # 0x2A
A_TargetPos_L = 43  # 0x2B
A_RunTime_H = 44  # 0x2C
A_RunTime_L = 45  # 0x2D
A_RunSpeed_H = 46  # 0x2E
A_RunSpeed_L = 47  # 0x2F
A_Lock = 48  # 0x30
A_CurrentPos = 56  # 0x38
A_CurrentSpeed = 58 # 0x3A
A_CurrentLoad = 60 # 0x3C
A_Voltage = 62  # 0x3E
A_Temp = 63  # 0x3F
A_RegWriteSign = 64  # 0x40


class CommandSet(CheckSum):
    def __init__(self, debug=False):
        self.debug = debug
        CheckSum.__init__(self)

    def final_data(self, servo_id, instruction, params=[]):
        #  Find Checksum and Data length
        checksum, data_length = self.check_sum(servo_id, instruction, params)
        #  Arrange data in array
        data = [Start_Byte, Start_Byte, servo_id, data_length,
                instruction] + params + [checksum]
        #  Convert Array into byte Array
        if self.debug:
            s = ' '
            print('raw data:', s.join(str(i) for i in data))
        data_bytes = bytearray(data)
        return data_bytes

    def read_set(self, servo_id, add, read_len):
        """
        Read Servo Parameters
        :return: Byte array for Read data from servo
        """
        data = [add, read_len]
        data_array = self.final_data(servo_id=servo_id,
                                     instruction=Read_Instruction, params=data)
        return data_array

    def write_set(self, servo_id, add, write_value):
        """
        Write to servo
        :return: Data set for Writing data to servo
        """
        if isinstance(write_value, int):
            data = [add, write_value]
        elif isinstance(write_value, list):
            data = [add] + write_value

        data_array = self.final_data(servo_id=servo_id,
                                     instruction=Write_Instruction,
                                     params=data)
        return data_array

    def reg_write_set(self, servo_id, add, write_value):
        """
        When the REG WRITE instruction frame is received, the received data
        is stored in the buffer reserve and the Registered Instruction
        Register is set at 1. When the ACTION instruction is received,
        the stored instruction is finally executed.
        :return: Data set for REG Writing data to servo
        """
        if isinstance(write_value, int):
            data = [add, write_value]
        elif isinstance(write_value, list):
            data = [add] + write_value
        data_array = self.final_data(servo_id=servo_id,
                                     instruction=Reg_Write_Instruction,
                                     params=data)
        return data_array

    def action_set(self):
        """
        Used For asynchronous Writing instruction
        :return: Data set for Action set to servo
        """
        servo_id = 0xFE
        data_array = self.final_data(servo_id=servo_id,
                                     instruction=Action_Instruction)
        return data_array

    def syc_write_set(self):
        """
        A SYNC WRITE instruction can modify the control table contents of
        multiple servos at one time,
        :return: Data set for Action set to servo
        """
        servo_id = 0xFE
        data_array = self.final_data(servo_id=servo_id,
                                     instruction=Syc_Write_Instruction,
                                     params=data)
        return data_array

    def reset_set(self, servo_id):
        """
        Reset Servo Configuration to default
        returns: Reset Data Set for given servo
        """
        data_array = self.final_data(servo_id=servo_id,
                                     instruction=Reset_Instruction)
        return data_array


class Commands(CommandSet):
    def __init__(self, debug=False):
        self.debug = debug
        CommandSet.__init__(self, self.debug)

    @staticmethod
    def mc_data(value):
        """
        Convert a word into Bytes
        :param value: Integer
        :return: 2 bytes from word(value)
        """
        data_l = value >> 8
        data_h = value & 255
        return data_l, data_h

    def ping(self, servo_id=254):
        data_array = self.final_data(servo_id, instruction=Ping_Instruction)
        return data_array

    #  READ
    def read_id(self, servo_id, read_len=1):
        return self.read_set(servo_id=servo_id, add=A_ID, read_len=read_len)

    def read_voltage(self, servo_id, read_len=1):
        return self.read_set(servo_id, add=A_Voltage, read_len=read_len)

    def read_temp(self, servo_id, read_len=1):
        return self.read_set(servo_id, add=A_Temp, read_len=read_len)

    def read_pos(self, servo_id, read_len=2):
        rec_data = self.read_set(servo_id, add=A_CurrentPos, read_len=read_len)
        return rec_data

    def read_speed(self, servo_id, read_len=2):
        rec_data = self.read_set(servo_id, add=A_CurrentSpeed, read_len=read_len)
        return rec_data

    def read_load(self, servo_id, read_len=2):
        rec_data = self.read_set(servo_id, add=A_CurrentLoad, read_len=read_len)
        return rec_data

    def read_lock(self, servo_id, read_len=1):
        return self.read_set(servo_id=servo_id, add=A_Lock,
                             read_len=read_len)

    def read_baud(self, servo_id, read_len=1):
        return self.read_set(servo_id=servo_id, add=A_Baud,
                             read_len=read_len)

    def read_angle_limit(self, servo_id, read_len=4):
        return self.read_set(servo_id=servo_id, add=A_MinAngleLimit,
                             read_len=read_len)

    def read_voltage_limit(self, servo_id, read_len=2):
        return self.read_set(servo_id=servo_id, add=A_MaxInVoltage,
                             read_len=read_len)

    def read_temp_limit(self, servo_id, read_len=1):
        return self.read_set(servo_id=servo_id, add=A_MaxTempLimit,
                             read_len=read_len)

    def read_answer_status(self, servo_id, read_len=1):
        #  0: Response to read and ping instructions
        #  1: Response packet to all the instructions
        return self.read_set(servo_id=servo_id, add=A_Answer_Status,
                             read_len=read_len)

    #  Commands Not on Config Software
    def read_torque_switch(self, servo_id, read_len=1):
        return self.read_set(servo_id, add=A_TorqueSwitch, read_len=read_len)

    def read_delay_time(self, servo_id, read_len=1):
        """
        Read Delay Time of servo, default is zero.
        Delay, when the servo receives a command that needs to be answered.
        Time range: parameter (0~254) *2US, if the parameter 250, that is,
        after 500us response, but the default is 0, which means the
        shortest response time.
        """
        return self.read_set(servo_id=servo_id, add=A_Return_delay,
                             read_len=read_len)

    def read_max_torque(self, servo_id, read_len=2):
        """
        Set the maximum output torque of the servo. 0X03FF corresponds to
        the maximum output torque of the servo
        """
        return self.read_set(servo_id=servo_id, add=A_MaxTorque,
                             read_len=read_len)

    def read_min_pwm(self, servo_id, read_len=2):
        return self.read_set(servo_id=servo_id, add=A_MinPWM,
                             read_len=read_len)

    def read_pid(self, servo_id, read_len=3):
        """
        Read Pid Values
        """
        return self.read_set(servo_id=servo_id, add=A_Proportional,
                             read_len=read_len)

    #  WRITE
    def write_id(self, servo_id, new_id):
        return self.write_set(servo_id, add=A_ID, write_value=new_id)

    def write_pos(self, servo_id, r_position, r_time=1, r_speed=500):
        #  data=> 0-3
        pos_ar = self.mc_data(r_position)
        time_ar = self.mc_data(r_time)
        speed_ar = self.mc_data(r_speed)
        data = list(pos_ar + time_ar + speed_ar)
        data_array = self.write_set(servo_id, add=A_TargetPos_H,
                                    write_value=data)
        return data_array

    def write_lock(self, servo_id, value):
        return self.write_set(servo_id, add=A_Lock, write_value=value)

    def write_temp_limit(self, servo_id, value):
        return self.write_set(servo_id, add=A_MaxTempLimit, write_value=value)

    def write_angle_limit(self, servo_id, min_angle=0, max_angle=1000):
        min_angle_byte = self.mc_data(min_angle)
        max_angle_byte = self.mc_data(max_angle)
        data = list(min_angle_byte + max_angle_byte)
        return self.write_set(servo_id, add=A_MinAngleLimit, write_value=data)

    def write_voltage_limit(self, servo_id, min_voltage=50, max_voltage=250):
        data = [max_voltage, min_voltage]
        return self.write_set(servo_id, add=A_MaxInVoltage, write_value=data)

    def write_baud(self, servo_id, baud_num=0x04):
        #  0x06 is baud address
        #  4 for 115200
        if baud_num <= 7:
            data_array = self.write_set(servo_id, add=A_Baud,
                                        write_value=baud_num)
            return data_array

        else:
            if self.debug:
                print('Invalid Baud Rate selection')
            return False

    def write_torque_switch(self, servo_id, torque_status):
        #  torque_status-> 0: Turn Off | 1: Turn On
        data_array = self.write_set(servo_id, add=A_TorqueSwitch,
                                    write_value=torque_status)
        return data_array

    def write_answer_status(self, servo_id, status=0):
        #  0: Response to read and ping instructions
        #  1: Response packet to all the instructions
        data_array = self.write_set(servo_id, add=A_Answer_Status,
                                    write_value=status)
        return data_array

    def write_delay_time(self, servo_id, status=0):
        """
        Read Delay Time of servo, default is zero.
        Delay, when the servo receives a command that needs to be answered.
        Time range: parameter (0~254) *2US, if the parameter is 250, that is,
        after 500us response, but the default is 0, which means the
        shortest response time.
        """
        data_array = self.write_set(servo_id, add=A_Return_delay,
                                    write_value=status)
        return data_array

    def write_max_torque(self, servo_id, data=1023):
        """
        Set the maximum output torque of the servo. 0X03FF corresponds to
        the maximum output torque of the servo
        """
        data_array = self.write_set(servo_id, add=A_MaxTorque,
                                    write_value=data)
        return data_array

    def write_min_pwm(self, servo_id, data=0):
        data_array = self.write_set(servo_id, add=A_MinPWM,
                                    write_value=data)
        return data_array

    def write_pid(self, servo_id, p=15, d=0, i=0):
        """
        Write PID values, in order P, D, and I
        """
        data = [p, d, i]
        data_array = self.write_set(servo_id, add=A_Proportional,
                                    write_value=data)
        return data_array

    def regulation_mode(self, servo_id, speed=500, direction=0):
        """
        360 degree motor mode
        :return: data Array for motor mode
        """
        direction_flag = direction << 10
        dir_speed = direction_flag + speed
        speed_arr = self.mc_data(dir_speed)
        data_array = self.write_set(servo_id, add=A_RunTime_H,
                                    write_value=list(speed_arr))
        return data_array


if __name__ == '__main__':
    ret = CommandSet().action_set()
    data = [x for x in ret]
    print(data, ret)
