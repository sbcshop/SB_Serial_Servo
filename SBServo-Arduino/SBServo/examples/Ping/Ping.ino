/*
* Ping Command test, test whether the corresponding ID servo on the bus is ready,
* the broadcast command is only applicable when there is only one servo on the bus
*/

#include <SBServo.h>

SBServo sb;

int LEDpin = 13;
void setup()
{
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin, HIGH);
  Serial.begin(115200);
  Serial1.begin(1000000);
  sb.pSerial = &Serial1;
  delay(1000);
}

void loop()
{
  int ID = sb.Ping(1);
  if(ID!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo ID:");
    Serial.println(ID, DEC);
    delay(100);
  }else{
    Serial.println("Ping servo ID error!");
    digitalWrite(LEDpin, HIGH);
    delay(2000);
  }
}
