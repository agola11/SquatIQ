
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
  Serial.begin(9600);   // We'll send debugging information via the Serial monitor
}
 
void loop(void) {
  fsrReading0 = analogRead(fsrAnalogPin0);
  fsrReading1 = analogRead(fsrAnalogPin1);
  fsrReading2 = analogRead(fsrAnalogPin2);
  fsrReading3 = analogRead(fsrAnalogPin3);
  fsrReading4 = analogRead(fsrAnalogPin4);

  Serial.print(fsrReading0);
  Serial.print(", ");
  Serial.print(fsrReading1);
  Serial.print(", ");
  Serial.print(fsrReading2);
  Serial.print(", ");
  Serial.print(fsrReading3);
  Serial.print(", ");
  Serial.println(fsrReading4);
  
  delay(5);
}
