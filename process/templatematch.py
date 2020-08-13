# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:15:40 2020

@author: adwait
"""
import sys
import cv2
import numpy as np
import math

#remove comment to run the code standalone
sys.path.append('C:/Users/adwait/Desktop/Python/AdheSee') 

from imagesegment import ImageSegment
import source.app.drawroi as drawroi
# from matplotlib import pyplot as plt

class TemplateMatch(ImageSegment):
    
    def detectLine(self, top_left, gray,gray_cropped, template, 
                   markers, roi, line_type, window = 5):
        w, h = template.shape[::-1]
        img = np.zeros(gray.shape).astype(np.uint8)

        markers_cropped = markers[roi[1]:roi[3],
                                  roi[0]:roi[2]][top_left[1]:(top_left[1] + h),
                                                 top_left[0]:(top_left[0] + w)]
        # plt.imshow(markers_cropped)
        a, b = markers_cropped.shape
        #max value of midpoint of rectangle assumed in window neighbourhood as marker value
        mk_val =np.max(markers_cropped[int(a/2-window):int(a/2+window),
                                 int(b/2-window):int(b/2+window)])
        # print("mareker val", mk_val)
        img[markers==mk_val] = 255
        img = img[roi[1]:roi[3], roi[0]:roi[2]].copy()
        # cv2.imshow("img",img)
        img_cropped = img[top_left[1]:(top_left[1] + h),
                            top_left[0]:(top_left[0] + w)].copy()
        # gray_cropped2 = gray[roi[1]:roi[3], roi[0]:roi[2]].copy()
        # gray_cropped2 = gray_cropped2[top_left[1]:(top_left[1] + h),
        #                     top_left[0]:(top_left[0] + w)].copy()
    ##    img_filtered = cv2.blur(img_cropped2,(5,5))
        # cv2.imshow("img_cropped",img_cropped)
        img_edges = cv2.Canny(img_cropped,50,90,apertureSize = 3)
        # cv2.imshow("img_edges",img_edges)
        lines = cv2.HoughLinesP(img_edges,1,np.pi/180,30,
                                minLineLength=50,maxLineGap=200)
        if lines is None:
            print("no line")
            return 0,gray_cropped
        else:
            # #draw all lines
            # for line in lines:
            #     x1,y1,x2,y2 = line[0]
            #     cv2.line(gray_cropped2,(x1,y1),(x2,y2),(255,255,255),2)
            #     cv2.imshow('all lines', gray_cropped2)
            #     print("length", math.hypot(x2-x1,y2-y1))
            
            if line_type == "Longest":
                #draw longest line (optional)
                line_sorted = sorted(lines, key=lambda x:math.hypot(x[0][2]-x[0][0],x[0][3]-x[0][1]),
                                      reverse = True)
                x1,y1,x2,y2 = line_sorted[0][0]
                line_len = math.hypot(x2-x1,y2-y1)
                line_fit = [(x2-x1)/line_len, (y2-y1)/line_len, x1, y1]
            elif line_type == "Shortest":
                #draw longest line (optional)
                line_sorted = sorted(lines, key=lambda x:math.hypot(x[0][2]-x[0][0],x[0][3]-x[0][1]),
                                      reverse = False)
                x1,y1,x2,y2 = line_sorted[0][0]
                line_len = math.hypot(x2-x1,y2-y1)
                line_fit = [(x2-x1)/line_len, (y2-y1)/line_len, x1, y1]
            elif line_type == "Top most":
                #draw topmost line
                line_sorted = sorted(lines, key=lambda x:(x[0][3]-x[0][1])/2,reverse = True)
                x1,y1,x2,y2 = line_sorted[0][0]
                line_len = math.hypot(x2-x1,y2-y1)
                line_fit = [(x2-x1)/line_len, (y2-y1)/line_len, x1, y1]
            elif line_type == "Bottom most":
                #draw topmost line
                line_sorted = sorted(lines, key=lambda x:(x[0][3]-x[0][1])/2,reverse = False)
                x1,y1,x2,y2 = line_sorted[0][0]
                line_len = math.hypot(x2-x1,y2-y1)
                line_fit = [(x2-x1)/line_len, (y2-y1)/line_len, x1, y1]
            elif line_type == "Best fit":            
                #get best fit line   
                line_pts = [(x[0][0],x[0][1]) for x in lines] + \
                           [(x[0][2],x[0][3]) for x in lines]
                line_fit = cv2.fitLine(np.float32(line_pts),cv2.DIST_L2,0,0.01,0.01)
        
            x1 = int(-100*line_fit[0]+line_fit[2])
            y1 = int(-100*line_fit[1]+line_fit[3])
            x2 = int(100*line_fit[0]+line_fit[2])
            y2 = int(100*line_fit[1]+line_fit[3])
            cv2.line(gray_cropped,(top_left[0]+x1,top_left[1]+y1),
                    (top_left[0]+x2,top_left[1]+y2),
                    (255,255,255),2)
    
            slope = np.rad2deg(np.arctan((y2-y1)/(x2-x1)))
    
            return slope, gray_cropped
            
    def findTemplate(self, img, template, method):
        w, h = template.shape[::-1]
        # Apply template Matching
    ##    method = eval(methods[5])
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        return top_left,bottom_right
    
    ##    cv2.imshow('gray0', gray_cropped2) 
    
    
    ##img = cv2.imread('data\side view3.png',0)
    ##img2 = img.copy()
    #choose template
    def selectTemplate(self, frame):
        frame_dup = frame.copy()
        roiCorners = drawroi.roi_dry("Frame", frame_dup)
        drawroi.trigger = 0 
        drawroi.pts = []
        xmin = min(roiCorners[:, 0])
        xmax = max(roiCorners[:, 0])
        ymin = min(roiCorners[:, 1])
        ymax = max(roiCorners[:, 1])
        roi = [xmin, ymin, xmax, ymax]
        template = cv2.cvtColor(frame[roi[1]:roi[3], roi[0]:roi[2]].copy(), 
                                cv2.COLOR_BGR2GRAY)
        # print(template.shape)
        w, h = template.shape[::-1]
        return template, w, h
        
    def main(self):
        # template1 = cv2.imread('C:/Users/adwait/Desktop/Python/data/side view pad.png',0)
        # template2 = cv2.imread('C:/Users/adwait/Desktop/Python/data/side view reflection.png',0)
        # w1, h1 = template1.shape[::-1]
        # w2, h2 = template2.shape[::-1]
        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        
        roi = [300,150,500,350] #(xmin, ymin, xmax, ymax)
        # roi = [300,0,500,500]
        filepath = 'C:/Users/adwait/Desktop/Python/data/sample data set/Basler_acA1300-200um__21927848__20200309_175055809.avi'
        cap = cv2.VideoCapture(filepath)
        ret, frame = cap.read()
        template1, w1, h1 = self.selectTemplate(frame) # Top
        template2, w2, h2 = self.selectTemplate(frame) # Bottom
        # cv2.imshow("new template", template3)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            gray_cropped = gray[roi[1]:roi[3], roi[0]:roi[2]].copy()
            #cv2.imshow('raw', gray)
            #[150:350,300:500]
            # frame_cropped = frame.copy()
            img = gray_cropped.copy()
        
            # cv2.waitKey(0) #slow down
            
            if cv2.waitKey(1) == ord('q'):
                break
        
            #watershed algorithm             
            # temp = ImageSegment()
            thresh = self.binarize(gray, "Global", 58,2, True)
            markers,sure_fg,sure_bg = self.watershed(frame, thresh, 
                                                     True, 10, 36)
            # cv2.imshow('sure_fg', sure_fg)
            # cv2.imshow('sure_bg', sure_bg)
        
            # plt.imshow(markers)
            frame[markers==-1] = [255,0,0]
            
            cv2.imshow("markers", cv2.normalize(markers[roi[1]:roi[3], roi[0]:roi[2]],0,255,
                                                cv2.NORM_MINMAX, dtype=cv2.CV_32F))
            
            # Apply template Matching
            top_left1, bottom_right1 = self.findTemplate(img, template1, eval(methods[5]))
            top_left2, bottom_right2 = self.findTemplate(img, template2, eval(methods[5]))
            cv2.imshow('detected', img)
        
            # Detect representative line
            angle1, gray_cropped = self.detectLine(top_left1,gray,gray_cropped,
                                                   template1,markers,roi, "Bottom most")
            angle2, gray_cropped = self.detectLine(top_left2,gray,gray_cropped,
                                                    template2,markers,roi, "Top most")
            # print("angles", angle1, angle2)
            print("angle", abs((angle1-angle2)/2))
        
            cv2.imshow('final line', gray_cropped) 
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

test = TemplateMatch()
test.main()