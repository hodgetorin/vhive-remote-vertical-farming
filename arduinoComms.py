#roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Bidirectional_Serial_communication_between_Raspberry_Pi_and_Arduino

# The Raspberry Pi will receive data from Arduino in bytes
# This program decodes those bytes and translates them into something we can read
# In the while True statement, readline() is used to read of full line of String from Arduino.
# If instead we want to read bytes, use read(size = 1) (to read 1 byte)
# If instead we want to see if the Arduino is sending info on its own, use
#                if (Serial.available() > 0): ....

import serial
import time

connected = False

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = None)
    ser.flush()
    connected = True
except serial.serialutil.SerialException as e:
    try:
        ser = serial.Serial('/dev/ttyACM1', 9600, timeout = None)
        ser.flush()
        connected = True
    except serial.serialutil.SerialException as e:
        print(e)

def flush():
    if connected:
        ser.flush()
        ser.flushInput()

def send(data):
    if connected:
        ser.write((data + "\n").encode("ascii"))
        return data
    
def readLine():
    if connected:
        return ser.readline().decode("ascii").rstrip()

def readLines(count):
    if connected:
        lines = []
        for i in range(count):
            lines.append(ser.readline().decode("ascii").rstrip())
            print(lines[i])
        return lines

# ACM0 is the serial device name
# 9600 is baud rate, which matches baud rate set in Arduino
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout = 1)
    ser.flush()
    
    while True:
        # Add 'b' before the string we want to send to convert it into bytes the Arduino can read
        # Be sure to add newline character at the end
        ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)