'''
Python Code for communicating over serial- can be configured for any device, however specific use case here was the RFD900

Usage:
Ensure port is the same on both computers/Jetson Nano/Raspberry Pi. If a linux system, port will be at /dev/ttyUSBx or something similar.
For windows, it will be a COMx port. You can check this in the device manager.

The Baud rate can be reprogrammed on the RFD900, but is currently set at 38400. Check the code to ensure it is still at that setting.
Both computers must have the baud rate set the same.

You can use this script to communicate with the other RFD900 while it is also running a version of this script
OR
You can communicate between this script and a serial terminal. For windows, a common serial terminal is PuTTy;
for testing this program, I communciated with the Jetson Xavier using this script while the Xavier used cutecom serial terminal.
Again make sure you have the correct port and baud rate selected. That's all that really matters.

This program allows you to send and recieve data between the two computers

Helpful Resources:
- Serial library documentation: https://pyserial.readthedocs.io/en/latest/pyserial_api.html
- read and writing using pyserial: http://firmlyembedded.co.za/useful-python-script-to-send-and-receive-serial-data/
'''

import serial as s
import time

class rfd_900:
    
    def __init__(self, port, baudrate):
         # your port name; I found this name from opening a serial terminal (cutecom in my case, use putty on windows)
        self.port = port
        self.baudrate = baudrate
        self.ser = s.Serial(self.port, self.baudrate, timeout=0.001)

    def write(self, data="hello world" ,count=1):
        '''Writes a piece of data count number of times'''
        if count == 0:
            count = 1 # fixes error: count must be at least 1
        
        while count != 0:
            data = data.encode('utf-8') # this encodeing is neccesary for data to be the correct format
            self.ser.write(data)
            time.sleep(1) # sends data every second. Change this to suit your need
            count = count - 1
            
    def read(self, count=1):
        '''Reads a piece of data count number of times, and prints the data each time.
        Returns:
            - returns the last read data. Can be altered to store an array'''
        if count == 0:
            count = 1 # fixes error: count must be at least 1
            
        while count != 0:
            while self.ser.in_waiting:
                data_in = self.ser.readline()
                data_in = data_in.decode('ascii')
                print(data_in)
                count = count - 1
                return data_in
                
    def read_and_write(self, state=0):
        '''For a more through system of reading and writing, use the following: can be further developed'''
    
        start_data = "Script Started"
        start_data = start_data.encode("utf-8")
        self.ser.write(start_data)

        while 1:
            if(state == 0):          # waits for incoming data
                while self.ser.in_waiting:
                    data = self.ser.readline()
                    data = data.decode('ascii')
                    if(data == '1'):  # received a '1' move onto next state
                        state = 1
                        print("1 received")
                        temp = "1 received"
                        temp = temp.encode("utf-8")
                        self.ser.write(temp)
                    else:           # wrong data stay at state 0
                        print("back to the start")
                        temp = "back to the start"
                        temp = temp.encode("utf-8")
                        self.ser.write(temp)

            elif(state == 1):          # waits for incoming data
                while self.ser.in_waiting:
                    data = self.ser.readline().decode("ascii")
                    if(data == '2'):  # received a '2' move on to next state
                        state = 2
                        print("2 received")
                        temp = "2 received"
                        temp = temp.encode("utf-8")
                        self.ser.write(temp)
                    else:            # wrong data return to state 0  
                        state = 0
                        print("back to the start")
                        temp = "back to the start"
                        temp = temp.encode("utf-8")
                        self.ser.write(temp)

            elif(state == 2):          # waits for incoming data
                while self.ser.in_waiting:
                    data = self.ser.readline().decode("ascii")
                    if(data == '3'):  # received a '3'  received a '3' print message
                        print("You win!")
                        temp = "You win!"
                        temp = temp.encode("utf-8")
                        self.ser.write(temp)
                        state = 0; 
                    else:             # wrong data return to state 0  
                        state = 0
                        print("back to the start")
                        temp = "back to the start"
                        temp = temp.encode("utf-8")
                        self.ser.write(temp)
                    