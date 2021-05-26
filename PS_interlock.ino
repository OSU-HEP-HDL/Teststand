#include <Wire.h>

float Vin = 5.;
float T[0];
float V1;
float R0=1180;
float R01=10000;
float R1, logR1;
float c1=298.15, b1=3070., b2=3380.;

float gettemp(){
  V1 = (5./1023)*analogRead(A0);
  R1 = V1*R0 / (Vin - V1);
  logR1 = log(R1/R01);
  T[0]=(1.0/(1/c1 + ((1/3380.)*logR1))) - 273.15;
  return T[0];
}

void setup() {
  Wire.begin();
  Serial.begin(9600);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  float moduleTemp;
  moduleTemp = gettemp();
  Serial.print(moduleTemp);
  Serial.print("\n");
  delay(1000);
  if(moduleTemp > 30){
    analogWrite(A4, 1023);
  }
  else{
    analogWrite(A4,0);
  }
  
}
