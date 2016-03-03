#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# import ev3dev.ev3 as ev3
# import time


import cv2
import numpy as np

# Videostream der Webcam
cap = cv2.VideoCapture(0)
# Größe für die morphologischen Operationen
kernel = np.ones((5,5),np.uint8)

while(1):
           
    # Take each frame
    _, frame = cap.read()
 
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
    # define range of blue color in HSV
    lower_blue = np.array([100,50,50])
    upper_blue = np.array([140,255,255])
    lower_red = np.array([170,50,50])
    upper_red = np.array([179,255,255])
    
    # Threshold the HSV image to get only blue colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    
    # Auf den Masken MORPH_OPEN
    mask_img_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
    mask_img_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
      
    # Auf des Masken MORPH_CLOSE  
    mask_img_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)
    mask_img_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)       
     
    # Bitwise-AND mask and original image
    img_blue = cv2.bitwise_and(frame,frame, mask= mask_img_blue)
    img_red = cv2.bitwise_and(frame,frame, mask= mask_img_red)

    # Kreiserkennung auf dem Originalbild
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,
                                param1=50,param2=30,minRadius=20,maxRadius=100)
    
    # Behandlung, wenn Kreise gefunden wurden   
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            
            # ROI erstellen, in der die Farbe verglichen werden soll.
            # Die ROI ist kleiner als der Kreis, da der Rand relativ 
            # stark rauscht
            width, height = frame.shape[:2]
            roi = np.zeros((width,height,1), np.uint8)
            cv2.circle(roi, (i[0],i[1]), i[2]/3,(255,255,255),i[2]/2,1)
            
            # Mittelwert der jeweiligen Maske in der ROI bestimmen;
            # wenn mehr als 50% der ROI der gesuchten Farbe entsprechen,
            # wird diese Farbe für den Ball angenommen
            if cv2.mean(mask_img_blue,roi)[0] > 130:
                cv2.circle(cimg,(i[0],i[1]),i[2],(255,0,0),2)
            elif cv2.mean(mask_img_red,roi)[0] > 130:
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),2)
            else:
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            
            ## Farbe bestimmen nur im Mittelpunkt des Kreises (ein Pixel)
            #if (mask_img_blue.item(i[1],i[0]) != 0):
            #    cv2.circle(cimg,(i[0],i[1]),i[2],(255,0,0),2)
            #elif (mask_img_red.item(i[1],i[0]) != 0):
            #    cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),2)
            #else:
            #    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            #                   
            ## draw the center of the circle
            #cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            
               
    else:
        #print "kein Kreis gefunden"
        pass
    
    cv2.namedWindow("circles", cv2.WINDOW_NORMAL)  
    cv2.imshow('circles',cimg) 
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL) 
    cv2.imshow('frame',frame)
    cv2.namedWindow("mask_img_blue", cv2.WINDOW_NORMAL) 
    cv2.imshow('mask_img_blue',mask_img_blue)
    cv2.namedWindow("mask_img_red", cv2.WINDOW_NORMAL) 
    cv2.imshow('mask_img_red',mask_img_red)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    
cv2.destroyAllWindows()





### meine Spielwiese ;) ###################################################

# img = cv2.imread('12778675_1670359409872608_1369794692069849486_o.jpg',0)
# img = cv2.medianBlur(img,5)
# cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
# cv2.namedWindow("circles", cv2.WINDOW_NORMAL)  
# cv2.imshow('circles',cimg)
# circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,
#                             param1=50,param2=30,minRadius=30,maxRadius=200)
#   
# if circles is not None:
#     circles = np.uint16(np.around(circles))
#     for i in circles[0,:]:
#         # draw the outer circle
#         cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#         # draw the center of the circle
#         cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
#           
# else:
#     print "kein Kreis gefunden"
#  
# cv2.namedWindow("detected circles", cv2.WINDOW_NORMAL)    
# cv2.imshow('detected circles',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()





#m = ev3.Motor('outA')

#m.connected
#m.run_timed(time_sp=3000, duty_cycle_sp=75)
#time.sleep(3)

    
#ev3.Screen.draw.rectangle((10,10,60,20), fill='black')
#time.sleep(5)