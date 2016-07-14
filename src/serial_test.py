import new_era as ne
import serial 
#serial_port = 'COM5'
serial_port = "/dev/ttyUSB0"

ser = serial.Serial(serial_port,19200,timeout=.1)

