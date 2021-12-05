########### find tag and detect then go there, and stop use attitude########################################
import cv2
from camera import gstreamer_pipeline
from detec_tag import Tag
import time
from gpio import IO
import keyboard
import curses
import numpy as np
#############################################################################################################
lower_blue1 = [100, 140, 130]
upper_blue1 = [120, 210, 180]

lower_black = [0, 0, 0]
upper_black = [50, 50, 100]

io = IO()

find = False
arrive = False
att = False
b_att = False
back_stop=False

tag = Tag(lower_blue1,upper_blue1)


up_camera = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 1, flip_method=2), cv2.CAP_GSTREAMER)
#######################################################################

def mouse_callback(event, x, y, flags, param):
    global hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        color = frame[y, x]
        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]
        print(hsv[0], hsv[1], hsv[2])
###############################################################################################################
while True:
    try:
        ret, frame = up_camera.read()
        
        frame = cv2.flip(frame,0)
        frame = cv2.flip(frame,1)
        if not ret :
            print('notopencamera')
            break

    # find color
        edge = tag.find_color(frame)

    # find contour
        stats,centroids = tag.find_contour(edge)
    
    # find property of contour that is tag we want
        try:
            error, find, arrive,areas = tag.find_tag(frame,stats,centroids)
        except:
            find=False
        


        ## can't find   
        cv2.waitKey(1)
        cv2.setMouseCallback('a',mouse_callback,frame)    
        cv2.imshow('a',frame)
        
        
    except KeyboardInterrupt:
        break
    except :
        print('error')
        pass
#####################################################################

#
up_camera.release()
