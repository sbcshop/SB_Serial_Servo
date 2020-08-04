/*
* Motor Mode Example
*/

#include <SBServo.h>

SBServo sb;

void setup()
{
  Serial.begin(115200);
  sb.pSerial = &Serial;
  delay(1000);
  sb.PWMMode(1);
}

void loop()
{
  sb.WritePWM(1, 500);
  delay(2000);
  sb.WritePWM(1, 0);
  delay(2000);
  sb.WritePWM(1, -500);
  delay(2000);
  sb.WritePWM(1,0);
  delay(2000);
}
