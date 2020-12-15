# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:24:56 2020

@author: adwait
"""
import numpy as np
import source.app.drawroi as drawroi
import logging

class MainRoiFunctions:

    def roiDraw(self): #draw roi
        if len(self.frame) != 0:
            logging.debug('%s', self.frame.shape)
##            self.roiCorners = np.array([],np.int32)
            frame_dup = self.frame_current.copy()
##            cv2.polylines(frame_dup, [self.roiCorners],
##                      True, (0,0,255), 2) #final polygon roi
            roiCorners = drawroi.roi_dry("Frame", frame_dup)
            logging.debug("roiCorners")
            roiBound = self.roiBoundingRectangle(roiCorners) #(xmin, ymin, xmax, ymax)
##            roiCorners = roiCorners - [roiBound[0],
##                                                 roiBound[1]]
            
##            self.video_effect(self.frame_current)
##            self.video_analysis() #CHECK

            #reinitialise draw_roi module variables
            drawroi.trigger = 0 
            drawroi.pts = []
            return roiCorners, roiBound

    def roiBoundingRectangle(self, roiCorners): #get bounding rectangle
        xmin = min(roiCorners[:, 0])
        xmax = max(roiCorners[:, 0])
        ymin = min(roiCorners[:, 1])
        ymax = max(roiCorners[:, 1])
        roi = [xmin, ymin, xmax, ymax]
        return roi

    def roiMerge(self): #combine multiple ROIs
        key = self.configROIWindow.roiNum.value()
        label = self.configROIWindow.roiDict[key]
        rc, rb = self.roiDraw()
        self.roiDict[label] = [rc, rb, [], [], []]
        
        self.update_roi()
        
        # self.getRoiBound()
        # roi = self.roiBound
        
        # self.analyzeDataWindow.roiChoice.blockSignals(True)
        # # self.analyzeDataWindow.roiChoice.clear()
        # # self.analyzeDataWindow.roiChoice.addItem("Default")
        
        # # self.analyzeDataWindow.initialize_dict("Default", range_clear = True)
        # # empty_array = np.zeros(int(self.frameCount), np.float64)
        # # self.dataDict = {}
        # # self.init_datadict("Default")
        # for k in self.roiDict.keys():
        #     if len(self.roiDict.keys()) > 1 and k == "Default":
        #         continue
        #     self.roiDict[k][3] = self.roiDict[k][0] - [self.roiBound[0],
        #                                                self.roiBound[1]]
            
        #     self.analyzeDataWindow.roiChoice.addItem(k)
        #     self.analyzeDataWindow.initialize_dict(k, range_clear = False)
            
        #     self.init_datadict(k)
        #     # for key in self.dataDict[k].keys():
        #     #     if key == "Ellipse fit":
        #     #         self.dataDict[k][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
        #     #     else:
        #     #         self.dataDict[k][key] = empty_array            
        #     # self.dataDict[k] = 6 * [np.zeros(int(self.frameCount), np.float64)] + \
        #     #     [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
        #     #         [np.zeros(int(self.frameCount), np.float64)]
        # self.analyzeDataWindow.roiChoice.blockSignals(False)
        # self.contour_data = [[], [], [], [], [], [], [], []]
        # self.plotSequence()
        # self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
        # self.video_analysis() #CHECK

    def getRoiBound(self): #get roiBound
        xmin, ymin, xmax, ymax = [], [], [], []
        for k in self.roiDict.keys():
            if len(self.roiDict.keys()) > 1 and k == "Default":
                continue
            xmin.append(self.roiDict[k][1][0])
            ymin.append(self.roiDict[k][1][1])
            xmax.append(self.roiDict[k][1][2])
            ymax.append(self.roiDict[k][1][3])
        self.roiBound = [min(xmin), min(ymin), max(xmax), max(ymax)]

    def update_roi(self): #update roi related settings and dicts everywhere
        self.analyzeDataWindow.roiChoice.blockSignals(True)
        self.analyzeDataWindow.roiChoice.clear()
        self.analyzeDataWindow.roiChoice.addItem("Default")

        # self.analyzeDataWindow.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
        #                                                 [0,100],[0,100],[0,1]]}
        # self.analyzeDataWindow.dataAnalDict['force settings'] = {}
        self.analyzeDataWindow.initialize_dict("Default", range_clear = True)
        # empty_array = np.zeros(int(self.frameCount), np.float64)
        self.dataDict = {}
        self.init_datadict("Default")
        # for key in self.dataDict["Default"].keys():
        #     if key == "Ellipse fit":
        #         self.dataDict["Default"][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
        #     else:
        #         self.dataDict["Default"][key] = empty_array        
        # self.dataDict = {"Default" : 6 * [np.zeros(int(self.frameCount), np.float64)] + \
        #                  [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
        #             [np.zeros(int(self.frameCount), np.float64)]}
        
        for k in self.configROIWindow.roiDict.values(): #update dictionary and combobox
            self.analyzeDataWindow.roiChoice.addItem(k)
            # self.analyzeDataWindow.rangeDict[k] = [[0,1],[0,100],[0,100],
            #                                       [0,100],[0,100], [0,1]]
            self.analyzeDataWindow.initialize_dict(k, range_clear = False)
            self.init_datadict(k)
            # for key in self.dataDict[k].keys():
            #     if key == "Ellipse fit":
            #         self.dataDict[k][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
            #     else:
            #         self.dataDict[k][key] = empty_array 
            # self.dataDict[k] = 6 * [np.zeros(int(self.frameCount), np.float64)] + \
            #                    [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
            #         [np.zeros(int(self.frameCount), np.float64)]

        self.contour_data = [[], [], [], [], [], [], [], []]

        keys = list(self.roiDict.keys())
        for k in keys: #delete non-existant keys from roiDict
            if k == "Default":
                continue
            if k not in self.configROIWindow.roiDict.values():
                del self.roiDict[k]

        if len(self.roiDict.keys()) > 1: #set to first roi
            self.analyzeDataWindow.roiChoice.setCurrentIndex(1)
        self.analyzeDataWindow.roiChoice.blockSignals(False)
        
        self.analyzeDataWindow.update_widgets() #update widget values based on dict

        self.getRoiBound() #update roi bounds
        roi = self.roiBound
        for k in self.roiDict.keys():
            if len(self.roiDict.keys()) > 1 and k == "Default":
                continue
            self.roiDict[k][3] = self.roiDict[k][0] - [self.roiBound[0],
                                                       self.roiBound[1]]
            self.init_datadict(k)
            # for key in self.dataDict[k].keys():
            #     if key == "Ellipse fit":
            #         self.dataDict[k][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
            #     else:
            #         self.dataDict[k][key] = empty_array
            # self.dataDict[k] = 6 * [np.zeros(int(self.frameCount), np.float64)] + \
            #                    [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
            #         [np.zeros(int(self.frameCount), np.float64)]

        self.plotSequence()
        self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
        self.video_analysis()

    def closeROIWindow(self): #close roi window
        logging.debug("close roi window")
        
        self.update_roi()
        # self.analyzeDataWindow.roiChoice.blockSignals(True)
        # self.analyzeDataWindow.roiChoice.clear()
        # self.analyzeDataWindow.roiChoice.addItem("Default")

        # # self.analyzeDataWindow.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
        # #                                                 [0,100],[0,100],[0,1]]}
        # # self.analyzeDataWindow.dataAnalDict['force settings'] = {}
        # self.analyzeDataWindow.initialize_dict("Default", range_clear = True)
        # # empty_array = np.zeros(int(self.frameCount), np.float64)
        # self.dataDict = {}
        # self.init_datadict("Default")
        # # for key in self.dataDict["Default"].keys():
        # #     if key == "Ellipse fit":
        # #         self.dataDict["Default"][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
        # #     else:
        # #         self.dataDict["Default"][key] = empty_array        
        # # self.dataDict = {"Default" : 6 * [np.zeros(int(self.frameCount), np.float64)] + \
        # #                  [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
        # #             [np.zeros(int(self.frameCount), np.float64)]}
        
        # for k in self.configROIWindow.roiDict.values(): #update dictionary and combobox
        #     self.analyzeDataWindow.roiChoice.addItem(k)
        #     # self.analyzeDataWindow.rangeDict[k] = [[0,1],[0,100],[0,100],
        #     #                                       [0,100],[0,100], [0,1]]
        #     self.analyzeDataWindow.initialize_dict(k, range_clear = False)
        #     self.init_datadict(k)
        #     # for key in self.dataDict[k].keys():
        #     #     if key == "Ellipse fit":
        #     #         self.dataDict[k][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
        #     #     else:
        #     #         self.dataDict[k][key] = empty_array 
        #     # self.dataDict[k] = 6 * [np.zeros(int(self.frameCount), np.float64)] + \
        #     #                    [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
        #     #         [np.zeros(int(self.frameCount), np.float64)]

        # self.contour_data = [[], [], [], [], [], [], [], []]

        # keys = list(self.roiDict.keys())
        # for k in keys: #delete non-existant keys from roiDict
        #     if k == "Default":
        #         continue
        #     if k not in self.configROIWindow.roiDict.values():
        #         del self.roiDict[k]

        # if len(self.roiDict.keys()) > 1: #set to first roi
        #     self.analyzeDataWindow.roiChoice.setCurrentIndex(1)
        # self.analyzeDataWindow.roiChoice.blockSignals(False)

        # self.getRoiBound() #update roi bounds
        # roi = self.roiBound
        # for k in self.roiDict.keys():
        #     if len(self.roiDict.keys()) > 1 and k == "Default":
        #         continue
        #     self.roiDict[k][3] = self.roiDict[k][0] - [self.roiBound[0],
        #                                                self.roiBound[1]]
        #     self.init_datadict(k)
        #     # for key in self.dataDict[k].keys():
        #     #     if key == "Ellipse fit":
        #     #         self.dataDict[k][key] = [[(0,0),(0,0),0,1]]*int(self.frameCount)
        #     #     else:
        #     #         self.dataDict[k][key] = empty_array
        #     # self.dataDict[k] = 6 * [np.zeros(int(self.frameCount), np.float64)] + \
        #     #                    [[[(0,0),(0,0),0,1]]*int(self.frameCount)] + \
        #     #         [np.zeros(int(self.frameCount), np.float64)]

        # self.plotSequence()
        # self.video_effect(self.frame_current[roi[1]:roi[3], roi[0]:roi[2]])
        # self.video_analysis()
        self.configROIWindow.close()

    def init_dict(self): #initialise roi dictionaries/roi labels
        self.analyzeDataWindow.roiChoice.blockSignals(True)
        self.analyzeDataWindow.roiChoice.clear()
        self.analyzeDataWindow.roiChoice.addItem("Default")
        self.analyzeDataWindow.roiChoice.blockSignals(False)
        # self.analyzeDataWindow.rangeDict = {"Default" : [[0,1],[0,100],
        #                                                 [0,100],[0,100],
        #                                                 [0,100],[0,1]]}
        # self.analyzeDataWindow.dataAnalDict['force settings'] = {}
        self.analyzeDataWindow.initialize_dict("Default", range_clear = True)
        self.analyzeDataWindow.update_widgets()

        self.configROIWindow.roiDict = {}
        self.configROIWindow.roiDef.setText("ROI Definition:")
        self.configROIWindow.roiNum.blockSignals(True)
        self.configROIWindow.roiNum.setValue(1)
        self.configROIWindow.roiNum.blockSignals(False)
        self.configROIWindow.roiLabel.blockSignals(True)
        self.configROIWindow.roiLabel.setText("")
        self.configROIWindow.roiLabel.blockSignals(False)