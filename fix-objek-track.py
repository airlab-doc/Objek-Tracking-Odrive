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

#inisialisasi posisi motor 
posisi_x = 90
posisi_y = 90 
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path untuk video file - jika dibutuhkan")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
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
	vs = VideoStream(src=0).start()
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
	frame = imutils.resize(frame, width=1500)
	cols, rows, _ = frame.shape
	center_x = int(rows/2)
	x_med = int (rows/2)
	center_y = int (cols/2)
	y_med = int (cols/2)
	#print (frame.shape)


	(success, boxes) = trackers.update(frame)
	#print(boxes)

	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]				
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "x = " +str(x)+"y = "+str(y)
		cv2.putText(frame, text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.50, (0,0,255))
		#Additional untuk garis vertikal dan horizontal gambar
		x_med = int ((x + x + w) / 2)
		y_med = int ((y + y + h) / 2)
		cv2.line (frame,(x_med,0),(x_med,1500),(77,255,166),2)
		cv2.line (frame,(0,y_med),(1500,y_med),(77,255,166),2)
		#print(text)
		print("center x = " +str(center_x)+", center y= " + str(center_y))
		print ("x Med = "+str(x_med)+", y med= "+str(y_med))

	cv2.imshow("Infiniti-Object-Tracker", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("s"):
		box = cv2.selectROI("Infiniti-Object-Tracker", frame, fromCenter=False,
			showCrosshair=False)
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		trackers.add(tracker, frame, box)

		# write ke motor driver odrive axis0
		# if x_med > center_x + 30:
		# 	posisi_x += 1.5
		# 	motor.axis0.controller.pos_setpoint = posisi_x

		# if x_med < center_x + 30:
		# 	posisi_x -= 1.5
		# 	motor.axis0.controller.pos_setpoint = posisi_x
		
		# if y_med > center_y + 20:
		# 	posisi_y += 1.5
		# 	motor.axis1.controller.pos_setpoint = posisi_y
		# if y_med < center_y + 20:
		# 	posisi_y += 1.5
		# 	motor.axis1.controller.pos_setpoint = posisi_y
		# # break

		#print("Array Lokasi: ", boxes)
		


	elif key == 27:
		break
if not args.get("video", False):
	vs.stop()
else:
	vs.release()
cv2.destroyAllWindows()