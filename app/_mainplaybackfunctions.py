# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 11:49:58 2020

@author: adwait
"""
from PyQt5.QtGui import QIcon
import cv2
import numpy as np
import time

class MainPlaybackFunctions:
    
    def playback(self): #set video playback status, Play: True / Pause: False
        if self.videoPath != "":
            print(self.playStatus)
            self.playStatus = not self.playStatus
            self.frameAction = "Play"
            self.playBtn.setIcon(QIcon('images/pause.png'))

            print("play")
            while True:
                print("Loop start", time.time())
                
                self.ret, self.frame_current = self.cap.read()
                print("try", self.ret)
                if self.ret == False: #reset video at end or at error
                    print("if")
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.videoPath)
                    self.ret, self.frame_current = self.cap.read()
                    self.framePos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    if self.repeatBtn.isChecked()==False:
                        self.playStatus = False #pause
                    else:
                        self.playStatus = True #play
                else:
                    self.framePos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    print("else", self.framePos)

                self.seekSlider.blockSignals(True)
                self.seekSlider.setValue(int(self.framePos))
                self.seekSlider.blockSignals(False)
                
                self.statusBar.showMessage("Frame number: " + str(int(self.framePos)) + "\t("
                                           + str(int((self.framePos)*100/self.frameCount)) +
                                           "%)" + "\tTime: " +
                                           "{0:.2f}".format(self.frameTime[int(self.framePos-1)]) + " s")
    
                print("frame no. get", self.framePos, self.frame_current.shape, time.time())

                
                roi = self.roiBound
                self.frame = self.frame_current[roi[1]:roi[3], roi[0]:roi[2]].copy() #filter inside roi
                print("Frame copy", time.time())
                self.effectChain = [True, 
                                    True if self.histogramCorrectType.currentText() != 'None' else False, 
                                    self.bgGroupBox.isChecked(), 
                                    self.dftGroupBox.isChecked()] #order: b/c, hist, bg sub, filter                
                
                self.video_effect(self.frame) #apply  b/c, hist, bg sub, filter effects
                print("Video Effect", time.time())
                
                self.roi_auto = self.threshROIGroupBox.isChecked()
                self.roi_hull = self.applyHullROI.isChecked()
                self.combine_roi = self.combineROI.isChecked()
                self.video_analysis() #tresholding and analysis
                print("Video Analysis", time.time())

##                if self.framePos == self.frameCount: #REMOVE -1 and CHECK
##                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
##                    print("reset")
                print(self.playStatus, self.frameAction, self.framePos)

    ##            time.sleep(1/self.fpsSlider.value()) #playback speed
                cv2.waitKey(1)

                if self.playStatus == False: #pause
                    print("frame_urrent", self.frame_current.shape)
                    while True:
                        # print("x")
                        cv2.waitKey(1)
                        self.playBtn.setIcon(QIcon('images/play.png'))
                        if self.playStatus == True: #resume
                            self.playBtn.setIcon(QIcon('images/pause.png'))
                            break
                        if self.frameAction == "Next": #next frame
                            self.frameAction = "Pause"
                            print(self.cap.get(cv2.CAP_PROP_POS_FRAMES),
                                  self.framePos)
                            # self.effectChain = [1, 1, 1, 1]
                            break
                        if self.frameAction == "Previous": #previous frame
                            #change below to consider last two frames as well.CHECK
    ##                        self.framePos = self.frameCount + self.framePos - 3 \
    ##                                   if self.framePos < 2 else self.framePos - 2
                            print(self.cap.get(cv2.CAP_PROP_POS_FRAMES),
                                  self.framePos)
                            self.framePos = self.frameCount - 1 \
                                       if self.framePos == 1 else self.framePos - 2
                            print(self.framePos)
                            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.framePos)
                            self.frameAction = "Pause"
                            print(self.cap.get(cv2.CAP_PROP_POS_FRAMES),
                                  self.framePos)
                            # self.effectChain = [1, 1, 1, 1]
                            break
                        if self.frameAction == "Stop": #stop
                            print("stop")
                            break

                                        
                if self.frameAction == "Stop": #stop
                    #TO DO: make a video initialize function
                    print("stop 2")
                    self.playBtn.setIcon(QIcon('images/play.png'))
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.framePos = 1 #avoid array indexing issue (-1)
                    self.seekSlider.blockSignals(True)
                    self.seekSlider.setValue(0)
                    self.seekSlider.blockSignals(False)
                    self.ret, self.frame_current = self.cap.read()
                    self.frame = self.frame_current.copy()
##                    self.roiBound = [0, 0, self.frameWidth, self.frameHeight]
##                    self.video_effect(self.frame)
                    self.roi_auto = self.threshROIGroupBox.isChecked()
                    self.roi_hull = self.applyHullROI.isChecked()
                    self.combine_roi = self.combineROI.isChecked()
##                    self.video_analysis() #tresholding and analysis
                    
                    self.renderVideo("Raw", self.ret, self.frame)
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.playStatus = False
                    # self.frame_current = self.frame.copy()
                    # self.effectChain = [1, 1, 1, 1]
                    self.recordStatus = False

                    self.statusBar.showMessage("Frame number: " + str(int(self.framePos-1)) + "\t("
                                           + str(int((self.framePos-1)*100/self.frameCount)) +
                                           "%)" + "\tTime: " +
                                           "{0:.2f}".format(self.frameTime[int(self.framePos-1)]) + " s")
                    break

                self.frame = None

    def stop_video(self):
        if self.videoPath != "":
            self.frameAction = "Stop"
            roiCorners = np.array([[0, 0],[self.frameWidth, 0], 
                                        [self.frameWidth, self.frameHeight], 
                                        [0, self.frameHeight]],np.int32)
            self.roiBound = [0, 0, self.frameWidth, self.frameHeight]
            self.roiDict = {"Default": [roiCorners, self.roiBound, [],
                                        roiCorners, roiCorners]}
            self.init_dict() #initialise dictionaries
        
    def next_frame(self):
        if self.videoPath != "":
            self.frameAction = "Next"

    def previous_frame(self):
        if self.videoPath != "":
            self.frameAction = "Previous"

    def seek_video(self):
        if self.videoPath != "":
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.seekSlider.value())
##            self.framePos = self.seekSlider.value()
##            if self.framePos == self.frameCount-1: #REMOVE -1 and CHECK
##                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            self.ret, self.frame_current = self.cap.read()
            if self.seekSlider.value() == 0:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            if self.ret == False: #CHECK
                print("if")
                self.cap.release()
                self.cap = cv2.VideoCapture(self.videoPath)
                self.ret, self.frame_current = self.cap.read()
##                self.framePos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
##            else:
            self.framePos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            print("else", self.framePos)

            self.seekSlider.blockSignals(True)
            self.seekSlider.setValue(self.framePos)
            self.seekSlider.blockSignals(False)

            self.statusBar.showMessage("Frame number: " + str(int(self.framePos)) + "\t("
                                           + str(int((self.framePos)*100/self.frameCount)) +
                                           "%)" + "\tTime: " +
                                           "{0:.2f}".format(self.frameTime[int(self.framePos-1)]) + " s")
##            self.framePos = 1 if self.framePos == 0 else self.framePos #avoid array indexing issue
                
##            self.statusBar.showMessage("Frame number: " + str(int(self.framePos)) + "\t("
##                                       + str(int((self.framePos)*100/self.frameCount)) +
##                                       "%)")
            roi = self.roiBound
            self.frame = self.frame_current[roi[1]:roi[3], roi[0]:roi[2]].copy() #filter inside roi
            self.effectChain = [True, 
                                True if self.histogramCorrectType.currentText() != 'None' else False, 
                                self.bgGroupBox.isChecked(), 
                                self.dftGroupBox.isChecked()] #order: b/c, hist, bg sub, filter                
            
            self.video_effect(self.frame) #apply filter, b/c, bg subtract effects
            
            self.roi_auto = self.threshROIGroupBox.isChecked()
            self.roi_hull = self.applyHullROI.isChecked()
            self.combine_roi = self.combineROI.isChecked()

            if self.framePos == 0:
##                self.blankPixmap = QPixmap('images/blank.png')
                self.statusBar.showMessage("Press play to begin")
                self.rawScene.removeItem(self.rawPixmapItem)
                self.rawPixmapItem = self.rawScene.addPixmap(self.blankPixmap)
                self.rawView.fitInView(self.rawPixmapItem, 1)
                self.effectScene.removeItem(self.effectPixmapItem)
                self.effectPixmapItem = self.effectScene.addPixmap(self.blankPixmap)
                self.effectView.fitInView(self.effectPixmapItem, 1)
            else:
                self.video_analysis() #tresholding and analysis
