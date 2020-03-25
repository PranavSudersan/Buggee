# -*- coding: utf-8 -*-
"""
Created on Sat May  4 11:56:24 2019

@author: adwait
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import draw_roi
import time
import statistics

class Effects:
    
##    def __init__(self, frame, roi_corners): #constructor
##        self.frame = frame
####        self.frame_bg = frame_bg
####        self.ms_type = ms_type
##        self.roi_corners = roi_corners
    #ms_type = 'Dry' #set as 'Dry' or 'Wet' depending on image
    #filename = 'dry pad.png'
    #frame = cv2.imread(filename)
    #if ms_type == 'Dry':
    #    #Create ROI manually
    #    roi_corners = roi_dry(frame) #draw ROI manually

    def getContours(self, tresh_type, tresh_size, tresh_cst = 0, 
                    resize_factor = 1, seg_fg = 0.7, seg_bg = 3,
                    min_area = 25, max_area = 1000000):
    #    global filename, ms_type, roi_corners
    #    frame = cv2.imread(filename)
        print("getContours")
        if self.frame is None:
            print('Error loading image')
            exit()
        print("start", time.time() * 1000)
        
##        if self.subtract == True: #bg subtract flag
##            self.bgSubtract()
            
##        if self.ms_type == 'Dry':
##            roi = self.roiBoundingRectangle() #(xmin, ymin, xmax, ymax)
        roi = self.roiBound
        print("roi", roi)
        frame_cropped = self.frame[roi[1]:roi[3], roi[0]:roi[2]].copy()
        frame_current = self.frame_current[roi[1]:roi[3], roi[0]:roi[2]].copy()
        frame_contour = self.frame_contour.copy()
        
        print(self.frame.shape, frame_cropped.shape)

           
        frame_gray = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2GRAY)
        print("gray", time.time() * 1000)

        if tresh_type == "Global":
            ret, frame_bin = cv2.threshold(frame_gray, tresh_size, 255, cv2.THRESH_BINARY)
        elif tresh_type == "Adaptive":
            frame_bin = cv2.adaptiveThreshold(frame_gray, 255, 
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, tresh_size, tresh_cst)
        elif tresh_type == "Otsu":
            ret, frame_bin = cv2.threshold(frame_gray, 0, 255,
                                           cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     
        print("treshold", time.time() * 1000)
        
    #    if subtract == True:
    #        frame_bg = cv2.adaptiveThreshold(frame_bg, 255, 
    #                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                      cv2.THRESH_BINARY, tresh_size, 1)
    #        frame_bin = bg_subtract(frame_bin, frame_bg)
        
        if self.roi_auto == True:
            # Detect ROI automatically

            print(self.tresh_size_roi, self.tresh_cst_roi, self.roi_tresh_type)
            frame_gray_roi = cv2.cvtColor(frame_current, cv2.COLOR_BGR2GRAY) #grayscale

            #bg subtract
            if self.bg_roi_apply == True:
                kernal = (self.bg_blur_size_roi, self.bg_blur_size_roi)
                frame_bg_roi = cv2.blur(frame_gray_roi, kernal)
                frame_subtracted_roi = self.backgroundSubtract(frame_gray_roi, frame_bg_roi,
                                                     self.bg_blend_roi, inv = True)
            else:
                frame_subtracted_roi = frame_gray_roi
            #blur
            frame_blur_roi = cv2.blur(frame_subtracted_roi,(self.blur_size_roi,self.blur_size_roi))

            #threshold
            if self.roi_tresh_type == "Global":
                ret, frame_bin_roi = cv2.threshold(frame_blur_roi, self.tresh_size_roi, 255, cv2.THRESH_BINARY)
            elif self.roi_tresh_type == "Adaptive":
                frame_bin_roi = cv2.adaptiveThreshold(frame_blur_roi, 255, 
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY,
                                                       self.tresh_size_roi, self.tresh_cst_roi)
            elif self.roi_tresh_type == "Otsu":
                ret, frame_bin_roi = cv2.threshold(frame_blur_roi, 0, 255,
                                           cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            elif self.roi_tresh_type == "Canny":
                frame_bin_roi = cv2.Canny(frame_blur_roi, self.tresh_size_roi,
                                               self.tresh_cst_roi, L2gradient = False)
            
##            #find and clean contours
##            contours_wet, hierarchy_edge = cv2.findContours(frame_bin_thresh, cv2.RETR_EXTERNAL, 
##                                               cv2.CHAIN_APPROX_SIMPLE)
##            i = 0
##            j = 0
##            print("length", len(contours_wet))
##            if len(contours_wet) != 0:
##                while i - j <= len(contours_wet) - 1:
##                    a = cv2.contourArea(contours_wet[i-j])
##                    if a < self.roi_min_area: #fill small areas                        
##                        cv2.drawContours(frame_bin_thresh, [contours_wet[i-j]],
##                                         -1, (0,0,0), -1)
##                        del contours_wet[i-j]
##                        print(i,j)
##                        j += 1 #count small areas
##                        i += 1
##                        continue
##                    i += 1
##
##            #morph roi
##            if self.roi_morph == True:
##                rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.x_roi_morph, self.y_roi_morph))
##                self.frame_bin_roi = cv2.morphologyEx(frame_bin_thresh, cv2.MORPH_CLOSE, rect_kernel)
##            else:
##                self.frame_bin_roi = frame_bin_thresh
##            self.roiCornersAuto = draw_roi.roi_wet(self.frame_bin_roi, self.epsilon_fraction)
            self.roiAutoFlag = 'Auto'
##
##            print("auto roi", time.time() * 1000)
##            mask_roi_auto = 255*np.ones(frame_bin.shape, dtype=np.uint8)
##            self.roiCornersAuto = self.resizeContour(self.roiCornersAuto,
##                                                     resize_factor)
##            cv2.fillPoly(mask_roi_auto, [self.roiCornersAuto], 0)
        else:
            self.roiAutoFlag = 'Manual'
            frame_bin_roi = np.empty(frame_bin.shape, dtype=np.uint8)
##            self.roiCornersAuto = None
##            mask_roi_auto = np.zeros(frame_bin.shape, dtype=np.uint8)
        self.frame_bin_roi_full = np.zeros(frame_bin_roi.shape, dtype=np.uint8)
##        cv2.drawContours(frame_contour, [self.roiCornersNew], -1, (0,0,255), 2)
        print("contours", time.time() * 1000)
##        mask1 = 255*np.ones(frame_bin.shape, dtype=np.uint8)
        mask1 = np.zeros(frame_bin.shape, dtype=np.uint8)

##        cv2.fillPoly(mask1, [self.roiDict["Default"][0]], 0)
        
        mask_full = 255*np.ones(frame_bin.shape, dtype=np.uint8)
        print(mask_full.shape)
        
##        if self.roi_auto == True:
##            mask_roi_auto = 255*np.ones(frame_bin.shape, dtype=np.uint8)
##            self.roiCornersAuto = self.resizeContour(self.roiCornersAuto,
##                                                     resize_factor)
##            cv2.fillPoly(mask_roi_auto, [self.roiCornersAuto], 0)
##        else:
##            mask_roi_auto = np.zeros(frame_bin.shape, dtype=np.uint8)
        self.areaDict = {} #area of contours calculated by pixel counting
        cpt = {}
        ellipse = {}
        if self.segment == True:
            sure_fg = np.zeros(frame_bin.shape, dtype=np.uint8)
            sure_bg = np.zeros(frame_bin.shape, dtype=np.uint8)
            segm = np.zeros(frame_bin.shape, dtype=np.uint8)
        
        for k in self.roiDict.keys():
            print(k) 
            if len(self.roiDict.keys()) > 1 and k == "Default": #skip full when roi added
                continue
            mask2 = 255*np.ones(frame_bin.shape, dtype=np.uint8)
            cv2.fillPoly(mask2, [self.roiDict[k][3]], 0)
            mask = cv2.bitwise_or(mask1, mask2)
            self.roiDict[k][4], mask_roi_auto = self.getAutoROI(frame_bin_roi,
                                                                mask, resize_factor)
            mask3 = cv2.bitwise_or(mask, mask_roi_auto)
            print("mask", time.time() * 1000)
            frame_masked = cv2.bitwise_or(frame_bin, mask3)
            frame_masked = cv2.bitwise_not(frame_masked)
            print("bitwise", time.time() * 1000)
            mask_full = cv2.bitwise_and(mask_full, mask3)

            # get actual roi area by coounting pixels (contour area, roi area)
            self.areaDict[k] = [np.count_nonzero(mask_roi_auto==0)]
            
            if self.segment == True:  #get segmented contours boundary by watershed algorithm
                frame_contour, cpt[k], contours, fg, bg, sg = \
                    self.imageSegment(k, frame_current, frame_contour, frame_masked, 
                                      min_area, max_area, seg_bg, seg_fg)
                sure_fg = cv2.bitwise_or(sure_fg, fg)
                sure_bg = cv2.bitwise_or(sure_bg, bg)
                segm = cv2.bitwise_or(segm, sg)          
            else: #get contours by finContours function
                contours, hierarchy = cv2.findContours(frame_masked, cv2.RETR_TREE,
                                                        cv2.CHAIN_APPROX_SIMPLE)
                frame_contour, cpt[k], contours = self.contourProperty(k, frame_contour,
                                                                       frame_masked, contours,
                                                                       min_area, max_area)
            # cv2.imshow("Masked", frame_masked)
            if len(contours) > 0: # 1 point needed to stack
                cont_comb = np.vstack(contours)
                if len(cont_comb) > 4: # min 5 points needed to fit ellipse
                    elps = cv2.fitEllipse(cont_comb) #fit and draw bounding ellipse
                    cv2.ellipse(frame_contour, elps,(51,255,255),2)
                else:
                    elps = ((0,0),(0,0),0,1)
            else:
                elps = ((0,0),(0,0),0,1)
            ellipse[k] = list(elps) + [self.calibFactor] #ellipse center, axis, angle, length calibration

        frame_masked = cv2.bitwise_or(frame_bin, mask_full)
        
        if self.segment == True:
            if self.show_fg == True:
                cv2.imshow("Sure Foreground", sure_fg)
            else:
                cv2.destroyWindow("Sure Foreground")
            if self.show_bg == True:
                cv2.imshow("Sure Background", sure_bg)
            else:
                cv2.destroyWindow("Sure Background")
            if self.show_segment == True:
                # cv2.imshow("Segmented", segm)
                plt.imshow(segm)
                plt.pause(0.05)
                plt.draw()
                plt.show()
            else:
                # plt.clf()
                plt.close()

                
##        frame_masked = cv2.bitwise_not(frame_masked)
        print("find contours", time.time() * 1000)
##        cv2.drawContours(frame_contour, self.contours, -1, (0,255,0), 1)

        print("window show", time.time() * 1000)

##        frame_masked = cv2.bitwise_not(frame_masked)
        return frame_bin, frame_masked, frame_contour, cpt, ellipse

    def getAutoROI(self, frame_bin_roi, mask, resize_factor): #get auto roi and corresponding mask
        if self.roi_auto == True:
            # Detect ROI automatically
            print(self.tresh_size_roi, self.tresh_cst_roi, self.roi_tresh_type)

##            if self.roi_tresh_type == "Global":
##                ret, frame_bin_roi = cv2.threshold(frame_gray, self.tresh_size_roi, 255, cv2.THRESH_BINARY)
##            elif self.roi_tresh_type == "Adaptive":
##                frame_bin_roi = cv2.adaptiveThreshold(frame_gray, 255, 
##                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
##                                          cv2.THRESH_BINARY,
##                                                       self.tresh_size_roi, self.tresh_cst_roi)
##            elif self.roi_tresh_type == "Otsu":
##                ret, frame_bin_roi = cv2.threshold(frame_gray, 0, 255,
##                                           cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            if self.distinct_roi == True:
                mask_inv = cv2.bitwise_not(mask)
                frame_bin_roi_masked = cv2.bitwise_and(mask_inv, frame_bin_roi)                
                frame_roi_wet, roiCornersAuto = draw_roi.roi_wet(frame_bin_roi_masked,
                                                      self.epsilon_fraction,
                                                      self.roi_min_area,
                                                      self.roi_hull,
                                                      self.combine_roi,
                                                        self.roi_morph, self.x_roi_morph,
                                                                      self.y_roi_morph)
            else:
                frame_roi_wet, roiCornersAuto = draw_roi.roi_wet(frame_bin_roi,
                                                      self.epsilon_fraction,
                                                      self.roi_min_area,
                                                      self.roi_hull,
                                                      self.combine_roi,
                                                    self.roi_morph, self.x_roi_morph,
                                                                      self.y_roi_morph)
##            self.roiAutoFlag = 'Auto'

            print("auto roi", time.time() * 1000)
            mask_roi_auto = 255*np.ones(frame_bin_roi.shape, dtype=np.uint8)
            roiCornersAuto = self.resizeContour(roiCornersAuto,
                                                     resize_factor)
            cv2.fillPoly(mask_roi_auto, [roiCornersAuto], 0)
            self.frame_bin_roi_full = cv2.bitwise_or(self.frame_bin_roi_full, frame_roi_wet)
        else:
##            self.roiAutoFlag = 'Manual'
            roiCornersAuto = None
            mask_roi_auto = np.zeros(frame_bin_roi.shape, dtype=np.uint8)

        return roiCornersAuto, mask_roi_auto

    def resizeContour(self, contour, s_factor): #resize contour geometry
        contour_resized = contour.copy()
        M_init = cv2.moments(contour_resized)
        if M_init["m00"] == 0: #on error
            return contour
        cX_init = int(M_init["m10"] / M_init["m00"])
        cY_init = int(M_init["m01"] / M_init["m00"])
##            s_factor = 0.9
        contour_resized[:, :, 0] = contour_resized[:, :, 0] * s_factor
        contour_resized[:, :, 1] = contour_resized[:, :, 1] * s_factor
        M_final = cv2.moments(contour_resized)
        if M_final["m00"] == 0: #on error
            return contour
        cX_final = int(M_final["m10"] / M_final["m00"])
        cY_final = int(M_final["m01"] / M_final["m00"])
        cX_shift = cX_init - cX_final
        cY_shift = cY_init - cY_final
        contour_resized[:, :, 0] = contour_resized[:, :, 0] + cX_shift
        contour_resized[:, :, 1] = contour_resized[:, :, 1] + cY_shift
        contour_resized = contour_resized.astype(int)
        return contour_resized

    #image segmentation by watershed algorithm and contour analysis
    def imageSegment(self, key, frame, frame_contour, frame_bin, 
                     min_area, max_area, k_size=3, dist_fr=0.7):
        frame_seg = frame.copy()
        kernel = np.ones((k_size,k_size),np.uint8)
        # sure background area
        sure_bg = cv2.dilate(frame_bin,kernel)
        
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(frame_bin,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform, dist_fr*dist_transform.max(),
                                     255,0)
        
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        
        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1
        
        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0
        
        markers = cv2.watershed(frame_seg,markers)
        
        markers[:,0] = 1 #clean up borders
        markers[:,-1] = 1
        markers[0,:] = 1
        markers[-1,:] = 1
        
        # frame[markers == -1] = [255,0,0] #border color
        # frame_contour[np.logical_and(markers != -1,markers != 1)] = [0,255,0] #fill color
        
        contours = []
        areas = []
        length = []
        moments = []
        ecc = []
        i = 0
        # hierarchy = []        
        for label in np.unique(markers):
            if label in [0,1,-1]:
                continue       
            # Create a mask
            mask = np.zeros(frame_bin.shape, dtype="uint8")
            mask[markers == label] = 255
            a = np.count_nonzero(mask==255) #area
            if a < min_area or a > max_area: #ignore small/large areas
                # frame_bin[markers == label] = 0
                continue
            areas.append(a)
            
            frame_contour[markers == label] = [0,255,0] #fill color
            
            # Find contours of each segment
            cnts, hr = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
            # cnts = cnts[0]
            # cv2.drawContours(frame_seg, cnts, -1, (0,150,0), 1)#contour borders detected
            contours += cnts
            
            #combine incase of inner and outer boundaries (holes)
            cnts_comb = np.vstack(cnts[i] for i in range(len(cnts))) 
            
            l = 0
            for c in cnts:
                l += cv2.arcLength(c, True) #contour length
            length.append(l)
            
            m = cv2.moments(cnts_comb) #contour moments
            moments.append(m)
            
            if m['mu20']+m['mu02'] == 0:
                ec = None
                # self.contour_data[5].append(None)
                continue #error
            else:
                ec = abs((m['mu20']-m['mu02'])**2 - (4*m['mu11']**2))/ \
                    (m['mu20']+m['mu02'])**2
                #reference: http://breckon.eu/toby/teaching/dip/opencv/SimpleImageAnalysisbyMoments.pdf
            ecc.append(ec)
            
            # contour full data
            self.contour_data[0].append(self.framePos)#Frame no.
            self.contour_data[1].append(key) #ROI label
            self.contour_data[2].append(i) #contour id
            self.contour_data[3].append(a) #contour area
            self.contour_data[4].append(l) #contour length
            self.contour_data[5].append(ec) #contour eccentricity
            self.contour_data[6].append(m) #moments
            self.contour_data[7].append(cnts_comb.tolist()) #contour array
            
            i += 1
        
        # self.roiDict[key][2] = contours[0]
        if ecc == []:
            ecc = [-1] #avoid median calc error
        #areas.sort(reverse = True) # sort areas in descending order
        totalArea = sum(areas)
        # contourArea = self.areaDict[key][0]
        totalLength = sum(length)
        contourNumber = len(areas)
        if self.roiAutoFlag == 'Auto': #auto roi
            #roiArea = cv2.contourArea(self.roiDict[key][4])
            roiArea = self.areaDict[key][0]
            roiLength = cv2.arcLength(self.roiDict[key][4], True)
        else: #manual roi
            roiArea = cv2.contourArea(self.roiDict[key][3])
            roiLength = cv2.arcLength(self.roiDict[key][3], True)            
        eccavg = statistics.median(ecc) #avg eccentricity (median)
        
        
        cpt = (totalArea, totalLength, contourNumber, roiArea, roiLength, eccavg)
        
        # if len(contours) > 0:
            # contours = contours[0]
        cv2.drawContours(frame_contour, contours, -1, (150,150,0), 1) #draw borders           
        # else:
        #     contours = []
            
        
        # if self.show_fg == True:
        #     cv2.imshow("Sure Foreground: " + key, sure_fg)
        # else:
        #     cv2.destroyWindow("Sure Foreground: " + key)
        # if self.show_bg == True:
        #     cv2.imshow("Sure Background: " + key, sure_bg)
        # else:
        #     cv2.destroyWindow("Sure Background: " + key)
        # if self.show_segment == True:
        #     cv2.imshow("Segmented: " + key, markers.astype(np.uint8))
        # else:
        #     cv2.destroyWindow("Segmented: " + key)
        # cv2.imshow("frame", frame)
        # cv2.imshow("frame_seg", frame_seg)
        return frame_contour, cpt, contours, sure_fg, sure_bg, markers.astype(np.uint8)     

    #Contour analysis from inbuilt contour property functions
    def contourProperty(self, key, frame, frame_masked, contours, min_area, max_area): 
    #    contours, frame_bin, frame_masked, frame_contour = img_contour(tresh, frame, ms_type, roi_corners)
        #cv2.createTrackbar( "Treshold box size", "Frame", 415, 500, img_contour)
    #    cv2.waitKey(0)
        #tresh_size = cv2.getTrackbarPos("Treshold box size", "Frame")
        #contours = img_contour(tresh_size)
    #    cv2.destroyAllWindows()
        # contours = self.roiDict[key][2]
        frame_contour = frame.copy()
        areas = []
        length = []
        moments = []
        ecc = []
        i = 0
        j = 0
        n = len(contours)
        print("contour property", n)
        if len(contours) != 0:
            while i - j <= len(contours) - 1:
                a = cv2.contourArea(contours[i-j])
                if a < min_area or a > max_area: #ignore small/large areas
                    cv2.fillPoly(frame_masked, [contours[i-j]], 0)
                    del contours[i-j]
                    j += 1 #count small areas
                    i += 1
                    continue
                areas.append(a)
                
                l = cv2.arcLength(contours[i-j], True)
                length.append(l)
                #contour full data
                self.contour_data[0].append(self.framePos)#Frame no.
                self.contour_data[1].append(key) #ROI label
                self.contour_data[2].append(i-j) #contour id
                self.contour_data[3].append(a) #contour area
                self.contour_data[4].append(l) #contour length
                self.contour_data[7].append(contours[i-j].tolist()) #contour array
                
                m = cv2.moments(contours[i-j]) #contour moments
                moments.append(m)
                self.contour_data[6].append(m) #moments
                if m['mu20']+m['mu02'] == 0:
                    self.contour_data[5].append(None)
                    continue #error
                else:
                    ec = abs((m['mu20']-m['mu02'])**2 - (4*m['mu11']**2))/ \
                        (m['mu20']+m['mu02'])**2
                    #reference: http://breckon.eu/toby/teaching/dip/opencv/SimpleImageAnalysisbyMoments.pdf
                    ecc.append(ec)
                    self.contour_data[5].append(ec) #contour eccentricity
                i += 1
        print(n, j, len(contours))
        # self.roiDict[key][2] = contours
        if ecc == []:
            ecc = [-1] #avoid median calc error
        #areas.sort(reverse = True) # sort areas in descending order
        totalArea = sum(areas)
        contourArea = np.count_nonzero(frame_masked==255)
        totalLength = sum(length)
        contourNumber = len(areas)
        if self.roiAutoFlag == 'Auto': #auto roi
            #roiArea = cv2.contourArea(self.roiDict[key][4])
            roiArea = self.areaDict[key][0]
            roiLength = cv2.arcLength(self.roiDict[key][4], True)
        else: #manual roi
            roiArea = cv2.contourArea(self.roiDict[key][3])
            roiLength = cv2.arcLength(self.roiDict[key][3], True)            
        eccavg = statistics.median(ecc) #avg eccentricity (median)
    #    plt.hist(areas, normed=True, bins=100) #histogram of setae area
        
        cpt = (contourArea, totalLength, contourNumber, roiArea, roiLength, eccavg)
        cv2.drawContours(frame_contour, contours, -1, (0,255,0), -1) #draw contours
        
        print('Contact Area: ', totalArea)    
        print ('Number of contours:', contourNumber)
        print ('ROI Area:', roiArea)
        
        print("area plot", time.time() * 1000)
        
        return frame_contour, cpt, contours
   
    def backgroundSubtract(self, frame, frame_bg, alpha, inv = False): #subtract background
        print(frame.shape)
        if alpha == 1: #direct subtraction if alpha is one
            frame_fg = cv2.subtract(255-frame,255-frame_bg)
            frame_fg_scaled = 255 - frame_fg
        else: #blend
##            alpha = 0.5
            frame_fg_scaled  = cv2.addWeighted(frame, 1 - alpha, 255 - frame_bg,
                                              alpha, 0.0)
        frame_subtracted = 255 - frame_fg_scaled if inv == True else frame_fg_scaled
        print("bgSubtract")
        return frame_subtracted

    def applyBrightnessContrast(self, brightness = 0, contrast = 0, frame = None):
        
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow

            buf = cv2.addWeighted(frame, alpha_b, frame, 0, gamma_b)
        else:
            buf = frame.copy()

        if contrast != 0:
            f = 131*(contrast + 127)/(127*(131-contrast))
            alpha_c = f
            gamma_c = 127*(1-f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

##        self.frame = buf #CHECK
        print("brightness")
        return buf

##    def window_show(window_name, frame, posx, posy, resize_fraction):
##        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
##    #    sc = 0.5 #window resize scale factor
##        h, w = tuple(int(resize_fraction*x) for x in frame.shape[:2])    
##        cv2.moveWindow(window_name, posx, posy)
##        cv2.resizeWindow(window_name, w, h)
##        cv2.imshow(window_name, frame)
   

    def imageFilter(self, ftype, param1, param2, frame): #image filtering
        roi = self.roiBound
        frame1 = frame[roi[1]:roi[3], roi[0]:roi[2]].copy() #filter inside roi
##        frame_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
##        del frame1
        if ftype == "Average Filter":
            frame_filtered = cv2.blur(frame1,(param1,param1))
        elif ftype == "Gaussian Filter":
            frame_filtered = cv2.GaussianBlur(frame1,(param1,param1),param2)
        elif ftype == "Median Filter":
            frame_filtered = cv2.medianBlur(frame1,param1)
        elif ftype == "Bilateral Filter":
            frame_filtered = cv2.bilateralFilter(frame1,0,param1,param2)
        elif ftype == "Morph Open":
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (param1,param2))
            frame_filtered = cv2.morphologyEx(frame1, cv2.MORPH_OPEN, rect_kernel)
        elif ftype == "Morph Close":
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (param1,param2))
            frame_filtered = cv2.morphologyEx(frame1, cv2.MORPH_CLOSE, rect_kernel)
        else:
            frame_filtered = frame1.copy()

##        frame_filtered2 = cv2.cvtColor(frame_filtered.astype(np.uint8),
##                                    cv2.COLOR_GRAY2BGR)
        h, w, s  = frame.shape
        l, r, t, d = roi[0], w - roi[2], roi[1], h - roi[3]
        print(h, w, s, t, d, l, r)
        #fill border with zero to equalize frame size
        frame_filtered2 = cv2.copyMakeBorder(frame_filtered, t, d, l, r,
                                               cv2.BORDER_CONSTANT, 0)
        
        return frame_filtered2
            

    def dftFilter(self, r_lp, r_hp, frame): #DFT Filter (Gaussian Bandpass)
        mask_gauss, img_back, img_back_gauss, img_back_scaled, \
            img_filtered, magnitude_spectrum, spectrum_masked = (None,)*7
        #DFT
        #if frame == None:
        #   frame = self.frame
        print("dft init", self.roiBound)
        roi = self.roiBound
        print("roi")
        frame1 = frame[roi[1]:roi[3], roi[0]:roi[2]].copy()
        print("dft")
        frame_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        del frame1
        print(frame_gray.shape)

        dft = cv2.dft(np.float32(frame_gray),flags = cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)


        magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],
                                                     dft_shift[:,:,1]))
        rows, cols = frame_gray.shape
        crow,ccol = int(rows/2) , int(cols/2)
        print("low pass")
        #Low Pass
        kernal = cv2.getGaussianKernel(max(rows, cols), r_lp)
        kernal2d = kernal * kernal.transpose()
        kernal2d = kernal2d / kernal2d.max()
##        kernal2d_inverse = 1 - kernal2d

        mask_lowpass = np.zeros((rows,cols),np.float64)
        if r_lp > 0:
            mask_lowpass = kernal2d[int((max(rows, cols)-rows)/2):
            int((max(rows, cols)+rows)/2),int((max(rows, cols)-cols)/2):
                int((max(rows, cols)+cols)/2)] #image sizes must be even integer
        else:
            mask_lowpass = np.zeros((rows,cols),np.float64)
        print("high pass")
        #High Pass
        kernal = cv2.getGaussianKernel(max(rows, cols), r_hp)
        kernal2d = kernal * kernal.transpose()
        kernal2d = kernal2d / kernal2d.max()
        kernal2d_inverse = 1 - kernal2d

        mask_highpass = np.ones((rows,cols),np.float64)
        if r_hp > 0:
            mask_highpass = kernal2d_inverse[int((max(rows, cols)-rows)/2):
            int((max(rows, cols)+rows)/2),int((max(rows, cols)-cols)/2):
                int((max(rows, cols)+cols)/2)] #image sizes must be even integer
        else:
            mask_highpass = np.ones((rows,cols),np.float64)
        print("band pass")
        #Band Pass
        if r_hp <= r_lp and r_lp > 0:
            mask_gauss = mask_lowpass * mask_highpass
            mask_gauss = mask_gauss/mask_gauss.max()
        else:
            mask_gauss = np.zeros((rows,cols),np.float64)

        del mask_lowpass, mask_highpass, kernal, kernal2d, kernal2d_inverse
        
        #Inverse DFT
        fshift = dft_shift*np.expand_dims(mask_gauss, axis = 2)
        f_ishift = np.fft.ifftshift(fshift)
        del fshift

        img_back = cv2.idft(f_ishift)
        img_back_gauss = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
        print("img_back_gauss", img_back_gauss.shape)
        spectrum_masked = magnitude_spectrum * mask_gauss
##        img_back_scaled = None
        img_back_scaled = 255*img_back_gauss/img_back_gauss.max()
        img_filtered = cv2.cvtColor(img_back_scaled.astype(np.uint8),
                                    cv2.COLOR_GRAY2BGR)
        print("dft end")
        h, w, s  = frame.shape
        l, r, t, d = roi[0], w - roi[2], roi[1], h - roi[3]
        print(h, w, s, t, d, l, r)
        #fill border with zero to equalize frame size
        img_filtered1 = cv2.copyMakeBorder(img_filtered, t, d, l, r,
                                               cv2.BORDER_CONSTANT, 0)

        print(img_filtered.shape, img_filtered1.shape, frame.shape)
        return img_filtered1, spectrum_masked
        
