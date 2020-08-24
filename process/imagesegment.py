# -*- coding: utf-8 -*-
"""
Created on Sat May  4 11:56:24 2019

@author: adwait
"""

import cv2
import numpy as np
# import matplotlib.pyplot as plt
import source.app.drawroi as drawroi
import source.process.imagetransform as imagetransform
import time
import statistics

class ImageSegment:
    
    #binarize frame by image thresholding
    def binarize(self, frame_gray, tresh_type, tresh_size, 
                 tresh_cst = 0, invert = False, morph = False,
                  morph_type = "Erosion", morph_size = 5, morph_iter = 1):
        # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
        elif tresh_type == "Canny":
                frame_bin = cv2.Canny(frame_gray, tresh_size, tresh_cst, 
                                      L2gradient = False)
            
        if invert == True:
            frame_bin = cv2.bitwise_not(frame_bin)
        
        if morph == True:
            frame_bin = self.morphTransform(frame_bin, morph_type, 
                                            morph_size, morph_iter)
        return frame_bin
    
    #apply morphological transformations
    def morphTransform(self, frame_bin, morph_type, k_size, n_iter):
        
        kernel = np.ones((k_size,k_size),np.uint8)
        if morph_type == 'Erosion':
            frame_morphed = cv2.erode(frame_bin, kernel,iterations = n_iter)
        elif morph_type == 'Dilation':
            frame_morphed = cv2.dilate(frame_bin, kernel,iterations = n_iter)
        elif morph_type == 'Opening':
            frame_morphed = cv2.morphologyEx(frame_bin, cv2.MORPH_OPEN, 
                                       kernel,iterations = n_iter)
        elif morph_type == 'Closing':
            frame_morphed = cv2.morphologyEx(frame_bin, cv2.MORPH_CLOSE, 
                                       kernel,iterations = n_iter)
        elif morph_type == 'Gradient':
            frame_morphed = cv2.morphologyEx(frame_bin, cv2.MORPH_GRADIENT, 
                                       kernel,iterations = n_iter)
        elif morph_type == 'Top Hat':
            frame_morphed = cv2.morphologyEx(frame_bin, cv2.MORPH_TOPHAT, 
                                       kernel,iterations = n_iter)
        elif morph_type == 'Black Hat':
            frame_morphed = cv2.morphologyEx(frame_bin, cv2.MORPH_BLACKHAT, 
                                       kernel,iterations = n_iter)
        return frame_morphed
    
    
    def getContours(self, tresh_type, tresh_size, tresh_cst, invert,
                    morph, morph_type, morph_size, morph_iter,
                    resize_factor = 1, dist_trans= False, seg_bg = 3, 
                    seg_fg = 3, min_area = 25, max_area = 1000000):
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
        # frame_cropped = self.frame[roi[1]:roi[3], roi[0]:roi[2]].copy()
        frame_current = self.frame_current[roi[1]:roi[3], roi[0]:roi[2]].copy()
        frame_contour = self.frame_contour.copy()
        
        print(self.frame.shape)

           
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        print("gray", time.time() * 1000)

        # if tresh_type == "Global":
        #     ret, frame_bin = cv2.threshold(frame_gray, tresh_size, 255, cv2.THRESH_BINARY)
        # elif tresh_type == "Adaptive":
        #     frame_bin = cv2.adaptiveThreshold(frame_gray, 255, 
        #                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                   cv2.THRESH_BINARY, tresh_size, tresh_cst)
        # elif tresh_type == "Otsu":
        #     ret, frame_bin = cv2.threshold(frame_gray, 0, 255,
        #                                    cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     
        frame_bin = self.binarize(frame_gray, tresh_type, tresh_size, 
                                  tresh_cst, invert, morph, morph_type, 
                                  morph_size, morph_iter)
        
        print("treshold", time.time() * 1000)
        
        if self.roi_auto == True:
            # Detect ROI automatically

            print(self.tresh_size_roi, self.tresh_cst_roi, self.roi_tresh_type)
            frame_gray_roi = cv2.cvtColor(frame_current, cv2.COLOR_BGR2GRAY) #grayscale

            #bg subtract
            if self.bg_roi_apply == True:
                kernal = (self.bg_blur_size_roi, self.bg_blur_size_roi)
                frame_bg_roi = cv2.blur(frame_gray_roi, kernal)
                frame_subtracted_roi = imagetransform.backgroundSubtract(frame_gray_roi, frame_bg_roi,
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

            self.roiAutoFlag = 'Auto'

        else:
            self.roiAutoFlag = 'Manual'
            frame_bin_roi = np.empty(frame_bin.shape, dtype=np.uint8)

        self.frame_bin_roi_full = np.zeros(frame_bin_roi.shape, dtype=np.uint8)

        print("contours", time.time() * 1000)

        mask1 = np.zeros(frame_bin.shape, dtype=np.uint8)

        
        mask_full = 255*np.ones(frame_bin.shape, dtype=np.uint8)
        print(mask_full.shape)
        
        self.areaDict = {} #area of contours calculated by pixel counting
        cpt = {}
        ellipse = {}
        if self.segment == True:
            sure_fg = np.zeros(frame_bin.shape, dtype=np.uint8)
            sure_bg = np.zeros(frame_bin.shape, dtype=np.uint8)
            # segm = np.zeros(frame_bin.shape, dtype=np.uint8)
        
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
                frame_contour, cpt[k], contours, fg, bg, mk = \
                    self.segmentWatershed(k, frame_current, frame_contour, frame_masked, 
                                      min_area, max_area, dist_trans, seg_bg, seg_fg)
                sure_fg = cv2.bitwise_or(sure_fg, fg)
                sure_bg = cv2.bitwise_or(sure_bg, bg)
                # segm = cv2.bitwise_or(segm, mk.astype(np.uint8))          
            else: #get contours by findContours function
                contours, hierarchy = cv2.findContours(frame_masked, cv2.RETR_TREE,
                                                        cv2.CHAIN_APPROX_SIMPLE)
                frame_contour, cpt[k], contours = self.segmentContour(k, frame_contour,
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
            self.displayWatershed(mk, sure_fg, sure_bg)

                
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
                frame_roi_wet, roiCornersAuto = drawroi.roi_wet(frame_bin_roi_masked,
                                                      self.epsilon_fraction,
                                                      self.roi_min_area,
                                                      self.roi_hull,
                                                      self.combine_roi,
                                                        self.roi_morph, self.x_roi_morph,
                                                                      self.y_roi_morph)
            else:
                frame_roi_wet, roiCornersAuto = drawroi.roi_wet(frame_bin_roi,
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

    #apply watershed algorithm
    def watershed(self, frame, frame_bin, dist_trans=False, k_size=3, dist_fr=3):
        
        kernel = np.ones((k_size,k_size),np.uint8)
        # sure background area
        sure_bg = cv2.dilate(frame_bin,kernel)
        
        # Finding sure foreground area
        if dist_trans == True:
            dist_transform = cv2.distanceTransform(frame_bin,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform, (dist_fr/100)*dist_transform.max(),
                                          255,0)
        else:
            k_size2 = dist_fr
            kernel = np.ones((k_size2,k_size2),np.uint8)
            sure_fg = cv2.erode(frame_bin,kernel)
        
        
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        
        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1
        
        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0
        
        markers = cv2.watershed(frame,markers)
        
        markers_norm = markers.copy()
        markers_norm[markers == -1] = 0
        markers_norm = np.uint8(markers_norm*255/markers_norm.max())
        markers_colored = cv2.applyColorMap(markers_norm, cv2.COLORMAP_VIRIDIS)
        # plt.imshow(markers)
        return markers, markers_colored, sure_fg, sure_bg
    
    #display foreground/background or markers  of watershed segmentation
    def displayWatershed(self, markers, sure_fg, sure_bg):
        
        if self.show_fg == True:
            cv2.imshow("Sure Foreground", sure_fg)
        else:
            cv2.destroyWindow("Sure Foreground")
        if self.show_bg == True:
            cv2.imshow("Sure Background", sure_bg)
        else:
            cv2.destroyWindow("Sure Background")
        if self.show_segment == True:
            # # cv2.imshow("Segmented", segm)
            # plt.imshow(markers)
            # plt.pause(0.05)
            # plt.draw()
            # plt.show()
            # markers_norm = markers.copy()
            # markers_norm[markers == -1] = 0
            # markers_norm = np.uint8(markers_norm*255/markers_norm.max())
            # markers_colored = cv2.applyColorMap(markers_norm, cv2.COLORMAP_VIRIDIS)
            cv2.imshow("Segments", markers)
        else:
            # plt.close()
            cv2.destroyWindow("Segments")
    
    
    #image segmentation by watershed algorithm and contour analysis
    def segmentWatershed(self, key, frame, frame_contour, frame_bin, 
                     min_area, max_area, dist_trans,  k_size, dist_fr):

        markers, markers_colored, sure_fg, sure_bg = self.watershed(frame, frame_bin, 
                                                                    dist_trans, 
                                                                    k_size, dist_fr)
        
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
        return frame_contour, cpt, contours, sure_fg, sure_bg, markers_colored     

    #Contour analysis from inbuilt contour property functions
    def segmentContour(self, key, frame, frame_masked, contours, min_area, max_area): 
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
        
        # print('Contact Area: ', totalArea)    
        # print ('Number of contours:', contourNumber)
        # print ('ROI Area:', roiArea)
        
        print("area plot", time.time() * 1000)
        
        return frame_contour, cpt, contours