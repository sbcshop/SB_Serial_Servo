/*
* The broadcast writing example.
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
  sb.WritePos(0xfe, 1000, 0, 1500);	// Servo ID=254(Broadcast ID), Speed=1500Step/Seconds, Position=1000
  delay(754);
  
  sb.WritePos(0xfe, 20, 0, 1500);	// Servo ID=254(Broadcast ID),	Speed=1500Step/Seconds, Position=20
  delay(754);
}
