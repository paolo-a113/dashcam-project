# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
size = (500, 500)
camera.resolution = size
rawCapture = PiRGBArray(camera, size=size)
camera.framerate = 25

# allow the camera to warmup
time.sleep(0.1)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
rec = cv2.VideoWriter('output.avi',fourcc,20.0, size)
# capture frames from the camera

startTime = time.time()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = frame.array

	rec.write(frame)
	
	if (time.time() - startTime) > 10:
		rec.release()
		break

	# show the frame
	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	
	
		
cv2.destroyAllWindows
