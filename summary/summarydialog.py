# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 22:24:56 2020

@author: adwait
"""
import matplotlib.pyplot as plt
import gc
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QSizePolicy
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QGroupBox,\
     QComboBox, QSpinBox, QGridLayout, QDialog, QLineEdit, QDoubleSpinBox, QSizePolicy
from source.summary.summaryanalyze import SummaryAnal
from source.threads.summplotthread import SummPlotThread
     
class SummaryWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.Window)
        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle("Configure Summary Plots")
        self.layout = QGridLayout()
        
        # self.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
        #                                [0,100],[0,100],[0,1]]}
   
        self.paramDict = {}
        self.varlist = []

        
        self.home()
        
    def home(self): #initialise dialog for summary combine
        self.summary = None
        # self.sumDialog = QDialog(self)
        # self.sumDialog.setWindowTitle("Configure Summary Plots")
##        self.sumDialog.resize(300, 300)
        
        #import data
        importButton = QPushButton("Select summary file..", self)
        
        combine = QCheckBox('Combine', self)
        
        combine.stateChanged.connect(lambda: self.combine_toggled(combine, importButton))
        importButton.clicked.connect(lambda: self.combine_summary_data(combine.isChecked()))
        
        #plot data
        plotTypeLabel = QLabel("Plot Type", self)
        plotType = QComboBox(self)
        rel_types = ["line", "scatter"]
        cat_types = ["strip", "swarm", "box", "violin",
                    "boxen", "point", "bar", "count"]
        plotType.addItems(rel_types + cat_types)
        
        xLabel = QLabel("X Variable", self)
        xVar = QComboBox(self)
        
        yLabel = QLabel("Y Variable", self)
        yVar = QComboBox(self)
        
        groupVarLabel = QLabel("<b>Group By:</b>", self)
        
        colorLabel = QLabel("Color", self)
        colorVar = QComboBox(self)
        
        columnLabel = QLabel("Column", self)
        columnVar = QComboBox(self)
        
        rowLabel = QLabel("Row", self)
        rowVar = QComboBox(self)

        styleLabel = QLabel("Style", self)
        styleVar = QComboBox(self)
        
        sizeLabel = QLabel("Size", self)
        sizeVar = QComboBox(self)
        
        plotTitleLabel = QLabel("Title", self)
        plotTitle =  QLineEdit(self)
        plotTitle.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # plotTitle.textChanged.connect(lambda: self.update_summary_dict('title',
        #                                                                plotTitle.text(),
        #                                                                0))
        plotTitle.setText('Test')
        
        self.filter_dialog_init()   #initialize filter dialog
        filterButton = QPushButton("Filter..", self)
        filterButton.clicked.connect(self.filterDialog.show)
        
        #plot format

        formatLabel = QLabel("Save as", self)
        plotFormat = QComboBox(self) #plot save format
        plotFormat.addItems(['jpg', 'svg', 'pdf', 'png', 'tif', 'tiff'])
        
        showMarkers = QCheckBox('Show Markers', self)
        
        opacityLabel = QLabel("Opacity", self)
        opacity = QDoubleSpinBox(self)
        
        contextLabel = QLabel("Context", self)
        context = QComboBox(self)
        context.addItems(['talk'])
        
        plotStyleLabel = QLabel("Style", self)
        plotStyle = QComboBox(self)
        plotStyle.addItems(['ticks'])
        
        colorPaletteLabel = QLabel("Context", self)
        colorPalette = QComboBox(self)
        colorPalette.addItems(['None'])
        
        rotateXLabel = QLabel("Rotate X Labels", self)
        rotateX = QSpinBox(self)
        rotateX.setValue(0)
        
        zeroLine = QCheckBox('Zero Line', self)
        
        legendSettings = QLabel("<b>Legend Settings:</b>", self)
        legendPos = QCheckBox('Outside plot', self)
        
        legendLocLabel = QLabel("Location", self)
        legendLoc = QComboBox(self)
        legendLoc.addItems(['best','upper right','upper left','lower left',
                            'lower right','right','center left','center right',
                            'lower center','upper center','center'])
        
        legendColLabel = QLabel("Columns", self)
        legendCol = QSpinBox(self)
        legendCol.setValue(1)
        
        
        
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
        showPlot = QPushButton("Show Plot", self)
        
        savePlot = QPushButton("Save Plot", self)
        
        resetButton = QPushButton("Reset", self)
        resetButton.clicked.connect(self.reset_summary)
        
        closeButton = QPushButton("Close", self)
        closeButton.clicked.connect(self.close_summary)
        

        # gridLayout = QGridLayout(self)
        
        importGroupBox = QGroupBox("Import Data")
        importGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        importLayout = QGridLayout()
        importGroupBox.setLayout(importLayout)
        importLayout.addWidget(combine, 0, 0, 1, 1)
        importLayout.addWidget(importButton, 0, 1, 1, 1)
        
        plotGroupBox = QGroupBox("Plot Data")
        plotGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        plotLayout = QGridLayout()
        plotGroupBox.setLayout(plotLayout)
        plotLayout.addWidget(plotTypeLabel, 0, 0, 1, 1)
        plotLayout.addWidget(plotType, 0, 1, 1, 1)
        plotLayout.addWidget(xLabel, 1, 0, 1, 1)
        plotLayout.addWidget(xVar, 1, 1, 1, 1)
        plotLayout.addWidget(yLabel, 2, 0, 1, 1)
        plotLayout.addWidget(yVar, 2, 1, 1, 1)
        plotLayout.addWidget(plotTitleLabel, 3, 0, 1, 1)
        plotLayout.addWidget(plotTitle, 3, 1, 1, 1)
        plotLayout.addWidget(filterButton, 4, 0, 1, 2)
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
        plotLayout.addWidget(colorVar, 1, 3, 1, 1)
        plotLayout.addWidget(columnLabel, 2, 2, 1, 1)
        plotLayout.addWidget(columnVar, 2, 3, 1, 1)
        plotLayout.addWidget(rowLabel, 3, 2, 1, 1)
        plotLayout.addWidget(rowVar, 3, 3, 1, 1)
        plotLayout.addWidget(styleLabel, 4, 2, 1, 1)
        plotLayout.addWidget(styleVar, 4, 3, 1, 1)
        plotLayout.addWidget(sizeLabel, 5, 2, 1, 1)
        plotLayout.addWidget(sizeVar, 5, 3, 1, 1)        
        
        
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
        plotFormatLayout.addWidget(opacityLabel, 3, 0, 1, 1)
        plotFormatLayout.addWidget(opacity, 3, 1, 1, 1)
        plotFormatLayout.addWidget(rotateXLabel, 4, 0, 1, 1)
        plotFormatLayout.addWidget(rotateX, 4, 1, 1, 1)
        plotFormatLayout.addWidget(formatLabel, 5, 0, 1, 1)
        plotFormatLayout.addWidget(plotFormat, 5, 1, 1, 1)
        plotFormatLayout.addWidget(showMarkers, 0, 2, 1, 1)        
        plotFormatLayout.addWidget(zeroLine, 1, 2, 1, 1)
        plotFormatLayout.addWidget(legendSettings, 2, 2, 1, 2, alignment = Qt.AlignCenter)
        plotFormatLayout.addWidget(legendPos, 3, 2, 1, 1)
        plotFormatLayout.addWidget(legendLocLabel, 4, 2, 1, 1)
        plotFormatLayout.addWidget(legendLoc, 4, 3, 1, 1)
        plotFormatLayout.addWidget(legendColLabel, 5, 2, 1, 1)
        plotFormatLayout.addWidget(legendCol, 5, 3, 1, 1)
        
        
        
        
        buttonGroupBox = QGroupBox()
        buttonLayout= QGridLayout()
        buttonGroupBox.setLayout(buttonLayout)
        buttonLayout.addWidget(showPlot, 0, 0, 1, 1)
        buttonLayout.addWidget(savePlot, 0, 1, 1, 1)
        buttonLayout.addWidget(resetButton, 0, 2, 1, 1)
        buttonLayout.addWidget(closeButton, 0, 3, 1, 1)
        
        
        self.layout.addWidget(importGroupBox, 0, 0)
        self.layout.addWidget(plotGroupBox, 1, 0)
        self.layout.addWidget(plotFormatGroupBox, 2, 0)
        self.layout.addWidget(buttonGroupBox, 3, 0)
        
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

    def combine_toggled(self, combine, importButton):
##        groupVar.setEnabled(combine.isChecked())
        oktext = "Select summary file.." if combine.isChecked() == False \
                 else "Select experiment list.."
        importButton.setText(oktext)

    def update_summary_dict(self, key, value, plotnum):
        self.summaryDict[key][plotnum] = value
        
    def combine_summary_data(self, combine): #combine summary plots
##        self.sumDialog.reject()
##        legend_parameter = self.sumlistwidget.currentItem().text()
        self.reset_summary()
        self.summary = SummaryAnal()
        if combine == True:            
            self.summary.combineSummary()
            if self.summary.list_filepath != "":
                self.comb = True
                self.statusBar.showMessage("Summary Data combined!")
                self.summary.filter_df(self.filter_dict)
                # self.summary.plotSummary(self.summaryDict,
                #                          self.summary.df_final,
                #                          self.summary.df_final,
                #                          legend_parameter)
                # self.summary.showSummaryPlot()
            else:
                self.statusBar.showMessage("No file selected")
                self.comb = False
                self.summary = None
        else:
            self.comb = False 
            self.summary.importSummary()
            if self.summary.summary_filepath != "":
                self.summary.filter_df(self.filter_dict)
                # self.summary.plotSummary(self.summaryDict,
                #                          self.summary.df_final,
                #                          self.summary.df_final,
                #                          legend_parameter)
                # self.summary.showSummaryPlot()
            else:
                self.summary = None
        
        
    def export_summary_plots(self): #export summary plots
        if self.comb == False and self.summary == None:
            self.reset_summary()
            self.summary = SummaryAnal()
            self.summary.importSummary()
            if self.summary.summary_filepath != "":
                # self.summary.filter_df(self.filter_dict)
                # self.summary.plotSummary(self.summaryDict,
                #                           self.summary.df_final,
                #                           self.summary.df_final)
                self.summary.plotSummary()
            else:
                self.summary = None
        #save summary plots in separate thread
        if self.summary != None:
            # saveSummPlotThread = SummPlotThread(self.summary,
            #                                     self.summaryDict['format'][0])
            # saveSummPlotThread.output.connect(self.process_indicate)
            # saveSummPlotThread.finished.connect(self.save_plot_indicate)
            # saveSummPlotThread.start()
            self.summary.saveSummaryPlot(self.summaryDict['format'][0])

    def save_plot_indicate(self):
        self.statusBar.showMessage("Summary Plots saved!")

    def show_summary_plots(self): #show summary plots
        if self.comb == False and self.summary == None:
            self.reset_summary()
            self.summary = SummaryAnal()
            self.summary.importSummary()
            if self.summary.summary_filepath != "":
                # self.summary.filter_df(self.filter_dict)
                # self.summary.plotSummary(self.summaryDict,
                #                          self.summary.df_final,
                #                          self.summary.df_final)
                self.summary.plotSummary()
            else:
                self.summary = None
        if self.summary != None:
            self.summary.showSummaryPlot()

    def reset_summary(self): #reset self.comb to False
        self.comb = False
        self.summary = None
        # self.filter_dialog_init()
##        self.summary_dialog_init()
        plt.clf()
        plt.cla()
        plt.close()
        gc.collect()
        # self.statusBar.showMessage("Reset!")

    def close_summary(self):
        self.sumDialog.done(0)
        
    def filter_dialog_init(self):
        self.filterDialog = QDialog()
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
        groupVar = QComboBox()
        groupVar.addItems(self.varlist)
        groupVar.currentIndexChanged.connect(lambda:
                                             self.update_filter_dict(rownum, 0,
                                                    groupVar.currentText()))
        
        conditionVar = QComboBox()
        conditionVar.addItems(["equal to", "not equal to", "less than", 
                                "greater than", "less than or equal to",
                                "greater than or equal to"])
        conditionVar.currentIndexChanged.connect(lambda:
                                                 self.update_filter_dict(rownum, 1,
                                                    conditionVar.currentText()))
            
        filterValue =  QLineEdit()
        filterValue.textChanged.connect(lambda:
                                       self.update_filter_dict(rownum, 2,
                                            filterValue.text()))
            
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
        # self.summaryDict['filter'] = self.filter_dict
        self.filterDialog.done(0)