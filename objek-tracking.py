from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2

# import odrive
# from odrive.enums input *
# import math
#menunggu odrive datang
# motor = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

#motor.axis0.controller.pos_setpoint = setpoint


#inisialisasi posisi motor 
#posisi = 90 


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path untuk video file - jika dibutuhkan")
ap.add_argument("-t", "--tracker", type=str, default="csrt",
	help="tipe object tracker yg digunakan")
args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}

trackers = cv2.MultiTracker_create()

if not args.get("video", False):
	print("Mulai stream kamera...")
	vs = VideoStream(src=1).start()
	time.sleep(1.0)
else:
	vs = cv2.VideoCapture(args["video"])

while True:

	frame = vs.read()
	# _, fro = vs.read()
	# rows, cols, _ = frame.shape
	# center = int(cols / 2)
	# x_med = int(cols / 2)
	#print (center)


	frame = frame[1] if args.get("video", False) else frame

	
	if frame is None:
		break
	frame = imutils.resize(frame, width=1300)
	rows, cols, _ = frame.shape
	center = int(cols/2)
	x_med = int (cols/2)
	y_med = int (rows/2)


	(success, boxes) = trackers.update(frame)
	print(boxes)

	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]
		x_med = int ((x + x + w) / 2)
		y_med = int ((y + y + h) / 2)				
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "x = " +str(x)+ "  y= "+str(y)
		# cv2.putText(frame, text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.50, (0,0,255))
		# #Additional untuk garis vertikal dan horizontal gambar
		
		cv2.line (frame,(x_med,0),(x_med,1300),(77,255,166),2)
		cv2.line (frame,(0,y_med),(1300,y_med),(77,255,166),2)
		print(text)
		print(center)
		print (x_med)

	cv2.imshow("Infiniti-Object-Tracker", frame)
	cv2.moveWindow("Infiniti-Object-Tracker",100,100)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("s"):
		box = cv2.selectROI("Infiniti-Object-Tracker", frame, fromCenter=False,
			showCrosshair=False)
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		trackers.add(tracker, frame, box)
		#write ke motor driver odrive
		# if x_med > center + 30:
		# 	posisi += 1.5
		# 	motor.axis0.controller.pos_setpoint = posisi

		# if x_med < center + 30:
		# 	posisi -= 1.5
		# 	motor.axis0.controller.pos_setpoint = posisi
		# break

		#print("Array Lokasi: ", boxes)
		


	elif key == 27:
		break
if not args.get("video", False):
	vs.stop()
else:
	vs.release()
cv2.destroyAllWindows()