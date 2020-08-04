/*
* Position Write Example writing examples.
*/

#include <SBServo.h>

SBServo sb;

void setup()
{
  Serial.begin(115200);
  sb.pSerial = &Serial;
  delay(1000);
}

void loop()
{
  sb.WritePos(1, 1000, 0, 1500);	// SERVO ID=1, Position=1000, Time=0, Speed=1500; 1500 Steps/Seconds,
  delay(754);
  
  sb.WritePos(1, 20, 0, 1500);	// SERVO ID=1, Position=20, Time=0, Speed=1500; 1500 Steps/Seconds,
  delay(754);
}
