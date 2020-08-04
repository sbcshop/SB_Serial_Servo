/*
* Read back all servo feedback parameters: Position, speed, load, voltage, temperature, moving state, current；
* FeedBack The function reads back the servo parameters in the buffer，
* Readxxx(-1): The function returns the corresponding servo state in the buffer；
* Readxxx(ID)，ID=-1,
* Return: FeedBack Buffer Parameters；
* ID>=0，directly return to the state of the specified ID servo through the read command, No need to call the FeedBack function.
*/

#include <SBServo.h>

SBServo sb;

int LEDpin = 13;

void setup()
{
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin, HIGH);
  Serial1.begin(1000000);
  Serial.begin(115200);
  sb.pSerial = &Serial1;
  delay(1000);
}

void loop()
{
  int Pos;
  int Speed;
  int Load;
  int Voltage;
  int Temper;
  int Move;
  int Current;
  if(sb.FeedBack(1)!=-1){
    digitalWrite(LEDpin, LOW);
    Pos = sb.ReadPos(-1);
    Speed = sb.ReadSpeed(-1);
    Load = sb.ReadLoad(-1);
    Voltage = sb.ReadVoltage(-1);
    Temper = sb.ReadTemperature(-1);
    Move = sb.ReadMove(-1);
    Current = sb.ReadCurrent(-1);
    Serial.print("Position:");
    Serial.println(Pos);
    Serial.print("Speed:");
    Serial.println(Speed);
    Serial.print("Load:");
    Serial.println(Load);
    Serial.print("Voltage:");
    Serial.println(Voltage);
    Serial.print("Temper:");
    Serial.println(Temper);
    Serial.print("Move:");
    Serial.println(Move);
    Serial.print("Current:");
    Serial.println(Current);
    delay(10);
  }else{
    digitalWrite(LEDpin, HIGH);
    Serial.println("FeedBack err");
    delay(500);
  }
  
  Pos = sb.ReadPos(1);
  if(Pos!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo position:");
    Serial.println(Pos, DEC);
    delay(10);
  }else{
    Serial.println("read position err");
    digitalWrite(LEDpin, HIGH);
    delay(500);
  }
  
  Voltage = sb.ReadVoltage(1);
  if(Voltage!=-1){
    digitalWrite(LEDpin, LOW);
	Serial.print("Servo Voltage:");
    Serial.println(Voltage, DEC);
    delay(10);
  }else{
    Serial.println("read Voltage err");
    digitalWrite(LEDpin, HIGH);
    delay(500);
  }
  
  Temper = sb.ReadTemperature(1);
  if(Temper!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo temperature:");
    Serial.println(Temper, DEC);
    delay(10);
  }else{
    Serial.println("read temperature err");
    digitalWrite(LEDpin, HIGH);
    delay(500);    
  }

  Speed = sb.ReadSpeed(1);
  if(Speed!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo Speed:");
    Serial.println(Speed, DEC);
    delay(10);
  }else{
    Serial.println("read Speed err");
    digitalWrite(LEDpin, HIGH);
    delay(500);    
  }
  
  Load = sb.ReadLoad(1);
  if(Load!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo Load:");
    Serial.println(Load, DEC);
    delay(10);
  }else{
    Serial.println("read Load err");
    digitalWrite(LEDpin, HIGH);
    delay(500);    
  }
  
  Current = sb.ReadCurrent(1);
  if(Current!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo Current:");
    Serial.println(Current, DEC);
    delay(10);
  }else{
    Serial.println("read Current err");
    digitalWrite(LEDpin, HIGH);
    delay(500);    
  }

  Move = sb.ReadMove(1);
  if(Move!=-1){
    digitalWrite(LEDpin, LOW);
    Serial.print("Servo Move:");
    Serial.println(Move, DEC);
    delay(10);
  }else{
    Serial.println("read Move err");
    digitalWrite(LEDpin, HIGH);
    delay(500);    
  }
  Serial.println();
}
