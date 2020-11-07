import cv2
import os
import time
import pandas as pd
import csv

def createPath(name):
	cwd = os.getcwd()
	id_df = pd.read_csv(cwd + "\\id_gen_db\\id_db.csv")
	if id_df.empty:
		with open(cwd + "\\id_gen_db\\id_db.csv", "a") as f:
			write = csv.writer(f)
			write.writerow([100, "admin"])

	lastrow = id_df.iloc[-1]
	id_no = int(lastrow["id"]) + 1
	parent_dir = "dataset/"
	id = "LA_" + str(id_no)
	path = parent_dir + id#+ id of a person
	return id_no, path
	


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
def imageCapture(img_count = 6, timecounter = 20):
	cwd = os.getcwd()
	name = input("Please enter the name: ")
	id, path = createPath(name)
	start = time.time()
	try:
		os.mkdir(path)
		os.mkdir(path + "/record")
	except:
		pass

	cam = cv2.VideoCapture(0)
	cv2.namedWindow("test")
	img_counter = 0

	while time.time()-start <= timecounter:
		k = cv2.waitKey(1)
		ret, frame = cam.read()
		if not ret:
			print("Failed to grab frame")
			break
		cv2.imshow("test", frame)

		if k == ord('s'):
			# key s pressed to save image
			img_name = "/"+ name +"_{}.png".format(img_counter)
			img_path = path + img_name
			print(img_path)
			print("saving...",img_name )
			cv2.imwrite(img_path, frame)
			print("{} saved!".format(img_name))
			img_counter += 1

		if img_counter == img_count:
			with open(cwd + "\\id_gen_db\\id_db.csv", "a") as f:
				write = csv.writer(f)
				write.writerow([id, name])
				print("User Id:", id)
				print("User Name:", name)
				print("Record added successfully..!")
			break
	cam.release()
	cv2.destroyAllWindows()
imageCapture()
