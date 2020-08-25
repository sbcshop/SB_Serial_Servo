from serial_comm import SerialComm
from command import Commands
from servo_instruction import SBSServo
from time import sleep


if __name__ == "__main__":
        servo=SBSServo()
        servo.connect(port="/dev/ttyS0", baudrate=115200) #Serial port used
        ServoID=servo.readID() #Read ID of connected servo motor
        print(ServoID) 
        while 1:        
            servo.writeAngleLimit(ID=1, angleMin=0, angleMax=0)
            
            servo.motor_mode(1, speed=500, direction=0) #clockwise direction
            sleep(5)
            servo.motor_mode(1, speed=0, direction=0)   #Stop
            sleep(2)
            servo.motor_mode(1, speed=500, direction=1) #Anti-Clockwise direction
            sleep(5)

