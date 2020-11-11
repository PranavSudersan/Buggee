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
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout

class Plotting:
    
    def __init__(self, fitWindow):
        self.fitWindow = fitWindow
        #plot display flags
        self.flag_ca = True
        self.flag_ra = False
        self.flag_cl = False
        self.flag_rl = False
        self.flag_cn = False
        self.flag_ecc = False
        self.flag_lf = False 
        self.flag_zp = False
        self.flag_xp = False
        self.flag_ap = False
        self.flag_fp = False
        self.flag_st = False
        self.flag_zd = False
        self.x_var = 'Time' #x axis default parameter
        self.legendPos = "upper right"
        # self.fig1_close = True
        self.show_title = True
        self.showLegend2 = True
        self.fontSize = 12
        #fitting
        # self.flag_fit = False
        # self.fit_x = 'Vertical Position (μm)'
        # self.fit_y = 'Vertical Force'
        # self.startFit = 0
        # self.endFit = 100
        self.fit_pos = '0.5,0.5'
        self.fit_show = False
        self.slope = ''
        self.slope_unit = ''
        
        #initialize figure with random data
        self.fig1 = Figure(figsize=(11, 5), dpi=100)
        ax = self.fig1.add_subplot(111)
        xdata = np.linspace(0, 4, 50)
        ydata = np.sin(xdata)
        ax.plot(xdata, ydata, 'r-', linewidth=1, markersize=1)
        
        self.plotWidget = PlotWidget(fig = self.fig1,
                                         cursor1_init=2,
                                         cursor2_init=6)
        
    def plotData(self, unit): #prepare plot

        xDict = {'Vertical Position (μm)':self.dist_vert1,
                 'Lateral Position (μm)':self.dist_lat1,
                 'Deformation (μm)':self.deform_vert,
                 'Time (s)':self.time1}
        xAxisData = xDict.get(self.x_var)
        
        markerlist = ["o", "v", "^", "s", "P", "*", "D", "<", "X", ">"]
        linelist = [":", "-.", "--", "-", ":", "-.", "--", "-", ":", "-."]
        
        plt.rcParams.update({'font.size': self.fontSize})
        
        # self.fig1 = plt.figure(num="Force/Area vs Time", figsize = [11, 5])
        # self.fig1 = Figure(figsize=(11, 5), dpi=100)
        
        # self.fig1.canvas.mpl_connect('close_event', self.handle_close)
        
        print("fig1")
        
        #store cursor position values before clearing plot
        if self.plotWidget.wid.cursor1 == None:
            c1_init = None
        else:
            c1_init = self.plotWidget.wid.cursor1.get_xdata()[0]
        
        if self.plotWidget.wid.cursor2 == None:
            c2_init = None
        else:
            c2_init = self.plotWidget.wid.cursor2.get_xdata()[0]
            
        self.fig1.clear()
        ax1 = self.fig1.add_subplot(1,1,1)
        lns = []
                
        # ax1.set_title('Speed = ' + str(self.speed_um) + ' μm/s')
        ax1.set_xlabel(self.x_var)
        ax1.set_ylabel('Vertical Force (μN)', color = 'r')
        p1, = ax1.plot(xAxisData[self.plot_slice], self.force_vert1_shifted[self.plot_slice], 'ro',
                     alpha=0.5, linewidth=1, markersize=1, label="Vertical Force")
        lns.append(p1)
        

        # self.plotWidget.mpl_connect('close_event', self.handle_close)
        
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
                
                x_start = min(xAxisData[startpoint:endpoint])
                x_end = max(xAxisData[startpoint:endpoint])
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
        
        if self.show_title == True:
            ax1.set_title('Speed = ' + str(speed_inview).replace('[','').replace(']','') 
                          + ' μm/s')
        if self.showLegend2 == True:
            dict_reg = dict(zip(lab_reg, lns_reg)) #legend dictionary (remove dup)
            self.fig1.legend(dict_reg.values(), dict_reg.keys(), loc='lower right',
                              ncol=len(lns_reg))
        
        if self.flag_ap == True: #show adhesion calc
            #fill adhesion energy region 
            ax1.fill_between(xAxisData[self.energy_slice],
                             self.forceDict["zero1"][0],
                             self.force_vert1_shifted[self.energy_slice],
                             color = 'black') 
            i = 0
            for k in self.rangeDict.keys():
                if len(self.rangeDict.keys()) > 1 and k == "Default":
                    continue
                ax1.axhline(y=self.forceDict["zero1"][i], color='y',
                            alpha=1, linestyle=linelist[i], linewidth=1)                
                ax1.axhline(y=self.forceDict["force_min1"][i], color='y',
                            alpha=1, linestyle=linelist[i], linewidth=1)
                ax1.axhline(y=self.forceDict["force_max1"][i], color='y',
                            alpha=1, linestyle=linelist[i], linewidth=1)
                ax1.axvline(x=xAxisData[self.time1.index(self.indDict["time1_max"][i])], 
                            color='y', alpha=1, linestyle=linelist[i], linewidth=1)
                i += 1

        if self.flag_ca == True or self.flag_ra == True:
            ax2 = ax1.twinx() #secondary axis
##                cmap = plt.cm.get_cmap("Reds")  # type: matplotlib.colors.ListedColormap
            num = len(self.rangeDict.keys())
##                colors = plt.cm.Reds(np.linspace(0.3,1,num))
            colors = plt.cm.Greens([0.7, 0.5, 0.9, 0.3, 1])
            ax2.set_prop_cycle(color=colors)
            ax2.set_ylabel('Area ($' + unit + '^2$)', color = 'g')
            if self.flag_ca == True:
                i = 0
                for k in self.rangeDict.keys():
                    if len(self.rangeDict.keys()) > 1 and k == "Default":
                        continue
                    p2, = ax2.plot(self.time2[self.plot_slice2],
                                   self.dataDict[k][0][self.plot_slice2],
                                   '-' + markerlist[i], alpha=0.5,
                                   linewidth=1, markersize=2,
                                   label="Contact Area: " + k)
                    # p2.set_animated(True) #BLIT THIS CHECK!!!
                    lns.append(p2)
                    if self.flag_ap == True: #adhesion calc
                        ax2.plot(self.indDict["time1_max"][i],
                                 self.areaDict["area2_pulloff"][i],
                                 'y' + markerlist[i], alpha=0.8)
                    if self.flag_fp == True: #friction calc
                        ax2.plot(self.indDict["time1_lat_avg"][i],
                                 self.areaDict["area_friction"][i],
                                 'g' + markerlist[i], alpha=0.8)
                    i += 1
            if self.flag_ra == True: #consider first key since auto roi is same for all keys
                colors = plt.cm.Blues([0.7, 0.5, 0.9, 0.3, 1])
                ax2.set_prop_cycle(color=colors)
                j = 0
                for k in self.rangeDict.keys():
                    if len(self.rangeDict.keys()) > 1 and k == "Default":
                        continue                
                    p3, = ax2.plot(self.time2[self.plot_slice2],
                                   self.dataDict[k][3][self.plot_slice2],
                                   '-' + markerlist[j], alpha=0.5, linewidth=1, markersize=2,
                                   label="ROI Area: " + k)
                    lns.append(p3)
                    j += 1

        
        if self.flag_lf == True:
            ax3 = ax1.twinx() #lateral force
            ax3.set_ylabel('Lateral Force (μN)', color = 'c')
            ax3.spines['left'].set_position(('outward', int(6*self.fontSize)))
            ax3.spines["left"].set_visible(True)
            ax3.yaxis.set_label_position('left')
            ax3.yaxis.set_ticks_position('left')
            if self.invert_latf == True:
                ax3.invert_yaxis()
            if self.flag_lf == True:
                p4, = ax3.plot(xAxisData[self.plot_slice], self.force_lat1_shifted[self.plot_slice], 'co',
                     alpha=0.5, linewidth=1, markersize=1, label="Lateral Force")

##            if self.flag_lf_filter == True:
##                p4, = ax3.plot(self.time1[self.plot_slice], self.force_lat1_filtered_shifted[self.plot_slice], '-c',
##                     alpha=0.5, linewidth=1, label="Lateral Force")

            if self.flag_fp == True: #show friction calc
                i = 0
                for k in self.rangeDict.keys():
                    if len(self.rangeDict.keys()) > 1 and k == "Default":
                        continue
                    ax3.axhline(y=self.forceDict["force_lat_max"][i],
                                color='g', alpha=1,
                                linestyle=linelist[i], linewidth=1)
                    ax3.axhline(y=self.forceDict["force_lat_min"][i],
                                color='g', alpha=1,
                                linestyle=linelist[i], linewidth=1)
                    ax1.axhline(y=self.forceDict["force_max2"][i],
                                color='g', alpha=1,
                                linestyle=linelist[i], linewidth=1)
                    ax3.axvline(x=xAxisData[self.time1.index(self.indDict["time1_lat_avg"][i])],
                                color='g', alpha=1,
                                linestyle=linelist[i], linewidth=1)
                    # ax2.plot(self.indDict["time1_lat_avg"][i],
                    #          self.areaDict["area_friction"][i],
                    #          'g' + markerlist[i], alpha=0.8)
                    i += 1
                ax3.axhline(y=self.forceDict["zero2"],
                            color='g', alpha=0.5,
                            linestyle=linelist[0], linewidth=1)                
            lns.append(p4)
        else:
            ax3 = None

        if self.flag_zp == True or self.flag_xp == True or self.flag_zd: #piezo position/deformation
            ax4 = ax1.twinx() #piezo waveform
            ax4.set_ylabel('Displacement (μm)', color = 'violet')
            if self.flag_ca == True or self.flag_ra == True: #shift axis if area plotted
                ax4.spines['right'].set_position(('outward', int(7*self.fontSize)))
##                ax4.invert_yaxis()
            if self.flag_zp == True:
                p5, = ax4.plot(xAxisData[self.plot_slice], self.dist_vert1[self.plot_slice], '-',
                     markersize=1, color = 'violet',
                               alpha=0.5, label="Vertical Piezo")
                lns.append(p5)
            if self.flag_xp == True:
                p6, = ax4.plot(xAxisData[self.plot_slice], self.dist_lat1[self.plot_slice], '-.',
                     markersize=1, color = 'violet',
                               alpha=0.5, label="Lateral Piezo")
                lns.append(p6)
            if self.flag_zd == True: #actual deformation plot
                p12, = ax4.plot(xAxisData[self.plot_slice], self.deform_vert[self.plot_slice], '-o',
                     markersize=1, color = 'violet',
                     alpha=0.5, label="Deformation")
                if self.flag_ap == True:
                    ax1.axvline(x=xAxisData[self.deform_tol], color='violet', 
                                alpha=1, linestyle=":", linewidth=1)
                lns.append(p12)
                
        if self.flag_cl == True or self.flag_rl == True:
            ax5 = ax1.twinx()
            num = len(self.rangeDict.keys())
            colors = plt.cm.copper(np.linspace(0.2,0.7,num))
            ax5.set_prop_cycle(color=colors)
            ax5.set_ylabel('Length ($' + unit + '$)', color = 'brown')
            if self.flag_ca == True or self.flag_ra == True: 
                ax5.spines['right'].set_position(('outward', int(7*self.fontSize)))            
            if self.flag_cl == True: #contact length
                i = 0
                for k in self.rangeDict.keys():
                    if len(self.rangeDict.keys()) > 1 and k == "Default":
                        continue                    
                    p7, = ax5.plot(self.time2[self.plot_slice2],
                                   self.dataDict[k][1][self.plot_slice2],
                                   '-' + markerlist[i], alpha=0.5, linewidth=1,
                                   markersize=2, label="Contact Length: " + k)
                    lns.append(p7)
                    i += 1
            if self.flag_rl == True: #roi length
##                ax5 = ax1.twinx()
                num = len(self.rangeDict.keys())
                colors = plt.cm.Wistia(np.linspace(0.2,0.7,num))
                ax5.set_prop_cycle(color=colors)
##                ax5.spines['right'].set_position(('outward', 70))
                j = 0
                for k in self.rangeDict.keys():
                    if len(self.rangeDict.keys()) > 1 and k == "Default":
                        continue
##                    ax5.set_ylabel('Length ($' + unit + '$)', color = 'brown')
                    p8, = ax5.plot(self.time2[self.plot_slice2],
                                   self.dataDict[k][4][self.plot_slice2],
                                   '-' + markerlist[j], alpha=0.5, linewidth=1,
                                   markersize=2, label="ROI Length: " + k)
                    lns.append(p8)
                    j += 1
        if self.flag_cn == True: #contact number
            ax5 = ax1.twinx()
            num = len(self.rangeDict.keys())
            colors = plt.cm.copper(np.linspace(0.2,0.7,num))
            ax5.set_prop_cycle(color=colors)
            ax5.spines['right'].set_position(('outward', int(7*self.fontSize)))
            i = 0
            for k in self.rangeDict.keys():
                if len(self.rangeDict.keys()) > 1 and k == "Default":
                    continue
                ax5.set_ylabel('Number', color = 'brown')
                p9, = ax5.plot(self.time2[self.plot_slice2],
                               self.dataDict[k][2][self.plot_slice2],
                               '-' + markerlist[i], alpha=0.5, linewidth=1,
                               markersize=2, label="Contact Number: " + k)
                lns.append(p9)
                i += 1
        if self.flag_ecc == True: #contact eccentricity
            ax5 = ax1.twinx()
            num = len(self.rangeDict.keys())
            colors = plt.cm.copper(np.linspace(0.2,0.7,num))
            ax5.set_prop_cycle(color=colors)
            ax5.spines['right'].set_position(('outward', int(7*self.fontSize)))
            i = 0
            for k in self.rangeDict.keys():
                if len(self.rangeDict.keys()) > 1 and k == "Default":
                    continue
                ax5.set_ylabel('Eccentricity' + unit + '$)', color = 'brown')
                p10, = ax5.plot(self.time2[self.plot_slice2],
                                self.dataDict[k][5][self.plot_slice2],
                                '-' + markerlist[i], alpha=0.5, linewidth=1,
                                markersize=2, label="Median Eccentricity: " + k)
                lns.append(p10)
                i += 1
        
        if self.flag_st == True or self.flag_lf_filter == True: #stress CHECK!
            ax6 = ax1.twinx() 
            ax6.set_ylabel('Stress (μN/$' + unit + '^2$)', color = 'c')
            ax6.spines['left'].set_position(('outward', int(6*self.fontSize)))
            ax6.spines["left"].set_visible(True)
            ax6.yaxis.set_label_position('left')
            ax6.yaxis.set_ticks_position('left')
            if self.flag_st == True:
                p11, = ax6.plot(xAxisData[self.plot_slice],
                                self.stress[self.plot_slice], 'co',
                                alpha=0.5, linewidth=1, markersize=1,
                                label="Stress")                            
            if self.flag_lf_filter == True:
                p11, = ax6.plot(xAxisData[self.plot_slice],
                                self.stress_filtered[self.plot_slice], '-c',
                                alpha=0.5, linewidth=1, markersize=1,
                                label="Stress")

            lns.append(p11)
            
##            lns = [p1, p3, p2, p4, p5]
##        else:
##            lns = [p1, p2]

        ax1.legend(handles=lns, loc = self.legendPos)

        if self.fitWindow.enableFitting.isChecked() == True:
            axDict = {'Vertical Force (μN)':ax1, 'Lateral Force (μN)':ax3}
            # yDict = {'Vertical Force (μN)':self.force_vert1_shifted,
            #          'Lateral Force (μN)':self.force_lat1_shifted}
            # fit_slice = slice(int(self.startFit * self.ptsnumber/100),
            #                   int(self.endFit * self.ptsnumber/100))
            self.slope_unit = self.fitWindow.yFit.currentText().split('(')[1].split(')')[0] + '/' +\
                              self.fitWindow.xFit.currentText().split('(')[1].split(')')[0]
            text_pos = self.fit_pos.split(",")
            
            # self.slope = fitting.polyfitData(xDict.get(self.fit_x)[fit_slice], yDict.get(self.fit_y)[fit_slice],
            #                          axDict.get(self.fit_y), xAxisData[fit_slice], unit = self.slope_unit,
            #                          eq_pos = text_pos, fit_order = 1, fit_show = self.fit_show)
            ax_fit = axDict.get(self.fitWindow.yFit.currentText())
            ax_fit.plot(xAxisData[self.fitWindow.fit_slice], 
                        self.fitWindow.fit_ydata, color = 'black',
                        linewidth=2, linestyle='dashed')
            
        ##        print(eq_pos)
            if self.fit_show == True and \
                self.fitWindow.fittingFunctionType.currentText() == 'Linear':
                    self.slope = self.fitWindow.fitParams['m']
                    slope_label = "Slope: " + "%.4f"%(self.slope) + \
                        ' (' + self.slope_unit + ')'
                    ax_top = self.fig1.get_axes()[-1]
                    ax_top.text(float(text_pos[0]), float(text_pos[1]),
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
        
        
        
        self.fig1.tight_layout()
        self.fig1.canvas.draw()
        
        self.plotWidget.wid.axes = self.fig1.get_axes()[-1]
            
        self.plotWidget.wid.add_cursors(cursor1_init=c1_init,
                                        cursor2_init=c2_init)
        
        print("plot finish")
        # self.plotWidget.wid.draw_idle()
        
        # self.fig1.tight_layout()
        # self.fig1.canvas.draw()
    
#     def showPlot(self): #show plot
# ##        self.fig1.show()
#         try:
#             # plt.pause(0.05)
#             # self.axes.relim()
#             # self.axes.autoscale()
#             self.fig1.tight_layout()
#             self.fig1.canvas.draw()
#             # self.plotWidget
#             # self.plotWidget.show()
#         except Exception as e:
#             print(e)
            
##        plt.show(block=False)
##        plt.draw()

    # def handle_close(self, evt): #figure closed event
    #     self.fig1_close = True
    #     print("close")

            
    def convertPlot(self): #convert plot to numpy
        self.fig1.canvas.draw()
        data = np.fromstring(self.fig1.canvas.tostring_rgb(),
                             dtype=np.uint8, sep='')
        data = data.reshape(self.fig1.canvas.get_width_height()[::-1] + (3,))
        return data

    def savePlot(self, filepath): #save force plots
        print("save plot")
        self.fig1.savefig(filepath, orientation='landscape',
                          transparent = True)
        #save figure object as pickle file
        with open(filepath[:-4] + '.pickle', 'wb') as f:
            pickle.dump(self.fig1, f, pickle.HIGHEST_PROTOCOL)
        

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