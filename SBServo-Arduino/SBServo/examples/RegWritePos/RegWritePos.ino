/*
* The asynchronous write example.
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
  sb.RegWritePos(1, 1000, 0, 1500); // SERVO ID=1, Position=1000, Time=0, Speed=1500; 1500 Steps/Seconds,
  sb.RegWritePos(2, 1000, 0, 1500); // SERVO ID=2, Position=1000, Time=0, Speed=1500; 1500 Steps/Seconds
  sb.RegWriteAction();
  delay(754);
  
  sb.RegWritePos(1, 20, 0, 1500); // SERVO ID=1, Position=20, Time=0, Speed=1500; 1500 Steps/Seconds,
  sb.RegWritePos(2, 20, 0, 1500); // //SERVO ID=1, Position=20, Time=0, Speed=1500; 1500 Steps/Seconds,
  sb.RegWriteAction();
  delay(754);
}
