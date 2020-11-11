# -*- coding: utf-8 -*-
"""
Created on Sat May  4 13:48:07 2019

@author: adwait
"""
import cv2
import numpy as np

pts = []
trigger = 0

# Import the required modules
def roi_dry(window_name, im_disp):
    
#    im_disp = frame.copy()
    window_name = "Left click: Drop points; Right Click: Close Polygon; Enter: Continue"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, 0, 0)
    
    print (" Left click to drop points around interested region.\n")
    print (" After finished, right click to show polygon.\n Press Enter to continue program.")
    
    def callback(event, x, y, flags, param):

        global trigger, pts
    
        if  event != cv2.EVENT_RBUTTONDOWN:
            if event == cv2.EVENT_LBUTTONDOWN:
                pts.append([x,y])
                if trigger >= 1:
                    pts_tmp = np.array(pts,np.int32)[-2:]
                    cv2.line(im_disp, tuple(pts_tmp[0]), #live line display
                                   tuple(pts_tmp[1]), 
                                   (0,0,255), 1)
                trigger += 1
        else:
            pts = np.array(pts,np.int32)
            cv2.polylines(im_disp, [pts], True, (0,0,255), 2) #final polygon roi
    #        pass

    cv2.setMouseCallback(window_name, callback)
    
    while True:
        cv2.imshow(window_name,im_disp)
        key = cv2.waitKey(10) & 0xFF
    
        if key == 13: #press enter to continue
            cv2.destroyAllWindows()
            print("pts", pts)
            return pts
    
    

def roi_wet(frame_bin, epsilon_fraction, min_area, hull = False,
            combine = False, roi_morph = False, x_roi_morph = 5, y_roi_morph = 30):
##    frame_bin = cv2.bitwise_not(frame)
##    print("1")

    contours_wet, hierarchy_edge = cv2.findContours(frame_bin, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    j = 0
    if len(contours_wet) != 0:
        while i - j <= len(contours_wet) - 1:
            a = cv2.contourArea(contours_wet[i-j])
            if a < min_area: #fill small areas
                cv2.drawContours(frame_bin, [contours_wet[i-j]],
                                 -1, (0,0,0), -1)
                del contours_wet[i-j]
                j += 1 #count small areas
                i += 1
                continue
            i += 1

    #morph roi
    if roi_morph == True:
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (x_roi_morph, y_roi_morph))
        frame_bin_roi = cv2.morphologyEx(frame_bin, cv2.MORPH_CLOSE, rect_kernel)
    else:
        frame_bin_roi = frame_bin

    #get contours of morphed frame (final)
    contours_wet, hierarchy_edge = cv2.findContours(frame_bin_roi, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)        
##    print("2")
    if contours_wet == []:
        frame_hull_final = np.array([[0,0],[0,0],[0,0],[0,0]], np.int32)
    else:
        contours_wet.sort(key= lambda x:cv2.contourArea(x), reverse = True)
        cont_comb = np.vstack(contours_wet[i] for i in range(len(contours_wet)))
        epsilon = epsilon_fraction*cv2.arcLength(contours_wet[0],True)
        frame_hull = cv2.approxPolyDP(contours_wet[0],epsilon,True)
        frame_hull2 = cont_comb if combine ==True else frame_hull
        frame_hull_final = cv2.convexHull(frame_hull2) if hull == True else frame_hull2
    return frame_bin_roi, frame_hull_final

