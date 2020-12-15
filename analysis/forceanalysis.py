# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 19:42:45 2019

@author: adwait
"""
# import matplotlib.pyplot as plt
import numpy as np
# import glob
import os.path
# from tkinter import filedialog
from PyQt5.QtWidgets import QFileDialog
import tkinter as tk
from statistics import mean, stdev
from scipy.signal import savgol_filter, medfilt
from tkinter import messagebox
# import ast
from scipy import integrate
import logging

from source.analysis.plotting import Plotting

class ForceAnal(Plotting):

    def __init__(self, fitWindow = None, configPlotWindow = None,
                 analyzeDataWindow = None):
        super().__init__(fitWindow, configPlotWindow)
        
        self.analyzeDataWindow = analyzeDataWindow
        # if self.analyzeDataWindow != None:
        #     self.analyzeDataWindow.__init__()
        #     self.analyzeDataWindow.zeroBtn.clicked.connect(lambda: 
        #                                                    self.setCursorPosition(
        #                                                        self.analyzeDataWindow.zeroLabel))
        #     self.analyzeDataWindow.forceBtn.clicked.connect(lambda: 
        #                                                self.setCursorPosition(
        #                                                    self.analyzeDataWindow.forceLabel))
        #     self.analyzeDataWindow.preloadBtn.clicked.connect(lambda: 
        #                                                    self.setCursorPosition(
        #                                                        self.analyzeDataWindow.preloadLabel))
        #     self.analyzeDataWindow.deformBtn.clicked.connect(lambda: 
        #                                                    self.setCursorPosition(
        #                                                        self.analyzeDataWindow.deformLabel))
        self.force_filepath = ""
        # self.force_vert1 = [0,0,0]
        # self.time1 = [0,0,0]
        self.speed_um = ""
        self.ptsnumber = 0
        # self.fig1_close = True
        
        # self.flag_ca = True
        # self.flag_ra = False
        # self.flag_cl = False
        # self.flag_rl = False
        # self.flag_cn = False
        # self.flag_ecc = False
        # self.flag_lf = False 
        # self.flag_zp = False
        # self.flag_xp = False
        # self.flag_ap = False
        # self.flag_fp = False
        # self.flag_st = False
        # self.flag_zd = False
        # self.x_var = 'Time' #x axis default parameter
        # self.flag_zshift = False #zero shift
        # self.flag_lf_filter = False
        # self.window_length = 101
        # self.polyorder = 2
        self.calib_lat1 = "29181.73*x"
        # self.invert_latf = False
        # self.flag_ct = True
        # self.ctv_slope = 0 #vertical cross talk slope
        # self.ctl_slope = 0 #lateral cross talk slope
        # self.startFull = 0 #plot range
        # self.endFull = 100
        # self.noiseSteps = ""
        # self.legendPos = "upper right"
        # #fitting
        # self.flag_fit = False
        # self.fit_x = 'Vertical Position (μm)'
        # self.fit_y = 'Vertical Force'
        # self.startFit = 0
        # self.endFit = 100
        # self.fit_pos = '0.5,0.5'
        # self.fit_show = False
        # self.slope = ''
        # self.slope_unit = ''
        # self.k_beam = '30,1' # Beam spring constant (μN/μm)
        # self.deform_tol = 100 #deformation contact start auto detect tolerance
        
##        self.friction_start = 1
##        self.friction_stop = 100
##        self.zero_start = 1 #percent of total number of points
##        self.zero_stop = 10 #percent of total number of points
##        self.adh_start = 1
##        self.adh_stop = 100
##        self.prl_start = 1
##        self.prl_stop = 100
##        self.force_friction = 0 #initialize

        # #area data dictionary
        # self.areaDict = {"area2_init":[], "area2_max":[], "area3_init":[],
        #                  "area2_pulloff":[], "area2_residue":[],
        #                  "area3_pulloff":[], "area3_max":[],
        #                  "area_friction":[]}
        # #length data dictionary
        # self.lengthDict = {"contLength_init":[], "contLength_max":[],
        #                    "roilen_init":[], "roilen_max":[],
        #                    "contLength_pulloff":[], "roilen_pulloff":[],
        #                    "ecc_pulloff":[], "contnum_pulloff": []} 
        # #bounding ellipse data dictionary
        # self.ellipDict = {"ellipAr_max":[], "ellipPer_max":[],
        #                   "ellipMajr_max":[], "ellipMinr_max":[]}
        # #force data dictionaryrangeDict
        # self.forceDict = {"force_adhesion1":[], "force_preload1":[],
        #                   "force_friction":[], "force_preload2":[],
        #                   "force_min1":[], "force_max1":[], "zero1":[], "zero2":[],
        #                   "zero1_stdv":[], "zero2_stdv":[], "force_lat_min":[],
        #                   "force_lat_max":[], "force_max2":[]}
        # #index/time data dictionary for calculation
        # self.indDict = {"force_lat_max_index":[], "force_lat_min_index":[],
        #                 "time1_max":[0], "time1_lat_avg":[]}
        #range dictionary (zero, adhesion, adh preload, friction, fr preload, fr zero)
        # self.rangeDict = {"Default" : [[0,1],[0,100],[0,100],[0,100],[0,100], [0,1]]} 
        

    def importData(self, msrListMode):
        if msrListMode == False:
            force_filepath, _ = QFileDialog.getOpenFileName(caption = "Select force data file")
        else:
            force_filepath = self.force_filepath
            # root = tk.Tk()
            # root.withdraw()
            # self.force_filepath =  filedialog.askopenfilename(title =
            #                                              "Select force data file")
            # root.destroy()
        if force_filepath != "":
            self.force_filepath = force_filepath
            with open(self.force_filepath, 'r') as f: #open force data file
                x1 = f.read().splitlines()
            
            self.fileDataDict = {} # for plotting
            # self.fileDataDict2 = {} # for summary file data
            self.summaryDataDict = {} #summary data values
            self.summaryDataDict['measurement params'] = {}
            self.summaryDataDict['data params'] = {}
            self.summaryDataDict['misc'] = {}
            
            expt_date = x1[1].split('\t')[0]
            folder_name = os.path.dirname(os.path.dirname(self.force_filepath))
            
            self.summaryDataDict['measurement params']["Date of Experiment"] = expt_date
            self.summaryDataDict['measurement params']["Data Folder"] = folder_name
            
            self.waveform = x1[5].split('\t')[1]
            logging.debug('%s', self.waveform)

            if self.waveform == 'custom': #index adjust for force data
                ir = 1
                ic = 1
            else:
                ir = 0
                ic = 0
                
            #collect force data 
            self.fileDataDict["Vertical piezo"] = [(float(y.split('\t')[0]))/1000 \
                                                   for y in x1[23+ir:]] #nm to μm units
            self.ptsnumber = int(float((x1[11+ir].split('\t')[1])))
            if ic == 1:
                self.fileDataDict["Lateral piezo"] = [(float(y.split('\t')[ic])/1000) \
                                                      for y in x1[23+ir:]] #nm to μm units
                speed1 = [int(float(y)) for y in x1[8].split('\t')[1:]]
                self.steps = [y for y in x1[7].split('\t')[1:]]
                logging.debug('%s', self.steps)
                self.step_num = len(x1[7].split('\t')[1:])
                self.pause = [int(float(y)) for y in x1[9].split('\t')[1:]]
            else:
                self.fileDataDict["Lateral piezo"] = [0] * self.ptsnumber
                speed1 = [int(float(x1[6].split('\t')[1]))]
                self.steps = ["Up/Down"] #Check
                self.step_num = 1
                self.pause = [0]
            self.fps = float((x1[20+ir].split('\t')[1]))
            self.frame_num = [int(float(y)) for y in (x1[21+ir].split('\t')[1:])]
            self.fileDataDict["Time"] = [float(y.split('\t')[1+ic]) for y in x1[23+ir:]]
            self.fileDataDict["Vertical Deflection Raw"] = [float(y.split('\t')[2+ic]) \
                                                        for y in x1[23+ir:]]
            self.fileDataDict["Lateral Deflection Raw"] = [float(y.split('\t')[3+ic])\
                                                       for y in x1[23+ir:]]
            self.calib_vert1 = x1[19+ir].split('\t')[1].replace("^", "**")
            #make 'Back' speeds negative
            # self.speed = [-speed1[self.steps.index(a)] if a == 'Back' \
            #               else speed1[self.steps.index(a)] for a in self.steps]
            self.speed = [-speed1[i] if self.steps[i] == 'Back' \
                          else speed1[i] for i in range(len(self.steps))]
            logging.debug('%s', self.ptsnumber)
            
            self.fileDataDict["Index"] = np.linspace(0, self.ptsnumber-1, 
                                                     self.ptsnumber, 
                                                     dtype = np.uint)
            
            # self.fileDataDict2["Steps"] = self.steps
            # self.summaryDataDict['data params'] = {}
            # self.summaryDataDict['data params']["Steps"] = self.steps
            # self.dataClean()

            # self.calcData()

    def dataClean(self): #clean force data
        #correct offshoot
        self.fileDataDict["Vertical Deflection"] = self.offShootCorrect(
            self.fileDataDict["Vertical Deflection Raw"])
        self.fileDataDict["Lateral Deflection"] = self.offShootCorrect(
            self.fileDataDict["Lateral Deflection Raw"])
            
    def evaluateForce(self): #calculate force from calibration equations
        self.fileDataDict["Vertical force"] = [-eval(self.calib_vert1) for x in \
                                               self.fileDataDict["Vertical Deflection"]]
        self.fileDataDict["Lateral force"] = [-eval(self.calib_lat1) for x in \
                                              self.fileDataDict["Lateral Deflection"]]
            
    def transformForce(self): #apply transformations to force
        dataAnalDict = self.analyzeDataWindow.dataAnalDict
        force_list = ['Vertical force', 'Lateral force']
        i = 0 #used to find correct key of force for cross talk correction
        for force in force_list:
            #zero force subtraction
            if dataAnalDict[force]["transform"]["Zero subtract"] == True:
                self.fileDataDict[force] = self.zeroSubtract(self.fileDataDict[force],
                                                             self.zeroDataDict[force])
            #cross talk correction
            if dataAnalDict['misc settings']['apply cross talk'].isChecked() == True:
                self.fileDataDict[force] = self.crosstalkCorrect(
                    self.fileDataDict[force_list[i]], 
                    self.fileDataDict[force_list[i-1]],
                    dataAnalDict[force]["transform"]["Cross Talk"], 
                    force.split(' ')[0])
            #filter data
            if dataAnalDict[force]["transform"]["Filter"] == True:
                window = dataAnalDict[force]["transform"]["Filter window"]
                order = dataAnalDict[force]["transform"]["Filter order"]
                self.fileDataDict[force] = savgol_filter(self.fileDataDict[force], 
                                                         window, order).tolist()
            
            i += 1        
            
    def crosstalkCorrect(self, f_in, f_dep, slope, f_type):
        if f_type == 'Vertical':
            f_err = [slope*(x - f_dep[1]) for x in f_dep]
        elif f_type == 'Lateral':
            f_err = [slope*(x - f_dep[1]) for x in f_dep]
        f_out = [f_in[i]-f_err[i] for i in range(0,len(f_in))]
        return f_out

    def offShootCorrect(self, data): #remove first point of each step
        # steps_bad = self.noiseSteps.split(",")
        steps_bad = self.analyzeDataWindow.dataAnalDict['misc settings']\
            ['noise steps'].text().split(",")
        data_new = data.copy()
        if steps_bad[0] == '':
            logging.debug("no steps")
            return data
        for i in steps_bad:
            logging.debug('%s, %s', "step", i)
            if i == '':
                continue
            ind = int((int(i)-1) * self.ptsnumber/self.step_num)
            data_new[ind] = data_new[ind + 1] #replace to next value
        return data_new

    # def zeroShift(self, data, zero): #shift force to zero
    #     data_shifted = [x-zero for x in data]
    #     return data_shifted
    
    def zeroSubtract(self, actual_data, zero_data):
        zero_shift = zero_data[0] - actual_data[0]
        zero_data_shifted = [x-zero_shift for x in zero_data]
##        self.defl_vert1_raw = self.forceData.defl_vert1.copy()
        data_subtracted = [actual_data[0] + actual_data[i] - zero_data_shifted[i] \
                                 for i in range(len(actual_data))]
        return data_subtracted

    def interpolData(self, t, data): #interpolate data at force time resolution
            t_near = sorted([[abs(a - t), a] for a in self.time2],
                           key=lambda l:l[0])[:2]
            wt_sum = t_near[0][0] + t_near[1][0] #take weighted avg
            wt = [t_near[1][0]/wt_sum, t_near[0][0]/wt_sum]
            data_t = np.average([data[self.time2.index(t_near[0][1])],
                                 data[self.time2.index(t_near[1][1])]],
                                           weights = wt)
            return data_t
        
    def calcData(self): #datafile related calculations
##            self.calib_lat1 = "-10.249*1000*x"
        logging.debug("calc")
        dataAnalDict = self.analyzeDataWindow.dataAnalDict
        
        #update plot slice
        plot_range = self.configPlotWindow.plotDict['plot settings']\
            ['plot range'].text().split(',')
        self.plot_slice = slice(int(plot_range[0]), int(plot_range[1]) + 1)
        
        time1 = self.fileDataDict["Time"]
        
        # self.plot_slice = slice(int(self.startFull * self.ptsnumber/100),
        #                         int(self.endFull * self.ptsnumber/100))
        
##        #correct offshoot
##        self.defl_vert1 = self.offShootCorrect(self.defl_vert)
##        self.defl_lat1 = self.offShootCorrect(self.defl_lat)
        self.dataClean()
        
        self.evaluateForce()
        
        self.transformForce()
        
        #file data units
        self.unitDict = {'Time': ' [s]',
                         'Index': '',
                         'Vertical force': ' [μN]',
                         'Lateral force': ' [μN]',
                         'Vertical piezo': ' [μm]',
                         'Lateral piezo': ' [μm]',
                         'Deformation': ' [μm]',
                         'Speed': ' [μm/s]'}
        
        # self.fileDataDict["Vertical force"] = [-eval(self.calib_vert1) for x in \
        #                                        self.fileDataDict["Vertical Deflection"]]
        # self.fileDataDict["Lateral force"] = [-eval(self.calib_lat1) for x in \
        #                                       self.fileDataDict["Lateral Deflection"]]

        # if self.flag_ct == True: #cross talk correction
        # force_list = ['Vertical force', 'Lateral force']
        # i = 0 #used to find correct key of force for cross talk correction
        # for force in force_list:
        #     #cross talk correction
        #     if dataAnalDict['misc settings']['apply cross talk'].isChecked() == True:
        #         self.fileDataDict[force] = self.crosstalkCorrect(
        #             self.fileDataDict[force_list[i]], 
        #             self.fileDataDict[force_list[i-1]],
        #             dataAnalDict[force]["transform"]["Cross Talk"], 
        #             force.split(' ')[0])
        #     #filter data
        #     if dataAnalDict[force]["transform"]["Filter"] == True:
        #         window = dataAnalDict[force]["transform"]["Filter window"]
        #         order = dataAnalDict[force]["transform"]["Filter order"]
        #         self.fileDataDict[force] = savgol_filter(self.fileDataDict[force], 
        #                                                  window, order).tolist()
        #     if dataAnalDict[force]["transform"]["Zero subtract"] == True:
        #         self.fileDataDict[force] = self.zeroSubtract(self.fileDataDict[force],
        #                                                      self.zeroDataDict[force])
        #     i += 1
            # self.force_lat1 = self.crosstalkCorrect(force_lat, force_vert,
            #                                         dataAnalDict["Lateral force"]
            #                                          ["transform"]["Cross Talk"],
            #                                          'Lateral')
            # self.force_vert1 = self.crosstalkCorrect(force_vert, force_lat,
            #                                          self.ctv_slope, 'Vertical')
            # self.force_lat1 = self.crosstalkCorrect(force_lat, force_vert,
            #                                         self.ctl_slope, 'Lateral')
        # else:
        #     self.force_vert1 = force_vert
        #     self.force_lat1 = force_lat
        
        #recalculate time array of video (considering measurement delay)
        tstart = 0
        self.time_video = np.empty((0, 100), dtype = np.float64)
        for y in range(self.step_num):
            time_video_temp = np.linspace(tstart, tstart + (self.frame_num[y]/self.fps),
                                     int(self.frame_num[y]), dtype = np.float64)
            self.time_video = np.append(self.time_video, time_video_temp)
            if y < self.step_num-1: 
                tstart = time1[int((y+1)*self.ptsnumber/self.step_num)] #CHANGE TO DIRECT DATA

        #noise filter lateral force
        # if self.flag_lf_filter == True:
        #     self.force_lat1_filtered = savgol_filter(self.force_lat1, self.window_length,
        #                                              self.polyorder).tolist()
        # else:
        #     self.force_lat1_filtered = []                
        
        force_vert1 = self.fileDataDict["Vertical force"]
        force_lat1 = self.fileDataDict["Lateral force"]
        
#         self.forceDict["force_adhesion1"] = []
#         self.forceDict["force_preload1"] = []
#         self.forceDict["force_friction"] = []
#         self.forceDict["force_preload2"] = []
#         self.forceDict["force_max1"] = []
#         self.forceDict["force_max2"] = []
#         self.forceDict["force_min1"] = []
#         self.forceDict["zero1"] = []
#         self.forceDict["force_lat_min"] = []
#         self.forceDict["force_lat_max"] = []
#         self.indDict["force_lat_max_index"] = []
#         self.indDict["force_lat_min_index"] = []
# ##        self.indDict["contact_time1"] = []
#         self.indDict["time1_max"] = []
        
        self.forceDict = {} #force calculation values
        self.indDict = {} #index values
        # self.summaryDataDict = {} #summary data values
        self.summaryDataDict['Vertical force'] = {}
        self.summaryDataDict['Lateral force'] = {}
        
        roi_list = dataAnalDict["Vertical force"]["ranges"].keys()
        for k in roi_list:
            logging.debug('%s', roi_list)
            if len(roi_list) > 1 and k == "Default":
                continue
            #initialize dict for the given roi label
            self.forceDict[k] = {}
            self.indDict[k] = {}
            self.summaryDataDict['Vertical force'][k] = {}
            self.summaryDataDict['Lateral force'][k] = {}
                #calculate friction force
##            if self.flag_lf == True or self.flag_lf_filter == True:
            limits = eval(dataAnalDict["Lateral force"]["ranges"][k]["Force"])
            friction_slice = slice(limits[0], limits[1]+1)
            # friction_slice = slice(int(self.rangeDict[k][3][0] * self.ptsnumber/100),
            #                int(self.rangeDict[k][3][1] * self.ptsnumber/100))
            force_lat_max = max(force_lat1[friction_slice])
            force_lat_max_index = friction_slice.start + \
                                       force_lat1[friction_slice]. \
                                       index(force_lat_max)
            force_lat_min = min(force_lat1[friction_slice])
            force_lat_min_index = friction_slice.start + \
                                       force_lat1[friction_slice]. \
                                       index(force_lat_min)
            force_friction = abs(force_lat_max - force_lat_min)
            logging.debug('%s, %s, %s', friction_slice, force_lat_max_index, force_lat_min_index)
##            else:
##                force_friction = 0
##                force_lat_min = 0
##                force_lat_max = 0
##                force_lat_max_index = 0
##                force_lat_min_index = 0
                
            
            #contact time calculate
##            contact_time1 = sum(self.pause)
            #Note: Contact time is the time for which the pad is kept stationary
            #in contact witht the surface
##            dist_vert1_maxcount = self.dist_vert1.count(min(self.dist_vert1))
##            dist_vert1_max_index = self.dist_vert1.index(min(self.dist_vert1))
##            if dist_vert1_maxcount == 1:
##                contact_time1 = 0
##            else:
##                contact_time1 = (dist_vert1_maxcount - 1) * (self.time1[dist_vert1_max_index+1] -
##                                                              self.time1[dist_vert1_max_index])        

            #ignore first point of force data due to overshoot
            limits = eval(dataAnalDict["Vertical force"]["ranges"][k]["Force"])
            adh_slice = slice(limits[0], limits[1]+1)
            # adh_slice = slice(int(self.rangeDict[k][1][0] * self.ptsnumber/100),
            #                    int(self.rangeDict[k][1][1] * self.ptsnumber/100))
            force_min1 = min(force_vert1[adh_slice])
            self.force_min_index = adh_slice.start + \
                              force_vert1[adh_slice].index(force_min1)
            limits = eval(dataAnalDict["Vertical force"]["ranges"][k]["Preload"])
            prl1_slice = slice(limits[0], limits[1]+1)
            # prl1_slice = slice(int(self.rangeDict[k][2][0] * self.ptsnumber/100),
            #                    int(self.rangeDict[k][2][1] * self.ptsnumber/100))
            force_max1 = max(force_vert1[prl1_slice])
            
            limits = eval(dataAnalDict["Lateral force"]["ranges"][k]["Preload"])
            prl2_slice = slice(limits[0], limits[1]+1)
            # prl2_slice = slice(int(self.rangeDict[k][4][0] * self.ptsnumber/100),
            #                    int(self.rangeDict[k][4][1] * self.ptsnumber/100))
            force_max2 = max(force_vert1[prl2_slice])
            
            limits = eval(dataAnalDict["Vertical force"]["ranges"][k]["Zero"])
            zero_slice = slice(limits[0], limits[1]+1)
            # zero_slice = slice(int(self.rangeDict[k][0][0] * self.ptsnumber/100),
            #                    int(self.rangeDict[k][0][1] * self.ptsnumber/100))
            zero1 = mean(force_vert1[zero_slice]) #average n points as vert zero
            zero1_stdv = stdev(force_vert1[zero_slice]) #vertical force error
            
            limits = eval(dataAnalDict["Lateral force"]["ranges"][k]["Zero"])
            zero2_slice = slice(limits[0], limits[1]+1)
            # zero2_slice = slice(int(self.rangeDict[k][5][0] * self.ptsnumber/100),
            #                    int(self.rangeDict[k][5][1] * self.ptsnumber/100))
            zero2 = mean(force_lat1[zero2_slice]) #average n points as lat zero
            zero2_stdv = stdev(force_lat1[zero2_slice]) #lateral force error
            time1_max = time1[self.force_min_index]

            zero2_filter = mean(force_lat1[zero2_slice]) #average n points as lat zero

            force_preload1 = abs(force_max1 - zero1) #adhesion preload
            # if self.flag_lf == True or self.flag_lf_filter == True:
            force_preload2 = abs(force_max2 - zero1) #friction preload
            # else:
            #     force_preload2 = 0
            force_adhesion1 = abs(force_min1 - zero1)
            logging.debug('%s, %s, %s', force_preload1, force_adhesion1, self.speed_um)

            self.summaryDataDict['Vertical force'][k]["Pulloff Force"] = force_adhesion1
            self.summaryDataDict['Vertical force'][k]["Adhesion Preload"] = force_preload1
            self.summaryDataDict['Vertical force'][k]["Vertical Force Stdev"] = zero1_stdv
            self.summaryDataDict['Lateral force'][k]["Friction Force"] = force_friction
            self.summaryDataDict['Lateral force'][k]["Friction Preload"] = force_preload2
            self.summaryDataDict['Lateral force'][k]["Lateral Force Stdev"] = zero2_stdv
            
            self.forceDict[k]["force_max2"] = force_max2
            self.forceDict[k]["force_max1"] = force_max1
            self.forceDict[k]["force_min1"] = force_min1
            self.forceDict[k]["zero1"] = zero1
            # self.forceDict[k]["zero1_stdv"] = zero1_stdv
            self.forceDict[k]["zero2"] = zero2
            # self.forceDict[k]["zero2_stdv"] = zero2_stdv
            self.forceDict[k]["force_lat_min"] = force_lat_min
            self.forceDict[k]["force_lat_max"] = force_lat_max
            self.indDict[k]["force_lat_max_index"] = force_lat_max_index
            self.indDict[k]["force_lat_min_index"] = force_lat_min_index
##            self.indDict["contact_time1"].append(contact_time1)
            self.indDict[k]["time1_max"] = time1_max
            logging.debug("end")

        #IMP: CHECK zero1 VARIABLE BELOW. DIFFERENT ZEROS NOT CONSIDERED BELOW!
        #shift force data for plotting
        # if self.flag_zshift == True:
        #     self.force_vert1_shifted = [x-zero1 for x in self.force_vert1]
        #     self.force_lat1_shifted = [x-zero2 for x in self.force_lat1]
        #     self.force_lat1_filtered_shifted = [x-zero2_filter for x in self.force_lat1_filtered]
        # else:
        #     self.force_vert1_shifted = self.force_vert1
        #     self.force_lat1_shifted = self.force_lat1
        #     self.force_lat1_filtered_shifted = self.force_lat1_filtered           
        self.speed_um = [x/1000 for x in self.speed] #speed in μm/s
        # self.fileDataDict2["Speed"] = self.speed_um
        # self.summaryDataDict['data params'] = {}
        self.summaryDataDict['data params']['Speed'] = {}
        # self.summaryDataDict['misc']['Speed']["Speed list"] = self.speed_um
        
        # self.speedDict = {} #step number corresponding to sliding/attachment detachment
        self.ptsperstep = int(self.ptsnumber/self.step_num) #number of points per step
        force_lat_index = int(mean([force_lat_min_index, force_lat_max_index]))
        logging.debug('%s, %s, %s', force_lat_index, self.ptsperstep, self.ptsnumber)
        if self.steps[0] == "Up/Down":
            self.summaryDataDict['data params']['Speed']["Sliding Speed"] = 0
            self.summaryDataDict['data params']['Speed']["Detachment Speed"] = self.speed[0]
            self.summaryDataDict['data params']['Speed']["Attachment Speed"] = self.speed[0] #CHECK!
            self.slideStep = "None"
        else:
            self.summaryDataDict['data params']['Speed']["Sliding Speed"] = self.speed_um[int(force_lat_index/self.ptsperstep)]
            ind_detach = int(self.force_min_index/self.ptsperstep)
            self.summaryDataDict['data params']['Speed']["Detachment Speed"] = self.speed_um[ind_detach]
            #last down step bfore detachment
            self.summaryDataDict['data params']['Speed']["Attachment Speed"] = self.speed_um[ind_detach - \
                                           self.steps[ind_detach::-1].index('Down')]
            #lateral sliding step
            self.slideStep = self.steps[int(force_lat_index/self.ptsperstep)]
            logging.debug('%s, %s, %s', "slide step ", force_lat_index, self.ptsperstep)
            # print("Speed dict", self.speedDict)
                   
        self.contact_time1 = sum(self.pause) #contact time
        
        # self.fileDataDict2["Sliding Step"] = self.slideStep
        # self.fileDataDict2["Contact Time"] = self.contact_time1
        # self.summaryDataDict['data params']["Sliding Step"] = self.slideStep
        self.summaryDataDict['data params']['Time'] = {}
        self.summaryDataDict['data params']['Time']["Contact Time"] = self.contact_time1
        #calculate actual vertical deformation
        # for a in self.force_vert1: 
        #     if abs(a-zero1) > self.deform_tol*zero1_stdv: #point of contact for given tolerence
        #         deform_index1 = self.force_vert1.index(a)
        #         break
        #     else:
        #         deform_index1 = 0

        kBeam = dataAnalDict['misc settings']['beam spring constant'].text()
        deform_limits = eval(dataAnalDict['misc settings']['deformation range'].text())
        dist_vert1 = self.fileDataDict["Vertical piezo"]
        # deform_index1 = int(dataAnalDict['misc settings']['deformation start'].text())
        # deform_index1 = self.deform_tol #index of point of contact
        # deform_index2 = max([self.force_vert1.index(a) for a in self.forceDict["force_min1"]]) #point of contact loss
        # deform_index2 = len(self.force_vert1)-1 if deform_index2 <= deform_index1 else deform_index2
        logging.debug('%s, %s, %s', "deform index", deform_limits[0], deform_limits[1])
        self.deform_init = dist_vert1[deform_limits[0]]#piezo value at contact loss
        self.fileDataDict["Deformation"] = [dist_vert1[i] - self.deform_init - \
                            ((force_vert1[i] - zero1)/float(kBeam.split(',')[0])) \
                                if i >= deform_limits[0] and i <= deform_limits[1] else 0 \
                                    for i in range(len(dist_vert1))]
        self.deform_pulloff = self.fileDataDict["Deformation"][deform_limits[1]] #deformation at contact loss
        
        #calculate adhesion energy (area under curve) 
        #TODO! Last zero1 value of rois taken for energy calculation
        pulloff_index = int(self.ptsperstep * int(deform_limits[1]/self.ptsperstep)) #start index of contact loss "step"
        force_shifted = [x-zero1 for x in force_vert1]
        zero_index = (force_shifted[pulloff_index:deform_limits[1]+1].index\
            (sorted([[abs(a - 0), a] for a in force_shifted[pulloff_index:deform_limits[1]+1]], 
                    key=lambda l:l[0])[0][1])) + pulloff_index #point where force reaches zero
        self.energy_slice = slice(zero_index, deform_limits[1] + 1)
        self.energy_adhesion = integrate.simps(force_shifted[self.energy_slice],
                                               self.fileDataDict["Deformation"][self.energy_slice])
        logging.debug('%s, %s, %s, %s', "energy", self.energy_adhesion, pulloff_index, zero_index)
        self.zero_array =zero1*np.ones(len(force_vert1))
        
        # self.fileDataDict2["Initial Deformation"] = self.deform_init
        # self.fileDataDict2["Pulloff Deformation"] = self.deform_pulloff
        # self.fileDataDict2["Adhesion Energy"] = self.energy_adhesion
        # self.summaryDataDict['misc'] = {}
        self.summaryDataDict['misc']["Adhesion Energy"] = self.energy_adhesion
        self.summaryDataDict['data params']['Deformation'] = {}
        self.summaryDataDict['data params']['Deformation']["Initial Deformation"] = self.deform_init
        self.summaryDataDict['data params']['Deformation']["Pulloff Deformation"] = self.deform_pulloff
        
        
    def getArea(self, time, dataDict): #get contact area/lenghths at pulloff etc
    #area data (2)
        logging.debug("Get area begin")
        self.dataDict = dataDict #data dictionary from videos
        
        time1 = self.fileDataDict["Time"]

        # self.areaDict["area2_init"] = []
        # self.areaDict["area2_max"] = []
        # self.areaDict["area3_init"] = []
        # self.areaDict["area3_max"] = []
        # self.areaDict["area2_pulloff"] = []
        # self.areaDict["area2_residue"] = []
        # self.areaDict["area3_pulloff"] = []
        # self.areaDict["area_friction"] = []

        # self.lengthDict["contLength_init"] = []
        # self.lengthDict["contLength_max"] = []
        # self.lengthDict["roilen_init"] = []
        # self.lengthDict["roilen_max"] = []
        # self.lengthDict["contLength_pulloff"] = []
        # self.lengthDict["roilen_pulloff"] = []
        # self.lengthDict["ecc_pulloff"] = []
        # self.lengthDict["contnum_pulloff"] = []

        # self.ellipDict["ellipAr_max"] = []
        # self.ellipDict["ellipPer_max"] = []
        # self.ellipDict["ellipMajr_max"] = []
        # self.ellipDict["ellipMinr_max"] = []
        
        # self.indDict["time1_lat_avg"] = []

        self.time2 = time.tolist()
        area2_full = [0] * len(time) #initialize

        #area/length whole plot slice
        time2_start = sorted([[abs(a - time1[self.plot_slice.start]), a] \
                         for a in self.time2], key=lambda l:l[0])[0][1]
        time2_end = sorted([[abs(a - time1[self.plot_slice.stop-1]), a] \
                         for a in self.time2], key=lambda l:l[0])[0][1]        
        self.plot_slice2 = slice(self.time2.index(time2_start),
                                self.time2.index(time2_end) + 1)         
        i = 0
        logging.debug('%s', dataDict.keys())
        self.areaDict = {}
        self.lengthDict = {}
        # self.ellipDict = {}
        self.summaryDataDict['Contact area'] = {}
        self.summaryDataDict['Contact length'] = {}
        self.summaryDataDict['ROI area'] = {}
        self.summaryDataDict['ROI length'] = {}
        self.summaryDataDict['Contact number'] = {}
        self.summaryDataDict['Eccentricity'] = {}
        
        for k in self.dataDict.keys():
            if len(self.dataDict.keys()) > 1 and k == "Default":
                continue
            logging.debug('%s', k)
            self.areaDict[k] = {}
            self.lengthDict[k] = {}
            self.summaryDataDict['Contact area'][k] = {}
            self.summaryDataDict['Contact length'][k] = {}
            self.summaryDataDict['ROI area'][k] = {}
            self.summaryDataDict['ROI length'][k] = {}
            self.summaryDataDict['Contact number'][k] = {}
            self.summaryDataDict['Eccentricity'][k] = {}            
            # self.ellipDict[k] = {}
            
            area2 = dataDict[k]["Contact area"].tolist() #contact area
            contLength = dataDict[k]["Contact length"].tolist() #contact length
            contnum = dataDict[k]["Contact number"].tolist() #contact number
            area3 = dataDict[k]["ROI area"].tolist() #roi area
            roilen = dataDict[k]["ROI length"].tolist() #roi length
            ecc = dataDict[k]["Eccentricity"].tolist() #median eccentricity
            # print("ellip", dataDict[k][6][0])
            ellipMajr = [x[3]*max(x[1][0],x[1][1]) for x in dataDict[k]["Ellipse fit"]] #ellipse major axis length
            ellipMinr = [x[3]*min(x[1][0],x[1][1]) for x in dataDict[k]["Ellipse fit"]] #ellipse minor axis length
            ellipAr = [np.pi*(x[1][0]/2)*(x[1][1]/2)*(x[3]**2) for x in dataDict[k]["Ellipse fit"]] #bounding ellipse area
            ellipPer = [x[3]*np.pi*((3*((x[1][0]/2)+(x[1][1]/2)))-\
                                    (((3*x[1][0]/2)+(x[1][1]/2))*\
                                     ((x[1][0]/2)+(3*x[1][1]/2)))**0.5)\
                        for x in dataDict[k]["Ellipse fit"]] #bounding ellipse perimeter (Ramanujan first approximation)
            
            
            area2_init = area2[0] #initial areas/lengths
            area3_init = area3[0]
            contLength_init = contLength[0] #initial lengths
            roilen_init = roilen[0]
##            print(self.indDict["time1_max"])

            area2_max = max(area2) #max area/lengths
            area3_max = max(area3)
            contLength_max = max(contLength)
            roilen_max = max(roilen)
            time2_max = sorted([[abs(a - self.indDict[k]["time1_max"]), a] \
                                     for a in self.time2], key=lambda l:l[0])[:2]
            logging.debug('%s', time2_max)

            wt_sum = time2_max[0][0] + time2_max[1][0] #take weighted avg
            wt = [time2_max[1][0]/wt_sum, time2_max[0][0]/wt_sum]
            try:
                area2_pulloff = np.average([area2[self.time2.index(
                    time2_max[0][1])],area2[self.time2.index(time2_max[1][1])]],
                                               weights = wt)
                area3_pulloff = np.average([area3[self.time2.index(
                    time2_max[0][1])],area3[self.time2.index(time2_max[1][1])]],
                                               weights = wt)
                contLength_pulloff = np.average([contLength[self.time2.index(
                    time2_max[0][1])],contLength[self.time2.index(time2_max[1][1])]],
                                               weights = wt)
                roilen_pulloff = np.average([roilen[self.time2.index(
                    time2_max[0][1])],roilen[self.time2.index(time2_max[1][1])]],
                                               weights = wt)
                ecc_pulloff = np.average([ecc[self.time2.index(
                    time2_max[0][1])],ecc[self.time2.index(time2_max[1][1])]],
                                               weights = wt)
                contnum_pulloff = int(np.average([contnum[self.time2.index(
                    time2_max[0][1])],contnum[self.time2.index(time2_max[1][1])]],
                                               weights = wt))
                #last area point of detachment step
                area2_residue = area2[sum(self.frame_num[:int(self.force_min_index/
                                                              self.ptsperstep)+1])-1]
            except Exception as e:
                logging.error(str(e))
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Analysis Error!", "Check force file/video file\n" +
                                    "Exception: " + str(e))
                root.destroy()
                area2_pulloff = 0
                return
                     
            logging.debug('%s, %s, %s, %s, %s', "adhesion calc", area2_max,
                          self.indDict[k]["time1_max"], time2_max, area2_pulloff)

##            if self.flag_lf == True or self.flag_lf_filter == True:
            force_lat_avg_index = int(mean([self.indDict[k]["force_lat_max_index"],
                                           self.indDict[k]["force_lat_min_index"]]))
            time1_lat_avg = time1[force_lat_avg_index]
            time2_lat_avg = sorted([[abs(a - time1_lat_avg), a] \
                                 for a in self.time2], key=lambda l:l[0])[:2]
            wt_sum2 = time2_lat_avg[0][0] + time2_lat_avg[1][0] #take weighted avg
            wt2 = [time2_lat_avg[1][0]/wt_sum2, time2_lat_avg[0][0]/wt_sum2]
            try:
                area_friction = np.average([area2[self.time2.index(
                    time2_lat_avg[0][1])],area2[self.time2.index(time2_lat_avg[1][1])]],
                                                weights = wt2)
            except Exception as e:
                logging.error(str(e))
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Analysis Error!", "Check force file/video file\n" +
                                "Exception: " + str(e))
                root.destroy()
                area_friction = 0
                return
            logging.debug('%s, %s, %s', "friction calc", area_friction, time1_lat_avg)
##            else:
##                area_friction = area2_init #zero
##                time1_lat_avg = 0
            
            self.indDict[k]["time1_lat_avg"] = time1_lat_avg

            #save contour properties to dictionary
            self.areaDict[k]["area2_init"] = area2_init
            self.areaDict[k]["area2_max"] = area2_max
            self.areaDict[k]["area3_init"] = area3_init
            self.areaDict[k]["area3_max"] = area3_max
            self.areaDict[k]["area2_pulloff"] = area2_pulloff
            self.areaDict[k]["area3_pulloff"] = area3_pulloff
            self.areaDict[k]["area_friction"] = area_friction
            self.areaDict[k]["area2_residue"] = area2_residue

            self.summaryDataDict['Contact area'][k]["Max Area"] = area2_max - area2_init
            self.summaryDataDict['Contact area'][k]["Pulloff Area"] = area2_pulloff - area2_init
            self.summaryDataDict['ROI area'][k]["ROI Max Area"] = area3_max
            self.summaryDataDict['ROI area'][k]["ROI Pulloff Area"] = area3_pulloff
            self.summaryDataDict['Contact area'][k]["Friction Area"] = area_friction - area2_init
            self.summaryDataDict['Contact area'][k]["Residue Area"] = area2_residue - area2_init

            self.lengthDict[k]["contLength_init"] = contLength_init
            self.lengthDict[k]["contLength_max"] = contLength_max
            self.lengthDict[k]["roilen_init"] = roilen_init
            self.lengthDict[k]["roilen_max"] = roilen_max
            self.lengthDict[k]["contLength_pulloff"] = contLength_pulloff
            self.lengthDict[k]["roilen_pulloff"] = roilen_pulloff
            # self.lengthDict[k]["ecc_pulloff"] = ecc_pulloff
            # self.lengthDict[k]["contnum_pulloff"] = contnum_pulloff
            
            self.summaryDataDict["Contact length"][k]["Max Length"] = contLength_max - contLength_init
            self.summaryDataDict["Contact length"][k]["Pulloff Length"] = contLength_pulloff - contLength_init
            self.summaryDataDict["ROI length"][k]["ROI Max Length"] = roilen_max
            self.summaryDataDict["ROI length"][k]["ROI Pulloff Length"] = roilen_pulloff
            
            self.summaryDataDict["Eccentricity"][k]["Pulloff Median Eccentricity"] = ecc_pulloff
            self.summaryDataDict['Contact number'][k]["Pulloff Contact Number"] = contnum_pulloff
            
            #get bounding ellipse properties at maximum contact
            ind_max = area2.index(area2_max) #index of maximum contact
            self.summaryDataDict['Contact area'][k]["Max Bounding Area"] = ellipAr[ind_max]
            self.summaryDataDict["Contact length"][k]["Max Bounding Perimeter"] = ellipPer[ind_max]
            self.summaryDataDict["Contact length"][k]["Max Bounding Length"] = ellipMajr[ind_max]
            self.summaryDataDict["Contact length"][k]["Max Bounding Width"] = ellipMinr[ind_max]
            
            
            #calculate full area
            area2_full = [area2_full[i] + area2[i] for i in range(len(area2))]
            i += 1
            
        #interpolate area data
        # area_interpol = [self.interpolData(self.time1[i], area2_full) \
        #                     for i in range(len(self.time1))]
        
        # if self.flag_st == True or self.flag_lf_filter == True: #stress   
        if self.configPlotWindow.plotDict['extras']['Stress'].isChecked() == True: #stress  
            #local stress dF/dA #CHECK
    ##        stress_local = np.diff(np.array(self.force_vert1))/np.diff(np.array(area_interpol))
    ##        self.stress = np.append(stress_local, stress_local[-1]) #make array size same as time1
            
            
            #stress F/A
            self.stress = [(self.fileDataDict["Vertical force"][i]-
                            self.fileDataDict["Vertical force"][0])/
                           (self.interpolData(time1[i], area2_full)-
                            self.interpolData(time1[0], area2_full)) for i \
                      in range(len(time1))]
            #noise filter stress using vertical force filter parameters
            window_length = self.analyzeDataWindow.dataAnalDict["Vertical force"]\
                ["transform"]["Filter window"]
            k_size = window_length+1 if window_length % 2 == 0 else window_length
            self.stress_filtered = medfilt(self.stress, kernel_size=k_size).tolist()
        
        logging.debug("get area finished")


#     def polyfitData(self, xdata, ydata, ax, x_plot, unit,
#                 eq_pos = [1,0.2], fit_order = 1, fit_show = False): #fit data and plot
#         data = zip(xdata, ydata, x_plot)
#         data = np.array(sorted(data, key = lambda x: x[0]))
#         coeff = np.polyfit(data[:,0],data[:,1], fit_order) #fitting coeffients
#         slope = coeff[0]
#         p_fit = np.poly1d(coeff)
#         y_fit = p_fit(data[:,0])
#         y_avg = np.sum(data[:,1])/len(data[:,1])
#         r2 = (np.sum((y_fit-y_avg)**2))/(np.sum((data[:,1] - y_avg)**2))
#         sign = '' if coeff[1] < 0 else '+'
#         eq_id = 'Slope'
#         eq_coff = ["$%.1e"%(coeff[i]) + "x^" + str(len(coeff) - i - 1) + "$"\
#              if i < len(coeff) - 2 else "%.4fx"%(coeff[i]) for i in range(len(coeff)-1)]
#         eq =  "y=" + '+'.join(eq_coff) + "+%.4f"%(coeff[len(coeff)-1]) + "; $R^2$=" + "%.4f"%(r2)  
#         eq_clean = eq.replace('+-', '-')
# ##        x_fit = np.linspace(min(data[:,0]), max(data[:,0]), 100)
#         ax.plot(data[:,2], y_fit, color = 'black',
#                 linewidth=2, linestyle='dashed')
# ##        print(eq_pos)
#         if fit_show == True:
#             ax.text(float(eq_pos[0]), float(eq_pos[1]), eq_id + ": " + "%.4f"%(slope) + ' (' + unit + ')',
#                     ha = 'right', transform=ax.transAxes, color = 'black',
#                     bbox=dict(facecolor='white', edgecolor = 'black', alpha=0.5))
#         print('data fitted', eq_clean)
#         return slope

#     def plotData(self, unit): #prepare plot

#         xDict = {'Vertical Position (μm)':self.dist_vert1,
#                  'Lateral Position (μm)':self.dist_lat1,
#                  'Deformation (μm)':self.deform_vert,
#                  'Time (s)':self.time1}
#         xAxisData = xDict.get(self.x_var)
        
#         markerlist = ["o", "v", "^", "s", "P", "*", "D", "<", "X", ">"]
#         linelist = [":", "-.", "--", "-", ":", "-.", "--", "-", ":", "-."]
        
#         self.fig1 = plt.figure(num="Force/Area vs Time", figsize = [11, 5])
#         self.fig1.canvas.mpl_connect('close_event', self.handle_close)
#         print("fig1")
#         self.fig1.clear()
#         ax1 = self.fig1.add_subplot(1,1,1)
#         lns = []
                
#         ax1.set_title('Speed = ' + str(self.speed_um) + ' μm/s')
#         ax1.set_xlabel(self.x_var)
#         ax1.set_ylabel('Vertical Force (μN)', color = 'r')
#         p1, = ax1.plot(xAxisData[self.plot_slice], self.force_vert1_shifted[self.plot_slice], 'ro',
#                      alpha=0.5, linewidth=1, markersize=1, label="Vertical Force")
#         lns.append(p1)

#         if self.ptsnumber != 0:
# ##            ptsperstep = int(self.ptsnumber/self.step_num)
#             i = 0
#             lns_reg = [] #region legend handle
#             lab_reg = [] #region legend label
#             for a in self.steps: #shade step regions
#                 if i < ((self.plot_slice.start+1)/self.ptsperstep)-1:
#                     i += 1
#                     continue
                
#                 if self.ptsperstep*(i+1)-1 > self.plot_slice.stop:
#                     endpoint = self.plot_slice.stop - 1
#                     exit_flag = True
#                 else:
#                     endpoint = self.ptsperstep*(i+1) - 1
#                     exit_flag = False
                
#                 if self.ptsperstep*i < self.plot_slice.start:
#                     startpoint = self.plot_slice.start
#                 else:
#                     startpoint = self.ptsperstep*i                   
                
#                 x_start = min(xAxisData[startpoint:endpoint])
#                 x_end = max(xAxisData[startpoint:endpoint])
#                 if a == 'Front':
#                     v1 = ax1.axvspan(x_start, x_end, alpha=0.9,
#                                     color='aliceblue', label = a)
#                     lns_reg.append(v1)
#                     lab_reg.append(a)
#                     if exit_flag == True:
#                         break
#                 elif a == 'Back':
#                     v2 = ax1.axvspan(x_start, x_end, alpha=0.9,
#                                 color='whitesmoke', label = a)
#                     lns_reg.append(v2)
#                     lab_reg.append(a)
#                     if exit_flag == True:
#                         break                    
#                 elif a == 'Up':
#                     v3 = ax1.axvspan(x_start, x_end, alpha=0.9,
#                                 color='honeydew', label = a)
#                     lns_reg.append(v3)
#                     lab_reg.append(a)
#                     if exit_flag == True:
#                         break                    
#                 elif a == 'Down':
#                     v4 = ax1.axvspan(x_start, x_end, alpha=0.9,
#                                 color='linen', label = a)
#                     lns_reg.append(v4)
#                     lab_reg.append(a)
#                     if exit_flag == True:
#                         break                    
#                 elif a == 'Pause':
#                     v5 = ax1.axvspan(x_start, x_end, alpha=0.9,
#                                 color='lightyellow', label = a)
#                     lns_reg.append(v5)
#                     lab_reg.append(a)
#                     if exit_flag == True:
#                         break
#                 i += 1
            
    
#         dict_reg = dict(zip(lab_reg, lns_reg)) #legend dictionary (remove dup)
#         self.fig1.legend(dict_reg.values(), dict_reg.keys(), loc='lower right',
#                          ncol=len(lns_reg))
        
#         if self.flag_ap == True: #show adhesion calc
#             #fill adhesion energy region 
#             ax1.fill_between(xAxisData[self.energy_slice],
#                              self.forceDict["zero1"][0],
#                              self.force_vert1_shifted[self.energy_slice],
#                              color = 'black') 
#             i = 0
#             for k in self.rangeDict.keys():
#                 if len(self.rangeDict.keys()) > 1 and k == "Default":
#                     continue
#                 ax1.axhline(y=self.forceDict["zero1"][i], color='y',
#                             alpha=1, linestyle=linelist[i], linewidth=1)                
#                 ax1.axhline(y=self.forceDict["force_min1"][i], color='y',
#                             alpha=1, linestyle=linelist[i], linewidth=1)
#                 ax1.axhline(y=self.forceDict["force_max1"][i], color='y',
#                             alpha=1, linestyle=linelist[i], linewidth=1)
#                 ax1.axvline(x=xAxisData[self.time1.index(self.indDict["time1_max"][i])], 
#                             color='y', alpha=1, linestyle=linelist[i], linewidth=1)
#                 i += 1

#         if self.flag_ca == True or self.flag_ra == True:
#             ax2 = ax1.twinx() #secondary axis
# ##                cmap = plt.cm.get_cmap("Reds")  # type: matplotlib.colors.ListedColormap
#             num = len(self.rangeDict.keys())
# ##                colors = plt.cm.Reds(np.linspace(0.3,1,num))
#             colors = plt.cm.Greens([0.7, 0.5, 0.9, 0.3, 1])
#             ax2.set_prop_cycle(color=colors)
#             ax2.set_ylabel('Area ($' + unit + '^2$)', color = 'g')
#             if self.flag_ca == True:
#                 i = 0
#                 for k in self.rangeDict.keys():
#                     if len(self.rangeDict.keys()) > 1 and k == "Default":
#                         continue
#                     p2, = ax2.plot(self.time2[self.plot_slice2],
#                                    self.dataDict[k][0][self.plot_slice2],
#                                    '-' + markerlist[i], alpha=0.5,
#                                    linewidth=1, markersize=2,
#                                    label="Contact Area: " + k)
#                     lns.append(p2)
#                     if self.flag_ap == True:
#                         ax2.plot(self.indDict["time1_max"][i],
#                                  self.areaDict["area2_pulloff"][i],
#                                  'y' + markerlist[i], alpha=0.8)
#                     i += 1
#             if self.flag_ra == True: #consider first key since auto roi is same for all keys
#                 colors = plt.cm.Blues([0.7, 0.5, 0.9, 0.3, 1])
#                 ax2.set_prop_cycle(color=colors)
#                 j = 0
#                 for k in self.rangeDict.keys():
#                     if len(self.rangeDict.keys()) > 1 and k == "Default":
#                         continue                
#                     p3, = ax2.plot(self.time2[self.plot_slice2],
#                                    self.dataDict[k][3][self.plot_slice2],
#                                    '-' + markerlist[j], alpha=0.5, linewidth=1, markersize=2,
#                                    label="ROI Area: " + k)
#                     lns.append(p3)
#                     j += 1

        
#         if self.flag_lf == True:
#             ax3 = ax1.twinx() #lateral force
#             ax3.set_ylabel('Lateral Force (μN)', color = 'c')
#             ax3.spines['left'].set_position(('outward', 60))
#             ax3.spines["left"].set_visible(True)
#             ax3.yaxis.set_label_position('left')
#             ax3.yaxis.set_ticks_position('left')
#             if self.invert_latf == True:
#                 ax3.invert_yaxis()
#             if self.flag_lf == True:
#                 p4, = ax3.plot(xAxisData[self.plot_slice], self.force_lat1_shifted[self.plot_slice], 'co',
#                      alpha=0.5, linewidth=1, markersize=1, label="Lateral Force")

# ##            if self.flag_lf_filter == True:
# ##                p4, = ax3.plot(self.time1[self.plot_slice], self.force_lat1_filtered_shifted[self.plot_slice], '-c',
# ##                     alpha=0.5, linewidth=1, label="Lateral Force")

#             if self.flag_fp == True: #show friction calc
#                 i = 0
#                 for k in self.rangeDict.keys():
#                     if len(self.rangeDict.keys()) > 1 and k == "Default":
#                         continue
#                     ax3.axhline(y=self.forceDict["force_lat_max"][i],
#                                 color='g', alpha=1,
#                                 linestyle=linelist[i], linewidth=1)
#                     ax3.axhline(y=self.forceDict["force_lat_min"][i],
#                                 color='g', alpha=1,
#                                 linestyle=linelist[i], linewidth=1)
#                     ax1.axhline(y=self.forceDict["force_max2"][i],
#                                 color='g', alpha=1,
#                                 linestyle=linelist[i], linewidth=1)
#                     ax3.axvline(x=xAxisData[self.time1.index(self.indDict["time1_lat_avg"][i])],
#                                 color='g', alpha=1,
#                                 linestyle=linelist[i], linewidth=1)
#                     ax2.plot(self.indDict["time1_lat_avg"][i],
#                              self.areaDict["area_friction"][i],
#                              'g' + markerlist[i], alpha=0.8)
#                     i += 1
#                 ax3.axhline(y=self.forceDict["zero2"],
#                             color='g', alpha=0.5,
#                             linestyle=linelist[0], linewidth=1)                
#             lns.append(p4)
#         else:
#             ax3 = None

#         if self.flag_zp == True or self.flag_xp == True or self.flag_zd: #piezo position/deformation
#             ax4 = ax1.twinx() #piezo waveform
#             ax4.set_ylabel('Displacement (μm)', color = 'violet')
#             if self.flag_ca == True or self.flag_ra == True: #shift axis if area plotted
#                 ax4.spines['right'].set_position(('outward', 70))
# ##                ax4.invert_yaxis()
#             if self.flag_zp == True:
#                 p5, = ax4.plot(xAxisData[self.plot_slice], self.dist_vert1[self.plot_slice], '-',
#                      markersize=1, color = 'violet',
#                                alpha=0.5, label="Vertical Piezo")
#                 lns.append(p5)
#             if self.flag_xp == True:
#                 p6, = ax4.plot(xAxisData[self.plot_slice], self.dist_lat1[self.plot_slice], '-.',
#                      markersize=1, color = 'violet',
#                                alpha=0.5, label="Lateral Piezo")
#                 lns.append(p6)
#             if self.flag_zd == True: #actual deformation plot
#                 p12, = ax4.plot(xAxisData[self.plot_slice], self.deform_vert[self.plot_slice], '-o',
#                      markersize=1, color = 'violet',
#                      alpha=0.5, label="Deformation")
#                 if self.flag_ap == True:
#                     ax1.axvline(x=xAxisData[self.deform_tol], color='violet', 
#                                 alpha=1, linestyle=":", linewidth=1)
#                 lns.append(p12)
                
#         if self.flag_cl == True or self.flag_rl == True:
#             ax5 = ax1.twinx()
#             num = len(self.rangeDict.keys())
#             colors = plt.cm.copper(np.linspace(0.2,0.7,num))
#             ax5.set_prop_cycle(color=colors)
#             ax5.set_ylabel('Length ($' + unit + '$)', color = 'brown')
#             if self.flag_ca == True or self.flag_ra == True: 
#                 ax5.spines['right'].set_position(('outward', 70))            
#             if self.flag_cl == True: #contact length
#                 i = 0
#                 for k in self.rangeDict.keys():
#                     if len(self.rangeDict.keys()) > 1 and k == "Default":
#                         continue                    
#                     p7, = ax5.plot(self.time2[self.plot_slice2],
#                                    self.dataDict[k][1][self.plot_slice2],
#                                    '-' + markerlist[i], alpha=0.5, linewidth=1,
#                                    markersize=2, label="Contact Length: " + k)
#                     lns.append(p7)
#                     i += 1
#             if self.flag_rl == True: #roi length
# ##                ax5 = ax1.twinx()
#                 num = len(self.rangeDict.keys())
#                 colors = plt.cm.Wistia(np.linspace(0.2,0.7,num))
#                 ax5.set_prop_cycle(color=colors)
# ##                ax5.spines['right'].set_position(('outward', 70))
#                 j = 0
#                 for k in self.rangeDict.keys():
#                     if len(self.rangeDict.keys()) > 1 and k == "Default":
#                         continue
# ##                    ax5.set_ylabel('Length ($' + unit + '$)', color = 'brown')
#                     p8, = ax5.plot(self.time2[self.plot_slice2],
#                                    self.dataDict[k][4][self.plot_slice2],
#                                    '-' + markerlist[j], alpha=0.5, linewidth=1,
#                                    markersize=2, label="ROI Length: " + k)
#                     lns.append(p8)
#                     j += 1
#         if self.flag_cn == True: #contact number
#             ax5 = ax1.twinx()
#             num = len(self.rangeDict.keys())
#             colors = plt.cm.copper(np.linspace(0.2,0.7,num))
#             ax5.set_prop_cycle(color=colors)
#             ax5.spines['right'].set_position(('outward', 70))
#             i = 0
#             for k in self.rangeDict.keys():
#                 if len(self.rangeDict.keys()) > 1 and k == "Default":
#                     continue
#                 ax5.set_ylabel('Number', color = 'brown')
#                 p9, = ax5.plot(self.time2[self.plot_slice2],
#                                self.dataDict[k][2][self.plot_slice2],
#                                '-' + markerlist[i], alpha=0.5, linewidth=1,
#                                markersize=2, label="Contact Number: " + k)
#                 lns.append(p9)
#                 i += 1
#         if self.flag_ecc == True: #contact eccentricity
#             ax5 = ax1.twinx()
#             num = len(self.rangeDict.keys())
#             colors = plt.cm.copper(np.linspace(0.2,0.7,num))
#             ax5.set_prop_cycle(color=colors)
#             ax5.spines['right'].set_position(('outward', 70))
#             i = 0
#             for k in self.rangeDict.keys():
#                 if len(self.rangeDict.keys()) > 1 and k == "Default":
#                     continue
#                 ax5.set_ylabel('Eccentricity' + unit + '$)', color = 'brown')
#                 p10, = ax5.plot(self.time2[self.plot_slice2],
#                                 self.dataDict[k][5][self.plot_slice2],
#                                 '-' + markerlist[i], alpha=0.5, linewidth=1,
#                                 markersize=2, label="Median Eccentricity: " + k)
#                 lns.append(p10)
#                 i += 1
        
#         if self.flag_st == True or self.flag_lf_filter == True: #stress
#             ax6 = ax1.twinx() 
#             ax6.set_ylabel('Stress (μN/$' + unit + '^2$)', color = 'c')
#             ax6.spines['left'].set_position(('outward', 60))
#             ax6.spines["left"].set_visible(True)
#             ax6.yaxis.set_label_position('left')
#             ax6.yaxis.set_ticks_position('left')
#             if self.flag_st == True:
#                 p11, = ax6.plot(xAxisData[self.plot_slice],
#                                 self.stress[self.plot_slice], 'co',
#                                 alpha=0.5, linewidth=1, markersize=1,
#                                 label="Stress")                            
#             if self.flag_lf_filter == True:
#                 p11, = ax6.plot(xAxisData[self.plot_slice],
#                                 self.stress_filtered[self.plot_slice], '-c',
#                                 alpha=0.5, linewidth=1, markersize=1,
#                                 label="Stress")

#             lns.append(p11)
            
# ##            lns = [p1, p3, p2, p4, p5]
# ##        else:
# ##            lns = [p1, p2]

#         ax1.legend(handles=lns, loc = self.legendPos)

#         if self.flag_fit == True:
#             axDict = {'Vertical Force (μN)':ax1, 'Lateral Force (μN)':ax3}
#             yDict = {'Vertical Force (μN)':self.force_vert1_shifted,
#                      'Lateral Force (μN)':self.force_lat1_shifted}
#             fit_slice = slice(int(self.startFit * self.ptsnumber/100),
#                               int(self.endFit * self.ptsnumber/100))
#             self.slope_unit = self.fit_y.split('(')[1].split(')')[0] + '/' +\
#                               self.fit_x.split('(')[1].split(')')[0]
#             text_pos = self.fit_pos.split(",")
            
#             self.slope = self.fitData(xDict.get(self.fit_x)[fit_slice], yDict.get(self.fit_y)[fit_slice],
#                                      axDict.get(self.fit_y), xAxisData[fit_slice], unit = self.slope_unit,
#                                      eq_pos = text_pos, fit_order = 1, fit_show = self.fit_show)
#         else:
#             self.slope = ''
#             self.slope_unit = ''
#         self.fig1.tight_layout()

# ##            print(e)
# ##            messagebox.showinfo("Plot Error!", "Check force file/video file\n" +
# ##                                "Exception: " + str(e))
        
#     def showPlot(self): #show plot
# ##        self.fig1.show()
#         try:
#             plt.pause(0.05)
#             self.fig1.canvas.draw()
#         except Exception as e:
#             print(e)
            
# ##        plt.show(block=False)
# ##        plt.draw()

#     def handle_close(self, evt): #figure closed event
#         self.fig1_close = True
    
#     def convertPlot(self): #convert plot to numpy
#         self.fig1.canvas.draw()
#         data = np.fromstring(self.fig1.canvas.tostring_rgb(),
#                              dtype=np.uint8, sep='')
#         data = data.reshape(self.fig1.canvas.get_width_height()[::-1] + (3,))
#         return data

#     def savePlot(self, filepath): #save force plots
#         print("save plot")
#         self.fig1.savefig(filepath, orientation='landscape',
#                           transparent = True)
    
    #find corresponding unit from the different unit dictionaries
    def findUnit(self, key):
        if key in self.unitDict.keys():
            return self.unitDict[key].replace('$', '')
        elif key in self.imageDataUnitDict.keys():
            return self.imageDataUnitDict[key].replace('$', '')
        elif key in self.miscUnitDict.keys():
            return self.miscUnitDict[key].replace('$', '')
        else:
            return '' #no unit
        
    
    def saveSummaryData(self, videofile1, videofile2, zeroforcefile, imageDataUnitDict, 
                        msrmnt_num, summary_filepath): #save and append data
        logging.debug("save summary")
##        self.summary_filepath = os.path.dirname(os.path.dirname(
##            self.force_filepath))+ "/Analysis/Summary/summary data.txt"
#         if os.path.exists(summary_filepath) == False:
#             with open(summary_filepath, "w", encoding="utf-8") as f:
# ##                f.write("Lateral Force Calib [μN] \t" + self.calib_lat1 + "\n")
#                 f.write("Max Area [" + unit + "^2]\tPulloff Area [" + unit + "^2]\tAdhesion [μN]\t" +
#                         "Adhesion Preload [μN]\tContact Time[s]\tSpeed [μm/s]\t" +
#                         "Steps\tFriction [μN]\tFriction Area [" + unit + "^2]\t" +
#                         "Friction Preload [μN]\tMeasurement number\t" +
#                         "Measurement OK?\tROI Labels\t" +
#                         "Step Dictionary\tVertical Force Stdev\t" +
#                         "Lateral Force Stdev\tSliding Step\t" +
#                         "ROI Max Area [" + unit + "^2]\tROI Pulloff Area [" + unit + "^2]\t" +
#                         "Max Length [" + unit + "]\tPulloff Length [" + unit + "]\t" +
#                         "ROI Max Length [" + unit + "^2]\tROI Pulloff Length [" + unit + "^2]\t" +
#                         "Pulloff Median Eccentricity\tPulloff Contact Number\t" +
#                         "Residue Area [" + unit + "^2]\tSlope [" + self.slope_unit + "]\t" + 
#                         "Beam Spring Constant [μN/μm]\tBeam Spring Constant Stdev\t" + 
#                         "Initial Deformation[μm]\tPulloff Deformation[μm]\tAdhesion Energy [pJ]\t" +
#                         "Max Bounding Area [" + unit + "^2]\t Max Bounding Perimeter [" + unit + "]\t" +
#                         "Max Bounding Length [" + unit + "]\tMax Bounding Width [" + unit + "]\t" +
#                         "Video file\tForce data file\t2nd Video file\tZero-Force file\n")

##        max_area = [self.areaDict["area2_max"][k] - self.areaDict["area2_init"][k] \
##                    for k in range(0, len(self.dataDict.keys())-1)]
##        pulloff_area = [self.areaDict["area_pulloff"][k] - self.areaDict["area2_init"][k] \
##                    for k in range(0, len(self.dataDict.keys())-1)]
##        friction_area = [self.areaDict["area_friction"][k] - self.areaDict["area2_init"][k] \
##                    for k in range(0, len(self.dataDict.keys())-1)]
        
#         roi_label = []
#         max_area2 = []
#         pulloff_area2 = []
#         max_area3 = []
#         pulloff_area3 = []
#         friction_area = []
#         max_contLength = []
#         pulloff_contLength = []
#         max_roilen = []
#         pulloff_roilen = []
#         pulloff_ecc = []
#         pulloff_contnum = []
#         residue_area2 = []
#         adhesion = []
#         preload1 = []
# ##        contact_time = []
#         friction = []
#         preload2 = []
#         elip_area = []
#         elip_per = []
#         elip_maj = []
#         elip_min = []
#         i = 0
        self.imageDataUnitDict = imageDataUnitDict
        # self.summaryDataDict['data params'] = {}
        
        self.summaryDataDict['measurement params']['Measurement number'] = msrmnt_num
        self.summaryDataDict['measurement params']['Measurement OK?'] = 'Y' #CHANGE!
        # self.summaryDataDict['data params']["Steps"] = self.steps        
        self.summaryDataDict['misc']["Sliding Step"] = self.slideStep
        
        kBeam = self.analyzeDataWindow.dataAnalDict['misc settings']['beam spring constant'].text()
        # self.fileDataDict2["Beam Spring Constant"] = kBeam.split(',')[0]
        # self.fileDataDict2["Beam Spring Constant Stdev"] = kBeam.split(',')[1]
        self.summaryDataDict['data params']["Spring Constant"] = {}
        self.summaryDataDict['data params']["Spring Constant"]["Beam Spring Constant"] = kBeam.split(',')[0]
        self.summaryDataDict['data params']["Spring Constant"]["Beam Spring Constant Stdev"] = kBeam.split(',')[1]
        
        # self.fileDataDict2["Slope"] = self.slope
        self.summaryDataDict['misc']["Slope"] = self.slope
        
        self.miscUnitDict = {'Adhesion Energy': ' [pJ]',
                             'Spring Constant': ' [μN/μm]',
                             'Slope': ' [' + self.slope_unit + ']'}
        
        roi_list = self.analyzeDataWindow.dataAnalDict["Vertical force"]["ranges"].keys()
        for k in roi_list:
            # print(i)
            if len(roi_list) > 1 and k == "Default":
                continue
            
            self.summaryDataDict['measurement params']["ROI Label"] = k
            summary_filepath_new = summary_filepath[:-4] + '(' + k + ')' + summary_filepath[-4:]
            
            header_list = []
            if os.path.exists(summary_filepath_new) == False:
                for x in self.summaryDataDict.keys():
                    if x in ['measurement params', 'misc']:
                        for y in self.summaryDataDict[x].keys():
                            unit = self.findUnit(y)
                            header_list.append(y + unit)
                    elif x == 'data params':
                        for y in self.summaryDataDict[x].keys():
                            unit = self.findUnit(y)
                            for z in self.summaryDataDict[x][y].keys():
                                header_list.append(z + unit)
                    else:
                        unit = self.findUnit(x)
                        for y in self.summaryDataDict[x][k].keys():
                            header_list.append(y + unit)
                
                header = '\t'.join(header_list) + '\t' + \
                    "Force data file\tZero-Force file\tVideo file\t2nd Video file\n"     
                            
                # header = "Measurement number\tMeasurement OK?\tROI Label\t" + \
                #     '\t'.join(self.speedDict.keys()) + '\t' + \
                #     '\t'.join(self.fileDataDict2.keys()) + '\t' + \
                #     '\t'.join(self.summaryDataDict[k].keys()) + '\t' + \
                #     "Force data file\tZero-Force file\tVideo file\t2nd Video file\n"                  
                with open(summary_filepath_new, "w", encoding="utf-8") as f:
                    f.write(header)
            
            data_list = []
            for x in self.summaryDataDict.keys():
                if x in ['measurement params', 'misc']:
                    for y in self.summaryDataDict[x].keys():
                        data_list.append(self.summaryDataDict[x][y])
                elif x == 'data params':
                    for y in self.summaryDataDict[x].keys():
                        for z in self.summaryDataDict[x][y].keys():
                            data_list.append(self.summaryDataDict[x][y][z])
                else:
                    for y in self.summaryDataDict[x][k].keys():
                        data_list.append(self.summaryDataDict[x][k][y])            
            # for x in self.summaryDataDict.keys():
            #     if x in ['measurement params', 'misc']:
            #         for y in self.summaryDataDict[x].keys():
            #             data_list.append(self.summaryDataDict[x][y])
            #     # elif x == 'misc':
            #     #     for y in self.summaryDataDict[x].keys():
            #     #         data_list.append(self.summaryDataDict[x][y])
            #     else:
            #         for y in self.summaryDataDict[x][k].keys():
            #             data_list.append(self.summaryDataDict[x][k][y])
            
            data_string = '\t'.join(map(str,data_list)) + '\t' + \
                self.force_filepath.split('/')[-1][:-4] + '\t' + \
                zeroforcefile + '\t' +  videofile1 + '\t' + \
                videofile2 + '\n'
                            
            # # data_string = str(msrmnt_num) + '\tY\t' + k + '\t' + \
            # #     '\t'.join(map(str, self.speedDict.values())) + '\t' + \
            # #     '\t'.join(map(str, self.fileDataDict2.values())) + '\t' + \
            # #     '\t'.join(map(str, self.summaryDataDict[k].values())) + '\t' + \
            # #     self.force_filepath.split('/')[-1][:-4] + '\t' + \
            # #     zeroforcefile + '\t' +  videofile1 + '\t' + \
            # #     videofile2 + '\n'
                
            with open(summary_filepath_new, "a") as f:
                f.write(data_string)
                
#             roi_label.append(k)
#             max_area2.append(self.areaDict["area2_max"][i] -
#                              self.areaDict["area2_init"][i])
#             pulloff_area2.append(self.areaDict["area2_pulloff"][i] -
#                                  self.areaDict["area2_init"][i])
#             max_area3.append(self.areaDict["area3_max"][i])
#             pulloff_area3.append(self.areaDict["area3_pulloff"][i])
#             friction_area.append(self.areaDict["area_friction"][i] -
#                                  self.areaDict["area2_init"][i])
#             max_contLength.append(self.lengthDict["contLength_max"][i] -
#                             self.lengthDict["contLength_init"][i])
#             pulloff_contLength.append(self.lengthDict["contLength_pulloff"][i] -
#                                       self.lengthDict["contLength_init"][i])
#             max_roilen.append(self.lengthDict["roilen_max"][i])
#             pulloff_roilen.append(self.lengthDict["roilen_pulloff"][i])
#             pulloff_ecc.append(self.lengthDict["ecc_pulloff"][i])
#             pulloff_contnum.append(self.lengthDict["contnum_pulloff"][i])
#             residue_area2.append(self.areaDict["area2_residue"][i] -
#                                  self.areaDict["area2_init"][i])            
#             adhesion.append(self.forceDict["force_adhesion1"][i])
#             preload1.append(self.forceDict["force_preload1"][i])
# ##            contact_time.append(self.indDict["contact_time1"][i])
#             friction.append(self.forceDict["force_friction"][i])
#             preload2.append(self.forceDict["force_preload2"][i])
#             elip_area.append(self.ellipDict["ellipAr_max"][i])
#             elip_per.append(self.ellipDict["ellipPer_max"][i])
#             elip_maj.append(self.ellipDict["ellipMajr_max"][i])
#             elip_min.append(self.ellipDict["ellipMinr_max"][i])
            
#             i += 1
        
        
        
            # with open(summary_filepath, "a") as f:
            #     f.write(str(max_area2)+'\t' +
            #             str(pulloff_area2)+'\t' +
            #             str(adhesion) + '\t' +
            #             str(preload1) +'\t' +
            #             str(self.contact_time1) +'\t' +
            #             str(self.speed_um) + '\t' + str(self.steps) + '\t' +
            #             str(friction) + '\t' +
            #             str(friction_area) + '\t' +
            #             str(preload2) + '\t' +
            #             str(msrmnt_num) + '\tY\t' +
            #             str(roi_label) + '\t' + str(self.speedDict) + '\t' +
            #             str(self.forceDict["zero1_stdv"]) + '\t' +
            #             str(self.forceDict["zero2_stdv"]) + '\t' +
            #             self.slideStep + '\t' +
            #             str(max_area3)+'\t' +
            #             str(pulloff_area3)+'\t' +
            #             str(max_contLength)+'\t' +
            #             str(pulloff_contLength)+'\t' +
            #             str(max_roilen)+'\t' +
            #             str(pulloff_roilen)+'\t' +
            #             str(pulloff_ecc)+'\t' +
            #             str(pulloff_contnum)+'\t' +
            #             str(residue_area2)+'\t' + str(self.slope) + '\t' +
            #             kBeam.split(',')[0] + '\t' + kBeam.split(',')[1] + '\t' +
            #             str(self.deform_init) + '\t' + str(self.deform_pulloff) + '\t' +
            #             str(self.energy_adhesion) + '\t' +
            #             str(elip_area)+'\t' + str(elip_per) + '\t' +
            #             str(elip_maj)+'\t' + str(elip_min) + '\t' +
            #             videofile1 + '\t' +
            #             self.force_filepath.split('/')[-1][:-4] +
            #             '\t' + videofile2 +
            #             '\t' + zeroforcefile + '\n')
        

##a = ForceData()
##a.importData()
##print("end")
####a.getArea([1,2,3], [4,5,6])
####a.plotData()
####a.savePlot("C:/Users/sudersanp/Desktop/Work/Codes/Video Analyser/test123")
####a.saveSummaryData()
##a.plotSummary()
##a.showSummaryPlot()
