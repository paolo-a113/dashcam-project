import cv2
import numpy as np
import time
import datetime
import array as arr


og_frame = None
Start = 1
mThresh = 10
mEvent = 0
rollCount = 0
rollArr = []

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

		og_frame_gray = cv2.cvtColor(og_frame, cv2.COLOR_BGR2GRAY)
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		diff_frame = cv2.absdiff(og_frame_gray, frame_gray)

		if np.mean(diff_frame) > mThresh:
			isMotion = 1
			print("MOTION")
			print(np.mean(diff_frame))
			mEventStart = time.time()
			mNow = datetime.datetime.now()
			mNow = mNow.strftime("%Y-%m-%d_%H-%M-%S")

			if mEvent == 0:
				print("START RECORDING")
				mEvent = 1
				out = cv2.VideoWriter("./vids/"+mNow+".avi",cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
				out.write(frame)
				mNowStart = mNow

			if mEvent == 1:
				out.write(frame)


		else:
			isMotion = 0
			print("")
			rollArr.append(frame)
			if len(rollArr) > 100:
				rollArr.pop(0)
			print(len(rollArr))

			if mEvent == 1:
				if (time.time() - mEventStart) < 10:
					out.write(frame)
					print(time.time()-mEventStart)

				else:
					print("STOP RECORDING")
					out.release()
					mEvent = 0
					outB = cv2.VideoWriter("./vids/"+mNowStart+"_b.avi",cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
					for i in len(rollArr):
						outB.write(rollArr[i])
					outB.release()
					rollArr = []
					# os.system("ffmpeg -i ./vids/" + mNowStart + ".avi ./vids/"+ mNowStart + ".mp4")
					# os.system("rm ./vids/" + mNowStart + ".avi")

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
out.release()

# Closes all the frames
cv2.destroyAllWindows()
