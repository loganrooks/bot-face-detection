char dataString[50] = {0};
int a =0; 
int b = 12;
void setup() {
Serial.begin(9600);              //Starting serial communication
pinMode(b,OUTPUT);
}
 /*
void loop() {
  a++;                          // a value increase every loop
  sprintf(dataString,"%02X",a); // convert a value to hexa 
  Serial.println(dataString);   // send the data
  delay(1000);                  // give the loop some break
}
*/
void loop(){

	if(Serial.available() > 0){
		char incomingByte = Serial.read();
		switch((char)incomingByte){
		 case 0:
			Serial.println("uh-uh");
      digitalWrite(b, LOW);
		  break;
		 case 1:
			Serial.println("yep");
      digitalWrite(b, HIGH);
		  break;

		 default:
		   break;
	} 
	}
 }
