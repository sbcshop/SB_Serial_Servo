/*
* SB Servo EEPROM parameters
*/

#include <SBServo.h>

int LEDpin = 13;

SBServo sb;

void setup()
{
  pinMode(LEDpin, OUTPUT);
  Serial.begin(1000000);
  sb.pSerial = &Serial;

  delay(1000);
  digitalWrite(LEDpin, LOW);
  sb.unLockEprom(1);  //  Unlock EEPROM
  sb.writeByte(1, SBSERVO_ID, 2); // Servo ID
  sb.writeWord(2, SBSERVO_MIN_ANGLE_LIMIT_L, 20);
  sb.writeWord(2, SBSERVO_ANGLE_LIMIT_L, 1000);
  sb.LockEprom(2);  // Lock EEPROM
  digitalWrite(LEDpin, HIGH);
}

void loop()
{

}
