#!/usr/bin/python

import serial , string, time

output = " " 
ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
counter = 0 
temp, humid = 0, 0

#while True:
while counter < 10:
    print "----"
    #while output != "":
    output = ser.readline()
    #parse the data
    # output will terminate after a newline char from arduino
    # newline char in arduino is given by "\r" 
    val = float(output.split("= ")[1].split("\r")[0])
    if output[0] == "T" : #its a temp
        temp = val
    elif output[0] == "H": # its humidity
        humid = val
        
    print "Temp", temp, "Humidity", humid

    output = " "
    counter +=1
