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

cam = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

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
		img_name = "/image_capture_{}.png".format(img_counter)
		img_path = path + img_name
		print(img_path)
		print("saving...",img_name )
		cv2.imwrite(img_path, frame)
		print("{} written!".format(img_name))
		img_counter += 1

cam.release()
cv2.destroyAllWindows()
