# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:30:18 2020

@author: adwait
"""
from PyQt5.QtWidgets import QGridLayout, QWidget, QGraphicsScene, \
     QGraphicsView, QSizePolicy
from PyQt5.QtChart import QChart, QScatterSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter  
   
# %% Live Plot Window  
class PlotWindow(QWidget):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent=parent)

        self.setGeometry(1410, 30, 500, 400)
        self.setWindowTitle("Live Plot")
        self.resizeEvent = self.onResize

        self.layout = QGridLayout(self)

        series = QScatterSeries()
        series.append(1, 3)
        series.append(4, 5)
        series.append(5, 4.5)
        series.append(7, 1)
        series.append(11, 2)
        
        self.liveChart = QChart() #live chart
        self.liveChart.legend().hide()
        self.liveChart.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.liveChart.addSeries(series)
        self.liveChart.createDefaultAxes()      
        
        self.liveChartScene = QGraphicsScene(self)
        self.liveChartScene.addItem(self.liveChart)
        
        self.liveChartView = QGraphicsView(self.liveChartScene, self)
        self.liveChartView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.liveChartView.setRenderHint(QPainter.Antialiasing)
        self.liveChartView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.liveChartView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.liveChartView.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)

        self.layout.addWidget(self.liveChartView, 0, 0)


    def home(self):
        self.show()

    def onResize(self, event):
        self.liveChartScene.removeItem(self.liveChart)
        self.liveChartView.resetCachedContent()
        w, h = (self.liveChartView.size().width(),self.liveChartView.size().height())

        self.liveChart.setMinimumSize(w, h)
        self.liveChart.createDefaultAxes()
        self.liveChartScene.setSceneRect(0, 0, w, h)
        self.liveChartScene.addItem(self.liveChart)
        self.liveChartView.setScene(self.liveChartScene)