# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:15:40 2020

@author: adwait
"""
# import sys
import cv2
import numpy as np
import math, statistics

#remove comment to run the code standalone
# sys.path.append('C:/Users/adwait/Desktop/Python/AdheSee') 

# from source.process.imagesegment import ImageSegment
import source.app.drawroi as drawroi

class TemplateMatch:
    
    def detectLine(self, label, top_left, frame, gray, markers, template, 
                   line_type, window = 5,
                   line_thresh = 30, line_length = 50, line_gap = 200,
                   line_color = (255,255,255), show_edge = False, show_lines = False):
        w, h = template.shape[::-1]
        img = np.zeros(gray.shape).astype(np.uint8)

        markers_cropped = markers[top_left[1]:(top_left[1] + h),
                                                 top_left[0]:(top_left[0] + w)]
        # plt.imshow(markers_cropped)
        a, b = markers_cropped.shape
        #median value of midpoint of rectangle assumed in window neighbourhood as marker value
        mk_val = statistics.median(markers_cropped[int(a/2-window):int(a/2+window),
                                                   int(b/2-window):int(b/2+window)].flatten())
        # print("mareker val", mk_val)
        img[markers==mk_val] = 255
        # cv2.imshow("img",img)
        img_cropped = img[top_left[1]:(top_left[1] + h),
                            top_left[0]:(top_left[0] + w)].copy()

        img_edges = cv2.Canny(img_cropped,100,200)
        
        if show_edge == True:
            cv2.imshow(label + ":Edges",img_edges)
        else:
            cv2.destroyWindow(label + ":Edges")
        
        lines = cv2.HoughLinesP(img_edges,1,np.pi/180,line_thresh,
                                minLineLength = line_length,
                                maxLineGap = line_gap)
        if lines is None:
            print("no line")
            return 0,[0,0,0,0],frame
        else:
            if show_lines == True:
                #draw all lines
                frame_cropped = frame[top_left[1]:(top_left[1] + h),
                                    top_left[0]:(top_left[0] + w)].copy()

                for line in lines:
                    x1,y1,x2,y2 = line[0]
                    cv2.line(frame_cropped,(x1,y1),(x2,y2),(100,100,255),2)
                cv2.imshow(label + ":Lines", frame_cropped)
            else:
                cv2.destroyWindow(label + ":Lines")
            
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
                line_sorted = sorted(lines, key=lambda x:(x[0][3]+x[0][1])/2,reverse = False)
                x1,y1,x2,y2 = line_sorted[0][0]
                line_len = math.hypot(x2-x1,y2-y1)
                line_fit = [(x2-x1)/line_len, (y2-y1)/line_len, x1, y1]
            elif line_type == "Bottom most":
                #draw topmost line
                line_sorted = sorted(lines, key=lambda x:(x[0][3]+x[0][1])/2,reverse = True)
                x1,y1,x2,y2 = line_sorted[0][0]
                line_len = math.hypot(x2-x1,y2-y1)
                line_fit = [(x2-x1)/line_len, (y2-y1)/line_len, x1, y1]
            elif line_type == "Best fit":            
                #get best fit line   
                line_pts = [(x[0][0],x[0][1]) for x in lines] + \
                           [(x[0][2],x[0][3]) for x in lines]
                line_fit = cv2.fitLine(np.float32(line_pts),cv2.DIST_L2,0,0.01,0.01)
            
            ax1 = int(-100*line_fit[0]+line_fit[2])
            ay1 = int(-100*line_fit[1]+line_fit[3])
            ax2 = int(100*line_fit[0]+line_fit[2])
            ay2 = int(100*line_fit[1]+line_fit[3])
            cv2.line(frame,(top_left[0]+ax1,top_left[1]+ay1),
                    (top_left[0]+ax2,top_left[1]+ay2),
                    line_color,2)
            
            line_endpoints = [x1,y1,x2,y2] if line_type != "Best fit" else [ax1,ay1,ax2,ay2]
            
            #get slope in degrees
            if ax1 == ax2:
                slope = 90
            else:
                slope = np.rad2deg(np.arctan((ay2-ay1)/(ax2-ax1)))
            
            print(slope, line_endpoints, frame)
            return slope, line_endpoints, frame
            
    def findTemplate(self, frame, gray, template, method, 
                     line_color = (255,255,255)):
        w, h = template.shape[::-1]
        # Apply template Matching
    ##    method = eval(methods[5])
        res = cv2.matchTemplate(gray,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame,top_left, bottom_right, line_color, 2)
        return top_left,bottom_right
    

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
        
    def measureAngle(self, label, frame, gray, markers, template,
                     line_type, window = 5,
                     line_thresh = 30, line_length = 50, line_gap = 200,
                     line_color = (255,255,255), show_edge = False, show_lines = False):
        
        # Apply template Matching
        top_left, bottom_right = self.findTemplate(frame, gray,
                                                     template, 
                                                     cv2.TM_SQDIFF_NORMED,
                                                     line_color)

        # cv2.imshow('detected', gray_cropped)
    
        # Detect representative line
        angle, line_endpoints, frame = self.detectLine(label, top_left,frame,gray,
                                               markers,template, line_type,
                                               window,
                                               line_thresh, line_length, 
                                               line_gap, line_color, show_edge,
                                               show_lines)

    
        # cv2.imshow('final line', gray_cropped) 
        return frame, angle, line_endpoints

    def getMarkers(self, frame, tresh_type, tresh_size, 
                 tresh_cst = 0, invert = True, morph = False,
                  morph_type = "Erosion", morph_size = 5, morph_iter = 1,
                 dist_trans=True, k_size=10, dist_fr=36, segment = False,
                 show_fg = False, show_bg = False, show_segment = False): #segment image and find markers
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #watershed algorithm (inherited from ImageSegment class)            
        thresh = self.binarize(gray, tresh_type, tresh_size,tresh_cst,invert,
                               morph, morph_type, morph_size, morph_iter)
        markers,markers_colored,sure_fg,sure_bg = self.watershed(frame, thresh,
                                                                 dist_trans, k_size, 
                                                                 dist_fr)
        
        if self.segment == True:
            self.displayWatershed(markers_colored, sure_fg, sure_bg)
        
        # markers_norm = markers.copy()
        # markers_norm[markers == -1] = 0
        # markers_norm = np.uint8(markers_norm*255/markers_norm.max())
        # markers_colored = cv2.applyColorMap(markers_norm, cv2.COLORMAP_VIRIDIS)                                    
        # cv2.imshow("markers_norm", markers_norm)
        
        return gray, markers, thresh, markers_colored
