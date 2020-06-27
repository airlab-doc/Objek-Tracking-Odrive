# Objek Tracking With Hikvision Camera for 100m Object Tracker 

### Pre-requisite
- Python 3
- OpenCV
- Numpy
- WebCamera
- Odrive V3.6
- Odrive Lib python
- Onvif

### Image Frame

Explore the `objek-tracking.py` file.

you can select the camera port using 
```
#For Webcam
vs = VideoStream(src=0).start() 
```
```
#For USB Camera
vs = VideoStream(src=1).start() 
```
```
#For IP Cam
vs = VideoStream(src="Your RTSP / IP and Port Address").start() 
```
### Type of Tracking Method
- csrt
- kcf
- boosting
- mil
- tld
- medianflow
- mosse

executing the tracking method : `python objek-tracking.py --tracker boosting` . but for default, when execute `python objek-tracking.py`,  `csrt` method is used.

### Actuator
for output, we use an Odrive v3.6 Driver motor, please check [this](https://odriverobotics.com/) for detail.

### Camera
for camera, we use an `onvif` method to control Pan-tilt-zoom of Hikvision Camera read [this](http://onvif.org). the result video will be streamed with RTSP protocol. check this tutorial [video](https://www.youtube.com/watch?v=xGYcYtCvT2Y) 


