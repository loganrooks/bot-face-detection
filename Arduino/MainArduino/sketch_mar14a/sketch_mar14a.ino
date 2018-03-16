/*

*/
#include <SD.h>
#include <TMRpcm.h>
#define SD_Chipselect 11
#include <LiquidCrystal.h>
#define playcomplete(x) ROM_playcomplete(PSTR(x)) 


pinmode(7, )

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int motorright = 7; //change
int motorleft = 8;
int camerapin = A0;
void setup() {
    tmrpcm.speakerPin = 9;
  tmrpcm.volume(1);
  pinMode(vibration,OUTPUT);

}
void naptime(){
  analogWrite(motorpin, 0);
  //playcomplete('Naptime.wav'); //"It's Nap Time"
  lcd.print(""); //animation of closing eyes
  //playcomplete('Snoring.wav');
  delay(10);
  //displayLCD("Wakeup.wav"); /"Ah that was a good nap! I need coffee"
  return;
}

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
