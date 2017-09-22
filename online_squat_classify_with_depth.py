from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from time import sleep

import csv
import serial
import numpy as np

PORT = '/dev/cu.usbmodem1411'
BAUDE = 9600
OFFSET = 5
NUM_SENSORS = 5
ACCEL_THRESH = 150
clf_pkl = 'experimentation/clf_multilabel_calibrated_v1.pkl'
clf = joblib.load(clf_pkl)

classes_inv = {0:'hlpron', 1:'hlsup', 2:'sup', 3:'heellift', 4:'pron', 5: 'heeldom', 6: 'hdpron', 7: 'hdsup', 8: 'normal'}

# Return a dictionary with events
def classify_events(X):
	#print(X)
	Z_scores = clf.predict_proba(X)
	Z_bin = clf.predict(X)
	mult_scores = np.multiply(Z_scores, Z_bin)
	mult_scores = mult_scores.reshape(mult_scores.shape[1],)

	events = {}
	idx = 0
	for score in mult_scores:
		if (score > 0):
			events[classes_inv[idx+2]] = score
		idx += 1

	return events


def main():
	ser = serial.Serial(PORT, BAUDE)
	clf = joblib.load(clf_pkl)

	ack = input("Press any key to start system.")
	print("Starting...")

	print("Calibrating depth sensor...")

	ser.close()
	ack = input("Stand tall and press any key.")
	print("Sensing top position...")

	idx = 0;
	upright_readings = []
	ser.open()
	ser.flushInput()
	while idx <= 250:
		line = ser.readline();
		print(line)
		try:
			line = line.strip().decode('utf-8')
			line = line.split(", ")
			acc_reading = int(line[-1])
			upright_readings.append(acc_reading)
			idx+=1
		except:
			continue

	upright_mean = -1 * int(np.mean(upright_readings))
	print(upright_mean)

	ser.close()
	ack = input("Squat to lowest position and press any key.")
	print("Sensing bottom position...")

	idx = 0;
	bottom_readings = []
	ser.open()
	ser.flushInput()
	while idx <= 250:
		line = ser.readline();
		print(line)
		try:
			line = line.strip().decode('utf-8')
			line = line.split(", ")
			acc_reading = int(line[-1])
			bottom_readings.append(acc_reading)
			idx+=1
		except:
			continue

	bottom_mean = -1 * int(np.mean(bottom_readings))
	print(bottom_mean)

	ser.close()
	ack = input("Press any key to start finding errors.")
	ser.open()
	ser.flushInput()
	accel_buffer = []
	# get a starting accelerometer value
	for i in range(5):
		line = ser.readline();
		print(line)
		try:
			line = line.strip().decode('utf-8')
			line = line.split(", ")
			acc_reading = int(line[-1])
			accel_buffer.append(acc_reading)
			idx+=1
		except:
			continue
	prev_accel = -1 * int(np.mean(accel_buffer))
	accel_buffer = []
	try:
		X = []
		while True:
			line = ser.readline();
			line = line.strip().decode('utf-8')
			line = line.split(", ")
			try:
				accel = int(line[-1])
				del line[-1]
				line = list(map(int, line))
				X.append(line)
				accel_buffer.append(accel)
			except:
				continue
			if len(X) == OFFSET:
				# transform F into a (1, NUM_SENSORS*OFFSET) shape feature vector
				events = {}
				try:
					X_f = np.array(X).flatten(order='F').reshape(1, -1)
					events = classify_events(X_f)
				except:
					print ("could not flatten")
				
				current_accel = -1 * int(np.mean(accel_buffer))
				if current_accel >= prev_accel + ACCEL_THRESH:
					# ascent
					percentage = (current_accel - bottom_mean) / (upright_mean - bottom_mean)
					print ("ASCENT: " + str(percentage))
				elif current_accel <= prev_accel - ACCEL_THRESH:
					# descent
					percentage = (upright_mean - current_accel) / (upright_mean - bottom_mean)
					print ("DESCENT: " + str(percentage))
				else:
					# stable
					print ("STABLE")
				prev_accel = current_accel
				accel_buffer = []
				X = []
				print(str(events) + ", ")
				print("_____________________")
	except KeyboardInterrupt:
		print("Stopping...")
		ser.close()

if __name__ == "__main__":
	main()