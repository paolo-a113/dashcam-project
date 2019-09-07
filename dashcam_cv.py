# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime
import cv2
import numpy as np
import sys

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
size = (500, 500)
camera.resolution = size
rawCapture = PiRGBArray(camera, size=size)
camera.framerate = 30

# allow the camera to warmup
time.sleep(0.1)

og_frame = None
Start = 1
mThresh = 10
mEvent = 0

fourcc = cv2.VideoWriter_fourcc(*'XVID')
rec = cv2.VideoWriter('./vids/output.avi',fourcc,25.0/2, size)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = frame.array

	#analyze difference
	if Start == 1:
		og_frame = np.copy(frame)
		Start = 0

	og_frame_gray = cv2.cvtColor(og_frame, cv2.COLOR_BGR2GRAY)
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	diff_frame = cv2.absdiff(og_frame_gray, frame_gray)

	if np.mean(diff_frame) > mThresh:
		isMotion = 1
		print("MOTION")
		mEventStart = time.time()
		mNow = datetime.datetime.now()
		mNow = mNow.strftime("%Y-%m-%d_%H:%M:%S")

		if mEvent == 0:
			print("START RECORDING")
			mEvent = 1
		rec = cv2.VideoWriter('./vids/'+mNow+'.avi',fourcc,25.0/2, size)
		rec.write(frame)

	else:
		isMotion = 0
		print("")

		if mEvent == 1:
			if (time.time() - mEventStart) < 10:
				rec.write(frame)
				print(time.time()-mEventStart)

			else:
				print("STOP RECORDING")
				rec.release()
				mEvent = 0

	# show the frame
	cv2.imshow("Original Frame", og_frame_gray)
	cv2.imshow("Frame", frame_gray)
	cv2.imshow("Motion Frame", diff_frame)

	key = cv2.waitKey(1) & 0xFF

	og_frame = np.copy(frame)

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

cv2.destroyAllWindows
