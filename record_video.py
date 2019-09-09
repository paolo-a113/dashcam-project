import cv2
import numpy as np
import time
import datetime
import array as arr
import threading
import os


og_frame = None
Start = 1
mThresh = 10
mEvent = 0
rollCount = 0
rollArr_B = []
rollArr_A = []
rollArr = []
mNow = ''
processes = []



def detect_motion(og_frame, frame):
	og_frame_gray = cv2.cvtColor(og_frame, cv2.COLOR_BGR2GRAY)
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	diff_frame = cv2.absdiff(og_frame_gray, frame_gray)
	return np.mean(diff_frame)

def convert_before_video(rollArr_B, mNow):
	out_b = cv2.VideoWriter("./vids/"+mNow+"_b.avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
	for i in range(len(rollArr_B)):
		out_b.write(rollArr_B[i])
	out_b.release()
	rollArr_B = []

if __name__ == "__main__":
	# Create a VideoCapture object
	cap = cv2.VideoCapture(0)

	# Check if camera opened successfully
	if (cap.isOpened() == False):
	  print("Unable to read camera feed")

	# Default resolutions of the frame are obtained.The default resolutions are system dependent.
	# We convert the resolutions from float to integer.
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	out = cv2.VideoWriter("./vids/"+mNow+".avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))


	while(True):
		time.sleep(0.01)
		ret, frame = cap.read()

		if ret == True:
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			#frame = frame.array

			#analyze difference
			og_frame = np.copy(frame)




			if detect_motion(og_frame, frame) > mThresh:
				isMotion = 1
				print("MOTION")
				print(detect_motion(og_frame, frame))
				mEventStart = time.time()

				if mEvent == 0:
					print("START RECORDING")
					mEvent = 1
					out.write(frame)

					mNow = datetime.datetime.now()
					mNow = mNow.strftime("%Y-%m-%d_%H-%M-%S")

				if mEvent == 1:
					out.write(frame)
					#rollArr_A.append(frame)

			else:
				isMotion = 0
				print("")

				if mEvent == 0:
					rollArr_B.append(frame)
					if len(rollArr_B) > 100:
						rollArr_B.pop(0)
					print(len(rollArr_B))

				if mEvent == 1:
					if (time.time() - mEventStart) < 10:
						out.write(frame)
						print(time.time()-mEventStart)

					else:
						mEvent = 0
						print("STOP RECORDING")
						out.release()
						convert_before_video(rollArr_B, mNow)
						rollArr_A = []

			# Display the resulting frame
			cv2.imshow("Original Frame", og_frame_gray)
			cv2.imshow("Frame", frame_gray)
			cv2.imshow("Motion Frame", diff_frame)

			# Press Q on keyboard to stop recording
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	  # Break the loop
		else:
			break

	# When everything done, release the video capture and video write objects
	cap.release()

	# Closes all the frames
	cv2.destroyAllWindows()
