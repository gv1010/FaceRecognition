import cv2
import os
name = ""
while name == "":

	name = input("Give your name: ")
	parent_dir = "dataset/"
	path = parent_dir + name #+ id of a person
	try:
		os.mkdir(path)
		os.mkdir(path + "/record")
	except:
		print("choose a different name")
		name = ""
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
	ret, frame = cam.read()
	if not ret:
		print("failed to grab frame")
		break
	cv2.imshow("test", frame)

	k = cv2.waitKey(1)
	if k%256 == 27:
		# ESC pressed
		print("Escape hit, closing...")
		break
	elif k%256 == 32:
		# SPACE pressed
		img_name = "/opencv_frame_{}.png".format(img_counter)
		img_path = path + img_name
		print(img_path)
		print("saving...",img_name )
		cv2.imwrite(img_path, frame)
		print("{} written!".format(img_name))
		img_counter += 1

cam.release()
cv2.destroyAllWindows()
