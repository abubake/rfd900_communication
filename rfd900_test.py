'''Script for using the RFD900 serial communciations class developed by Baker Herrin using serial library'''
from rfd900_serial import rfd_900

rfd = rfd_900(port = '/dev/ttyUSB0', baudrate = 38400) #initalizes the rfd900 to the correct baud rate and communication (COM) port
rfd.write(data="hi there!",count=1) # writes a message count times to the other
val = rfd.read(count=1) # wait for something to read
print(val)