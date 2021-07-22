#include <Arduino.h>
#include <Wire.h>
#include "Adafruit_SHT31.h"

// To get module temperature
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

// To get air temperature and humidity
bool enableHeater = false;
uint8_t loopCnt = 0;

Adafruit_SHT31 sht31 = Adafruit_SHT31();

// setup
void setup() {
  Wire.begin();
  Serial.begin(9600);
  
  while (!Serial)
    delay(10);     // will pause Zero, Leonardo, etc until serial console opens

  if (! sht31.begin(0x44)) {   // Set to 0x45 for alternate i2c addr
    while (1) delay(1);
  }
    
}

void loop() {
  float t = sht31.readTemperature();
  float h = sht31.readHumidity();

  float moduleTemp = gettemp();

  Serial.print(moduleTemp);
  Serial.print("\t");
  Serial.print(t);
  Serial.print("\t");
  Serial.print(h);
  Serial.print("\n");
  if(moduleTemp>30){
    analogWrite(A4, 1023);
  }
  else{
    analogWrite(A4,0);
  }
  delay(1000);
}
