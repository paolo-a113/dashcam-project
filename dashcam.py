from picamera import PiCamera
from time import sleep
from datetime import datetime
import os

def set_lodef():
	global cam
	cam.resolution = (640, 480)
	cam.framerate = 5
	
def set_hidef():
	global cam
	cam.resolution = (1920, 1080)
	cam.framerate = 25

def main():
	global cam
	cam = PiCamera()
	set_hidef()
	time_string = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

	cam.start_preview()

	cam.start_recording(time_string + 
	'.h264')
	cam.wait_recording(25)
	cam.stop_recording()
	cam.stop_preview()

	os.system('MP4Box -add ' + time_string + '.h264 ' + time_string + '.mp4')
	os.system('rm ' + time_string + '.h264')
	
	
	
if __name__ == "__main__":
    # execute only if run as a script
    main()

