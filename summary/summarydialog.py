# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 22:24:56 2020

@author: adwait
"""
import matplotlib.pyplot as plt
import gc
import os
import time
import cv2
from PyQt5.QtCore import Qt, pyqtSignal
# from PyQt5.QtGui import QSizePolicy
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QGroupBox,\
    QComboBox, QSpinBox, QGridLayout, QDialog, QLineEdit, QDoubleSpinBox,\
        QSizePolicy, QFileDialog, QTabWidget, QTableWidgetItem, QTableWidget,\
            QListWidget, QAbstractItemView, QTextEdit
from source.summary.summaryanalyze import SummaryAnal
# from source.threads.summplotthread import 
import pandas as pd
     
class SummaryWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.Window)
        self.setGeometry(100, 100, 500, 650)
        self.setWindowTitle("Configure Summary Plots")
        self.layout = QGridLayout()
        
        # self.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
        #                                [0,100],[0,100],[0,1]]}
   
        self.paramDict = {}
        self.varlist = []
        self.dataTransformList = []
        self.transformList = []

        
        self.home()
        
    def home(self): #initialise dialog for summary combine
        self.summary = None
        # self.sumDialog = QDialog(self)
        # self.sumDialog.setWindowTitle("Configure Summary Plots")
##        self.sumDialog.resize(300, 300)
        
        dataSourceLabel = QLabel("From:", self)
        dataSource = QComboBox(self)
        dataSource.addItems(['File', 'Folder', 'Filelist sheet'])
        self.paramDict['Data source'] = dataSource
        
        dataFormatLabel = QLabel("Format:", self)
        dataFormat = QComboBox(self)
        dataFormat.addItems(['ASCII', 'Excel'])
        self.paramDict['Data format'] = dataFormat
        
        delimLabel = QLabel("Delimiter:", self)
        delimText =  QComboBox(self)
        delimText.addItems(['tab', 'space', 'comma', 'semicolon', 'colon', 'dot',
                            'pipe', 'double pipe', 'backslash', 'forward slash'])
        self.paramDict['Delimiter'] = delimText
        
        headerLabel = QLabel("Header line:", self)
        headerLine =  QSpinBox(self)
        headerLine.setValue(0)
        self.paramDict['Header line'] = headerLine
        
        subfolderLabel = QLabel("Sub folder:", self)
        self.subfolder =  QTextEdit(self)
        self.subfolder.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.subfolder.setText('/Analysis/Summary/')
        self.paramDict['Subfolder'] = self.subfolder    
              
        #import data
        importButton = QPushButton("Select..", self)    
        importButton.clicked.connect(lambda: self.import_data(dataSource))
        
        #create variable
        self.variable_dialog_init()
        createVar = QPushButton("Create Variable..", self)    
        createVar.clicked.connect(self.makeVarDialog.show)
        
        #create pivot table
        self.pivot_dialog_init()
        createPivot = QPushButton("Pivot..", self)    
        createPivot.clicked.connect(self.pivotDialog.show)
        
        #melt data (reshape)
        self.melt_dialog_init()
        meltData = QPushButton("Reshape..", self)    
        meltData.clicked.connect(self.meltDialog.show)
        
        #filter data
        self.filter_dialog_init()   
        filterButton = QPushButton("Filter..", self)
        filterButton.clicked.connect(self.filterDialog.show)
        
        transformStepsButton = QPushButton("Steps:", self)
        transformStepsButton.clicked.connect(self.show_transform_data)
        
        self.transformSteps = DraggableListWidget(copyItem = True, 
                                                  delMethod = self.update_transform)
        self.transformSteps.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.transformSteps.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        # self.transformSteps.model().rowsRemoved.connect(lambda: self.update_transform)
        
        #TODO: assign widget to VALUES of pivot table for "groupby" function selection
        # testBtn = QPushButton('Test')
        # self.transformSteps.setItemWidget(self.transformSteps.item(2), testBtn)
        
        self.filenameLabel = QLabel("", self)
        self.filenameLabel.setWordWrap(True)
        self.paramDict['File name'] = self.filenameLabel
        
        # dataSource.indexChanged.connect(lambda: self.source_changed(dataSource, 
        #                                                           importButton))        
        
        #plot data
        plotTypeLabel = QLabel("Plot Type", self)
        plotType = QComboBox(self)
        self.rel_types = ["line", "scatter"]
        self.cat_types = ["strip", "swarm", "box", "violin",
                          "boxen", "point", "bar", "count"]
        plotType.addItems(self.rel_types + self.cat_types)
        plotType.currentIndexChanged.connect(lambda: self.plot_type_changed(plotType.currentText()))
        self.paramDict['Plot type'] = plotType
        
        xLabel = QLabel("X Variable", self)
        self.xVar = QComboBox(self)
        self.paramDict['X Variable'] = self.xVar
        
        yLabel = QLabel("Y Variable", self)
        self.yVar = QComboBox(self)
        self.paramDict['Y Variable'] = self.yVar
        
        groupVarLabel = QLabel("<b>Group By:</b>", self)
        
        colorLabel = QLabel("Color", self)
        self.colorVar = QComboBox(self)
        self.paramDict['Color Parameter'] = self.colorVar
        
        columnLabel = QLabel("Column", self)
        self.columnVar = QComboBox(self)
        self.paramDict['Column Parameter'] = self.columnVar
        
        rowLabel = QLabel("Row", self)
        self.rowVar = QComboBox(self)
        self.paramDict['Row Parameter'] = self.rowVar

        styleLabel = QLabel("Style", self)
        self.styleVar = QComboBox(self)
        self.paramDict['Style Parameter'] = self.styleVar
        
        sizeLabel = QLabel("Size", self)
        self.sizeVar = QComboBox(self)
        self.paramDict['Size Parameter'] = self.sizeVar
        
        plotTitleLabel = QLabel("Title", self)
        plotTitle =  QLineEdit(self)
        plotTitle.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        # plotTitle.textChanged.connect(lambda: self.update_summary_dict('title',
        #                                                                plotTitle.text(),
        #                                                                0))
        plotTitle.setText('Test')
        self.paramDict['Title'] = plotTitle
        
        calcStats = QCheckBox('Calculate stats', self)
        self.paramDict['Calculate stats'] = calcStats
        
        previewPlot = QCheckBox('Preview plot', self)
        self.paramDict['Preview'] = previewPlot
        
        # self.calcStats = QCheckBox('Calculate Stats', self)
        #datetime format
        datetimeLabel = QLabel("Datetime Format", self)
        datetimeFormat = QComboBox(self)
        datetimeFormat.addItems(['Date', 'Time', 'Datetime'])
        self.paramDict['Datetime format'] = datetimeFormat
        
        #plot format
        formatLabel = QLabel("Save as", self)
        self.saveFormat = QComboBox(self) #plot save format
        self.saveFormat.addItems(['jpg', 'svg', 'pdf', 'png', 'tif', 'tiff'])
        # self.paramDict['Save format'] = saveFormat
        
        self.showMarkers = QCheckBox('Show Markers', self)
        self.paramDict['Show Markers'] = self.showMarkers
        
        fontScaleLabel = QLabel("Font Scale", self)
        fontScale = QDoubleSpinBox(self)
        fontScale.setSingleStep(0.1)
        # fontScale.setRange(0, 1)
        fontScale.setValue(1)
        self.paramDict['Font scale'] = fontScale
        
        contextLabel = QLabel("Context", self)
        context = QComboBox(self)
        context.addItems(['paper', 'notebook', 'talk', 'poster'])
        self.paramDict['Plot context'] = context
        
        plotStyleLabel = QLabel("Style", self)
        plotStyle = QComboBox(self)
        plotStyle.addItems(['ticks', 'darkgrid', 'whitegrid', 'dark', 'white'])
        self.paramDict['Plot style'] = plotStyle
        
        colorPaletteLabel = QLabel("Color Palette", self)
        colorPalette = QComboBox(self)
        colorPalette.addItems(['None', 'deep', 'muted', 'bright', 
                               'pastel', 'dark', 'colorblind',
                               'Set1', 'Set2', 'Set3', 'Paired', 
                               'Reds', 'Blues','Greens', 'Oranges',
                               'viridis', 'plasma', 'inferno', 'magma', 
                               'hot', 'afmhot', 'cool', 
                               'hsv', 'gnuplot', 'terrain'])
        self.paramDict['Color palette'] = colorPalette
        
        rotateXLabel = QLabel("Rotate X Labels", self)
        rotateX = QSpinBox(self)
        rotateX.setValue(0)
        self.paramDict['X label rotate'] = rotateX
        
        zeroLine = QCheckBox('Zero Line', self)
        self.paramDict['Zero line'] = zeroLine
        
        applyDespine = QCheckBox('Despine', self)
        self.paramDict['Despine'] = applyDespine
        
        legendSettings = QLabel("<b>Legend Settings:</b>", self)
        legendPos = QCheckBox('Outside plot', self)
        self.paramDict['Legend outside'] = legendPos
        
        legendLocLabel = QLabel("Location", self)
        legendLoc = QComboBox(self)
        legendLoc.addItems(['best','upper right','upper left','lower left',
                            'lower right','right','center left','center right',
                            'lower center','upper center','center'])
        self.paramDict['Legend location'] = legendLoc
        
        legendColLabel = QLabel("Columns", self)
        legendCol = QSpinBox(self)
        legendCol.setValue(1)
        self.paramDict['Legend columns'] = legendCol
        
        
        
        # plotFormat.currentIndexChanged.connect(lambda:
        #                                        self.update_summary_dict('format',
        #                                                                 plotFormat.currentText(),
        #                                                                 0))
        # fitLabel = QLabel("<b>Fit</b>", self.sumDialog)
        # orderLabel = QLabel("<b>Order</b>", self.sumDialog)

        # self.summaryDict = {'x var': [None, None, None, None],
        #                     'y var': [None, None, None, None],
        #                     'cbar var': [None, None, None, None],
        #                     'plot num': [None, None, None, None],
        #                     'fit': [None, None, None, None],
        #                     'order': [None, None, None, None],
        #                     'title': [None], 
        #                     'format': [None],
        #                     'plot type': ["Scatter"]} #initialize

        
        
        
        # self.update_summary_dict('format', plotFormat.currentText(), 0)
        
        # self.grouplist = ["Date", "Folder_Name", "Species", "Sex", "Leg", "Pad",
        #                    "Weight", "Temperature", "Humidity", "Medium",
        #                    "Substrate", "Contact_Angle-Water", "Contact_Angle-Hexadecane",
        #                    "Label", "ROI Label","Measurement_Number", "Contact_Time", 
        #                    "Detachment Speed", "Attachment Speed", "Sliding Speed", 
        #                    "Sliding_Step"]
        # self.grouplist.sort()

        
        # ind = groupVar.findText("ROI Label")
        # groupVar.setCurrentIndex(groupVar.findText("ROI Label"))
##        groupVar.setEnabled(False)

        
        

        # combine.stateChanged.connect(lambda: self.combine_toggled(groupVar, combine, okButton))       
        # okButton.clicked.connect(lambda: self.combine_summary_data(combine.isChecked(),
        #                                                            groupVar.currentText()))


        
##        okButton.setDefault(True)
        #buttons
        self.showPlot = QPushButton("Show Plot", self)
        self.showPlot.clicked.connect(self.show_summary_plots)
        self.showPlot.setEnabled(False)
        
        self.savePlot = QPushButton("Save Plot", self)        
        self.savePlot.clicked.connect(self.export_summary_plots)
        self.savePlot.setEnabled(False)
        
        # self.show_data_init()   #initialize data dialog
        self.dataDialog = PandasTableWidget()
        self.statsButton = QPushButton("Show Stats", self)
        self.statsButton.clicked.connect(self.show_stats)
        self.statsButton.setEnabled(False)
        
        closeButton = QPushButton("Close", self)
        closeButton.clicked.connect(self.close)
        

        # gridLayout = QGridLayout(self)
        
        importGroupBox = QGroupBox("Import Data")
        importGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        importLayout = QGridLayout()
        importGroupBox.setLayout(importLayout)
        importLayout.addWidget(dataSourceLabel, 0, 0, 1, 1)
        importLayout.addWidget(dataSource, 0, 1, 1, 1)
        importLayout.addWidget(dataFormatLabel, 0, 2, 1, 1)
        importLayout.addWidget(dataFormat, 0, 3, 1, 1)
        importLayout.addWidget(delimLabel, 1, 0, 1, 1)
        importLayout.addWidget(delimText, 1, 1, 1, 1)
        importLayout.addWidget(headerLabel, 1, 2, 1, 1)
        importLayout.addWidget(headerLine, 1, 3, 1, 1)
        importLayout.addWidget(subfolderLabel, 2, 0, 1, 1)
        importLayout.addWidget(self.subfolder, 2, 1, 1, 3)
        importLayout.addWidget(importButton, 3, 0, 1, 1)
        importLayout.addWidget(self.filenameLabel, 3, 1, 1, 3)
        
        transformGroupBox = QGroupBox("Transform Data")
        transformGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        transformLayout = QGridLayout()
        transformGroupBox.setLayout(transformLayout)
        transformLayout.addWidget(createVar, 2, 0, 1, 1)
        transformLayout.addWidget(createPivot, 3, 0, 1, 1)
        transformLayout.addWidget(meltData, 0, 0, 1, 1)
        transformLayout.addWidget(filterButton, 1, 0, 1, 1)
        transformLayout.addWidget(transformStepsButton, 0, 1, 1, 1)
        transformLayout.addWidget(self.transformSteps, 1, 1, 3, 1)
        
        plotGroupBox = QGroupBox("Plot Data")
        plotGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        plotLayout = QGridLayout()
        plotGroupBox.setLayout(plotLayout)
        plotLayout.addWidget(plotTypeLabel, 0, 0, 1, 1)
        plotLayout.addWidget(plotType, 0, 1, 1, 1)
        plotLayout.addWidget(xLabel, 1, 0, 1, 1)
        plotLayout.addWidget(self.xVar, 1, 1, 1, 1)
        plotLayout.addWidget(yLabel, 2, 0, 1, 1)
        plotLayout.addWidget(self.yVar, 2, 1, 1, 1)
        plotLayout.addWidget(plotTitleLabel, 3, 0, 1, 1)
        plotLayout.addWidget(plotTitle, 3, 1, 1, 1)
        plotLayout.addWidget(calcStats, 4, 0, 1, 1)
        plotLayout.addWidget(previewPlot, 5, 0, 1, 1)
        
        # plotLayout.addWidget(self.calcStats, 5, 0, 1, 2)
        # self.summary_layout_make(1, 'Pulloff_Area', 'Adhesion_Force',
        #                          'Detachment Speed', gridLayout, 2)
        # self.summary_layout_make(2, 'Pulloff_Area', 'Adhesion_Force',
        #                          'Adhesion_Preload', gridLayout, 3)
        # self.summary_layout_make(3, 'Pulloff_Area', 'Adhesion_Force',
        #                          'Contact_Time', gridLayout, 4)
        # self.summary_layout_make(4, 'Pulloff_Area', 'Adhesion_Force',
        #                          'Sliding_Step', gridLayout, 5)
        plotLayout.addWidget(groupVarLabel, 0, 2, 1, 2, alignment = Qt.AlignCenter)
        plotLayout.addWidget(colorLabel, 1, 2, 1, 1)
        plotLayout.addWidget(self.colorVar, 1, 3, 1, 1)
        plotLayout.addWidget(columnLabel, 2, 2, 1, 1)
        plotLayout.addWidget(self.columnVar, 2, 3, 1, 1)
        plotLayout.addWidget(rowLabel, 3, 2, 1, 1)
        plotLayout.addWidget(self.rowVar, 3, 3, 1, 1)
        plotLayout.addWidget(styleLabel, 4, 2, 1, 1)
        plotLayout.addWidget(self.styleVar, 4, 3, 1, 1)
        plotLayout.addWidget(sizeLabel, 5, 2, 1, 1)
        plotLayout.addWidget(self.sizeVar, 5, 3, 1, 1)        
        
        
        plotFormatGroupBox = QGroupBox("Plot Format")
        plotFormatGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        plotFormatLayout = QGridLayout()
        plotFormatGroupBox.setLayout(plotFormatLayout)        
        
        
        plotFormatLayout.addWidget(contextLabel, 0, 0, 1, 1)
        plotFormatLayout.addWidget(context, 0, 1, 1, 1)
        plotFormatLayout.addWidget(plotStyleLabel, 1, 0, 1, 1)
        plotFormatLayout.addWidget(plotStyle, 1, 1, 1, 1)
        plotFormatLayout.addWidget(colorPaletteLabel, 2, 0, 1, 1)
        plotFormatLayout.addWidget(colorPalette, 2, 1, 1, 1)
        plotFormatLayout.addWidget(fontScaleLabel, 3, 0, 1, 1)
        plotFormatLayout.addWidget(fontScale, 3, 1, 1, 1)
        plotFormatLayout.addWidget(rotateXLabel, 4, 0, 1, 1)
        plotFormatLayout.addWidget(rotateX, 4, 1, 1, 1)
        plotFormatLayout.addWidget(datetimeLabel, 5, 0, 1, 1)
        plotFormatLayout.addWidget(datetimeFormat, 5, 1, 1, 1)
        plotFormatLayout.addWidget(formatLabel, 6, 0, 1, 1)
        plotFormatLayout.addWidget(self.saveFormat, 6, 1, 1, 1)
        plotFormatLayout.addWidget(self.showMarkers, 0, 2, 1, 1)        
        plotFormatLayout.addWidget(zeroLine, 1, 2, 1, 1)
        plotFormatLayout.addWidget(applyDespine, 0, 3, 1, 1)
        plotFormatLayout.addWidget(legendSettings, 2, 2, 1, 2, alignment = Qt.AlignCenter)
        plotFormatLayout.addWidget(legendPos, 3, 2, 1, 1)
        plotFormatLayout.addWidget(legendLocLabel, 4, 2, 1, 1)
        plotFormatLayout.addWidget(legendLoc, 4, 3, 1, 1)
        plotFormatLayout.addWidget(legendColLabel, 5, 2, 1, 1)
        plotFormatLayout.addWidget(legendCol, 5, 3, 1, 1)
        
        
        
        
        buttonGroupBox = QGroupBox()
        buttonGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        buttonLayout= QGridLayout()
        buttonGroupBox.setLayout(buttonLayout)
        buttonLayout.addWidget(self.showPlot, 0, 0, 1, 1)
        buttonLayout.addWidget(self.savePlot, 0, 1, 1, 1)
        buttonLayout.addWidget(self.statsButton, 0, 2, 1, 1)
        buttonLayout.addWidget(closeButton, 0, 3, 1, 1)
        
        
        self.layout.addWidget(importGroupBox, 0, 0, 1, 1)
        self.layout.addWidget(transformGroupBox, 0, 1, 1, 1)
        self.layout.addWidget(plotGroupBox, 1, 0, 1, 2)
        self.layout.addWidget(plotFormatGroupBox, 2, 0, 1, 2)
        self.layout.addWidget(buttonGroupBox, 3, 0, 1, 2)
        
        self.setLayout(self.layout)
        
##        self.sumDialog.show()

    # def summary_layout_make(self, plotnum, x_init, y_init, cb_init,
    #                         layout, vpos):
        
    #     varlist = ["Adhesion_Force", "Adhesion_Preload", "Friction_Force",
    #                "Friction_Preload", "Max_Area", "Pulloff_Area",
    #                "Friction_Area", "ROI_Max_Area", "ROI_Pulloff_Area",
    #                "Max_Length", "Pulloff_Length", "ROI_Max_Length",
    #                "ROI_Pulloff_Length", "Pulloff_Contact_Number",
    #                "Residue_Area", "Pulloff_Median_Eccentricity", "ROI Label",
    #                "Measurement_Number", "Contact_Time", "Detachment Speed",
    #                "Attachment Speed", "Sliding Speed", "Sliding_Step", "Slope",
    #                "Adhesion_Stress", "Friction_Stress", 
    #                "Normalized_Adhesion_Force", "Beam_Spring_Constant",
    #                "Initial_Deformation","Pulloff_Deformation","Adhesion_Energy",
    #                "Max_Bounding_Area", "Max_Bounding_Perimeter",
    #                "Max_Bounding_Length", "Max_Bounding_Width", 
    #                "Normalized_Adhesion_Energy", "Date_of_Experiment"]
    #     varlist.sort()
    #     plotLabel = QLabel(str(plotnum), self.sumDialog)
    #     self.update_summary_dict('plot num', plotnum, plotnum-1)

    #     xVar = QComboBox(self.sumDialog) #x variable
    #     xVar.addItems(varlist)
    #     xVar.currentIndexChanged.connect(lambda: self.update_summary_dict('x var',
    #                                                                       xVar.currentText(),
    #                                                                       plotnum-1))
    #     xVar.setCurrentIndex(xVar.findText(x_init))
    #     self.update_summary_dict('x var', xVar.currentText(), plotnum-1)

    #     yVar = QComboBox(self.sumDialog) #y variable
    #     yVar.addItems(varlist)
    #     yVar.currentIndexChanged.connect(lambda: self.update_summary_dict('y var',
    #                                                                       yVar.currentText(),
    #                                                                       plotnum-1))
    #     yVar.setCurrentIndex(yVar.findText(y_init))
    #     self.update_summary_dict('y var', yVar.currentText(), plotnum-1)
        
    #     colorbarVar = QComboBox(self.sumDialog) #colorbar variable
    #     colorbarVar.addItems(varlist)
    #     colorbarVar.currentIndexChanged.connect(lambda: self.update_summary_dict('cbar var',
    #                                                                              colorbarVar.currentText(),
    #                                                                              plotnum-1))
    #     colorbarVar.setCurrentIndex(colorbarVar.findText(cb_init))
    #     self.update_summary_dict('cbar var', colorbarVar.currentText(), plotnum-1)

    #     polyfit = QCheckBox(self.sumDialog) #polynomial fit
    #     polyfit.stateChanged.connect(lambda: self.update_summary_dict('fit',
    #                                                                   polyfit.isChecked(),
    #                                                                   plotnum-1))
    #     self.update_summary_dict('fit', polyfit.isChecked(), plotnum-1)

    #     polyorder = QSpinBox(self.sumDialog) #polynomial order
    #     polyorder.valueChanged.connect(lambda: self.update_summary_dict('order',
    #                                                                   polyorder.value(),
    #                                                                   plotnum-1))
    #     polyorder.setRange(1, 10)
    #     polyorder.setValue(1)
    #     self.update_summary_dict('order', polyorder.value(), plotnum-1)
        
    #     layout.addWidget(plotLabel, vpos, 0, 1, 1)
    #     layout.addWidget(xVar, vpos, 1, 1, 1)
    #     layout.addWidget(yVar, vpos, 2, 1, 1)
    #     layout.addWidget(colorbarVar, vpos, 3, 1, 1)
    #     layout.addWidget(polyfit, vpos, 4, 1, 1, alignment = Qt.AlignCenter)
    #     layout.addWidget(polyorder, vpos, 5, 1, 1)

#     def combine_toggled(self, source, importButton):
# ##        groupVar.setEnabled(combine.isChecked())
#         oktext = "Select summary file.." if source.currentText() == False \
#                  else "Select experiment list.."
#         importButton.setText(oktext)
    
    #update list of variables in dropdown
    def update_dropdown_params(self):
        # self.varlist = list(map(str,self.datadf_filtered.columns))
        self.varlist = list(map(str,self.dataTransformList[-1].columns))
        self.varlist.sort()
        var_list = ['None'] + self.varlist
        #combobox widgets
        combobox_wids = [self.xVar, self.yVar, self.colorVar, self.columnVar,
                         self.rowVar, self.styleVar, self.sizeVar]
        for wid in combobox_wids:
            if var_list != [wid.itemText(i) for i in range(wid.count())]:
                wid.clear()
                wid.addItems(var_list)
        
        list_wids = [self.pivotVars, self.varListWid, self.meltVars] #list widgets
        for wid in list_wids:
            if self.varlist != [wid.item(i).text() for i in range(wid.count())]:
                wid.clear()
                wid.addItems(self.varlist)
        
        self.transformSteps.clear()
        self.transformSteps.addItems(self.transformList)
        # self.xVar.addItems(['None'] + self.varlist)
        # self.yVar.addItems(['None'] + self.varlist)
        # self.colorVar.addItems(['None'] + self.varlist)
        # self.columnVar.addItems(['None'] + self.varlist)
        # self.rowVar.addItems(['None'] + self.varlist)
        # self.styleVar.addItems(['None'] + self.varlist)
        # self.sizeVar.addItems(['None'] + self.varlist)  
    
    #update tansform lists on step item delete
    def update_transform(self):
        print('deleted')
        stepnum = [int(self.transformSteps.item(i).text().split(':')[0]) \
                   for i in range(self.transformSteps.count())]
        list_len = len(self.transformList)
        j = 0
        for i in range(list_len):
            if i not in stepnum:
                if i != 0:
                    del self.transformList[i-j]
                    del self.dataTransformList[i-j]
                    j += 1
                else: #dont delete raw data
                    self.transformSteps.insertItem(0, '0:Raw data')
        #reset number order
        for i in range(self.transformSteps.count()):
            text = self.transformSteps.item(i).text()
            self.transformList[i] = str(i) + ':' + text.split(':')[1]
            self.transformSteps.item(i).setText(self.transformList[i])                
            
    # disable/enable relevant combo boxes
    def plot_type_changed(self, plot_type):
        if plot_type in self.rel_types:
            self.styleVar.setEnabled(True)
            self.sizeVar.setEnabled(True)
            self.showMarkers.setEnabled(True)
        elif plot_type in self.cat_types:
            self.styleVar.setEnabled(False)
            self.sizeVar.setEnabled(False)
            self.showMarkers.setEnabled(False)
            
    # def update_summary_dict(self, key, value, plotnum):
    #     self.summaryDict[key][plotnum] = value
        
    def import_data(self, source): #import summary data
##        self.sumDialog.reject()
##        legend_parameter = self.sumlistwidget.currentItem().text()
        self.reset_summary()
        self.summary = SummaryAnal()
        if source.currentText() == 'Filelist sheet':
            self.filepath, _ =  QFileDialog.getOpenFileName(caption =
                                                            "Select experiment list file")
            if self.filepath != "":
                self.dataTransformList = []
                self.transformList = []
                self.folderpath = os.path.dirname(self.filepath)
                self.datadf = self.summary.combineSummaryFromList(list_filepath = self.filepath,
                                                                  subfolder = self.subfolder.toPlainText(),
                                                                  data_format = self.paramDict['Data format'].currentText(),
                                                                  delimiter = self.paramDict['Delimiter'].currentText(),
                                                                  header_line = self.paramDict['Header line'].value())
                
            # if self.summary.list_filepath != "":
                # self.comb = True
                # self.statusBar.showMessage("Summary Data combined!")
                # self.datadf_filtered = self.summary.filter_df(self.datadf,
                #                                               self.filter_dict)
                self.dataTransformList.append(self.datadf)
                stepnum = str(len(self.transformList))
                self.transformList.append(stepnum +':Raw data')
                
                self.update_dropdown_params()
                
                self.showPlot.setEnabled(True)
                self.savePlot.setEnabled(False)
                self.statsButton.setEnabled(True)
                self.filenameLabel.setText(self.filepath)
                # self.summary.plotSummary(self.summaryDict,
                #                          self.summary.df_final,
                #                          self.summary.df_final,
                #                          legend_parameter)
                # self.summary.showSummaryPlot()
            # else:
            #     # self.statusBar.showMessage("No file selected")
            #     # self.comb = False
            #     self.summary = None
        elif source.currentText() == 'File':
            # self.comb = False
            self.filepath, _ = QFileDialog.getOpenFileName(caption =
                                                           "Select summary data file")            
            if self.filepath != "":
                self.dataTransformList = []
                self.transformList = []
                self.folderpath = os.path.dirname(self.filepath)
                self.datadf = self.summary.importSummary(filepath = self.filepath,
                                                         data_format = self.paramDict['Data format'].currentText(),
                                                         delimiter = self.paramDict['Delimiter'].currentText(),
                                                         header_line = self.paramDict['Header line'].value())
                # self.create_var('test var [mPa^2]', '''['Pulloff Force']/['Pulloff Area']''') #CHECK
                
            # if self.summary.summary_filepath != "":
                # self.datadf_filtered = self.summary.filter_df(self.datadf, 
                #                                               self.filter_dict)
                self.dataTransformList.append(self.datadf)
                stepnum = str(len(self.transformList))
                self.transformList.append(stepnum +':Raw data')
                
                self.update_dropdown_params()
                
                self.showPlot.setEnabled(True)
                self.savePlot.setEnabled(False)
                self.statsButton.setEnabled(True)
                self.filenameLabel.setText(self.filepath)
                # self.summary.plotSummary(self.summaryDict,
                #                          self.summary.df_final,
                #                          self.summary.df_final,
                #                          legend_parameter)
                # self.summary.showSummaryPlot()
            # else:
            #     self.summary = None
        elif source.currentText() == 'Folder':
            self.folderpath = QFileDialog.getExistingDirectory(caption =
                                                           "Select folder")
            if self.folderpath != "":
                self.dataTransformList = []
                self.transformList = []
                self.datadf = self.summary.combineSummaryFromFolder(folderpath = self.folderpath,
                                                                    subfolder = self.subfolder.toPlainText(),
                                                                    data_format = self.paramDict['Data format'].currentText(),
                                                                    delimiter = self.paramDict['Delimiter'].currentText(),
                                                                    header_line = self.paramDict['Header line'].value())
                
            # if self.summary.summary_filepath != "":
                # self.datadf_filtered = self.summary.filter_df(self.datadf, 
                #                                               self.filter_dict)
                self.dataTransformList.append(self.datadf)
                stepnum = str(len(self.transformList))
                self.transformList.append(stepnum +':Raw data')
                
                self.update_dropdown_params()
                
                self.showPlot.setEnabled(True)
                self.savePlot.setEnabled(False)
                self.statsButton.setEnabled(True)
                self.filenameLabel.setText(self.folderpath)
                # self.summary.plotSummary(self.summaryDict,
                #                          self.summary.df_final,
                #                          self.summary.df_final,
                #                          legend_parameter)
                # self.summary.showSummaryPlot()
            # else:
            #     self.summary = None
        
        
    def export_summary_plots(self): #export summary plots
        # if self.comb == False and self.summary == None:
        #     self.reset_summary()
        #     self.summary = SummaryAnal()
        #     self.summary.importSummary()
        #     if self.summary.summary_filepath != "":
        #         # self.summary.filter_df(self.filter_dict)
        #         # self.summary.plotSummary(self.summaryDict,
        #         #                           self.summary.df_final,
        #         #                           self.summary.df_final)
        #         self.summary.plotSummary()
        #     else:
        #         self.summary = None
        #save summary plots in separate thread
        if self.summary != None:
            # saveSummPlotThread = SummPlotThread(self.summary,
            #                                     self.summaryDict['format'][0])
            # saveSummPlotThread.output.connect(self.process_indicate)
            # saveSummPlotThread.finished.connect(self.save_plot_indicate)
            # saveSummPlotThread.start()
            # self.summary.plotSummary(self.datadf_filtered, self.paramDict)
            self.summary.saveSummaryPlot(self.folderpath,
                                         self.saveFormat.currentText())
             #export data to excel 
            # self.datadf_filtered.to_excel(self.folderpath +
            #                        '/summary_data_' + self.paramDict['Title'].text() + 
            #                        '-' + time.strftime("%y%m%d%H%M%S") + '.xlsx')
            
            #export data and stats to excel
            filepath = self.folderpath + '/summary_data_' + \
                self.paramDict['Title'].text() + '-' + \
                    time.strftime("%y%m%d%H%M%S") + '.xlsx'
            writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
            self.dataTransformList[-1].to_excel(writer, sheet_name='data')
            #save statistics
            self.summary.calculateStats(self.dataTransformList[-1], self.paramDict)
            for key in self.summary.statDf.keys():
                self.summary.statDf[key].to_excel(writer, sheet_name=key)
                
            #export settings
            self.make_param_series()
            self.paramSeries.to_excel(writer, sheet_name='settings')
            # aov.to_excel(writer, sheet_name='anova')
            # norm_test.to_excel(writer, sheet_name='norm_test')
            # var_eq_test.to_excel(writer, sheet_name='variance_eq_test')
            writer.save()              

        print("saved data")            

    #create series of parameter values
    def make_param_series(self):
        self.paramSeries = pd.Series(name = 'Value')
        for key in self.paramDict.keys():
            wid = self.paramDict[key]
            widtype = wid.__class__.__name__
            if widtype in ["QCheckBox", "QGroupBox"]:
                self.paramSeries[key] = str(wid.isChecked())
            elif widtype in ["QComboBox"]:
                self.paramSeries[key] = str(wid.currentText())
            elif widtype in ["QLineEdit", "QLabel"]:
                self.paramSeries[key] = wid.text()
            elif widtype in ["QTextEdit"]:
                self.paramSeries[key] = wid.toPlainText()
            elif widtype in ["dict", 'list', 'NoneType']: #dictionary/tuple/None
                self.paramSeries[key] = str(wid)
            else:    
                self.paramSeries[key] = str(wid.value())
        
        filter_cond = ' '.join([' '.join(map(str,cond)) for cond in self.filter_dict.values()])
        self.paramSeries['Filter condition'] = filter_cond

                
    # def save_plot_indicate(self):
    #     self.statusBar.showMessage("Summary Plots saved!")
    #export data and stats
    # def export_data(self):

    #     filepath = self.folderpath + '/summary_data_' + \
    #         self.paramDict['Title'].text() + '-' + \
    #             time.strftime("%y%m%d%H%M%S") + '.xlsx'
    #     writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    #     self.datadf_filtered..to_excel(writer, sheet_name='data')
    #     #save statistics
    #     for key in self.summary.statDf.keys():
    #         df[key].to_excel(writer, sheet_name=key)
    #     # aov.to_excel(writer, sheet_name='anova')
    #     # norm_test.to_excel(writer, sheet_name='norm_test')
    #     # var_eq_test.to_excel(writer, sheet_name='variance_eq_test')
    #     writer.save()        

    def show_summary_plots(self): #show summary plots
        # if self.comb == False and self.summary == None:
        #     self.reset_summary()
        #     self.summary = SummaryAnal()
        #     self.summary.importSummary()
        #     if self.summary.summary_filepath != "":
        #         # self.summary.filter_df(self.filter_dict)
        #         # self.summary.plotSummary(self.summaryDict,
        #         #                          self.summary.df_final,
        #         #                          self.summary.df_final)
        #         self.summary.plotSummary()
        #     else:
        #         self.summary = None
        if self.summary != None:
            self.summary.plotSummary(self.dataTransformList[-1], self.paramDict)
            # self.update_plot()
            self.summary.showSummaryPlot(self.paramDict)
            self.savePlot.setEnabled(True)
            # self.summary.showSummaryPlot()
    
    #show statistical data
    def show_stats(self):
        if self.summary != None:
            self.summary.calculateStats(self.dataTransformList[-1], self.paramDict)
            dataframes = self.summary.statDf.copy()
            dataframes['data'] = self.dataTransformList[-1]
            
            self.dataDialog.show_table(dataframes)
    
    def show_transform_data(self):
        if self.summary != None:
            dataDict = dict(zip(self.transformList, self.dataTransformList))
            self.dataDialog.show_table(dataDict)
            
            # # data_display = QWidget()
            # # data_display.setWindowTitle("Data")
            # # data_display.resize(100, 100)
            
            # # layout = QGridLayout(data_display)
            
            # # data_tabs = QTabWidget() #B&C and flitering tabs
            # self.dataTab.clear()
            
            # for key in dataframes.keys():
            #     # table = tabulate(dataframes[key], headers='keys', tablefmt = 'pretty')
            #     # wid = QTextEdit()
            #     # wid.setText(table)
            #     df = dataframes[key]
            #     table = QTableWidget()
            #     # model = PandasModel(df)
            #     # table.setModel(model)
            #     r, c = df.shape
            #     table.setColumnCount(c)
            #     table.setRowCount(r)
            #     for j in range(c):
            #         table.setHorizontalHeaderItem(j, QTableWidgetItem(str(df.columns[j])))
            #         for i in range(r):
            #             table.setItem(i, j, QTableWidgetItem(str(df.iloc[i,j])))
                
            #     self.dataTab.addTab(table,key)
                
            # # layout.addWidget(data_tabs, 0, 0, 1, 0)  
            
            # self.dataDialog.show()
    
    # #initialize data dialog
    # def show_data_init(self):
    #     self.dataDialog = QDialog(self)
    #     self.dataDialog.setWindowTitle("Data")
    #     self.dataDialog.resize(600, 400)
        
    #     layout = QGridLayout(self.dataDialog)
        
    #     self.dataTab = QTabWidget() #B&C and flitering tabs
        
    #     # for key in dataframes.keys():
    #     #     table = tabulate(dataframes[key], headers='keys', tablefmt = 'psql')
    #     #     wid = QTextEdit()
    #     #     wid.setText(table)
    #     #     data_tabs.addTab(wid,key)
            
    #     layout.addWidget(self.dataTab, 0, 0, 1, 0)
    
    #update plot data and draw canvas
    # def update_plot(self):
    #     self.summary.plotSummary(self.datadf_filtered, self.paramDict)

    def reset_summary(self): #reset self.comb to False
        # self.comb = False
        self.summary = None

        # self.filter_dialog_init()
##        self.summary_dialog_init()
        cv2.destroyAllWindows()
        plt.clf()
        plt.cla()
        plt.close()
        gc.collect()
        # self.statusBar.showMessage("Reset!")

    # def close_summary(self):
    #     self.sumDialog.done(0)
    
    def variable_dialog_init(self):
        self.makeVarDialog = QDialog(self)
        self.makeVarDialog.setWindowTitle("Create New Variable")
        self.makeVarDialog.resize(468, 69)
        
        self.makeVarLayout = QGridLayout(self.makeVarDialog)
        
        varNameLabel = QLabel('Variable Name')
        formulaLabel = QLabel('Formula')
        
        self.makeVarAdd = QPushButton("ADD")
        self.makeVarAdd.clicked.connect(self.vardialog_add_widgets)
        
        self.makeVarOk = QPushButton("OK")
        self.makeVarOk.clicked.connect(self.close_variable_dialog)
        
        #variable list dialog
        self.varListWid = DraggableListWidget(copyItem = True)
        
        varListDlg = QDialog(self)
        varListDlg.setWindowTitle("Drag and drop variable")
        varListDlg.resize(250, 400)
        layout = QGridLayout(varListDlg)
        layout.addWidget(self.varListWid, 0, 0, 1, 1)
        
        
        self.varListBtn = QPushButton("Variables..")
        self.varListBtn.clicked.connect(varListDlg.show)
        
        self.makeVarLayout.addWidget(varNameLabel, 0, 0, 1, 1)
        self.makeVarLayout.addWidget(formulaLabel, 0, 1, 1, 1)
        self.makeVarLayout.addWidget(self.makeVarAdd, 1, 1, 1, 1)
        self.makeVarLayout.addWidget(self.makeVarOk, 1, 0, 1, 1)
        
        self.newVarDict = {} #variable name and formula dictionary
        self.newVarNum = 0 #number of defined varaibles (or rows)
        
        # self.vardialog_add_widgets()
    
    #add row of new variable input widgets
    def vardialog_add_widgets(self):
        self.newVarNum += 1
        self.newVarDict[self.newVarNum] = ['', '']
        
        varName =  QLineEdit()
        formula =  QTextEdit()
        
        varName.textChanged.connect(lambda: self.update_varname_dict(self.newVarNum,
                                                                     varName.text(),
                                                                    formula.toPlainText()))
        formula.textChanged.connect(lambda: self.update_varname_dict(self.newVarNum,
                                                                     varName.text(),
                                                                    formula.toPlainText()))

        varPlus = QPushButton("+")
        varMinus = QPushButton("-")
        
        widget_list = [varName, formula, varPlus, varMinus]
        
        varPlus.clicked.connect(lambda: self.add_remove_newvar('+', widget_list, 
                                                               self.newVarNum))
        varMinus.clicked.connect(lambda: self.add_remove_newvar('-', widget_list,
                                                                self.newVarNum))
        
        self.makeVarLayout.addWidget(varName, self.newVarNum, 0, 1, 1)
        self.makeVarLayout.addWidget(formula, self.newVarNum, 1, 1, 1)
        self.makeVarLayout.addWidget(varPlus, self.newVarNum, 2, 1, 1)
        self.makeVarLayout.addWidget(varMinus, self.newVarNum, 3, 1, 1)
        self.makeVarLayout.addWidget(self.varListBtn, self.newVarNum + 1, 0, 1, 1)
        # self.makeVarLayout.addWidget(self.makeVarAdd, self.newVarNum + 1, 2, 1, 2)
        self.makeVarLayout.addWidget(self.makeVarOk, self.newVarNum + 1, 1, 1, 1)
        
    def add_remove_newvar(self, action, wid_list, rownum):
        if action == '+':
            self.vardialog_add_widgets()
        elif action == '-':
            for wid in wid_list:
                self.makeVarLayout.removeWidget(wid)
                wid.deleteLater()
            self.newVarNum -= 1
            del self.newVarDict[rownum]
            if self.newVarNum == 0:
                self.makeVarLayout.removeWidget(self.varListBtn)
                self.makeVarLayout.addWidget(self.makeVarAdd, 1, 1, 1, 1)
                self.makeVarLayout.addWidget(self.makeVarOk, 1, 0, 1, 1)
            self.makeVarDialog.resize(468, 69)
            
    
    def update_varname_dict(self, rownum, var_name, formula):
        if var_name != '' and formula != '':
            self.newVarDict[rownum] = [var_name, formula]
        
    
    def close_variable_dialog(self):
        datadf_newvar = self.dataTransformList[-1].copy()
        for key in self.newVarDict.keys():
            datadf_newvar = self.summary.create_var(var_name = self.newVarDict[key][0],
                                                           formula = self.newVarDict[key][1],
                                                           datadf = datadf_newvar)
        self.dataTransformList.append(datadf_newvar)
        stepnum = str(len(self.transformList))
        self.transformList.append(stepnum +':Create variable')
        self.update_dropdown_params()

        # self.datadf_filtered = self.summary.filter_df(self.datadf, 
        #                                               self.filter_dict)
        self.makeVarDialog.done(0)


    #melt dialog to reshape datafame from wide-form to long-form
    def melt_dialog_init(self):
        self.meltDialog = QDialog(self)
        self.meltDialog.setWindowTitle("Reshape data")
        self.meltDialog.resize(400, 400)
        
        layout = QGridLayout(self.meltDialog)
        
        meltVarsLabel = QLabel('VARIABLES')
        self.meltVars = DraggableListWidget(copyItem = False)
        
        rowLabel = QLabel('ROWS')
        self.meltRowVars = DraggableListWidget(copyItem = False)
        
        varNameLabel = QLabel('VARIABLE NAME')
        self.meltVarName = QLineEdit()
        
        valueNameLabel = QLabel('VALUE NAME')
        self.meltValueName = QLineEdit()
        
        okbutton = QPushButton("OK")
        okbutton.clicked.connect(self.close_melt_dialog)

        layout.addWidget(meltVarsLabel, 0, 0, 1, 1)
        layout.addWidget(self.meltVars, 1, 0, 5, 1)
        layout.addWidget(rowLabel, 0, 1, 1, 1)
        layout.addWidget(self.meltRowVars, 1, 1, 1, 1)
        layout.addWidget(varNameLabel, 2, 1, 1, 1)
        layout.addWidget(self.meltVarName, 3, 1, 1, 1)
        layout.addWidget(valueNameLabel, 4, 1, 1, 1)
        layout.addWidget(self.meltValueName, 5, 1, 1, 1)
        layout.addWidget(okbutton, 6, 0, 1, 2)

    def close_melt_dialog(self):
        row_list = [self.meltRowVars.item(i).text() for i in range(self.meltRowVars.count())]
       
        if row_list != []:
            meltDict = {'Variable columns': row_list,
                        'Variable name': self.meltVarName.text(),
                        'Value name': self.meltValueName.text()}
            
            datadf_reshaped = self.summary.melt_df(df = self.dataTransformList[-1],
                                                        melt_dict = meltDict)
            self.dataTransformList.append(datadf_reshaped)
            stepnum = str(len(self.transformList))
            self.transformList.append(stepnum +':Reshape')
            self.update_dropdown_params()
        self.meltDialog.done(0)
        
    #pivot table dialog
    def pivot_dialog_init(self):
        self.pivotDialog = QDialog(self)
        self.pivotDialog.setWindowTitle("Pivot data")
        self.pivotDialog.resize(400, 400)
        
        layout = QGridLayout(self.pivotDialog)
        
        pivotVarsLabel = QLabel('VARIABLES')
        self.pivotVars = DraggableListWidget(copyItem = False)
        
        rowLabel = QLabel('ROWS')
        self.pivotRowVars = DraggableListWidget(copyItem = False)
        
        columnLabel = QLabel('COLUMNS')
        self.pivotColumnVars = DraggableListWidget(copyItem = False)
        
        valueLabel = QLabel('VALUES')
        self.pivotValueVars = DraggableListWidget(copyItem = False)
        
        groupbyLabel = QLabel('GROUP BY')
        self.pivotGroupFuncs = QComboBox(self.pivotDialog)
        func_list = ['sum', 'min', 'max', 'count', 'mean', 'median', 'std dev']
        self.pivotGroupFuncs.addItems(func_list)
        
        okbutton = QPushButton("OK")
        okbutton.clicked.connect(self.close_pivot_dialog)

        layout.addWidget(pivotVarsLabel, 0, 0, 1, 1)
        layout.addWidget(self.pivotVars, 1, 0, 5, 1)
        layout.addWidget(rowLabel, 0, 1, 1, 1)
        layout.addWidget(self.pivotRowVars, 1, 1, 1, 1)
        layout.addWidget(columnLabel, 2, 1, 1, 1)
        layout.addWidget(self.pivotColumnVars, 3, 1, 1, 1)
        layout.addWidget(valueLabel, 4, 1, 1, 1)
        layout.addWidget(self.pivotValueVars, 5, 1, 1, 1)
        layout.addWidget(groupbyLabel, 6, 0, 1, 1)
        layout.addWidget(self.pivotGroupFuncs, 6, 1, 1, 1)
        layout.addWidget(okbutton, 7, 0, 1, 2)
    
    def close_pivot_dialog(self):
        val_list = [self.pivotValueVars.item(i).text() for i in range(self.pivotValueVars.count())]
        row_list = [self.pivotRowVars.item(i).text() for i in range(self.pivotRowVars.count())]
        col_list = [self.pivotColumnVars.item(i).text() for i in range(self.pivotColumnVars.count())]
        
        #BUG: only first value taken
        val_list = val_list[0] if val_list != [] else None
        row_list = row_list if row_list != [] else None
        col_list = col_list if col_list != [] else None
        
        datadf_pivot = self.summary.create_pivot(df = self.dataTransformList[-1],
                                                          vals = val_list,
                                                          rows = row_list,
                                                          cols = col_list,
                                                          agg = self.pivotGroupFuncs.currentText())
        self.dataTransformList.append(datadf_pivot)
        stepnum = str(len(self.transformList))
        self.transformList.append(stepnum +':Pivot')
        self.update_dropdown_params()
        self.pivotDialog.done(0)
                
    def filter_dialog_init(self):
        self.filterDialog = QDialog(self)
        self.filterDialog.setWindowTitle("Filter")
        self.filterDialog.resize(468, 69)
        
        self.filterLayout = QGridLayout(self.filterDialog)
        
        self.filterOk = QPushButton("OK")
        self.filterOk.clicked.connect(self.close_filter_dialog)
        
        self.filter_count = 0
        self.filterAdd = QPushButton("ADD")
        self.filterAdd.clicked.connect(lambda: self.filter_add_widgets("Add",-1))

        self.filterLayout.addWidget(self.filterOk, 0, 0, 1, 2)
        self.filterLayout.addWidget(self.filterAdd, 0, 2, 1, 2)
        
        self.filter_dict = {}
        # self.filter_dialog_widgets(self.filter_count)
    
    def filter_dialog_widgets(self, rownum):
        
        filterValue =  QLineEdit()
        filterValue.textChanged.connect(lambda:
                                       self.update_filter_dict(rownum, 2,
                                            filterValue.text()))
        
        
        groupVar = QComboBox()
        groupVar.addItems(self.varlist)
        groupVar.currentIndexChanged.connect(lambda:
                                             self.filter_var_change(groupVar,
                                                                    filterValue, 
                                                                    rownum))
        filterValue.setToolTip('Example: ' + str(self.datadf[groupVar.currentText()][0]))
        
        conditionVar = QComboBox()
        conditionVar.addItems(["equal to", "not equal to", "less than", 
                                "greater than", "less than or equal to",
                                "greater than or equal to"])
        conditionVar.currentIndexChanged.connect(lambda:
                                                 self.update_filter_dict(rownum, 1,
                                                    conditionVar.currentText()))
            
        
            
        connectiveVar = QComboBox()
        connectiveVar.addItems(["None", "AND", "OR", "Delete"])
        connectiveVar.currentIndexChanged.connect(lambda: self.filter_add_widgets(
            connectiveVar.currentText(),rownum,self.filterLayout.indexOf(connectiveVar),
            groupVar, conditionVar, filterValue, connectiveVar))
        
        self.filterLayout.addWidget(groupVar, rownum, 0, 1, 1)
        self.filterLayout.addWidget(conditionVar, rownum, 1, 1, 1)
        self.filterLayout.addWidget(filterValue, rownum, 2, 1, 1)
        self.filterLayout.addWidget(connectiveVar, rownum, 3, 1, 1)
        self.filterLayout.addWidget(self.filterOk, rownum+1, 0, 1, 2)
        self.filterLayout.addWidget(self.filterAdd, rownum+1, 2, 1, 2)
        
        #filter dictionary: variable, condition, value, connective operator
        self.filter_dict[rownum] = [groupVar.currentText(), conditionVar.currentText(),
                                    filterValue.text(), connectiveVar.currentText()]
    
    def filter_var_change(self, groupVar, filterValue, rownum):
        self.update_filter_dict(rownum, 0, groupVar.currentText())
        filterValue.setToolTip('Example: ' + str(self.datadf[groupVar.currentText()][0]))
    
    def filter_add_widgets(self, var, key, itemnum=None, groupVar=None, 
                           conditionVar=None, filterValue=None, connectiveVar=None):
        if itemnum == None: #Add clicked
            rownum = self.filter_count-1
        else:
            rownum = int(((itemnum+1)/4)-1) #row number corresponding to changed item
        
        filter_keys = list(self.filter_dict.keys())
        filter_keys.sort()
                       
        if var == "Delete":
            self.filterLayout.removeWidget(groupVar)
            groupVar.deleteLater()
            self.filterLayout.removeWidget(conditionVar)
            conditionVar.deleteLater()
            self.filterLayout.removeWidget(filterValue)
            filterValue.deleteLater()
            self.filterLayout.removeWidget(connectiveVar)
            connectiveVar.deleteLater()                        
            
            
            # self.filterDialog.resize(self.filterDialog.size().width(),
            #                          self.filterDialog.minimumHeight())
            if rownum == self.filter_count-1 and self.filter_count > 1:
                widgetLast = self.filterLayout.itemAt((4*(self.filter_count-1))-1).widget()
                widgetLast.setCurrentIndex(widgetLast.findText("None")) 
                key_prev = filter_keys[filter_keys.index(key)-1]
                self.filter_dict[key_prev][3] = "None"
            
            del self.filter_dict[key]

            self.filter_count -= 1
            self.filterDialog.resize(468, 69)

        elif var in ["AND", "OR", "Add"]:
            if connectiveVar != None:
                self.filter_dict[key][3] = connectiveVar.currentText() 
            if rownum == self.filter_count-1 or key == -1:
                self.filter_count += 1
                key_new = max(filter_keys) + 1 if len(filter_keys) != 0  else 0
                self.filter_dialog_widgets(key_new)
        
        # self.filterDialog.update()       
        # print(self.filterDialog.sizeHint())
        # self.filterDialog.resize(self.filterDialog.sizeHint())
        
    def update_filter_dict(self, key, index, val):        
        self.filter_dict[key][index] = val
        
    def close_filter_dialog(self):
        print(self.filter_dict)
        datadf_filtered = self.summary.filter_df(self.dataTransformList[-1], self.filter_dict)
        self.dataTransformList.append(datadf_filtered)
        stepnum = str(len(self.transformList))
        self.transformList.append(stepnum +':Filter')
        self.update_dropdown_params()
        # self.summaryDict['filter'] = self.filter_dict
        self.filterDialog.done(0)
        
#draggable list widget
class DraggableTextListWidget(QListWidget):
    def mimeData(self, items):
        md = super().mimeData(items)
        text = ''.join([it.text() for it in items])
        md.setText(text)
        return md

#draggable list widget
#copyItem set to True to copy, False to move
class DraggableListWidget(QListWidget):
    def __init__(self, copyItem, delMethod = None):
        super().__init__()
        # self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QAbstractItemView.DragDrop)
        if copyItem == True:
            self.setDefaultDropAction(Qt.CopyAction)
        else:
            self.setDefaultDropAction(Qt.MoveAction)
        
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.delMethod = delMethod

    def mimeData(self, items):
        md = super().mimeData(items)
        text = "['" + ''.join([it.text() for it in items]) + "']"
        md.setText(text)
        return md

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(pyqtSignal("dropped"), links)
        else:
            event.setDropAction(Qt.MoveAction)
            super().dropEvent(event)
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                self.takeItem(self.row(item))
            if self.delMethod != None:
                self.delMethod()

class PandasTableWidget(QDialog):
    #initialize data dialog
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data")
        self.resize(600, 400)
        
        self.dataTab = QTabWidget()
        
        layout = QGridLayout(self)               
        layout.addWidget(self.dataTab, 0, 0, 1, 0)
        
    #show data
    #input dataDict: dict with table name and dataframe
    def show_table(self, dataDict):

        self.dataTab.clear()
        
        for key in dataDict.keys():
            df = dataDict[key]
            table = QTableWidget()
            r, c = df.shape
            table.setColumnCount(c)
            table.setRowCount(r)
            for j in range(c):
                table.setHorizontalHeaderItem(j, QTableWidgetItem(str(df.columns[j])))
                for i in range(r):
                    table.setItem(i, j, QTableWidgetItem(str(df.iloc[i,j])))
            
            self.dataTab.addTab(table,key)
        
        self.show()
    

        
        # for key in dataframes.keys():
        #     table = tabulate(dataframes[key], headers='keys', tablefmt = 'psql')
        #     wid = QTextEdit()
        #     wid.setText(table)
        #     data_tabs.addTab(wid,key)
            
                    
# #model for QTableView for dataframe display        
# class PandasModel(QAbstractTableModel):
#     """
#     Class to populate a table view with a pandas dataframe
#     """
#     def __init__(self, data, parent=None):
#         QAbstractTableModel.__init__(self, parent)
#         self._data = data
    
#     def rowCount(self, parent=None):
#         return len(self._data.values)
    
#     def columnCount(self, parent=None):
#         return self._data.columns.size
    
#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 if(index.column() != 0):
#                     return str('%.2f'%self._data.values[index.row()][index.column()])
#                 else:
#                     return str(self._data.values[index.row()][index.column()])
#         return None
    
#     def headerData(self, section, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return self._data.columns[section]
#         elif orientation == Qt.Vertical and role == Qt.DisplayRole:
#             return str(self._data.index[section])
#         return None
    
#     def flags(self, index):
#         flags = super(self.__class__, self).flags(index)
#         flags |= Qt.ItemIsSelectable
#         flags |= Qt.ItemIsEnabled
#         return flags