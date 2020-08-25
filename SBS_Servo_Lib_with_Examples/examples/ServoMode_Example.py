from serial_comm import SerialComm
from command import Commands
from servo_instruction import SBSServo
from time import sleep


if __name__ == "__main__":
        servo=SBSServo()
        servo.connect(port="/dev/ttyS0", baudrate=115200)
        ServoID=servo.readID()
        print(ServoID) 
        while 1:
            servo.writeAngleLimit(ID=1, angleMin=0, angleMax=1000) #set min max angle

            servo.servoWrite(ID=1, position=0, r_time=0, r_speed=900) #Set to 0 position
            sleep(3)
            servo.servoWrite(ID=1, position=999, r_time=0, r_speed=900) #Set to 999 position
            sleep(3)
