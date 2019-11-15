// Example by Tom Igoe
import processing.serial.*;
Serial myPort;  // The serial port
String val; // test
float valAsFloat;
ArrayList<Float> vals = new ArrayList<Float>();
int numVals = 100;
float border = 0.05;
float tempMin = 20.0;
float tempMax = 100.0;

PImage therm, trump1, trump2, trump3;
int imSz = 200;
float rectH = 0;
float angle = 0;

// OSC
import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;

void setup() {
  size(1000, 1000);
  noStroke();
  
  // load image
  therm = loadImage("thermometre.png");
  trump1 = loadImage("trump_01.png");
  trump1.resize(imSz, 0);
  trump2 = loadImage("trump_02.png");
  trump2.resize(imSz, 0);
  trump3 = loadImage("trump_03.png");
  trump3.resize(imSz, 0);
  
  // List all the available serial ports
  printArray(Serial.list());
  // Open the port you are using at the rate you want:
  myPort = new Serial(this, "COM5", 9600);  
  
  // OSC
  oscP5 = new OscP5(this,12000);
  myRemoteLocation = new NetAddress("127.0.0.1",12000);
}

void draw() {
  background(255);
  
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
  
  println(valAsFloat);
  
  rectH = map(valAsFloat, 20, 50, height - 416, height - 214);
  
  fill(255, 0, 0);
  rect(0, height - rectH, width, rectH);
  image(therm, 0, 0);
  
  PImage imToShow = new PImage();
  
  if(valAsFloat >= 00 && valAsFloat < 30) {
   imToShow = trump1; 
  }
  if(valAsFloat >= 30 && valAsFloat < 35) {
   imToShow = trump2; 
  }
  if(valAsFloat >= 35) {
   imToShow = trump3; 
  }
  
  pushMatrix();
  translate(width * 0.2, height * 0.5);
  rotate(angle);
  image(imToShow, -imToShow.width / 2, -imToShow.height / 2);
  popMatrix();
  
  pushMatrix();  
  translate(width * 0.8, height * 0.5);
  rotate(angle);
  image(imToShow, -imToShow.width / 2, -imToShow.height / 2);
  popMatrix();
  
  angle += 0.01;
}
