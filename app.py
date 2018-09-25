# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import vlc
from threading import Thread

def myfunc(i):
    print ("Start threading %d")
    os.system("pkill omxplayer")
    os.system("omxplayer -o local --loop --no-osd /home/pi/motion/1.mp4")   
    print ("Finish Leeepaing %d")
    
def myfunc3(i):
    print ("Start threading %d")    
    os.system("omxplayer -o local --loop --no-osd /home/pi/motion/2.mp4")   
    print ("Finish Leeepaing %d")
    
    
#def myfunc4(i):
#    p = vlc.MediaPlayer("voice.mp3")
#    p.play()
    

def myfunc2(i):
     os.system("pkill omxplayer")
     os.system("omxplayer -o local --loop --no-osd /home/pi/motion/2.mp4")   
     print("End")
     
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=80000, help="minimum area size")
args = vars(ap.parse_args())


 
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
t = Thread(target = myfunc3, args=(1,))
t.start()
# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text	
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied"
        
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:            
            break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
		    
	        
                
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
	#	(x, y, w, h) = cv2.boundingRect(c)
	#	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)			
		text = "Occupied"
		
	 

	# draw the text and timestamp on the frame
	#cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
	#	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	#cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	#	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record if the user presses a key
	if text == "Occupied":         
            t = Thread(target = myfunc, args=(1,))
            #t2 = Thread(target = myfunc4, args=(1,))
            t.start()
            #t2.start()         
         
            time.sleep(110)
            t = Thread(target = myfunc2, args=(3,))
            t.start()
            time.sleep(5)
           
            
         
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
        #cv2.imshow("Security Feed", frame)
	key = cv2.waitKey(1) & 0xFF
        #cv2.destroyAllWindows()
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()


