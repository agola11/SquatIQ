from sklearn.externals import joblib
from sklearn.svm import LinearSVC

import csv
import serial
import numpy as np

PORT = '/dev/cu.usbmodem1421'
BAUDE = 9600
OFFSET = 5
NUM_SENSORS = 5
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

	#print(mult_scores)
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
	try:
		X = []
		while True:
			line = ser.readline();
			line = line.strip().decode('utf-8')
			line = line.split(", ")
			try:
				line = list(map(int, line))
				X.append(line)
			except:
				continue
			if len(X) == OFFSET:
				#print ("OFFSET...")
				# transform F into a (1, NUM_SENSORS*OFFSET) shape feature vector
				try:
					X_f = np.array(X).flatten(order='F').reshape(1, -1)
					events = classify_events(X_f)
					print(events)
					X = []
				except:
					print ("could not flatten")
					X= []
					continue
	except KeyboardInterrupt:
		print("Stopping...")

if __name__ == "__main__":
	main()