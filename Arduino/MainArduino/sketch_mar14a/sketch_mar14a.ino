/*

*/
#include <SD.h>
#include <TMRpcm.h>
#define SD_Chipselect 11

#include <LedControl.h>
#include <Servo.h>
#include <NewPing.h>


int E1 = 3;
int E2 = 11;
int M1 = 12;  //two motors
int M2 = 13;
int vibration = 4; //vibration motor

int trigPin = A0;   //ultrasonic sensor
int echoPin = A1;   //
int tempSen = A3;   //temperature sensor
int ardConnect_1 = A4;   //pins for serial communication to nano
int ardConnect_2 = A5;

// define pins and other constants
//const int servo1Pin = 9;
const int max_distance = 300;

int DIN = 0;   //dot matrix display 
int CLK = 1;
int CS = 2;
int maxInUse = 1;


// variables to use later on
int dist;

// create instances of servo and ping class
Servo Servo1;
NewPing sonar(trigPin, echoPin, max_distance);


/***
MaxMatrix m(DIN, CLK, CS, maxInUse);


char smile01[] = {8, 8,
                  B00111100,
                  B01000010,
                  B10010101,
                  B10100001,
                  B10100001,
                  B10010101,
                  B01000010,
                  B00111100
                 };
char smile02[] = {8, 8,
                  B00111100,
                  B01000010,
                  B10010101,
                  B10010001,
                  B10010001,
                  B10010101,
                  B01000010,
                  B00111100
                 }; */

LedControl lc=LedControl(DIN,CLK,CS,0);


TMRpcm tmrpcm;
void setup() {
  tmrpcm.speakerPin = 9;
  tmrpcm.volume(1);
  
  pinMode(trigPin, INPUT);
  pinMode(echoPin, INPUT);
  pinMode(vibration,OUTPUT);
  pinMode(M1,OUTPUT);
  pinMode(M1,OUTPUT);
  pinMode(4, OUTPUT); 
	
  
  lc.shutdown(0,false);       //The MAX72XX is in power-saving mode on startup
  lc.setIntensity(0,15);      // Set the brightness to maximum value
  lc.clearDisplay(0);
}

/***Displaying faces on the LED Matrix ***/
void face(int n){
    
    byte smile[8]=   {0x3C,0x42,0xA5,0x81,0xA5,0x99,0x42,0x3C};
    byte neutral[8]= {0x3C,0x42,0xA5,0x81,0xBD,0x81,0x42,0x3C};
    byte frown[8]=   {0x3C,0x42,0xA5,0x81,0x99,0xA5,0x42,0x3C};
    
    
    switch(n){
      case '0':
      printByte(smile);
      delay(1000);
      break;
    
      case '1':
      printByte(neutral);
      delay(1000);
      break;
      
      case '2':
      printByte(frown);
      break;
    }
}


void printByte(byte character [])
{
  int i = 0;
  for(i=0;i<8;i++)
  {
    lc.setRow(0,i,character[i]);
  }
}



/***Robot falling asleep***/
void naptime(){
  digitalWrite(M1, LOW);
  digitalWrite(M2, LOW);
  speakerActivate(4); //"It's nap time!"
  face(2); //animation of closing eyes
  speakerActivate(5); //('Snoring.wav');
  delay(10);
  speakerActivate(6); //displayLCD("Wakeup.wav"); /"Ah that was a good nap! I need coffee"
  return;
}


void shiver(){
  vibration = HIGH;
  //digitalWrite(vibration,HIGH);
  delay(1000);
  vibration = LOW;
  //digitalWrite(vibration,LOW);
 }

void joke() {
  speakerActivate(5);
}
  



void speakerActivate(int code){
  noInterrupts();
  if (SD.begin(SD_Chipselect)){return ;}
   if(code >= 0 && code<=9){
    char* file[ ] = {String(code).concat(".wav")};
    tmrpcm.play(file[0]);
    }
  interrupts();
  return;
}
    


void forward(dir, PWM){
  /*Moving the car forward*/
  digitalWrite(M1,HIGH);   
  digitalWrite(M2, HIGH);       
  analogWrite(E1, PWM);   //PWM Speed Control
  analogWrite(E2, PWM);   //PWM Speed Control
  delay(50);
}

void head(){
  /* Controls the servo, 90 is center, angle from 0~180, rotates really fast.*/
  Servo1.write(90);
  delay(3000);  //wait 3 seconds
  Servo1.write(0);
  delay(500);  //wait 0.5 seconds
  Servo1.write(90);
  delay(500);  //wait 0.5 seconds
  Servo1.write(180);
  delay(500);  //wait 0.5 seconds 
}

void lookAround(){
  /* Moving head around for a small angle, looking for target
   * if anything is within range of 30cm, follw on that direction
   * return a direction, 'LEFT', 'RIGHT', 'FORWARD', 'BACKWARD', 'STOP'
   */
  const char dir = Null
  Servo1.write(90);
  delay(50); 
  dist0 = sonar.ping_cm();   
  Servo1.write(80);
  delay(50);  
  dist1 = sonar.ping_cm();  
  Servo1.write(100);
  delay(20);  
  dist2 = sonar.ping_cm(); 
  
  return dir
}

void follow(){
  /* This function allows the car to follow a traget, 
   *  detects the distance from the traget using ultrasonic sensor,
   *  stops when about 15cm from the sensor,
   */
  follow = 0   //False by default
  while sonar.ping_cm() >= 15:
    forward();
    follow = 1   //True, following target target
  const char dir = lookAround()
  //PWM is decided based on distance it is from the target
  //forward(dir, PWM)
}

void loop()
{
  //Obtain readings from ultrasonic sensot
  Serial.print("Ping: ");
  dist = sonar.ping_cm();  
  Serial.print(dist);
  Serial.println("cm");
  delay(100);
  head();
  forward();
  
  if(Serial.available() > 0){
    
    incomingByte = Serial.read();
		switch((char)incomingByte){
		 case '0':
			speakerActivate(0); //different user
		  break;
		 case '1':
			speakerActivate(0); //different user
		  break;

		 default:
		   break;
      } 
    }
}
