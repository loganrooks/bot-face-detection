char dataString[50] = {0};
int a =0; 

void setup() {
Serial.begin(9600);              //Starting serial communication
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
		  break;
		 case 1:
			Serial.println("yep");
		  break;

		 default:
		   break;
	} 
	}
 }
