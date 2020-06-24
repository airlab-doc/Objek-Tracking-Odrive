# Objek-Tracking-Odrive
if you want to ask us, please visit www.infinitigroup.co.id

### Pre-requisite
- Python 3
- OpenCV
- Numpy
- WebCamera
- Odrive V3.6
- Odrive Lib python

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

