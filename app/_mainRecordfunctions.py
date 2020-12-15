# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 21:46:56 2020

@author: adwait
"""
import numpy as np
import cv2
from tkinter import messagebox, Tk
from PIL import ImageFont, ImageDraw, Image
from PyQt5.QtGui import QIcon
import logging

class MainRecordFunctions:
    
    def recordVideo(self, frame1, frame2):
        logging.debug("recordvideo")
        if self.forceData.force_filepath == "":
            start_framenum = -1
            end_framenum = -1
        else:
            # self.forceData.getArea(self.frameTime, self.dataDict)
            start_framenum = self.forceData.plot_slice2.start
            end_framenum = self.forceData.plot_slice2.stop + 1
        
        if self.recordStatus == True:
            if int(self.framePos) >= start_framenum:
                h , w = 1024, 1280
                # dim = (w, h)
                if frame2.ndim == 2:
                    frame2 = cv2.cvtColor(frame2, cv2.COLOR_GRAY2BGR)
                
    ##            if self.showContours.isChecked() == False:
    ##                roi = self.roiBound
    ##                self.merged_frame[:h, :w] = self.image_resize(frame1[roi[1]:roi[3],
    ##                                                              roi[0]:roi[2]],
    ##                                              w, h, inter = cv2.INTER_AREA)
    ##            else:
                
                self.merged_frame[:h, :w], scaleFactor = self.image_resize(frame1, w, h,
                                                                          inter = cv2.INTER_AREA)
                
                if self.configRecWindow.fourRec.isChecked() == True:
                    if self.forceData.force_filepath == "" or self.cap2 == None:
                        root = Tk()
                        root.withdraw()
                        messagebox.showinfo("Error!", "Check 2nd video file or force data file. Not found!")
                        root.destroy()
                        self.record_frame() #finish recording
                        self.playStatus = False #pause video
                        return
    ##                frame2 = cv2.cvtColor(self.frame_contours, cv2.COLOR_GRAY2BGR)
                    # frame2 = self.frame_contour.copy()
                    # ret, frame3 = self.cap2.read()
                    # self.forceData.getArea(self.frameTime, self.dataDict)
                    # self.forceData.plotData(self.lengthUnit.currentText()) #prepare plot
                    # frame4 = cv2.resize(cv2.cvtColor(self.forceData.convertPlot(), cv2.COLOR_RGB2BGR),
                    #                                       (w, h), interpolation = cv2.INTER_AREA)
                    
                    #only record till plot range. continue playing to get all data
                    if int(self.framePos) == end_framenum:
                    # if ret == False: #video at end
                        logging.debug("2nd video end")
                        self.cap2.release()
                        self.cap2 = None
                        self.record_frame() #finish recording
                        self.playStatus = True
                        return
                    else:
                        frame2 = self.frame_contour.copy()
                        ret, frame3 = self.cap2.read()
                        self.forceData.getArea(self.frameTime, self.dataDict)
                        # self.forceData.plotData(self.imageDataUnitDict) #prepare plot
                        self.forceData.plotImageAnimate(int(self.framePos))
                        frame4 = cv2.resize(cv2.cvtColor(self.forceData.convertPlot(), cv2.COLOR_RGB2BGR),
                                                              (w, h), interpolation = cv2.INTER_AREA)
                        framenumber1 = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                        framenumber2 = self.cap2.get(cv2.CAP_PROP_POS_FRAMES)
                        logging.debug('%s, %s, %s', "position", framenumber1, framenumber2)
                        if framenumber1 != framenumber2: #check both videos are in sync
                            root = Tk()
                            root.withdraw()
                            messagebox.showinfo("Error!", "Video frame numbers dont match!\n" +
                                                "Video-1 frame:\t" + str(framenumber1) + "\n" +
                                                "Video-2 frame:\t" + str(framenumber2))
                            root.destroy()
                            self.record_frame() #finish recording
                            self.playStatus = False #pause video
                            return
                        logging.debug('%s, %s, %s', "position", self.cap.get(cv2.CAP_PROP_POS_FRAMES),
                                      self.cap2.get(cv2.CAP_PROP_POS_FRAMES))
                        
                        self.merged_frame[:h, w:], r = self.image_resize(frame3, w, h,
                                                                  inter = cv2.INTER_AREA)
                        self.merged_frame[h:, :w], r = self.image_resize(frame2, w, h,
                                                                  inter = cv2.INTER_AREA)
                        self.merged_frame[h:, w:], r = self.image_resize(frame4, w, h,
                                                                  inter = cv2.INTER_AREA)
                        # Write video2 title
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        bottomLeftCornerOfText = (int(1.0*w), int(0.05*h))
                        fontScale = 1.5
                        fontColor = (0,0,250)
                        thickness = 3
                        lineType = 1
            
                        cv2.putText(self.merged_frame, 
                                    self.configRecWindow.video2Title.text(), 
                                    bottomLeftCornerOfText, font,fontScale,
                                    fontColor,thickness, lineType)
                else:
                    #only record till plot range. continue playing to get all data
                    if int(self.framePos) == end_framenum:
                        self.record_frame() #finish recording
                        self.playStatus = True
                        return
                    else:
                        self.merged_frame[:h, w:], r = self.image_resize(frame2, w, h,
                                                                  inter = cv2.INTER_AREA)
    
                # Write video1 title
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (int(0.0*w), int(0.05*h))
                fontScale = 1.5
                fontColor = (0,0,250)
                thickness = 3
                lineType = 1
    
                cv2.putText(self.merged_frame, 
                            self.configRecWindow.video1Title.text(), 
                            bottomLeftCornerOfText, font,fontScale,
                            fontColor,thickness, lineType)
                
                # Write time
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (int(1.55*w), int(0.1*h))
                fontScale = 2
                fontColor = (0,200,200)
                thickness = 10
                lineType = 2
                logging.debug('%s, %s', self.frameTime.item(int(self.framePos-1)), bottomLeftCornerOfText)
                text = 'Time: ' + "{0:.3f}".format(self.frameTime.item(int(self.framePos-1))) + ' s'
                cv2.putText(self.merged_frame, text, 
                            bottomLeftCornerOfText, font,fontScale,
                            fontColor,thickness, lineType)
                
                #Draw scale bar
                logging.debug('%s, %s', scaleFactor, "scalef")
                pixLength = scaleFactor * self.pixelValue.value()
                scalepos1 = (int(0.8*w), int(0.95*h))
                scalepos2 = (int(scalepos1[0] + pixLength), scalepos1[1])
                scalelabelpos = (int(scalepos1[0] + 0.5 * (pixLength - 100)),
                                 scalepos1[1] + 10) #length of label is 51 pixels
                cv2.line(self.merged_frame, scalepos1, scalepos2,
                         fontColor, thickness)
                fontScale = 1
                thickness = 5
                color = (0,200,200)
                text = str(int(self.lengthValue.value())) + ' ' + self.lengthUnit.currentText()
    
                font = ImageFont.truetype("arial.ttf", 28, encoding="unic")
                img_pil = Image.fromarray(self.merged_frame)
                draw = ImageDraw.Draw(img_pil)
                draw.text(scalelabelpos, text, font = font, fill = color)
                self.merged_frame = np.array(img_pil)
    
                logging.debug('%s, %s, %s', self.merged_frame.shape, w, h)
                self.out.write(self.merged_frame)
                cv2.namedWindow("Recording Preview", cv2.WINDOW_KEEPRATIO)
                cv2.imshow("Recording Preview", self.merged_frame)
                cv2.resizeWindow("Recording Preview", 800, 400)
            elif self.configRecWindow.fourRec.isChecked() == True:
                ret, frame3 = self.cap2.read()

    def record_frame(self):
        logging.debug("record_frame")
        if self.recordStatus == True:
            self.out.release()
            self.recordBtn.setIcon(QIcon('images/record.png'))
            self.recordBtn.setEnabled(False)
            self.middleleftGroupBox.setEnabled(True)
            self.bcGroupBox.setEnabled(True)
            self.dftGroupBox.setEnabled(True)
            self.threshGroupBox.setEnabled(True)
            self.threshROIGroupBox.setEnabled(True)
            self.dataGroupBox.setEnabled(True)
            self.roiBtn.setEnabled(True)
            self.analyzeVideo.setEnabled(True)
            self.recordStatus = False
            self.playStatus = False
        else:
            self.recordBtn.setIcon(QIcon('images/recording.png'))
            self.middleleftGroupBox.setEnabled(False)
            self.bcGroupBox.setEnabled(False)
            self.dftGroupBox.setEnabled(False)
            self.threshGroupBox.setEnabled(False)
            self.threshROIGroupBox.setEnabled(False)
            self.dataGroupBox.setEnabled(False)
            self.roiBtn.setEnabled(False)
            self.analyzeVideo.setEnabled(False)
            self.recordStatus = True
            self.playback()
##        self.recordStatus = not self.recordStatus

    #function to resize frame for recording   
    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        
        dim = None
        (h, w) = image.shape[:2]
        resized = np.zeros([height, width, 3], dtype = np.uint8)
        
        if width is None and height is None:
            return image, 0
        
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        elif height is None:
            r = width / float(w)
            dim = (width, int(h * r))

        else:
            rh = height / float(h)
            rw = width / float(w)

            if rh < rw:
                r = rh
                dim = (int(w * r), height)
            else:
                r = rw
                dim = (width, int(h * r))
                
        hdiff = int((height - dim[1])/2)
        wdiff = int((width - dim[0])/2)
 
        resized[hdiff:(hdiff + dim[1]),
                wdiff:(wdiff + dim[0])] = cv2.resize(image, dim,
                                                     interpolation = inter)
        logging.debug('%s, %s', dim, resized.shape)

        return resized, r

    def showRecWindow(self): #open recording configuration window
        self.configRecWindow.showWindow(self.recordingPath)

    def configureRecord(self):
        if self.videoPath != "":
            self.w = self.roiBound[2] - self.roiBound[0]
            self.h = self.roiBound[3] - self.roiBound[1]
                   
            logging.debug('%s, %s, %s', "configurerecord", self.w, self.h)
            self.codecChoices = {'DIVX': cv2.VideoWriter_fourcc(*'DIVX'),
                                 'MJPG': cv2.VideoWriter_fourcc('M','J','P','G'),
                                      'FFV1': cv2.VideoWriter_fourcc('F','F','V','1')}
            fourcc = self.codecChoices.get(self.configRecWindow.codec.currentText())
            self.recordingPath = self.configRecWindow.textbox.toPlainText()
            if self.configRecWindow.fourRec.isChecked() == True:
                i = 2
            else:
                i = 1
            w = 2560
            h = i * 1024
            size = (w, h)
##            fps = self.frameRate
            fps = self.configRecWindow.fps.value() #fixed playback fps
            self.out = cv2.VideoWriter(self.recordingPath, fourcc, fps, size)

            self.merged_frame = np.empty([h, w, 3], dtype = np.uint8)
            logging.debug('%s, %s', self.recordingPath, self.merged_frame.shape)
            self.recordBtn.setEnabled(True)

        videofile2 = self.configRecWindow.videoTextbox.toPlainText() #second video
        logging.debug(videofile2)
        if videofile2 != "":
            self.cap2 = cv2.VideoCapture(videofile2)
        self.configRecWindow.close()
        self.seekSlider.setValue(0) #reset to beginning
        # self.showContours.setChecked(False) #uncheck show contours
        self.clear_data() #clear data