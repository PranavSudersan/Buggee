# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 20:46:36 2020

@author: adwait
"""
import numpy as np

class MainParameterChanged:
    
    def rawViewTabChanged(self): #raw view tab changed
        tabname = self.rawViewTab.tabText(self.rawViewTab.currentIndex())
        self.rawView = self.rawViewDict[tabname]
        if len(self.frame) != 0:
            self.video_analysis()        

    def effectViewTabChanged(self): #effect view tab changed
        tabname = self.effectViewTab.tabText(self.effectViewTab.currentIndex())
        self.effectView = self.effectViewDict[tabname]
        if len(self.frame) != 0:
            self.video_analysis() 

    def threshold_change(self): #threshold change
        print("tresh", self.threshSlider1.value(), self.threshType)
        if self.threshType.currentText() == "Adaptive":
            if self.threshSlider1.value() %2 == 0: #make sure its odd
                self.threshSlider1.blockSignals(True)
                self.threshSlider1.setValue(self.threshSlider1.value() + 1)
                self.threshSlider1.blockSignals(False)
            if self.threshSpinBox1.value() %2 == 0: #make sure its odd
                self.threshSpinBox1.blockSignals(True)
                self.threshSpinBox1.setValue(self.threshSpinBox1.value() + 1)
                self.threshSpinBox1.blockSignals(False)

        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.threshSpinBox1.blockSignals(True)
            self.threshSpinBox1.setValue(self.threshSlider1.value())
            self.threshSpinBox1.blockSignals(False)
            self.threshSpinBox2.blockSignals(True)
            self.threshSpinBox2.setValue(self.threshSlider2.value())
            self.threshSpinBox2.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.threshSlider1.blockSignals(True)
            self.threshSlider1.setValue(self.threshSpinBox1.value())
            self.threshSlider1.blockSignals(False)
            self.threshSlider2.blockSignals(True)
            self.threshSlider2.setValue(self.threshSpinBox2.value())
            self.threshSlider2.blockSignals(False)

        if len(self.frame) != 0:
            self.video_analysis()

    def segment_change(self): #image segment change
        if self.applySegment.isChecked() == True:
            self.segmentFGButton.setEnabled(True)
            self.segmentFGSlider.setEnabled(True)
            self.segmentFGSpinBox.setEnabled(True)
            self.segmentBGButton.setEnabled(True)
            self.segmentBGSlider.setEnabled(True)
            self.segmentBGSpinBox.setEnabled(True)
            self.showSegment.setEnabled(True)
            self.segment = True
        else:
            self.segmentFGButton.setEnabled(False)
            self.segmentFGSlider.setEnabled(False)
            self.segmentFGSpinBox.setEnabled(False)
            self.segmentBGButton.setEnabled(False)
            self.segmentBGSlider.setEnabled(False)
            self.segmentBGSpinBox.setEnabled(False)
            self.showSegment.setEnabled(False)
            self.segment = False
        
        if len(self.frame) != 0:
            self.video_analysis()        

    def segment_param_change(self): #segment parameter change
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.segmentFGSpinBox.blockSignals(True)
            self.segmentFGSpinBox.setValue(self.segmentFGSlider.value()/10)
            self.segmentFGSpinBox.blockSignals(False)
            self.segmentBGSpinBox.blockSignals(True)
            self.segmentBGSpinBox.setValue(self.segmentBGSlider.value())
            self.segmentBGSpinBox.blockSignals(False)          
        elif changed_object.__class__.__name__ in ["QSpinBox", "QDoubleSpinBox"]:
            self.segmentFGSlider.blockSignals(True)
            self.segmentFGSlider.setValue(int(self.segmentFGSpinBox.value()*10))
            self.segmentFGSlider.blockSignals(False)
            self.segmentBGSlider.blockSignals(True)
            self.segmentBGSlider.setValue(self.segmentBGSpinBox.value())
            self.segmentBGSlider.blockSignals(False)
        
        if len(self.frame) != 0:
            self.video_analysis()
            
    def segment_show(self): #show segmented image window
        self.show_segment = self.showSegment.isChecked()
        if len(self.frame) != 0:
            self.video_analysis()
    
    def segment_show_fg(self): #show sure foreground window
        self.show_fg = self.segmentFGButton.isChecked()
        if len(self.frame) != 0:
            self.video_analysis()
        
    def segment_show_bg(self): #show sure background window
        self.show_bg = self.segmentBGButton.isChecked()
        if len(self.frame) != 0:
            self.video_analysis()

    def dft_change(self): #dft filter change
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.lowPassSpinBox.blockSignals(True)
            self.lowPassSpinBox.setValue(self.lowPassSlider.value())
            self.lowPassSpinBox.blockSignals(False)
            self.highPassSpinBox.blockSignals(True)
            self.highPassSpinBox.setValue(self.highPassSlider.value())
            self.highPassSpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.lowPassSlider.blockSignals(True)
            self.lowPassSlider.setValue(self.lowPassSpinBox.value())
            self.lowPassSlider.blockSignals(False)
            self.highPassSlider.blockSignals(True)
            self.highPassSlider.setValue(self.highPassSpinBox.value())
            self.highPassSlider.blockSignals(False)

        self.filter_adjust()
        
        if len(self.frame) != 0:
            print(self.frame_current.size)
            if self.playStatus == False:
                roi = self.roiBound
                if self.dftGroupBox.isChecked() == True:
                    self.effectChain = [1, 1, 1, 0] #order: b/c, bg sub, filter, tresh
                    self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
                    self.video_analysis()
                elif changed_object.__class__.__name__ == "QGroupBox":
                    self.frame = self.frame_current[roi[1]:roi[3], roi[0]:roi[2]].copy()
                    self.effectChain = [1, 1, 0, 0]
                    self.video_effect(self.frame)
                    self.video_analysis()

    def filter_adjust(self): #adjust parameters of filtering
        ftypes = ['Gaussian Filter', 'Median Filter']
        if self.filterType.currentText() in ftypes:
            if self.lowPassSlider.value() < 3: #min value 3
                self.lowPassSlider.blockSignals(True)
                self.lowPassSlider.setValue(3)
                self.lowPassSlider.blockSignals(False)
            if self.lowPassSpinBox.value() < 3: #min value 3
                self.lowPassSpinBox.blockSignals(True)
                self.lowPassSpinBox.setValue(3)
                self.lowPassSpinBox.blockSignals(False)
            if self.lowPassSlider.value() %2 == 0: #make sure its odd
                self.lowPassSlider.blockSignals(True)
                self.lowPassSlider.setValue(self.lowPassSlider.value() + 1)
                self.lowPassSlider.blockSignals(False)
            if self.lowPassSpinBox.value() %2 == 0: #make sure its odd
                self.lowPassSpinBox.blockSignals(True)
                self.lowPassSpinBox.setValue(self.lowPassSpinBox.value() + 1)
                self.lowPassSpinBox.blockSignals(False)
        elif self.filterType.currentText() in ['Average Filter', 
                                               'Morph Open', 'Morph Close']:
            if self.lowPassSlider.value() < 1: #min value 1
                self.lowPassSlider.blockSignals(True)
                self.lowPassSlider.setValue(1)
                self.lowPassSlider.blockSignals(False)
            if self.lowPassSpinBox.value() < 1: #min value 1
                self.lowPassSpinBox.blockSignals(True)
                self.lowPassSpinBox.setValue(1)
                self.lowPassSpinBox.blockSignals(False)
            if self.highPassSlider.value() < 1: #min value 1
                self.highPassSlider.blockSignals(True)
                self.highPassSlider.setValue(1)
                self.highPassSlider.blockSignals(False)
            if self.highPassSpinBox.value() < 1: #min value 1
                self.highPassSpinBox.blockSignals(True)
                self.highPassSpinBox.setValue(1)
                self.highPassSpinBox.blockSignals(False)
        elif self.filterType.currentText() == 'Bilateral Filter':
            if self.highPassSlider.value() > 9: #max value 9
                self.highPassSlider.blockSignals(True)
                self.highPassSlider.setValue(9)
                self.highPassSlider.blockSignals(False)
            if self.highPassSpinBox.value() > 9: #max value 9
                self.highPassSpinBox.blockSignals(True)
                self.highPassSpinBox.setValue(9)
                self.highPassSpinBox.blockSignals(False)

    
    def bc_change(self): #brightness-contrast change
        print("bc_change")
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.brightnessSpinBox.blockSignals(True)
            self.brightnessSpinBox.setValue(self.brightnessSlider.value())
            self.brightnessSpinBox.blockSignals(False)
            self.contrastSpinBox.blockSignals(True)
            self.contrastSpinBox.setValue(self.contrastSlider.value())
            self.contrastSpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.brightnessSlider.blockSignals(True)
            self.brightnessSlider.setValue(self.brightnessSpinBox.value())
            self.brightnessSlider.blockSignals(False)
            self.contrastSlider.blockSignals(True)
            self.contrastSlider.setValue(self.contrastSpinBox.value())
            self.contrastSlider.blockSignals(False)
        if len(self.frame) != 0:
            if self.playStatus == False:
                print("bc anal")
                roi = self.roiBound
                self.effectChain = [1, 1, 1, 1]
                self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
                self.video_analysis()

    def epsilon_change(self): #epsilon (roi hull) change
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.epsilonSpinBox.blockSignals(True)
            self.epsilonSpinBox.setValue(self.epsilonSlider.value())
            self.epsilonSpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.epsilonSlider.blockSignals(True)
            self.epsilonSlider.setValue(self.epsilonSpinBox.value())
            self.epsilonSlider.blockSignals(False)
        elif changed_object.__class__.__name__ == "QCheckBox":
            self.roi_hull = self.applyHullROI.isChecked()

        self.epsilon_fraction = 10**((self.epsilonSpinBox.value())/10)
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()

    def roi_morph_change(self): #change roi morph params
        if self.morphROI.isChecked() == True:
            self.morphXSpinBox.setEnabled(True)
            self.morphYSpinBox.setEnabled(True)
        else:
            self.morphXSpinBox.setEnabled(False)
            self.morphYSpinBox.setEnabled(False)
        self.roi_morph = self.morphROI.isChecked()
        self.x_roi_morph = self.morphXSpinBox.value()
        self.y_roi_morph = self.morphYSpinBox.value()
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()

    def roi_min_change(self): #change roi min
        self.roi_min_area = self.roiMinSpinBox.value()
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()

    def threshold_roi_change(self): #change threshold to detect roi (Wet case)
        self.roi_tresh_type = self.threshROIType.currentText()
        if self.threshROIType.currentText() == "Adaptive":
            self.threshROISlider1.setMinimum(3)
            self.threshROISpinBox1.setMinimum(3)
            if self.threshROISlider1.value() %2 == 0: #make sure its odd
                self.threshROISlider1.blockSignals(True)
                self.threshROISlider1.setValue(self.threshROISlider1.value() + 1)
                self.threshROISlider1.blockSignals(False)
            if self.threshROISpinBox1.value() %2 == 0: #make sure its odd
                self.threshROISpinBox1.blockSignals(True)
                self.threshROISpinBox1.setValue(self.threshROISpinBox1.value() + 1)
                self.threshROISpinBox1.blockSignals(False)
        else:
            self.threshROISlider1.setMinimum(1)
            self.threshROISpinBox1.setMinimum(1)

        changed_object = self.sender() #signal source

        if changed_object.__class__.__name__ == "QSlider":
            self.threshROISpinBox1.blockSignals(True)
            self.threshROISpinBox1.setValue(self.threshROISlider1.value())
            self.threshROISpinBox1.blockSignals(False)
            self.threshROISpinBox2.blockSignals(True)
            self.threshROISpinBox2.setValue(self.threshROISlider2.value())
            self.threshROISpinBox2.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.threshROISlider1.blockSignals(True)
            self.threshROISlider1.setValue(self.threshROISpinBox1.value())
            self.threshROISlider1.blockSignals(False)
            self.threshROISlider2.blockSignals(True)
            self.threshROISlider2.setValue(self.threshROISpinBox2.value())
            self.threshROISlider2.blockSignals(False)
            
        self.tresh_size_roi = self.threshROISpinBox1.value()
        self.tresh_cst_roi = self.threshROISpinBox2.value()
        
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()

    def blur_roi_change(self): #change roi  blur
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.blurROISpinBox.blockSignals(True)
            self.blurROISpinBox.setValue(self.blurROISlider.value())
            self.blurROISpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.blurROISlider.blockSignals(True)
            self.blurROISlider.setValue(self.blurROISpinBox.value())
            self.blurROISlider.blockSignals(False)

        self.blur_size_roi = self.blurROISpinBox.value()
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()        

    def bg_roi_change(self): #bg roi checkbox change
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QCheckBox":
            self.bg_roi_apply = self.applybgROI.isChecked()
            if self.bg_roi_apply == True:
                self.bgblurROISpinBox.setEnabled(True)
                self.bgblurROISlider.setEnabled(True)
                self.bgblendROISpinBox.setEnabled(True)
                self.bgblendROISlider.setEnabled(True)
            else:
                self.bgblurROISpinBox.setEnabled(False)
                self.bgblurROISlider.setEnabled(False)
                self.bgblendROISpinBox.setEnabled(False)
                self.bgblendROISlider.setEnabled(False)
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()

    def bg_blur_roi_change(self): # change bg roi blur
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.bgblurROISpinBox.blockSignals(True)
            self.bgblurROISpinBox.setValue(self.bgblurROISlider.value())
            self.bgblurROISpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.bgblurROISlider.blockSignals(True)
            self.bgblurROISlider.setValue(self.bgblurROISpinBox.value())
            self.bgblurROISlider.blockSignals(False)

        self.bg_blur_size_roi = self.bgblurROISpinBox.value()
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()        
        
    def bg_blend_roi_change(self): #change bg blend
        changed_object = self.sender() #signal source
        if changed_object.__class__.__name__ == "QSlider":
            self.bgblendROISpinBox.blockSignals(True)
            self.bgblendROISpinBox.setValue(self.bgblendROISlider.value()/100)
            self.bgblendROISpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QDoubleSpinBox":
            self.bgblendROISlider.blockSignals(True)
            self.bgblendROISlider.setValue(int(self.bgblendROISpinBox.value()*100))
            self.bgblendROISlider.blockSignals(False)

        self.bg_blend_roi = self.bgblendROISpinBox.value()
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()        
        
    def bg_change(self): #background subtract change
        print("bg change")

        if self.backgroundCorrection.currentText() == "Gaussian Correction":
            if self.bgSlider.value() %2 == 0: #make sure its odd
                self.bgSlider.blockSignals(True)
                self.bgSlider.setValue(self.bgSlider.value() + 1)
                self.bgSlider.blockSignals(False)
            if self.bgSpinBox.value() %2 == 0: #make sure its odd
                self.bgSpinBox.blockSignals(True)
                self.bgSpinBox.setValue(self.bgSpinBox.value() + 1)
                self.bgSpinBox.blockSignals(False)
                
        changed_object = self.sender() #signal source

        if changed_object.__class__.__name__ == "QSlider":
            self.bgSpinBox.blockSignals(True)
            self.bgSpinBox.setValue(self.bgSlider.value())
            self.bgSpinBox.blockSignals(False)
        elif changed_object.__class__.__name__ == "QSpinBox":
            self.bgSlider.blockSignals(True)
            self.bgSlider.setValue(self.bgSpinBox.value())
            self.bgSlider.blockSignals(False)
            
        if len(self.frame) != 0:
            if self.playStatus == False:
                roi = self.roiBound
                if self.bgGroupBox.isChecked() == True:
                    self.effectChain = [1, 1, 1, 0] #order: b/c, bg sub, filter, tresh
                    self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
                    self.video_analysis()
                elif changed_object.__class__.__name__ == "QGroupBox":
                    self.frame = self.frame_current[roi[1]:roi[3], roi[0]:roi[2]].copy()
                    self.effectChain = [1, 0, 1, 0]
                    self.video_effect(self.frame)
                    self.video_analysis()

    def anal_change(self): #analysis video/ contour change
        print("anal change")
        if len(self.frame) != 0:
            if self.analyzeVideo.isChecked() == False:
                self.rawViewTab.setTabEnabled(1,False)
                # self.showContours.setEnabled(False)
                # self.showEffect.setEnabled(False)
            else:
                self.rawViewTab.setTabEnabled(1,True)
                # self.showContours.setEnabled(True)
                # self.showEffect.setEnabled(True)
            roi = self.roiBound
            if self.playStatus == False:
                self.effectChain = [1, 1, 1, 0] #order: b/c, bg sub, filter, tresh
                self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
                self.video_analysis()
        else:
            self.analyzeVideo.setChecked(False)
    
    # def effect_change(self): #effect dropdown change
    #     print("effect change")
    #     if len(self.frame) != 0:
    #         if self.playStatus == False and self.analyzeVideo.isChecked() == True:
    #             if self.videoEffect.currentText() == "Force/Area Plot":
    #                 self.forceData.getArea(self.frameTime, self.dataDict)
    #                 self.forceData.plotData(self.lengthUnit.currentText()) #prepare plot
    #                 self.w = self.roiBound[2] - self.roiBound[0]
    #                 self.h = self.roiBound[3] - self.roiBound[1]
    #                 dim = (1280, 1024) #CHECK!
    #                 self.frameEffect = cv2.resize(cv2.cvtColor(self.forceData.convertPlot(), cv2.COLOR_RGB2BGR),
    #                                               dim, interpolation = cv2.INTER_AREA)

    #             else:
    #                 self.frameEffect = self.effectChoices.get(self.videoEffect. \
    #                                                 currentText())
    #             self.renderVideo("Effect", self.ret, self.frameEffect)

    def fps_change(self):#fps value change
        print("fps change", self.frameCount)
        self.frameRate = self.fpsSpinBox.value()
        self.frameTime = np.linspace(0,
                                     self.frameCount/self.frameRate,
                                     int(self.frameCount), dtype = np.float64)

    def auto_roi_change(self): #auto roi checkbox change
        self.roi_auto = self.threshROIGroupBox.isChecked()
        if self.roi_auto == True:
            self.effectViewTab.setTabEnabled(4,True)
            # self.videoEffect.model().item(5).setEnabled(True) CHECK TAB DISABLE!
##            self.distinctAutoROI.setEnabled(True)
        else:
            self.effectViewTab.setTabEnabled(4,False)
            # self.videoEffect.model().item(5).setEnabled(False) CHECK TAB DISABLE!
##            self.distinctAutoROI.blockSignals(True)
##            self.distinctAutoROI.setChecked(False)
##            self.distinct_roi = False
##            self.distinctAutoROI.blockSignals(False)
##            self.distinctAutoROI.setEnabled(False)
        if len(self.frame) != 0:# and self.roi_auto == True:
            self.video_analysis()

    def distinct_roi_change(self):
        self.distinct_roi = self.distinctAutoROI.isChecked()
        self.combine_roi = self.combineROI.isChecked()
        if len(self.frame) != 0 and self.roi_auto == True:
            self.video_analysis()

    def update_calib(self): #update area data on calibration
        if self.videoPath != "":
            for k in self.roiDict.keys():
                if len(self.roiDict.keys()) > 1 and k == "Default":
                    continue
                # calibFactorOld = self.calibFactor
                self.calibFactor = self.lengthValue.value()/self.pixelValue.value()
                self.dataDict[k][0][int(self.framePos-1)] *= self.calibFactor**2
                self.dataDict[k][1][int(self.framePos-1)] *= self.calibFactor
                self.dataDict[k][3][int(self.framePos-1)] *= self.calibFactor**2
                self.dataDict[k][4][int(self.framePos-1)] *= self.calibFactor
            self.plotSequence()