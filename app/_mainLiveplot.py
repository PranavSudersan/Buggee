# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 22:05:47 2020

@author: adwait
"""
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox, Tk
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPolygonF
from PyQt5.QtChart import QChart, QScatterSeries
from PyQt5.QtWidgets import QSizePolicy

class MainLivePlot:
    
    def plot_live_data(self): #plot graph
        if self.forceData.force_filepath == "": #area plot only           
            if self.frameCount != 1: #ignore for image
                self.plotWindow.liveChart.removeAllSeries()
                self.plotWindow.liveChartScene.removeItem(self.plotWindow.liveChart)
                self.plotWindow.liveChartView.resetCachedContent()
                self.plotWindow.liveChart = QChart() #live chart
                self.plotWindow.liveChart.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                self.plotWindow.liveChart.legend().hide()
                print(self.plotWindow.liveChartView.size())

                w, h = (self.plotWindow.liveChartView.size().width(),
                                                          self.plotWindow.liveChartView.size().height())
                print(w,h)
                self.plotWindow.liveChart.setMinimumSize(w, h)
            
                self.curve1 = QScatterSeries()#initialise live plot curves
                self.initialise_live_plot(self.curve1, Qt.blue) #contact area plot
                print(self.frameTime.shape)
                for k in self.roiDict.keys():
                    if len(self.roiDict.keys()) > 1 and k == "Default":
                        continue
                    self.curve1.append(self.series_to_polyline(self.frameTime,
                                                              self.dataDict[k][0]))
                self.plotWindow.liveChart.addSeries(self.curve1)
                if self.roi_auto == True: # roi area plot
                    self.curve2 = QScatterSeries()
                    self.initialise_live_plot(self.curve2, Qt.red)
                    for k in self.roiDict.keys():
                        if len(self.roiDict.keys()) > 1 and k == "Default":
                            continue
                            self.curve2.append(self.series_to_polyline(self.frameTime,
                                                                      self.dataDict[k][3]))
                    self.plotWindow.liveChart.addSeries(self.curve2)
                
                self.plotWindow.liveChart.createDefaultAxes()
                self.plotWindow.liveChartScene.addItem(self.plotWindow.liveChart)
                self.plotWindow.liveChartView.setScene(self.plotWindow.liveChartScene)
                print("live plot end")
        elif self.forceData.fig1_close == False: #area and force plot
            self.forceData.getArea(self.frameTime, self.dataDict)
            self.forceData.plotData(self.lengthUnit.currentText())
            self.forceData.showPlot()
        
    def plot_data(self): #plot graph
        if self.forceData.force_filepath == "":
            self.plotWindow.home() #live area data show
        else:
            if self.playStatus == True: #pause video if running (bug)
                self.playBtn.click() 
            self.forceData.fig1_close = False #area data show
            self.forceData.getArea(self.frameTime, self.dataDict)
            self.forceData.plotData(self.lengthUnit.currentText())
            self.forceData.showPlot()
            plt.show()
        
    def initialise_live_plot(self, curve, color): #initalise live plot
        pen = curve.pen()
        pen.setColor(color)#Qt.blue
        pen.setWidthF(1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.setMarkerSize(4.0)    

    def series_to_polyline(self, xdata, ydata): #convert plot data for Qt
        """Convert series data to QPolygon(F) polyline
        This code is derived from PythonQwt's function named 
        `qwt.plot_curve.series_to_polyline`"""
        xsize = len(xdata)
        ysize = len(ydata)
        if xsize != ysize:
            root = Tk()
            root.withdraw()
            messagebox.showinfo("Live Plot Error!", "Check force file/video file\n" + \
                                "Exception: x axis and y axis array sizes don't match")
            root.destroy()
            self.playStatus = False
            
        polyline = QPolygonF(xsize)
        pointer = polyline.data()
        dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
        memory = np.frombuffer(pointer, dtype)
        memory[:(xsize-1)*2+1:2] = xdata
        memory[1:(ysize-1)*2+2:2] = ydata
        return polyline   