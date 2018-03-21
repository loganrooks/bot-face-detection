/*

*/
#include <SD.h>
#include <TMRpcm.h>
#define SD_Chipselect 11
#include <LiquidCrystal.h>


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

int DIN = 0;   //dot matrix display 
int CLK = 1;
int CS = 2;
int maxInUse = 1;

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
                 };


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
	
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
  
}


void face(){
   m.setDot(6,2,true);
   delay(1000);
   m.setDot(6,3,true);
   delay(1000);
   m.clear();
   for (int i =0; i<8; i++){
	m.setDot(i,i, true);
	delay(300);
}

m.clear();


m.writeSprite(0,0,smile01);
delay(1000);

for (int i =0; i<8; i++){
  m.shiftLeft(false, false);
  delay(300);
}
m.clear();
}

void naptime(){
  analogWrite(motorpin, 0);
  speakerActivater(4); //"It's nap time!"
  lcd.print(""); //animation of closing eyes
  speakerActivate(5) //('Snoring.wav');
  delay(10);
  speakerActivate(6); //displayLCD("Wakeup.wav"); /"Ah that was a good nap! I need coffee"
  return;
})

void speakerActivate(int code){
  noInterrupts();
  if (SD.begin(SD_Chipselect)){return ;}
   if(code >= 0 && code<=9){
    char* file[ ] = {String(code).concat(".wav")};
    tmrpcm.play(file[0]);
    }
  return;
}
    
void shiver(){
  vibration = HIGH;
  delay(1000);
  vibration = LOW;
 }
void joke() {
Speak(5);
}
  


void loop() {
    
}
