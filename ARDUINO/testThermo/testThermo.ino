#include "Adafruit_MAX31855.h"

int thermoDO = 39;
int thermoCS = 41;
int thermoCLK = 43;

Adafruit_MAX31855 thermocouple(thermoCLK, thermoCS, thermoDO);
  
void setup() {
  Serial.begin(9600);
  
  //Serial.println("MAX31855 test");
  // Attendre que le circuit MAX se stabilise.
  delay(500);
}

void loop() {
    // Test de lecture basique, afficher simplement la température courante
   //Serial.print("Internal Temp = ");
   //Serial.println(thermocouple.readInternal());

   // Lecture en degrés Celcius
   double c = thermocouple.readCelsius();
   if (isnan(c)) {
     //Serial.println("Quelque chose ne fonctionne pas avec le thermocouple!");
   } else {
     //Serial.print("C = ");
     Serial.println(c);
   }
   
   // Décommenter les lignes suivante pour afficher la température
   // en degrés Farenheit (unité qui à cours au USA)
   //Serial.print("F = ");
   //Serial.println(thermocouple.readFarenheit());
 
   // Attendre une seconde
   //delay(100);
}
