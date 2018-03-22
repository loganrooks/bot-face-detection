char dataString[50] = {0};
int a =0; 

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
  a++;                          // a value increase every loop
  sprintf(dataString,"%02X",a); // convert a value to hexa 
  Serial.println(dataString);   // send the data
  delay(1000);                  // give the loop some break
}

void loop(){

	if(Serial.available() > 0){
		incomingByte = Serial.read();
		switch((char)incomingByte){
		 case '0':
			my_blink(10);
		  break;
		 case '1':
			my_blink(12);
		  break;

		 default:
		   break;
	} 
	}
 }
