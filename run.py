import face_recognition
import cv2
import numpy as np
from imutils import paths
import os
import time
import pandas as pd
import csv
from datetime import date, datetime
import pickle

"""
This file runs loads the trained pickle file, opens the camera, when the users face is detected,
then current time will be updated in the users specific record sub folder, and stored in csv
format.
"""


def gstreamer_pipeline(capture_width=3280, capture_height=2464, display_width=820, display_height=616, framerate=21, flip_method=0):
	return (
		"nvarguscamerasrc ! "
		"video/x-raw(memory:NVMM), "
		"width=(int)%d, height=(int)%d, "
		"format=(string)NV12, framerate=(fraction)%d/1 ! "
		"nvvidconv flip-method=%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
		"videoconvert ! "
		"video/x-raw, format=(string)BGR ! appsink"
		% (
			capture_width,
			capture_height,
			framerate,
			flip_method,
			display_width,
			display_height,
		)
	)


#video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

# Load a sample picture and learn how to recognize it.
#obama_image = face_recognition.load_image_file("2.jpg")
#obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
#
## Load a second sample picture and learn how to recognize it.
#biden_image = face_recognition.load_image_file("4.jpg")
#biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names


# pickle_in = open("dict.pickle","rb")
# example_dict = pickle.load(pickle_in)
cwd = os.getcwd()
def lastModifiedPickle(path):
	"""
	Takes path as input looks for the last modified file in the path
	and return the latest updated path.
	
	Args:
		path:		nameface_serialize directory path
		
	Returns:
		latest updated file in the directory
	"""
	files = os.listdir(path)
	paths = [os.path.join(path, basename) for basename in files]
	return max(paths, key=os.path.getctime)

encodingsPath = cwd + "\\nameface_serialize"
newencodePath =  lastModifiedPickle(encodingsPath)
#print(newencodePath)
pickle_in = open(newencodePath,"rb")
unzip = pickle.load(pickle_in)
known_face_names, known_face_encodings, ids = unzip
print(ids)
video_capture = cv2.VideoCapture(0)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
payment_update = pd.read_csv(cwd + "\\payment\\Payment Update.csv")
mark_attendence = pd.read_csv(cwd + "\\mark attendence\\Mark Attendence.csv")
time_capture = []

while True:
	# Grab a single frame of video
	today = date.today()
	ret, frame = video_capture.read()

	# Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]

	# Only process every other frame of video to save time
	if process_this_frame:
		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_names = []
		for face_encoding in face_encodings:
			# See if the face is a match for the known face(s)
			s = time.time()
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = "Unknown"
			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			print(time.time() - s, process_this_frame)


			if matches[best_match_index]:
				id = ids[best_match_index]
				name = known_face_names[best_match_index]
				payment_row = payment_update[payment_update["id"] == id]
				#print(row)
				time_capture.append(time.time())
				#attendence_row = mark_attendence[mark_attendence[""]]

				print(payment_row["daysCount"].values[0], payment_row["feesPaid"].values[0])
				#Creates csv file and appends the datetimestamp
				with open(cwd + "\\dataset\\"+ id + "\\record\\" +str(date.today().day)+ str(date.today().month)+ str(date.today().year)+".csv", "a") as f:
					write = csv.writer(f)
					now = datetime.now()
					date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
					print(date_time)
					write.writerow([id, date_time])

				if payment_row["feesPaid"].values[0].lower() == "no":
					print("Hi", name, "!", "Please clear your dues.")
					alert = "Pending Dues !"
					name = alert

			face_names.append(name)
	process_this_frame = not process_this_frame


	# Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	# Display the resulting image
	cv2.imshow('Video', frame)

	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
