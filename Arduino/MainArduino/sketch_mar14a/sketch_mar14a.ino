/*

*/
#include <SD.h>
#include <TMRpcm.h>
#define SD_Chipselect 11
#include <LiquidCrystal.h>


int E1 = 3;
int E2 = 11;
int M1 = 12;
int M2 = 13;
int vibration = 4;

int trigPin = A0;
int echoPin = A1;
int ardConnect_1 = A4;   //pins for serial communication
int ardConnect_2 = A5;

int led1 = 0;
int led2 = 1;
int led3 = 2;


TMRpcm tmrpcm;
void setup() {
  tmrpcm.speakerPin = 9;
  tmrpcm.volume(1);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, OUTPUT);
  pinMode(vibration,OUTPUT);
  pinMode(M1,OUTPUT);
  pinMode(M1,OUTPUT);
	
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
  
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
