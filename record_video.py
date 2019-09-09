import cv2
import numpy as np
import time
import datetime
import array as arr
import multiprocessing as mp


og_frame = None
Start = 1
mThresh = 10
mEvent = 0
rollCount = 0
rollArr_B = []
rollArr_A = []
rollArr = []
mNow = []
processes = []



def detect_motion(og_frame, frame):
	og_frame_gray = cv2.cvtColor(og_frame, cv2.COLOR_BGR2GRAY)
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	diff_frame = cv2.absdiff(og_frame_gray, frame_gray)
	return np.mean(diff_frame)

def convert_video(rollArr_B, rollArr_A, mNow):
	rollArr = rollArr_B + rollArr_A
	out = cv2.VideoWriter("./vids/"+mNow+".avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
	for i in range(len(rollArr)):
		out.write(rollArr[i])
	out.release()
	rollArr_B = []
	rollArr_A = []
	rollArr = []

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



	while(True):
		ret, frame = cap.read()

		if ret == True:
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			#frame = frame.array

			#analyze difference
			if Start == 1:
				og_frame = np.copy(frame)
				Start = 0


			if detect_motion(og_frame, frame) > mThresh:
				isMotion = 1
				print("MOTION")
				print(detect_motion(og_frame, frame))
				mEventStart = time.time()

				if mEvent == 0:
					print("START RECORDING")
					mEvent = 1
					rollArr_A.append(frame)
					# out = cv2.VideoWriter("./vids/"+mNow+".avi",cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
					# out.write(frame)
					mNow = datetime.datetime.now()
					mNow = mNow.strftime("%Y-%m-%d_%H-%M-%S")

				if mEvent == 1:
					# out.write(frame)
					rollArr_A.append(frame)

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
						rollArr_A.append(frame)
						print(time.time()-mEventStart)

				else:
					mEvent = 0
					print("STOP RECORDING")
					processes.append(p = mp.Process(target=convert_video, args=(rollArr_B, rollArr_A, mNow)))
					for pr in processes:
						pr.start()
						pr.join()

			# Display the resulting frame
			cv2.imshow('frame',frame)

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
