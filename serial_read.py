import serial

PORT = '/dev/cu.usbmodem1421'
BAUDE = 9600

ser = serial.Serial(PORT, BAUDE)

while True:
	print(ser.readline())