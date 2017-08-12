#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

int fsrAnalogPin0 = A0; // FSR is connected to analog 0
int fsrAnalogPin1 = A1;
int fsrAnalogPin2 = A2; 
int fsrAnalogPin3 = A3; 
int fsrAnalogPin4 = A4;  

int fsrReading0;
int fsrReading1;
int fsrReading2;
int fsrReading3;
int fsrReading4;

 
void setup(void) {
  Serial.begin(9600);   // send debugging information via the Serial monitor
  mma.begin();
  mma.setRange(MMA8451_RANGE_2_G);
}
 
void loop(void) {
  fsrReading0 = analogRead(fsrAnalogPin0);
  fsrReading1 = analogRead(fsrAnalogPin1);
  fsrReading2 = analogRead(fsrAnalogPin2);
  fsrReading3 = analogRead(fsrAnalogPin3);
  fsrReading4 = analogRead(fsrAnalogPin4);
  mma.read();

  Serial.print(fsrReading0);
  Serial.print(", ");
  Serial.print(fsrReading1);
  Serial.print(", ");
  Serial.print(fsrReading2);
  Serial.print(", ");
  Serial.print(fsrReading3);
  Serial.print(", ");
  Serial.print(fsrReading4);
  Serial.print(", ");
  Serial.println(mma.y);
  
  delay(5);
}
