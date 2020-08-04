/*

* The synchronous writing example. 
*/

#include <SBServo.h>

SBServo sb;

byte ID[2];
u16 Position[2];
u16 Speed[2];

void setup()
{
  Serial.begin(1000000);
  sb.pSerial = &Serial;
  delay(1000);
  ID[0] = 1;
  ID[1] = 2;
}

void loop()
{
  Position[0] = 1000;
  Position[1] = 1000;
  Speed[0] = 1500;
  Speed[1] = 1500;
  sb.SyncWritePos(ID, 2, Position, 0, Speed); // ID Array=[1, 2], Array Length=2, Position Array=[1000, 1000],
                                              // Time=0, Speed Array=[1500, 1500]; 1500 Steps/Seconds,
  delay(754);

  Position[0] = 20;
  Position[1] = 20;
  sb.SyncWritePos(ID, 2, Position, 0, Speed); // ID Array=[1, 2], Array Length=2, Position Array=[20, 20],
                                              // Time=0, Speed Array=[1500, 1500]; 1500 Steps/Seconds,
  delay(754);
}
