/*************************
Felix Cote
  Simple motor control speed
***************************/

int dirpin = 23;
int steppin = 25;

int dirpin2 = 33;
int steppin2 = 31;

int ledpin = 2;

unsigned long currentMicros = 0;  
unsigned long previousMotorMicros = 0;
int motorSpeed = 6000;

void setup() 
{
pinMode(dirpin, OUTPUT);
pinMode(steppin, OUTPUT);

pinMode(dirpin2, OUTPUT);
pinMode(steppin2, OUTPUT);

pinMode(ledpin, OUTPUT);

Serial.begin(9600);
Serial.println("Serial port ready");
}


void loop()
{ 
  digitalWrite(ledpin, HIGH);
  
  currentMicros = micros();
  if(currentMicros - previousMotorMicros >= motorSpeed) {
    
    doStep(steppin2, dirpin2);
    doStep(steppin, dirpin);

    previousMotorMicros += motorSpeed;
  }
}

void doStep(int STEP_PIN, int DIR_PIN) {
    digitalWrite(DIR_PIN, LOW);
    digitalWrite(STEP_PIN, LOW);
    digitalWrite(STEP_PIN, HIGH);
}
