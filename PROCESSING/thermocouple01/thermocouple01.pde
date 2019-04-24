// Example by Tom Igoe
import processing.serial.*;
Serial myPort;  // The serial port
String val;
float valAsFloat;

import processing.sound.*;
SinOsc sine;

void setup() {
  // List all the available serial ports
  printArray(Serial.list());
  // Open the port you are using at the rate you want:
  myPort = new Serial(this, "COM5", 9600);
  
  sine = new SinOsc(this);
  sine.play();
}

void draw() {
  while (myPort.available() > 0) {
    val = myPort.readStringUntil('\n');    
    
    if(val != null) {
      valAsFloat = float(val);
      // Map mouseX from 20Hz to 1000Hz for frequency
      float frequency = map(valAsFloat, 25, 37, 80.0, 1000.0);
      println(frequency);
      sine.freq(frequency);
    }
  }
}
