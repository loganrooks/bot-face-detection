#!/usr/bin/python

import serial , string, time

output = " " 
#need to account for fact that the comport can change
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM1', 9600, 8, 'N', 1, timeout=1)

counter = 0 


#while True:
while counter < 10:
        #while output != "":
    val = 1
    val = bytes([val])
    num = ser.write(val)
    print("Bytes sent:",num)
    #parse the data
    # output will terminate after a newline char from arduino
    # newline char in arduino is given by "\r" 
    time.sleep(3)
    val = 0
    val =bytes([val])
    ser.write(val)
    counter +=1
#ser.write('3')