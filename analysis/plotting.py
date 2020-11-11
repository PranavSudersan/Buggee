# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:49:51 2020

@author: adwait
"""
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
# import source.analysis.fitting as fitting
import pickle

from source.analysis.plot2widget import PlotWidget
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout

class Plotting:
    
    def __init__(self, fitWindow, configPlotWindow):
        self.fitWindow = fitWindow
        self.configPlotWindow = configPlotWindow
        #plot display flags
        # self.flag_ca = True
        # self.flag_ra = False
        # self.flag_cl = False
        # self.flag_rl = False
        # self.flag_cn = False
        # self.flag_ecc = False
        # self.flag_vf = True
        # self.flag_lf = False 
        # self.flag_zp = False
        # self.flag_xp = False
        # self.flag_ap = False
        # self.flag_fp = False
        # self.flag_st = False
        # self.flag_zd = False
        # self.invert_latf = False
        # self.x_var = 'Time' #x axis default parameter
        # self.legendPos = "upper right"
        # self.fig1_close = True
        # self.show_title = True
        # self.showLegend2 = True
        # self.fontSize = 12
        #fitting
        # self.flag_fit = False
        # self.fit_x = 'Vertical Position (μm)'
        # self.fit_y = 'Vertical Force'
        # self.startFit = 0
        # self.endFit = 100
        self.fit_pos = [0.5,0.5]
        # self.fit_show = False
        self.slope = ''
        self.slope_unit = ''
        self.fitTextBox = None
        
        self.markerlist = ["o", "v", "^", "s", "P", "*", "D", "<", "X", ">"]
        self.linelist = [":", "-.", "--", "-", ":", "-.", "--", "-", ":", "-."]
        # num = len(self.rangeDict.keys())
        # self.colorDict =  {'Green':plt.cm.Greens([0.7, 0.5, 0.9, 0.3, 1]),
        #                    'Blue':plt.cm.Blues([0.7, 0.5, 0.9, 0.3, 1]),
        #                    'Copper':plt.cm.copper([0.3, 0.9, 0.5, 0.7, 1]),
        #                    'Wistia':plt.cm.Wistia([0.7, 0.5, 0.9, 0.3, 1])}
        self.sourceLabel = None
        #initialize figure with random data
        self.fig1 = Figure(figsize=(11, 5), dpi=100)
        ax = self.fig1.add_subplot(111)
        self.xAxisData = np.linspace(0, 4, 50)
        ydata = np.sin(self.xAxisData)
        self.fixYLimits = True
        ax.plot(self.xAxisData, ydata, 'r-', linewidth=1, markersize=1)
        
        self.plotWidget = PlotWidget(fig = self.fig1,
                                         cursor1_init=0,
                                         cursor2_init=None,
                                         fixYLimits = self.fixYLimits,
                                         method = self.updatePosition)

        
    def plotData(self, imageDataUnitDict): #prepare plot
        #plot settings parameters
        self.x_var = self.configPlotWindow.plotDict['plot settings']['x axis'].currentText() #x axis default parameter
        legendPos = self.configPlotWindow.plotDict['plot settings']['legend position'].text()
        show_title = self.configPlotWindow.plotDict['plot settings']['show title'].isChecked()
        showLegend2 = self.configPlotWindow.plotDict['plot settings']['show step legend'].isChecked()
        # figsize = self.configPlotWindow.plotDict['plot settings']['figure size'].text()
        plot_style = self.configPlotWindow.plotDict['plot settings']['style'].currentText()
        self.fontSize = self.configPlotWindow.plotDict['plot settings']['font size'].value()
        self.lineWidth = self.configPlotWindow.plotDict['plot settings']['line width'].value()
        self.markerSize = self.configPlotWindow.plotDict['plot settings']['marker size'].value()
        self.opacity = self.configPlotWindow.plotDict['plot settings']['opacity'].value()
        self.fixYLimits = self.configPlotWindow.plotDict['plot settings']['fix y bounds'].isChecked()
        self.zeroShiftY = self.configPlotWindow.plotDict['plot settings']['zero shift Y'].isChecked()
        # self.plot_slice = self.configPlotWindow.plotDict['plot settings']['plot range']
        stress_show = self.configPlotWindow.plotDict['extras']['Stress'].isChecked()
        adhesion_show = self.configPlotWindow.plotDict['extras']['Adhesion'].isChecked()
        friction_show = self.configPlotWindow.plotDict['extras']['Friction'].isChecked()
        steps_show = self.configPlotWindow.plotDict['extras']['Steps'].isChecked()
        self.fit_show = self.configPlotWindow.plotDict['extras']['Fit'].isChecked()
        
        deform_range = eval(self.analyzeDataWindow.dataAnalDict['misc settings']['deformation range'].text())
        
        # xDict = {'Vertical Position (μm)':self.dist_vert1,
        #          'Lateral Position (μm)':self.dist_lat1,
        #          'Deformation (μm)':self.deform_vert,
        #          'Time (s)':self.time1}
        # self.xAxisData = xDict.get(self.x_var)
        
        # self.fileDataDict = {'Time': self.time1,
        #               'Vertical force': self.force_vert1_shifted,
        #               'Lateral force': self.force_lat1_shifted,
        #               'Vertical piezo': self.dist_vert1,
        #               'Lateral piezo': self.dist_lat1,
        #               'Deformation': self.deform_vert}
        
        #image data units
        self.imageDataUnitDict = imageDataUnitDict
        
        self.xAxisData = self.fileDataDict.get(self.x_var)
        
        # markerlist = ["o", "v", "^", "s", "P", "*", "D", "<", "X", ">"]
        seaborn_styles = ['seaborn-bright','seaborn-colorblind','seaborn-dark-palette',
                          'seaborn-dark','seaborn-darkgrid','seaborn-deep','seaborn-muted',
                          'seaborn-notebook','seaborn-paper','seaborn-pastel',
                          'seaborn-poster','seaborn-talk','seaborn-ticks',
                          'seaborn-white','seaborn-whitegrid']
        
        matplotlib.style.use("default")
        if plot_style in seaborn_styles: #initialize seaborn
            matplotlib.style.use("seaborn")
        matplotlib.style.use(plot_style)
        
        self.fig1.set_facecolor(matplotlib.rcParams["figure.facecolor"])
        self.fig1.set_edgecolor(matplotlib.rcParams["figure.edgecolor"])
        matplotlib.rcParams.update({'font.size': self.fontSize})
        self.fig1.set_size_inches(self.fig1.get_size_inches())

        print("fig resize")
        # self.fig1.canvas.draw()
        # self.fig1 = plt.figure(num="Force/Area vs Time", figsize = [11, 5])
        # self.fig1 = Figure(figsize=(11, 5), dpi=100)
        
        # self.fig1.canvas.mpl_connect('close_event', self.handle_close)
        
        print("fig1")
        
        #store cursor position values before clearing plot
        # if self.plotWidget.wid.cursor1 == None:
        #     c1_init = None
        # else:
        c1_init = self.plotWidget.wid.cursor1.get_xdata()[0]
        
        # if self.plotWidget.wid.cursor2 == None:
        c2_init = None
        # else:
        #     c2_init = self.plotWidget.wid.cursor2.get_xdata()[0]
            
        self.fig1.clear()
        # self.fig1.suptitle("Hey there!")
        # self.fig1.__init__(figsize=(11, 5), dpi=100)
        # self.plotWidget.fig = self.fig1

        # self.plotWidget.__init__(fig = self.fig1,
        #                          cursor1_init=c1_init,
        #                          cursor2_init=c2_init,
        #                          fixYLimits = self.fixYLimits,
        #                          method = self.updatePosition)
        
        ax1 = self.fig1.add_subplot(1,1,1)
        ax1.yaxis.set_visible(False)
        ax1.set_xlabel(self.x_var + self.unitDict[self.x_var])
        lns = []
                      
        # ax1.set_title('Speed = ' + str(self.speed_um) + ' μm/s')
        # if self.flag_vf == True: 
        #     ax1.yaxis.set_visible(True)
        #     # ax1.spines['right'].set_position(('outward', 0))
        #     # ax1.spines["right"].set_visible(True)            
        #     # ax1.yaxis.set_label_position('right')
        #     # ax1.yaxis.set_ticks_position('right')
        #     self.updateAxisPos(ax1, 'left', 0) 
        #     ax1.set_xlabel(self.x_var)
        #     ax1.set_ylabel('Vertical Force (μN)', color = 'r')
        #     p1, = ax1.plot(self.xAxisData[self.plot_slice], self.force_vert1_shifted[self.plot_slice], 'ro',
        #                  alpha=0.5, linewidth=1, markersize=1, label="Vertical Force")
        #     lns.append(p1)
        

        # self.plotWidget.mpl_connect('close_event', self.handle_close)
        if steps_show == True:
            if self.ptsnumber != 0:
    ##            ptsperstep = int(self.ptsnumber/self.step_num)
                i = 0
                lns_reg = [] #region legend handle
                lab_reg = [] #region legend label
                speed_inview = [] #speed list in plot range
                for a in self.steps: #shade step regions
                    if i < ((self.plot_slice.start+1)/self.ptsperstep)-1:
                        i += 1
                        continue
                    
                    if self.ptsperstep*(i+1)-1 > self.plot_slice.stop:
                        endpoint = self.plot_slice.stop - 1
                        exit_flag = True
                    else:
                        endpoint = self.ptsperstep*(i+1) - 1
                        exit_flag = False
                    
                    if self.ptsperstep*i < self.plot_slice.start:
                        startpoint = self.plot_slice.start
                    else:
                        startpoint = self.ptsperstep*i                   
                    
                    x_start = min(self.xAxisData[startpoint:endpoint])
                    x_end = max(self.xAxisData[startpoint:endpoint])
                    if a == 'Front':
                        v1 = ax1.axvspan(x_start, x_end, alpha=0.9,
                                        color='aliceblue', label = a)
                        lns_reg.append(v1)
                        lab_reg.append(a)
                        speed_inview.append(self.speed_um[i])
                        if exit_flag == True:
                            break
                    elif a == 'Back':
                        v2 = ax1.axvspan(x_start, x_end, alpha=0.9,
                                    color='whitesmoke', label = a)
                        lns_reg.append(v2)
                        lab_reg.append(a)
                        speed_inview.append(self.speed_um[i])
                        if exit_flag == True:
                            break                    
                    elif a == 'Up':
                        v3 = ax1.axvspan(x_start, x_end, alpha=0.9,
                                    color='honeydew', label = a)
                        lns_reg.append(v3)
                        lab_reg.append(a)
                        speed_inview.append(self.speed_um[i])
                        if exit_flag == True:
                            break                    
                    elif a == 'Down':
                        v4 = ax1.axvspan(x_start, x_end, alpha=0.9,
                                    color='linen', label = a)
                        lns_reg.append(v4)
                        lab_reg.append(a)
                        speed_inview.append(self.speed_um[i])
                        if exit_flag == True:
                            break                    
                    elif a == 'Pause':
                        v5 = ax1.axvspan(x_start, x_end, alpha=0.9,
                                    color='lightyellow', label = a)
                        lns_reg.append(v5)
                        lab_reg.append(a)
                        speed_inview.append(self.speed_um[i])
                        if exit_flag == True:
                            break
                    i += 1
        
            if show_title == True:
                title = 'Speed = ' + str(speed_inview).replace('[','').replace(']','') + ' μm/s'
                ax1.text(0.5, 1.05, title, ha = 'center', transform=ax1.transAxes, 
                          fontsize = 'large', color = 'black', picker = 5)
                # self.fig1.suptitle(title)
                # ax1.set_title('Speed = ' + str(speed_inview).replace('[','').replace(']','') 
                #               + ' μm/s')
            if showLegend2 == True:
                dict_reg = dict(zip(lab_reg, lns_reg)) #legend dictionary (remove dup)
                self.fig1.legend(dict_reg.values(), dict_reg.keys(), loc='lower right',
                                  ncol=len(lns_reg))

        self.imageAxisDict = {} #active axes of image analysis data
        self.plotAxisDict = {} #active axes of all plots
        
        #plot datafile/image curves
        for source in ['datafile', 'image']:
            for category in self.configPlotWindow.plotDict[source].keys():
                category_dict = self.configPlotWindow.plotDict[source][category]
                # ax2 = ax1.twinx()
                # ax2.yaxis.set_visible(False)
                ax2 = None
                i = 0 #axis counter for each category
                for curve in category_dict['curves'].keys():
                    if category_dict['combine'].isChecked() == True:
                        # ax2 = ax1.twinx()
                        # ax2.yaxis.set_visible(False)
                        curve_ax = list(category_dict['curves'].keys())[0]
                        ylabel = category
                        i = 0                    
                    else:
                        # ax2 = ax1
                        curve_ax = curve
                        ylabel = curve
                        i += 1
                    if source == 'datafile':
                        ax2, lns = self.plotFileData(ax1, ax2, curve, i, ylabel,
                                                category_dict['curves'][curve], 
                                                category_dict['curves'][curve_ax], 
                                                lns)
                    elif source == 'image':
                        ax2, lns = self.plotImageData(ax1, ax2,
                                                    curve, i, ylabel,
                                                    category_dict['curves'][curve],
                                                    category_dict['curves'][curve_ax], 
                                                    lns)


        i = 0
        self.imageAxisDict['pulloff area point'] = []
        self.imageAxisDict['friction area point'] = []
        for k in self.dataDict.keys():
            if len(self.dataDict.keys()) > 1 and k == "Default":
                continue
            if adhesion_show == True: #show adhesion calc                      
                if 'Vertical force' in self.plotAxisDict.keys():
                    if self.zeroShiftY == True:
                        zero_val = self.fileDataDict['Vertical force'][self.plot_slice.start]
                    else:
                        zero_val = 0                    
                    ax = self.plotAxisDict['Vertical force']
                    ax.axhline(y=self.forceDict[k]["zero1"]-zero_val, color='y',
                                alpha=1, linestyle=self.linelist[i], linewidth=1)                
                    ax.axhline(y=self.forceDict[k]["force_min1"]-zero_val, color='y',
                                alpha=1, linestyle=self.linelist[i], linewidth=1)
                    ax.axhline(y=self.forceDict[k]["force_max1"]-zero_val, color='y',
                                alpha=1, linestyle=self.linelist[i], linewidth=1)
                    ax.axvline(x=self.xAxisData[self.fileDataDict['Time'].index(self.indDict[k]["time1_max"])], 
                                color='y', alpha=1, linestyle=self.linelist[i], linewidth=1)
                if 'Contact area' in self.plotAxisDict.keys():
                    if self.zeroShiftY == True:
                        zero_val_area = self.dataDict[k]["Contact area"][self.plot_slice2.start]
                    else:
                        zero_val_area = 0                    
                    ax = self.plotAxisDict['Contact area']
                    p, = ax.plot(self.indDict[k]["time1_max"],
                                  self.areaDict[k]["area2_pulloff"]-zero_val_area,
                                  'y' + self.markerlist[i], 
                                  markersize = 2*self.markerSize, alpha=0.8)
                    self.imageAxisDict['pulloff area point'].append(p)
                    if self.fixYLimits == True:
                        self.plotWidget.wid.artistDict['pulloff area point' + 
                                                       ": " + k] = p
                        p.set_animated(True)

            if friction_show == True and 'Lateral force' in self.plotAxisDict.keys(): #show friction calc
                if 'Lateral force' in self.plotAxisDict.keys():
                    if self.zeroShiftY == True:
                        zero_val = self.fileDataDict['Lateral force'][self.plot_slice.start]
                        zero_val_vert = self.fileDataDict['Vertical force'][self.plot_slice.start]
                    else:
                        zero_val = 0        
                        zero_val_vert = 0
                    ax = self.plotAxisDict['Lateral force']
                    ax.axhline(y=self.forceDict[k]["zero2"]-zero_val,
                                color='g', alpha=0.5,
                                linestyle=self.linelist[i], linewidth=1)                    
                    ax.axhline(y=self.forceDict[k]["force_lat_max"]-zero_val,
                                color='g', alpha=1,
                                linestyle=self.linelist[i], linewidth=1)
                    ax.axhline(y=self.forceDict[k]["force_lat_min"]-zero_val,
                                color='g', alpha=1,
                                linestyle=self.linelist[i], linewidth=1)
                    ax.axvline(x=self.xAxisData[self.fileDataDict['Time'].index(self.indDict[k]["time1_lat_avg"])],
                                color='g', alpha=1,
                                linestyle=self.linelist[i], linewidth=1)
                if 'Vertical force' in self.plotAxisDict.keys():
                    ax = self.plotAxisDict['Vertical force'] #friction preload
                    ax.axhline(y=self.forceDict[k]["force_max2"]-zero_val_vert,
                                color='g', alpha=1,
                                linestyle=self.linelist[i], linewidth=1)
            # print("legends",curve, lns)
                if 'Contact area' in self.plotAxisDict.keys():
                    if self.zeroShiftY == True:
                        zero_val_area = self.dataDict[k]["Contact area"][self.plot_slice2.start]
                    else:
                        zero_val_area = 0                      
                    ax = self.plotAxisDict['Contact area']
                    p, = ax.plot(self.indDict[k]["time1_lat_avg"],
                                  self.areaDict[k]["area_friction"]-zero_val_area,
                                  'g' + self.markerlist[i], 
                                  markersize = 2*self.markerSize, alpha=0.8)
                    self.imageAxisDict['friction area point'].append(p)
                    if self.fixYLimits == True:
                        self.plotWidget.wid.artistDict['friction area point' + 
                                                       ": " + k] = p
                        p.set_animated(True)

            i += 1
        
        #delete these if not plotted
        if len(self.imageAxisDict['pulloff area point']) == 0:
            del self.imageAxisDict['pulloff area point']
        if len(self.imageAxisDict['friction area point']) == 0:
            del self.imageAxisDict['friction area point'] 
            

        if adhesion_show == True: #show adhesion calc
            if 'Vertical force' in self.plotAxisDict.keys():
                if self.zeroShiftY == True:
                    zero_val = self.fileDataDict['Vertical force'][self.plot_slice.start]
                else:
                    zero_val = 0
                ydata = [x - zero_val for x in self.fileDataDict['Vertical force'][self.energy_slice]]
                ax = self.plotAxisDict['Vertical force']                
                #fill adhesion energy region 
                #CHECK! zero of last roi taken for energy shading
                roi_key = list(self.forceDict.keys())[-1] 
                ax.fill_between(self.xAxisData[self.energy_slice],
                                  self.forceDict[roi_key]["zero1"]-zero_val,
                                  ydata,
                                  color = 'black', alpha = 0.3) 
                ax.axvline(x=self.xAxisData[deform_range[0]], color='violet', 
                            alpha=1, linestyle=":", linewidth=1)
                ax.axvline(x=self.xAxisData[deform_range[1]], color='violet', 
                            alpha=1, linestyle=":", linewidth=1)
            # i = 0
            # for k in self.rangeDict.keys():
            #     if len(self.rangeDict.keys()) > 1 and k == "Default":
            #         continue
            #     ax1.axhline(y=self.forceDict["zero1"][i], color='y',
            #                 alpha=1, linestyle=self.linelist[i], linewidth=1)                
            #     ax1.axhline(y=self.forceDict["force_min1"][i], color='y',
            #                 alpha=1, linestyle=self.linelist[i], linewidth=1)
            #     ax1.axhline(y=self.forceDict["force_max1"][i], color='y',
            #                 alpha=1, linestyle=self.linelist[i], linewidth=1)
            #     ax1.axvline(x=self.xAxisData[self.time1.index(self.indDict["time1_max"][i])], 
            #                 color='y', alpha=1, linestyle=self.linelist[i], linewidth=1)
            #     i += 1

        # if self.flag_ca == True or self.flag_ra == True:                
                
#             ax2 = ax1.twinx() #secondary axis
# ##                cmap = plt.cm.get_cmap("Reds")  # type: matplotlib.colors.ListedColormap
#             num = len(self.rangeDict.keys())
# ##                colors = plt.cm.Reds(np.linspace(0.3,1,num))
#             colors = plt.cm.Greens([0.7, 0.5, 0.9, 0.3, 1])
#             # colors = plt.cm.Greens(np.linspace(0.2,0.7,num))
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
#                     # p2.set_animated(True) #BLIT THIS CHECK!!!
#                     lns.append(p2)
#                     if self.flag_ap == True: #adhesion calc
#                         ax2.plot(self.indDict["time1_max"][i],
#                                  self.areaDict["area2_pulloff"][i],
#                                  'y' + markerlist[i], alpha=0.8)
#                     if self.flag_fp == True: #friction calc
#                         ax2.plot(self.indDict["time1_lat_avg"][i],
#                                  self.areaDict["area_friction"][i],
#                                  'g' + markerlist[i], alpha=0.8)
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
#             # ax3.spines['left'].set_position(('outward', int(6*self.fontSize)))
#             # ax3.spines["left"].set_visible(True)
#             # ax3.yaxis.set_label_position('left')
#             # ax3.yaxis.set_ticks_position('left')
#             self.updateAxisPos(ax3, 'left', 6)
#             self.updateAxisPos(ax1, 'left', 0)
#             if self.invert_latf == True:
#                 ax3.invert_yaxis()
#             if self.flag_lf == True:
#                 p4, = ax3.plot(self.xAxisData[self.plot_slice], self.force_lat1_shifted[self.plot_slice], 'co',
#                      alpha=0.5, linewidth=1, markersize=1, label="Lateral Force")

# ##            if self.flag_lf_filter == True:
# ##                p4, = ax3.plot(self.time1[self.plot_slice], self.force_lat1_filtered_shifted[self.plot_slice], '-c',
# ##                     alpha=0.5, linewidth=1, label="Lateral Force")

            # if friction_show == True: #show friction calc
            #     # i = 0
            #     # for k in self.rangeDict.keys():
            #     #     if len(self.rangeDict.keys()) > 1 and k == "Default":
            #     #         continue
            #     #     ax3.axhline(y=self.forceDict["force_lat_max"][i],
            #     #                 color='g', alpha=1,
            #     #                 linestyle=self.linelist[i], linewidth=1)
            #     #     ax3.axhline(y=self.forceDict["force_lat_min"][i],
            #     #                 color='g', alpha=1,
            #     #                 linestyle=self.linelist[i], linewidth=1)
            #     #     ax1.axhline(y=self.forceDict["force_max2"][i],
            #     #                 color='g', alpha=1,
            #     #                 linestyle=self.linelist[i], linewidth=1)
            #     #     ax3.axvline(x=self.xAxisData[self.time1.index(self.indDict["time1_lat_avg"][i])],
            #     #                 color='g', alpha=1,
            #     #                 linestyle=self.linelist[i], linewidth=1)
            #     #     # ax2.plot(self.indDict["time1_lat_avg"][i],
            #     #     #          self.areaDict["area_friction"][i],
            #     #     #          'g' + markerlist[i], alpha=0.8)
            #     #     i += 1
            #     if 'Lateral force' in self.plotAxisDict.keys(): #only one zero line plotted
            #         ax = self.plotAxisDict['Lateral force']
            #         ax.axhline(y=self.forceDict["zero2"],
            #                     color='g', alpha=0.5,
            #                     linestyle=self.linelist[0], linewidth=1)                
#             lns.append(p4)
#         else:
#             ax3 = None

#         if self.flag_zp == True or self.flag_xp == True or self.flag_zd: #piezo position/deformation
#             ax4 = ax1.twinx() #piezo waveform
#             ax4.set_ylabel('Displacement (μm)', color = 'violet')
#             if self.flag_ca == True or self.flag_ra == True: #shift axis if area plotted
#                 ax4.spines['right'].set_position(('outward', int(7*self.fontSize)))
# ##                ax4.invert_yaxis()
#             self.updateAxisPos(ax1, 'left', 0)
#             if self.flag_zp == True:
#                 p5, = ax4.plot(self.xAxisData[self.plot_slice], self.dist_vert1[self.plot_slice], '-',
#                      markersize=1, color = 'violet',
#                                alpha=0.5, label="Vertical Piezo")
#                 lns.append(p5)
#             if self.flag_xp == True:
#                 p6, = ax4.plot(self.xAxisData[self.plot_slice], self.dist_lat1[self.plot_slice], '-.',
#                      markersize=1, color = 'violet',
#                                alpha=0.5, label="Lateral Piezo")
#                 lns.append(p6)
#             if self.flag_zd == True: #actual deformation plot
#                 p12, = ax4.plot(self.xAxisData[self.plot_slice], self.deform_vert[self.plot_slice], '-o',
#                      markersize=1, color = 'violet',
#                      alpha=0.5, label="Deformation")
                # if adhesion_show == True:
                #     ax1.axvline(x=self.xAxisData[self.deform_tol], color='violet', 
                #                 alpha=1, linestyle=":", linewidth=1)
#                 lns.append(p12)
        
        
        # image analysis data plotting
#         self.imageAxisDict = {} #active axes of image analysis data

#         if self.flag_ca == True: #contact area
#             ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                          ax_secondary = None,
#                                          spine_type = 'right',
#                                          spine_position= 0, 
#                                          yaxis_label = 'Area ($' + unit + '^2$)', 
#                                          ylabel = 'Contact Area', 
#                                          y_index = 0, 
#                                          color = 'Green', 
#                                          legend = lns)
#             self.imageAxisDict[0] = p
            # i = 0
            # for k in self.rangeDict.keys():
            #     if len(self.rangeDict.keys()) > 1 and k == "Default":
            #         continue
            #     if adhesion_show == True: #adhesion calc
            #         p, = ax2.plot(self.indDict["time1_max"][i],
            #                       self.areaDict["area2_pulloff"][i],
            #                       'y' + self.markerlist[i], alpha=0.8)
            #         self.imageAxisDict['pulloff area point'] = [p]
            #         if self.fixYLimits == True:
            #             self.plotWidget.wid.artistDict['pulloff area point'] = p
            #             p.set_animated(True)
            #     if friction_show == True: #friction calc
            #         p, = ax2.plot(self.indDict["time1_lat_avg"][i],
            #                       self.areaDict["area_friction"][i],
            #                       'g' + self.markerlist[i], alpha=0.8)
            #         self.imageAxisDict['friction area point'] = [p]
            #         if self.fixYLimits == True:
            #             self.plotWidget.wid.artistDict['friction area point'] = p
            #             p.set_animated(True)
                # i += 1
#             if self.flag_ra == True: #roi area
#                 ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                          ax_secondary = ax2,
#                                          spine_type = 'right',
#                                          spine_position= 0, 
#                                          yaxis_label = 'Area ($' + unit + '^2$)', 
#                                          ylabel = 'ROI Area', 
#                                          y_index = 3, 
#                                          color = 'Blue', 
#                                          legend = lns)
#                 self.imageAxisDict[3] = p
#         elif self.flag_ra == True: #roi area
#                 ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                          ax_secondary = None,
#                                          spine_type = 'right',
#                                          spine_position= 0, 
#                                          yaxis_label = 'Area ($' + unit + '^2$)', 
#                                          ylabel = 'ROI Area', 
#                                          y_index = 3, 
#                                          color = 'Blue', 
#                                          legend = lns)
#                 self.imageAxisDict[3] = p
                
#         # if self.flag_cl == True or self.flag_rl == True:
#         if self.flag_ca == True or self.flag_ra == True:
#             spine_pos = 7
#         else:
#             spine_pos = 0
        
#         if self.flag_cl == True: #contact length 
#             ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                          ax_secondary = None,
#                                          spine_type = 'right',
#                                          spine_position= spine_pos, 
#                                          yaxis_label = 'Length ($' + unit + '$)', 
#                                          ylabel = 'Contact Length', 
#                                          y_index = 1, 
#                                          color = 'Copper', 
#                                          legend = lns)
#             self.imageAxisDict[1] = p
#             if self.flag_rl == True: #roi length
#                 ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                          ax_secondary = ax2,
#                                          spine_type = 'right',
#                                          spine_position= spine_pos, 
#                                          yaxis_label = 'Length ($' + unit + '$)', 
#                                          ylabel = 'ROI Length', 
#                                          y_index = 4, 
#                                          color = 'Wistia', 
#                                          legend = lns)
#                 self.imageAxisDict[4] = p
#         elif self.flag_rl == True: #roi length
#             ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                          ax_secondary = None,
#                                          spine_type = 'right',
#                                          spine_position= spine_pos, 
#                                          yaxis_label = 'Length ($' + unit + '$)', 
#                                          ylabel = 'ROI Length', 
#                                          y_index = 4, 
#                                          color = 'Wistia', 
#                                          legend = lns)
#             self.imageAxisDict[4] = p
                


# #             ax5 = ax1.twinx()
# #             num = len(self.rangeDict.keys())
# #             colors = plt.cm.copper(np.linspace(0.2,0.7,num))
# #             ax5.set_prop_cycle(color=colors)
# #             ax5.set_ylabel('Length ($' + unit + '$)', color = 'brown')
# #             if self.flag_ca == True or self.flag_ra == True: 
# #                 ax5.spines['right'].set_position(('outward', int(7*self.fontSize)))            
# #             if self.flag_cl == True: #contact length
# #                 i = 0
# #                 for k in self.rangeDict.keys():
# #                     if len(self.rangeDict.keys()) > 1 and k == "Default":
# #                         continue                    
# #                     p7, = ax5.plot(self.time2[self.plot_slice2],
# #                                     self.dataDict[k][1][self.plot_slice2],
# #                                     '-' + markerlist[i], alpha=0.5, linewidth=1,
# #                                     markersize=2, label="Contact Length: " + k)
# #                     lns.append(p7)
# #                     i += 1
# #             if self.flag_rl == True: #roi length
# # ##                ax5 = ax1.twinx()
# #                 num = len(self.rangeDict.keys())
# #                 colors = plt.cm.Wistia(np.linspace(0.2,0.7,num))
# #                 ax5.set_prop_cycle(color=colors)
# # ##                ax5.spines['right'].set_position(('outward', 70))
# #                 j = 0
# #                 for k in self.rangeDict.keys():
# #                     if len(self.rangeDict.keys()) > 1 and k == "Default":
# #                         continue
# # ##                    ax5.set_ylabel('Length ($' + unit + '$)', color = 'brown')
# #                     p8, = ax5.plot(self.time2[self.plot_slice2],
# #                                     self.dataDict[k][4][self.plot_slice2],
# #                                     '-' + markerlist[j], alpha=0.5, linewidth=1,
# #                                     markersize=2, label="ROI Length: " + k)
# #                     lns.append(p8)
# #                     j += 1
#         if self.flag_cn == True: #contact number
#             # num = len(self.rangeDict.keys())
#             # colors = plt.cm.copper(np.linspace(0.2,0.7,num))
#             ax2 ,lns, p = self.plotImageData(ax_primary = ax1, 
#                                         ax_secondary = None,
#                                         spine_type = 'right',
#                                         spine_position=7, 
#                                         yaxis_label = 'Number', 
#                                         ylabel = 'Contact Number', 
#                                         y_index = 2, 
#                                         color = 'Copper', 
#                                         legend = lns)
#             self.imageAxisDict[2] = p
#             # ax5 = ax1.twinx()
#             # num = len(self.rangeDict.keys())
#             # colors = plt.cm.copper(np.linspace(0.2,0.7,num))
#             # ax5.set_prop_cycle(color=colors)
#             # ax5.spines['right'].set_position(('outward', int(7*self.fontSize)))
#             # i = 0
#             # for k in self.rangeDict.keys():
#             #     if len(self.rangeDict.keys()) > 1 and k == "Default":
#             #         continue
#             #     ax5.set_ylabel('Number', color = 'brown')
#             #     p9, = ax5.plot(self.time2[self.plot_slice2],
#             #                    self.dataDict[k][2][self.plot_slice2],
#             #                    '-' + markerlist[i], alpha=0.5, linewidth=1,
#             #                    markersize=2, label="Contact Number: " + k)
#             #     lns.append(p9)
#             #     i += 1
#         if self.flag_ecc == True: #contact eccentricity
#             ax2 ,lns, p = self.plotImageData(ax_primary = ax1,
#                                         ax_secondary = None,
#                                         spine_type = 'right',
#                                         spine_position = 7, 
#                                         yaxis_label = 'Eccentricity', 
#                                         ylabel = 'Median Eccentricity', 
#                                         y_index = 5, 
#                                         color = 'Copper', 
#                                         legend = lns)
#             self.imageAxisDict[5] = p
            # ax5 = ax1.twinx()
            # num = len(self.rangeDict.keys())
            # colors = plt.cm.copper(np.linspace(0.2,0.7,num))
            # ax5.set_prop_cycle(color=colors)
            # ax5.spines['right'].set_position(('outward', int(7*self.fontSize)))
            # i = 0
            # for k in self.rangeDict.keys():
            #     if len(self.rangeDict.keys()) > 1 and k == "Default":
            #         continue
            #     ax5.set_ylabel('Eccentricity' + unit + '$)', color = 'brown')
            #     p10, = ax5.plot(self.time2[self.plot_slice2],
            #                     self.dataDict[k][5][self.plot_slice2],
            #                     '-' + markerlist[i], alpha=0.5, linewidth=1,
            #                     markersize=2, label="Median Eccentricity: " + k)
            #     lns.append(p10)
            #     i += 1
        
        if stress_show == True: #or self.flag_lf_filter == True: #stress CHECK!
            ax6 = ax1.twinx()
            area_unit = self.imageDataUnitDict['Contact area'].split('[')[1].split(']')[0]
            ax6.set_ylabel('Stress (μN/$' + area_unit + '$)', color = 'c')
            # ax6.spines['left'].set_position(('outward', int(6*self.fontSize)))
            # ax6.spines["left"].set_visible(True)
            # ax6.yaxis.set_label_position('left')
            # ax6.yaxis.set_ticks_position('left')
            self.updateAxisPos(ax6, 'left', 6)
            # self.updateAxisPos(ax1, 'left', 0)
            # if self.flag_st == True:
            if self.zeroShiftY == True:
                zero_val = self.stress[self.plot_slice.start]
            else:
                zero_val = 0  
            ydata = [x - zero_val for x in self.stress[self.plot_slice]]
            p11, = ax6.plot(self.xAxisData[self.plot_slice],
                            ydata, 'co',
                            alpha = self.opacity, 
                            linewidth = self.lineWidth, 
                            markersize = self.markerSize,
                            label="Stress")                            
            # if self.flag_lf_filter == True:
            #     p11, = ax6.plot(self.xAxisData[self.plot_slice],
            #                     self.stress_filtered[self.plot_slice], '-c',
            #                     alpha=0.5, linewidth=1, markersize=1,
            #                     label="Stress")

            lns.append(p11)
            
##            lns = [p1, p3, p2, p4, p5]
##        else:
##            lns = [p1, p2]
        # legendPos = (0.5,0.5)
        # pos = eval(legendPos) if legendPos[0] == '(' else legendPos
        # self.legend_main = self.fig1.get_axes()[-1].legend(handles=lns, loc = pos)
        
        # if show_title == True:
        #     title = 'Speed = ' + str(speed_inview).replace('[','').replace(']','') + ' μm/s'
        #     self.fig1.suptitle(title)
        # leg_drag = self.legend_main.set_draggable(True, use_blit = True, update = 'loc')
        # print(self.legend_main.get_window_extent())

# get_loc_in_canvas
        if self.fitWindow.enableFitting.isChecked() == True:
            # axDict = {'Vertical Force (μN)':ax1, 'Lateral Force (μN)':ax3}
            # yDict = {'Vertical Force (μN)':self.force_vert1_shifted,
            #          'Lateral Force (μN)':self.force_lat1_shifted}
            # fit_slice = slice(int(self.startFit * self.ptsnumber/100),
            #                   int(self.endFit * self.ptsnumber/100))
            # self.slope_unit = self.fitWindow.yFit.currentText().split('(')[1].split(')')[0] + '/' +\
            #                   self.fitWindow.xFit.currentText().split('(')[1].split(')')[0]
            # self.slope_unit = '' #CHECK
            if self.unitDict[self.fitWindow.yFit.currentText()] != '':
                unit_top = self.unitDict[self.fitWindow.yFit.currentText()].split('[')[1].split(']')[0]
            else:
                unit_top = ''
            if self.unitDict[self.fitWindow.xFit.currentText()] != '':
                unit_bottom = self.unitDict[self.fitWindow.xFit.currentText()].split('[')[1].split(']')[0]
            else:
                unit_bottom = ''
            self.slope_unit = unit_top + '/' + unit_bottom
            # text_pos = self.fit_pos.split(",")
            
            # self.slope = fitting.polyfitData(xDict.get(self.fit_x)[fit_slice], yDict.get(self.fit_y)[fit_slice],
            #                          axDict.get(self.fit_y), xAxisData[fit_slice], unit = self.slope_unit,
            #                          eq_pos = text_pos, fit_order = 1, fit_show = self.fit_show)
            # ax_fit = self.plotAxisDict.get(self.fitWindow.yFit.currentText())
            # ax_fit.plot(self.xAxisData[self.fitWindow.fit_slice], 
            #             self.fitWindow.fit_ydata, color = 'black',
            #             linewidth=2*self.lineWidth, linestyle='dashed')
            
        ##        print(eq_pos)
            if self.fit_show == True: #show fitted curve
                ax_fit = self.plotAxisDict.get(self.fitWindow.yFit.currentText())
                if self.zeroShiftY == True:
                    zero_val = self.fileDataDict[self.fitWindow.yFit.currentText()][self.plot_slice.start]
                else:
                    zero_val = 0
                ydata = [x - zero_val for x in self.fitWindow.fit_ydata]                
                ax_fit.plot(self.xAxisData[slice(*self.fitWindow.fit_range)], 
                            ydata, color = 'black', linewidth=2*self.lineWidth, 
                            linestyle='dashed')
                #display slope if linear fit
                if self.fitWindow.fittingFunctionType.currentText() == 'Linear':                    
                    self.slope = self.fitWindow.fitParams['m']
                    slope_label = "Slope: " + "%.4f"%(self.slope) + ' ' + self.slope_unit
                    ax_top = self.fig1.get_axes()[-1]
                    self.fitTextBox = ax_top.text(*self.fit_pos,
                                                  slope_label, ha = 'right',
                                                  transform=ax_top.transAxes, 
                                                  color = 'black',
                                                  bbox=dict(facecolor='white', 
                                                            edgecolor = 'black', 
                                                            alpha=0.5),
                                                  picker = 5)
        else:
            self.slope = ''
            self.slope_unit = ''
            self.fitTextBox = None
        
        #draw legend
        pos = eval(legendPos) if legendPos[0] == '(' else legendPos
        self.legend_main = self.fig1.get_axes()[-1].legend(handles=lns, loc = pos)
        
        
        
        self.fig1.tight_layout()
        self.fig1.canvas.draw()
        
        print("axes", self.fig1.get_axes())
        # self.plotWidget.__init__(fig = self.fig1,
        #                          cursor1_init=c1_init,
        #                          cursor2_init=c2_init,
        #                          fixYLimits = self.fixYLimits,
        #                          method = self.updatePosition)
        self.plotWidget.wid.axes = self.fig1.get_axes()[-1]
            
        
        self.plotWidget.wid.add_cursors(cursor1_init=c1_init,
                                        cursor2_init=c2_init)
        
        # self.toggleAnimation(True)
        self.plotWidget.wid.fixYLimits = self.fixYLimits
        self.plotWidget.wid.updateBackground()        
        # self.toggleAnimation(False)
        
        self.axesUnique = set([])
        for ind in self.imageAxisDict.keys():
            self.axesUnique.add(self.imageAxisDict[ind][0].axes)
       
        # self.plotWidget.resize(self.plotWidget.minimumSizeHint())
        # self.fig1.canvas.draw()
        self.sourceLabel = None #to prevent range buttons react to cursor drag
        print("plot finish")
        
        # self.plotWidget.update()
        # self.plotWidget.wid.resizeWindow(None)
        # self.plotWidget.wid.draw_idle()

    
    def plotImageAnimate(self, frame_pos): 
        self.plotWidget.wid.toggleAnimation(True)
        # restore the background region
        self.fig1.canvas.restore_region(self.plotWidget.wid.background)
        for ind in self.imageAxisDict.keys():
            i = 0
            for k in self.dataDict.keys():
                if len(self.dataDict.keys()) > 1 and k == "Default":
                    continue
                if self.zeroShiftY == True:
                    zero_val_area = self.dataDict[k]["Contact area"][self.plot_slice2.start]
                else:
                    zero_val_area = 0
                if ind == "pulloff area point":
                    self.imageAxisDict[ind][i].set_ydata(self.areaDict[k]["area2_pulloff"]-zero_val_area)
                elif ind == "friction area point":
                    self.imageAxisDict[ind][i].set_ydata(self.areaDict[k]["area_friction"]-zero_val_area)
                else:
                    print(ind)
                    if self.zeroShiftY == True:
                        zero_val = self.dataDict[k][ind][self.plot_slice2.start]
                    else:
                        zero_val = 0
                    ydata = [x - zero_val for x in self.dataDict[k][ind][self.plot_slice2]]
                    self.imageAxisDict[ind][i].set_ydata(ydata)
                print("out", ind, i, k)
                if self.fixYLimits == True:
                    # redraw just the current rectangle
                    self.imageAxisDict[ind][i].axes.draw_artist(self.imageAxisDict[ind][i])

                i += 1
        
        self.plotWidget.wid.updateCursor(self.plotWidget.wid.cursor1, 
                                         self.time2[frame_pos-1])
        #draw cursor only within plot range
        if frame_pos >=  self.plot_slice2.start + 1 and frame_pos < self.plot_slice2.stop + 1:
            self.plotWidget.wid.updateCursor(self.plotWidget.wid.cursor1, 
                                             self.time2[frame_pos-1])
            self.plotWidget.wid.axes.draw_artist(self.plotWidget.wid.cursor1)            
        else: #just set cursor on start and dont draw
            self.plotWidget.wid.updateCursor(self.plotWidget.wid.cursor1, 
                                             self.time2[self.plot_slice2.start])            

        if self.fixYLimits == True:
            for ind in self.imageAxisDict.keys():
                self.fig1.canvas.blit(self.imageAxisDict[ind][0].axes.bbox)
        else:
            for axes in self.axesUnique:
                axes.relim()
                axes.autoscale_view()
                self.fig1.draw_artist(axes) 
            for ind in self.imageAxisDict.keys():
                self.fig1.canvas.blit(self.imageAxisDict[ind][0].axes.get_tightbbox(self.fig1.canvas.get_renderer()))

        self.plotWidget.wid.toggleAnimation(False)
        self.sourceLabel = None
    
    def updateAxisPos(self, ax, spine_type, spine_position):
        ax.spines[spine_type].set_position(('outward', 
                                            int(spine_position*self.fontSize)))
        ax.spines[spine_type].set_visible(True)
        ax.yaxis.set_ticks_position(spine_type)
        ax.yaxis.set_label_position(spine_type)

    def plotFileData(self, ax_primary, ax_secondary, curve, num, 
                     ylabel, curve_dict, curve_dict_ax, legend):
        if curve_dict['show'].isChecked() == True: 
            if num > 0: #for multiple axis with no combine
                ax2 = ax_primary.twinx() #secondary axis
            else:
                if ax_secondary == None:
                    ax2 = ax_primary.twinx() #secondary axis
                else:
                    ax2 = ax_secondary
                    ax2.yaxis.set_visible(True)
            # self.fig1.get_axes()[0].yaxis.set_visible(False)
            # ax2.yaxis.set_visible(False)
            self.updateAxisPos(ax2, curve_dict_ax['position'].currentText(), 
                               curve_dict_ax['shift'].value()) 
            # ax2.set_xlabel(self.x_var)
            ax2.set_ylabel(ylabel + self.unitDict[curve], 
                           color = curve_dict_ax['color'])
            if curve_dict_ax['invert'].isChecked() == True:
                ax2.invert_yaxis()
            line_marker = curve_dict['line style'].currentText() + \
                curve_dict['marker'].currentText()
            if self.zeroShiftY == True:
                zero_val = self.fileDataDict[curve][self.plot_slice.start]
            else:
                zero_val = 0
            ydata = [x - zero_val for x in self.fileDataDict[curve][self.plot_slice]]
            p1, = ax2.plot(self.xAxisData[self.plot_slice], 
                           ydata, 
                           line_marker,
                           linewidth = self.lineWidth, 
                           markersize = self.markerSize,
                           alpha = self.opacity, label=curve,
                           color = curve_dict['color'])
            legend.append(p1)
            self.plotAxisDict[curve] = ax2
        else:
            ax2 = ax_secondary
            # print("legends",curve, legend)
        
        return ax2, legend
    
    def plotImageData(self, ax_primary, ax_secondary, curve, num, 
                     ylabel, curve_dict, curve_dict_ax, legend):
        
        
        if curve_dict['show'].isChecked() == True: 
            if num > 0: #for multiple axis with no combine
                ax2 = ax_primary.twinx() #secondary axis
            else:
                if ax_secondary == None:
                    ax2 = ax_primary.twinx() #secondary axis
                else:
                    ax2 = ax_secondary
                    ax2.yaxis.set_visible(True)           
            
            
            self.updateAxisPos(ax2, curve_dict_ax['position'].currentText(), 
                               curve_dict_ax['shift'].value())
            # self.updateAxisPos(ax_primary, 'left', 0)
            color_array = [0.7, 0.5, 0.9, 0.3, 1]
            color_map = plt.get_cmap(curve_dict['color'].currentText())(color_array)
            ax2.set_ylabel(ylabel + self.imageDataUnitDict[curve],
                           color = color_map[0])
            if curve_dict_ax['invert'].isChecked() == True:
                ax2.invert_yaxis()
            if self.fixYLimits == True:
                y_bound = [float(x) for x in curve_dict_ax['y bounds'].text().split(',')]
                ax2.set_ylim(y_bound)
            else:
                self.plotWidget.wid.artistDict[ylabel] = ax2
                ax2.set_animated(True)
            
            
            ax2.set_prop_cycle(color=color_map)
            
            i = 0
            lines = []
            for k in self.dataDict.keys():
                if len(self.dataDict.keys()) > 1 and k == "Default":
                    continue
                
                if self.zeroShiftY == True:
                    zero_val = self.dataDict[k][curve][self.plot_slice2.start]
                else:
                    zero_val = 0
                ydata = [x - zero_val for x in self.dataDict[k][curve][self.plot_slice2]]
                p, = ax2.plot(self.time2[self.plot_slice2],
                              ydata,
                              '-' + self.markerlist[i], 
                              alpha = self.opacity, 
                              linewidth = self.lineWidth,
                              markersize= self.markerSize, 
                              label= curve + ": " + k)
                if self.fixYLimits == True:
                    self.plotWidget.wid.artistDict[curve + ": " + k] = p
                    p.set_animated(True) #BLIT THIS CHECK!!!
    
                legend.append(p)
                lines.append(p)
                i += 1
            self.imageAxisDict[curve] = lines
            self.plotAxisDict[curve] = ax2
        else:
            ax2 = ax_secondary

        return ax2, legend
    
    #update y bounds
    def updateYBounds(self):
        print('clicked')
        source = 'image'
        for category in self.configPlotWindow.plotDict[source].keys():
            category_dict = self.configPlotWindow.plotDict[source][category]
            for curve in category_dict['curves'].keys():
                if curve in self.imageAxisDict.keys():
                    print(curve)
                    y_bounds = ','.join(map(str,self.plotAxisDict[curve].get_ybound()))
                    print(y_bounds)
                    category_dict['curves'][curve]['y bounds'].setText(y_bounds)
            
    
    def updatePosition(self):

        # final_pos = tuple(self.plotWidget.wid.axes.transLimits.transform
        #                   ((self.plotWidget.wid.final_pos)))
        if self.plotWidget.wid.clicked_artist == self.fitTextBox:
            self.fit_pos = list(self.fitTextBox.get_position())
        # elif self.plotWidget.wid.clicked_artist == self.legend_main:
        #     pos = str(tuple(self.legend_main.get_window_extent()))
        #     self.configPlotWindow.plotDict['plot settings']['legend position'].setText(pos)
        elif self.plotWidget.wid.clicked_artist in [self.plotWidget.wid.cursor1,
                                                    self.plotWidget.wid.cursor2]:
            if self.sourceLabel != None:
                xdata =  self.xAxisData
                x1 = self.plotWidget.wid.cursor1.get_xdata()[0]                                
                x1_ind = np.searchsorted(xdata, [x1])[0]
                
                if len(self.sourceLabel.text().split(',')) == 2:
                    x2 = self.plotWidget.wid.cursor2.get_xdata()[0]
                    x2_ind = np.searchsorted(xdata, [x2])[0]
                    xstart = min(x1_ind, x2_ind)
                    xend = max(x1_ind, x2_ind)
                    xend = xend-1 if xend == len(xdata) else xend            
                    self.sourceLabel.setText(str(xstart) + ',' + str(xend))
                else:
                    xstart = x1_ind-1 if x1_ind == len(xdata) else x1_ind
                    self.sourceLabel.setText(str(xstart))
                # self.sourceLabel = None
     
    def setCursorPosition(self, label): #change xAxisData to time1 or index
        self.sourceLabel = label
        cursor_range = label.text().split(',')
        if int(cursor_range[0]) < self.plot_slice.start or \
            int(cursor_range[0]) >= self.plot_slice.stop:
            cursor_range[0] = self.plot_slice.start

        # cursor_list = [self.plotWidget.wid.cursor1, self.plotWidget.wid.cursor2]
        
        # i = 1
        # for cursor in cursor_list:
        #     if i <= len(cursor_range):
        #         if cursor == None:
        #             cursor_list[i-1] = self.plotWidget.wid.cursor_initialize(
        #                 self.xAxisData[int(cursor_range[i-1])],"cursor" + str(i))
        #         else:
        #             self.plotWidget.wid.updateCursor(cursor, 
        #                                              self.xAxisData[int(cursor_range[i-1])])
        #             self.plotWidget.wid.axes.draw_artist(cursor)
        #     else:
        #         cursor = None
        #     i += 1
        # print(cursor_list)
                
        if self.plotWidget.wid.cursor1 == None:
            self.plotWidget.wid.cursor1 = self.plotWidget.wid.cursor_initialize(
                self.xAxisData[int(cursor_range[0])],"cursor1")
        else:
            self.plotWidget.wid.updateCursor(self.plotWidget.wid.cursor1, 
                                              self.xAxisData[int(cursor_range[0])])
            self.plotWidget.wid.axes.draw_artist(self.plotWidget.wid.cursor1)
        
        if len(cursor_range) == 2:
            if int(cursor_range[1]) < self.plot_slice.start or \
            int(cursor_range[1]) >= self.plot_slice.stop:
                cursor_range[1] = self.plot_slice.stop - 1
                
            if self.plotWidget.wid.cursor2 == None:
                self.plotWidget.wid.cursor2 = self.plotWidget.wid.cursor_initialize(
                    self.xAxisData[int(cursor_range[1])],"cursor2")
            else:
                self.plotWidget.wid.updateCursor(self.plotWidget.wid.cursor2, 
                                                  self.xAxisData[int(cursor_range[1])])
                self.plotWidget.wid.axes.draw_artist(self.plotWidget.wid.cursor2)
        else:
            if self.plotWidget.wid.cursor2 != None:
                self.plotWidget.wid.cursor2.set_xdata([])
                self.plotWidget.wid.cursor2.set_ydata([])
        print(cursor_range)
        # self.fig1.canvas.draw()
        self.plotWidget.wid.draw_idle()
        # self.plotWidget.wid.updateBackground()
            
    
    # def plotImageData(self, ax_primary, ax_secondary, spine_type, spine_position, 
    #                   yaxis_label, ylabel, y_index, color, legend, y_bound = [50000, 100000]):
        
    #     if ax_secondary == None:
    #         ax_secondary = ax_primary.twinx()
    #         # ax_secondary.spines[spine_type].set_position(('outward', 
    #         #                                      int(spine_position*self.fontSize)))
    #         # ax_secondary.spines[spine_type].set_visible(True)
    #         # ax_secondary.yaxis.set_label_position(spine_type)
    #         # ax_secondary.yaxis.set_ticks_position(spine_type)            
    #         ax_secondary.set_ylabel(yaxis_label, color = self.colorDict[color][0])
    #         self.updateAxisPos(ax_secondary, spine_type, spine_position)
    #         self.updateAxisPos(ax_primary, 'left', 0)

    #         if self.fixYLimits == True:
    #             ax_secondary.set_ylim(y_bound)
    #         else:
    #             self.plotWidget.wid.artistDict[yaxis_label] = ax_secondary
    #             ax_secondary.set_animated(True)
        
    #     ax_secondary.set_prop_cycle(color=self.colorDict[color])
        
    #     i = 0
    #     lines = []
    #     for k in self.rangeDict.keys():
    #         if len(self.rangeDict.keys()) > 1 and k == "Default":
    #             continue
            
    #         p, = ax_secondary.plot(self.time2[self.plot_slice2],
    #                         self.dataDict[k][y_index][self.plot_slice2],
    #                         '-' + self.markerlist[i], alpha=0.5, linewidth=1,
    #                         markersize=2, label= ylabel + ": " + k)
    #         if self.fixYLimits == True:
    #             self.plotWidget.wid.artistDict[ylabel + ": " + k] = p
    #             p.set_animated(True) #BLIT THIS CHECK!!!

    #         legend.append(p)
    #         lines.append(p)
    #         i += 1

    #     return ax_secondary, legend, lines

    # def setPlotRange(self): #set global plot range
    #     fig = Figure(figsize=(11, 5), dpi=100)
    #     ax = fig.add_subplot(111)
    #     xdata = self.time1
    #     ydata = self.force_vert1_shifted #CHECK! make this more general
    #     ax.plot(xdata, ydata, 'r-', linewidth=1, markersize=1)        
    #     plotWidget = PlotWidget(fig = fig,
    #                             cursor1_init=min(xdata),
    #                             cursor2_init=max(xdata),
    #                             method = self.updateRange)
    #     self.fullPlotWidget = plotWidget.wid
    #     plotWidget.show()
    
    # def updateRange(self): #update plot range slice
    #     self.plot_slice = slice(self.fullPlotWidget.cursor1.get_xdata(),
    #                             self.fullPlotWidget.cursor2.get_xdata())

    def toggleCursorVisibility(self, state):
        if self.plotWidget.wid.cursor1 != None:
            self.plotWidget.wid.cursor1.set_visible(state)
        if self.plotWidget.wid.cursor2 != None:
            self.plotWidget.wid.cursor2.set_visible(state)
        
        
    def convertPlot(self): #convert plot to numpy
        # self.fig1.canvas.draw()
        data = np.fromstring(self.fig1.canvas.tostring_rgb(),
                             dtype=np.uint8, sep='')
        data = data.reshape(self.fig1.canvas.get_width_height()[::-1] + (3,))
        return data

    def savePlot(self, filepath): #save force plots
        print("save plot")
        self.toggleCursorVisibility(False)     
        self.fig1.savefig(filepath, orientation='landscape',
                          transparent = True)
        #save figure object as pickle file
        with open(filepath[:-4] + '.pickle', 'wb') as f:
            pickle.dump(self.fig1, f, pickle.HIGHEST_PROTOCOL)
        
        self.toggleCursorVisibility(True)
        

# class PlotWindow(QWidget):
#     def __init__(self, fig, *args, **kwargs):
# ##        super(QWidget, self).__init__(*args, **kwargs)
#         super().__init__()
#         self.setGeometry(100, 100, 1000, 500)
#         self.setWindowTitle("Plot")
#         self.fig = fig
#         self.home()
        
#     def home(self):
#         self.plotWidget = Plot2Widget(self.fig,cursor1_init=2,cursor2_init=6)
#         plotToolbar = NavigationToolbar(self.plotWidget, self)
        
#         plotGroupBox = QGroupBox()
#         plotlayout=QGridLayout()
#         plotGroupBox.setLayout(plotlayout)
#         plotlayout.addWidget(plotToolbar, 0, 0, 1, 1)
#         plotlayout.addWidget(self.plotWidget, 1, 0, 1, 1)
        
#         layout=QGridLayout()
#         layout.addWidget(plotGroupBox, 0, 0, 1, 1)
        
#         self.setLayout(layout)
        # self.show()
        # startFitLabel = QLabel("Start (%):")