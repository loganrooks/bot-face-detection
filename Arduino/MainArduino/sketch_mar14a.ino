/**/#include <LiquidCrystal.h>#define playcomplete(x) ROM_playcomplete(PSTR(x)) pinmode(7, )const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;LiquidCrystal lcd(rs, en, d4, d5, d6, d7);int motorright = 7; //changeint motorleft = 8;int camerapin = A0;void naptime(){  analogWrite(motorpin, 0);  //playcomplete('Naptime.wav'); //"It's Nap Time"  lcd.print(""); //animation of closing eyes  //playcomplete('Snoring.wav');  delay(10);  //displayLCD("Wakeup.wav"); /"Ah that was a good nap! I need coffee"  return;}void speakerActivate(int num){  noInterrupts();  switch(num)  { case 0:      playcomplete('hello.wav');      //hello sequence      break;    case 1:      //temperature sequence      playcomplete('Temperature.wav'); //"Brr, it's cold"      break;        case 2:       playcomplete('Shiny.wav');      //shiny sequence      break;    case 3:      //emotion sequence      break;    case 4:      naptime();      break;    case 5:      jokes();      break;  }  return;}        void setup() {    }void loop() {    }