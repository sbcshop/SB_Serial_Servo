#!/usr/bin/python3

"""
This file contains Servo Instructions SB-S Servo
This file uses the command and serial files to Communicate with SBS Servo
Developed by - SB Components
http://sb-components.co.uk
"""

from serial_comm import SerialComm
from command import Commands


class SBSServo(SerialComm, Commands):
    """
    This is a class for handle servo command frames
    """

    def __init__(self):
        SerialComm.__init__(self)
        Commands.__init__(self, self.debug)

    def connect(self, port, baudrate=115200):
        """
        Open the port and connect
        """
        self.log.info('Connecting to SB-S Servo on Port %s & baudrate %d..',
                      port,
                      baudrate)
        status = self.connect_port(port, baudrate)
        if status:
            self.log.info('Initialized')
        else:
            self.log.info('Initialization Failed..!!')

    def byte_to_int(self, byte, order='big', sign=False):
        return int.from_bytes(byte, byteorder=order, signed=sign)

    def tempRead(self, ID):
        """
        Read Servo Temperature
        """
        data_array = self.read_temp(ID)
        data = self.write(data_array)
        if data:
            return self.byte_to_int(data[-2])
        else:
            return data

    def voltageRead(self, ID):
        """
        Read Servo Voltage
        """
        data_array = self.read_voltage(ID)
        data = self.write(data_array)
        if data:
            return (self.byte_to_int(data[-2])) / 10
        else:
            return data

    def positionRead(self, ID):
        """
        Read Servo Position
        """
        data_array = self.read_pos(ID)
        data = self.write(data_array)
        if data:
            pos = self.byte_to_int(data[5] + data[6])
            return pos

    def torqueRead(self, ID):
        """
        Read Servo Torque
        """
        data_array = self.read_load(ID)
        data = self.write(data_array)
        if data:
            torque = self.byte_to_int(data[5] + data[6], sign=True)
            if torque & (1 << 10):
                torque = -(torque & ~(1 << 10))
            return torque

    def speedRead(self, ID):
        """
        Read Servo Speed
        """
        data_array = self.read_speed(ID)
        data = self.write(data_array)
        if data:
            speed = self.byte_to_int(data[5] + data[6])
            if speed & (1 << 15):
                speed = -(speed & ~(1 << 15))
            return speed

    def adjustAngleOffset(self, ID=1, offset=0):
        """
        Adjust angle offset to zero
        """
        pass

    def readAngleOffset(self, ID):
        """
        Read Servo Angle Offset
        """
        return None

    def readAngleLimit(self, ID):
        """
        Read Servo Angle Limit
        """
        data_array = self.read_angle_limit(ID)
        response = self.write(data_array)
        if response:
            min_angle = int.from_bytes(response[5] + response[6],
                                       byteorder='big')
            max_angle = int.from_bytes(response[7] + response[8],
                                       byteorder='big')
            return min_angle, max_angle

    def writeAngleLimit(self, ID, angleMin=0, angleMax=1000):
        """
        Write Servo Angle Limit
        """
        data_array = self.write_angle_limit(ID, angleMin, angleMax)
        self.write(data_array, waitForResponse=True)

    def readVolLimit(self, ID):
        """
        Read Servo Voltage Limit
        """
        data_array = self.read_voltage_limit(ID)
        response = self.write(data_array)
        if response:
            max_voltage = int.from_bytes(response[5], byteorder='big') / 10
            min_voltage = int.from_bytes(response[6], byteorder='big') / 10
            return min_voltage, max_voltage

    def writeVolLimit(self, ID, voltMin=5.0, voltMax=12.0):
        """
        Read Servo Voltage Limit
        """
        data_array = self.write_voltage_limit(ID, int(voltMin * 10),
                                              int(voltMax * 10))
        self.write(data_array, waitForResponse=True)

    def readTempLimit(self, ID):
        """
        Read Servo Temperature Limit
        """
        data_array = self.read_temp_limit(ID)
        response = self.write(data_array)
        if response:
            max_temp = int.from_bytes(response[5], byteorder='big')
            return max_temp

    def writeTempLimit(self, ID, temp=85):
        """
        Write Servo Temperature Limit
        """
        data_array = self.write_temp_limit(ID, temp)
        self.write(data_array, waitForResponse=True)

    def torqueServo(self, ID, status):
        """
        Enable/Disable Servo Torque
        """
        data_array = self.write_torque_switch(ID, status)
        self.write(data_array, waitForResponse=False)

    def write_lock_status(self, ID, lock_status):
        """
        Change the lock of servo for writing into EEPROM
        :param ID: ID of servo
        :param lock_status: Status of lock. 0-> locked; 1-> unlocked
        :return: None
        """
        data_array = self.write_lock(ID, lock_status)
        self.write(data_array, waitForResponse=False)

    def writeID(self, ID, new_id):
        """
        CHANGES NEEDED
        Write Servo ID
        """
        #  Write New ID into servo
        if ID != new_id:
            data_array = self.write_id(ID, new_id)
            self.write(data_array)

    def readID(self, total_servos=253):
        """
        Scan connected Servo
        :total_servos: Number of servos to scan, int
        :return: Connected servo IDs
        """
        total_servos = 7
        id_array = []
        for i in range(1, total_servos):
            data_array = self.read_id(servo_id=i)
            response = self.write(data_array, waitForResponse=True,
                                  timeout=.75)
            if response:
                rec_id = int.from_bytes(response[5], byteorder='big')
                if rec_id:
                    id_array.append(rec_id)
        return id_array

    def write_baudrate(self, ID, new_baud=4):
        """
        Change/Write BAUD Rate of the servo motor
        """
        #  Write New ID into servo
        data_array = self.write_baud(ID, new_baud)
        self.write(data_array)

    def servoWrite(self, ID=1, position=0, r_time=0, r_speed=0):
        """
        Rotate: Change/Write servo time and position values
        """
        data_array = self.write_pos(ID, position, r_time=r_time,
                                    r_speed=r_speed)
        self.write(data_array, waitForResponse=False)

    def read_answer(self, ID):
        #  0: Response to read and ping instructions
        #  1: Response packet to all the instructions
        data_array = self.read_answer_status(servo_id=ID)
        response = self.write(data_array)
        if response:
            status = int.from_bytes(response[5], byteorder='big')
            return status

    def write_answer(self, ID=1, status=0):
        """
        0: Response to read and ping instructions
        1: Response packet to all the instructions
        """
        data_array = self.write_answer_status(ID, status)
        self.write(data_array, waitForResponse=False)

    #  Not On Configuration Software
    def read_delay(self, ID):
        """
        Read Delay Time of servo, default is zero.
        Delay, when the servo receives a command that needs to be answered.
        Time range: parameter (0~254) *2US, if the parameter 250, that is,
        after 500us response, but the default is 0, which means the
        shortest response time.
        """
        data_array = self.read_delay_time(servo_id=ID)
        response = self.write(data_array)
        if response:
            status = int.from_bytes(response[5], byteorder='big')
            return status

    def write_delay(self, ID=1, delay=0):
        """
        Read Delay Time of servo, default is zero.
        Delay, when the servo receives a command that needs to be answered.
        Time range: parameter (0~254) *2US, if the parameter 250, that is,
        after 500us response, but the default is 0, which means the
        shortest response time.
        """
        data_array = self.write_delay_time(ID, delay)
        self.write(data_array, waitForResponse=False)

    def read_torque_limit(self, ID):
        """
        Set the maximum output torque of the servo. 0X03FF corresponds to
        the maximum output torque of the servo
        """
        data_array = self.read_max_torque(servo_id=ID)
        response = self.write(data_array)
        if response:
            limit = int.from_bytes(response[5] + response[6],
                                   byteorder='big')
            return limit

    def write_torque_limit(self, ID=1, delay=0):
        """
        Set the maximum output torque of the servo. 0X03FF corresponds to
        the maximum output torque of the servo
        """
        data_array = self.write_max_torque(ID, delay)
        self.write(data_array, waitForResponse=False)

    def read_pwm(self, ID):
        data_array = self.read_min_pwm(servo_id=ID)
        response = self.write(data_array)
        if response:
            limit = int.from_bytes(response[5] + response[6], byteorder='big')
            return limit

    def write_pwm(self, ID=1, data=0):
        data_array = self.write_min_pwm(ID, data)
        self.write(data_array, waitForResponse=False)

    def read_pid_value(self, ID):
        data_array = self.read_pid(servo_id=ID)
        response = self.write(data_array)
        if response:
            p = int.from_bytes(response[5], byteorder='big')
            d = int.from_bytes(response[6], byteorder='big')
            i = int.from_bytes(response[7], byteorder='big')
            return p, d, i

    def write_pid_value(self, ID=1, p=15, d=0, i=0):
        data_array = self.write_pid(ID, p=p, d=d, i=i)
        self.write(data_array, waitForResponse=False)

    def motor_mode(self, ID, speed=500, direction=0):
        """
        :param ID: ID of motor
        :param speed: speed of motor
        :param direction: 0 for anticlockwise, 1 for clockwise
        """
        data_array = self.regulation_mode(servo_id=ID, speed=speed,
                                          direction=direction)
        self.write(data_array, waitForResponse=False)


if __name__ == "__main__":
    sbss = SBSServo()
    sbss.connect(port="COM10", baudrate=115200)
    # ids = sbss.readID(1)
    sbss.motor_mode(2, 00, direction=0)
    # print(ids)
