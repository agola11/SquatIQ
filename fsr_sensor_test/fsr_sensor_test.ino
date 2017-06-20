
int ffsrAnalogPin = A0; // FSR is connected to analog 0
int sfsrAnalogPin = A7; // FSR is connected to analog 7
int ffsrReading;      // the analog reading from the FSR resistor divider
int sfsrReading;      // the analog reading from the FSR resistor divider
 
void setup(void) {
  Serial.begin(9600);   // We'll send debugging information via the Serial monitor
}
 
void loop(void) {
  ffsrReading = analogRead(ffsrAnalogPin);
  sfsrReading = analogRead(sfsrAnalogPin);
  Serial.print("Analog reading1 = ");
  Serial.print(ffsrReading);
  Serial.print(" Analod reading2 = ");
  Serial.println(sfsrReading);
  delay(150);
}
