// Example by Tom Igoe
import processing.serial.*;
Serial myPort;  // The serial port
String val;
float valAsFloat;
ArrayList<Float> vals = new ArrayList<Float>();
int numVals = 100;
float border = 0.1;
float tempMin = 30.0;
float tempMax = 100.0;

// OSC
import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;

void setup() {
  size(1000, 800);
  
  // List all the available serial ports
  printArray(Serial.list());
  // Open the port you are using at the rate you want:
  myPort = new Serial(this, "COM5", 9600);
  
  
  // OSC
  oscP5 = new OscP5(this,12000);
  myRemoteLocation = new NetAddress("127.0.0.1",12000);
}

void draw() {
  background(50);
  
  while (myPort.available() > 0) {
    val = myPort.readStringUntil('\n');
    
    if(val != null) {
      valAsFloat = float(val);
      print(val);
      vals.add(valAsFloat);
      if(vals.size() > numVals) {
       vals.remove(0); 
      }
      
      OscMessage myMessage = new OscMessage("/temp");
      myMessage.add(map(valAsFloat, tempMin, tempMax, 100, 300));
      oscP5.send(myMessage, myRemoteLocation);      
    }
  }
  
  for(float temp = tempMin; temp <= tempMax; temp += 5) {
    float y = map(temp, tempMin, tempMax, (1-border)*height, border*height);
    stroke(220);
    strokeWeight(1);
    line(border*width, y, (1-border)*width, y);
    text(temp, 5, y);
  }
  
  
  noFill();
  stroke(240);
  strokeWeight(3);
  beginShape();
  for(int i = 0; i < vals.size(); i++) {
   float x = map(i, 0, vals.size(), border*width, (1-border)*width);
   float y = map(vals.get(i), tempMin, tempMax, (1-border)*height, border*height);
   vertex(x, y);
  }
  endShape();
}
