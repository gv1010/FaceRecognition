import face_recognition
from imutils import paths
import os
import pandas as pd
import re
import time
from tqdm import tqdm
import pickle

class Encoder:
	def createEncoding():
		"""
		When the user is added or deleted, we run this function, to encode the faces or delete the deleted users encodings.
		As the number of users increases, this function will take a lot of time to finish the encoding.
		
		Args:
					None
		Returns:
					returns the newly created a faceencoded pickle file
		"""

		cwd = os.getcwd()
		imagePaths = list(paths.list_images(cwd + "\\dataset"))

		knownEncodings = []
		knownNames = []
		knownIds = []
		st = time.time()
		print(int(st))
		for (i, imagePath) in tqdm(enumerate(imagePaths)):
			id = imagePath.split(os.path.sep)[-2]
			name = " ".join(re.findall(r"[a-zA-Z]+", imagePath.split(os.path.sep)[-1].split(".")[0].lower()))
			print(name)
			ext = imagePath.split(os.path.sep)[-1]
			#print(imagePath)
			if ext.split(".")[-1].lower() in ["jpg", 'png', 'jpeg']:
				f_image = face_recognition.load_image_file(imagePath)
				faces_encoding = face_recognition.face_encodings(f_image)
				try:
					knownEncodings.append(faces_encoding[0])
					knownNames.append(name)
					knownIds.append(id)
					print(faces_encoding[0])
				except:
					pass

		name_faceencode = [tuple(knownNames), tuple(knownEncodings), tuple(knownIds)]
		print(name_faceencode)
		pickelPath = cwd + "\\nameface_serialize\\" + str(int(time.time())) + ".pickle"
		pickle_out = open(pickelPath ,"wb")
		pickle.dump(name_faceencode, pickle_out)
		pickle_out.close()
		print("Images Encoded in ", (time.time()-st))

		return pickelPath
