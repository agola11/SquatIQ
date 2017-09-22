import csv
import serial

PORT = '/dev/cu.usbmodem1411'
BAUDE = 9600

ser = serial.Serial(PORT, BAUDE)

## in out front back

ack = input("Press any key to start recording data.")
print("Recording...")
with open('experimentation/adam_fisch/raw_sensor_data/testing/clock.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	try:
		while True:
			line = ser.readline();
			line = line.strip().decode('utf-8')
			line = line.split(", ")
			writer.writerow(line)
	except KeyboardInterrupt:
		print("Stopping...")

