# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 22:24:56 2020

@author: adwait
"""
import matplotlib.pyplot as plt
import gc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, \
     QComboBox, QSpinBox, QGridLayout, QDialog, QLineEdit
from source.summary.summaryanalyze import SummaryAnal
from source.threads.summplotthread import SummPlotThread
     
class SummaryDialog:

    def summary_dialog_init(self): #initialise dialog for summary combine
        self.summary = None
        self.sumDialog = QDialog(self)
        self.sumDialog.setWindowTitle("Configure Summary Plots")
##        self.sumDialog.resize(300, 300)
        
        plotTitleLabel = QLabel("<b>Plot Title</b>", self.sumDialog)
        plotLabel = QLabel("<b>Plot Number</b>", self.sumDialog)
        xLabel = QLabel("<b>X Variable</b>", self.sumDialog)
        yLabel = QLabel("<b>Y Variable</b>", self.sumDialog)
        colorbarLabel = QLabel("<b>Colorbar Variable</b>", self.sumDialog)
        groupVarLabel = QLabel("<b>Group By</b>", self.sumDialog)
        formatLabel = QLabel("<b>Format</b>", self.sumDialog)
        fitLabel = QLabel("<b>Fit</b>", self.sumDialog)
        orderLabel = QLabel("<b>Order</b>", self.sumDialog)

        self.summaryDict = {'x var':[None, None, None, None],
                            'y var':[None, None, None, None],
                            'cbar var':[None, None, None, None],
                            'plot num':[None, None, None, None],
                            'fit': [None, None, None, None],
                            'order': [None, None, None, None],
                            'title':[None], 
                            'format':[None],
                            'plot type':["Scatter"]} #initialize

        plotTitle =  QLineEdit(self.sumDialog)
        plotTitle.textChanged.connect(lambda: self.update_summary_dict('title',
                                                                       plotTitle.text(),
                                                                       0))
        plotTitle.setText('Adhesion vs Area')
        
        plotFormat = QComboBox(self.sumDialog) #plot save format
        plotFormat.addItems(['jpg', 'svg', 'pdf', 'png', 'tif', 'tiff'])
        plotFormat.currentIndexChanged.connect(lambda:
                                               self.update_summary_dict('format',
                                                                        plotFormat.currentText(),
                                                                        0))
        self.update_summary_dict('format', plotFormat.currentText(), 0)
        
        grouplist = ["Date", "Folder_Name", "Species", "Sex", "Leg", "Pad",
                   "Weight", "Temperature", "Humidity", "Medium",
                   "Substrate", "Data_OK", "Include_Data", "Label", "ROI Label",
                     "Measurement_Number", "Contact_Time", "Detachment Speed",
                   "Attachment Speed", "Sliding Speed", "Sliding_Step"]
        grouplist.sort()

        groupVar = QComboBox(self.sumDialog)
        groupVar.addItems(grouplist)
        # ind = groupVar.findText("ROI Label")
        groupVar.setCurrentIndex(groupVar.findText("ROI Label"))
##        groupVar.setEnabled(False)

        combine = QCheckBox('Combine', self.sumDialog)
        okButton = QPushButton("Select summary file..", self.sumDialog)

        combine.stateChanged.connect(lambda: self.combine_toggled(groupVar, combine, okButton))       
        okButton.clicked.connect(lambda: self.combine_summary_data(combine.isChecked(),
                                                                   groupVar.currentText()))

        plotTypeLabel = QLabel("<b>Plot Type</b>", self.sumDialog)
        plotType = QComboBox(self.sumDialog) #x variable
        plotType.addItems(["Scatter", "Box", "Violin"])
        plotType.currentIndexChanged.connect(lambda: self.update_summary_dict('plot type',
                                                                          plotType.currentText(),
                                                                          0))
        
##        okButton.setDefault(True)
        resetButton = QPushButton("Reset", self.sumDialog)
        resetButton.clicked.connect(self.reset_summary)

        gridLayout = QGridLayout(self.sumDialog)
        
        gridLayout.addWidget(plotTitleLabel, 0, 0, 1, 1)
        gridLayout.addWidget(plotTitle, 0, 1, 1, 1)
        gridLayout.addWidget(plotLabel, 1, 0, 1, 1)
        gridLayout.addWidget(xLabel, 1, 1, 1, 1)
        gridLayout.addWidget(yLabel, 1, 2, 1, 1)
        gridLayout.addWidget(colorbarLabel, 1, 3, 1, 1)
        gridLayout.addWidget(fitLabel, 1, 4, 1, 1, alignment = Qt.AlignCenter)
        gridLayout.addWidget(orderLabel, 1, 5, 1, 1)
        self.summary_layout_make(1, 'Pulloff_Area', 'Adhesion_Force',
                                 'Detachment Speed', gridLayout, 2)
        self.summary_layout_make(2, 'Pulloff_Area', 'Adhesion_Force',
                                 'Adhesion_Preload', gridLayout, 3)
        self.summary_layout_make(3, 'Pulloff_Area', 'Adhesion_Force',
                                 'Contact_Time', gridLayout, 4)
        self.summary_layout_make(4, 'Pulloff_Area', 'Adhesion_Force',
                                 'Sliding_Step', gridLayout, 5)
        gridLayout.addWidget(combine, 0, 2, 1, 1)
        gridLayout.addWidget(groupVarLabel, 0, 2, 1, 1, alignment = Qt.AlignRight)
        gridLayout.addWidget(groupVar, 0, 3, 1, 1)
        gridLayout.addWidget(formatLabel, 0, 4, 1, 1, alignment = Qt.AlignRight)
        gridLayout.addWidget(plotFormat, 0, 5, 1, 1)
        gridLayout.addWidget(plotTypeLabel, 6, 0, 1, 1)
        gridLayout.addWidget(plotType, 6, 1, 1, 1)
        gridLayout.addWidget(okButton, 6, 3, 1, 1)
        gridLayout.addWidget(resetButton, 6, 5, 1, 1)
        
##        self.sumDialog.show()

    def summary_layout_make(self, plotnum, x_init, y_init, cb_init,
                            layout, vpos):
        
        varlist = ["Adhesion_Force", "Adhesion_Preload", "Friction_Force",
                   "Friction_Preload", "Max_Area", "Pulloff_Area",
                   "Friction_Area", "ROI_Max_Area", "ROI_Pulloff_Area",
                   "Max_Length", "Pulloff_Length", "ROI_Max_Length",
                   "ROI_Pulloff_Length", "Pulloff_Contact_Number",
                   "Residue_Area", "Pulloff_Median_Eccentricity", "ROI Label",
                   "Measurement_Number", "Contact_Time", "Detachment Speed",
                   "Attachment Speed", "Sliding Speed", "Sliding_Step", "Slope",
                   "Adhesion_Stress", "Friction_Stress", 
                   "Normalized_Pulloff_Force", "Beam_Spring_Constant",
                   "Initial_Deformation","Pulloff_Deformation","Adhesion_Energy",
                   "Max_Bounding_Area", "Max_Bounding_Perimeter",
                   "Max_Bounding_Length", "Max_Bounding_Width", 
                   "Normalized_Adhesion_Energy", "Date_of_Experiment"]
        varlist.sort()
        plotLabel = QLabel(str(plotnum), self.sumDialog)
        self.update_summary_dict('plot num', plotnum, plotnum-1)

        xVar = QComboBox(self.sumDialog) #x variable
        xVar.addItems(varlist)
        xVar.currentIndexChanged.connect(lambda: self.update_summary_dict('x var',
                                                                          xVar.currentText(),
                                                                          plotnum-1))
        xVar.setCurrentIndex(xVar.findText(x_init))
        self.update_summary_dict('x var', xVar.currentText(), plotnum-1)

        yVar = QComboBox(self.sumDialog) #y variable
        yVar.addItems(varlist)
        yVar.currentIndexChanged.connect(lambda: self.update_summary_dict('y var',
                                                                          yVar.currentText(),
                                                                          plotnum-1))
        yVar.setCurrentIndex(yVar.findText(y_init))
        self.update_summary_dict('y var', yVar.currentText(), plotnum-1)
        
        colorbarVar = QComboBox(self.sumDialog) #colorbar variable
        colorbarVar.addItems(varlist)
        colorbarVar.currentIndexChanged.connect(lambda: self.update_summary_dict('cbar var',
                                                                                 colorbarVar.currentText(),
                                                                                 plotnum-1))
        colorbarVar.setCurrentIndex(colorbarVar.findText(cb_init))
        self.update_summary_dict('cbar var', colorbarVar.currentText(), plotnum-1)

        polyfit = QCheckBox(self.sumDialog) #polynomial fit
        polyfit.stateChanged.connect(lambda: self.update_summary_dict('fit',
                                                                      polyfit.isChecked(),
                                                                      plotnum-1))
        self.update_summary_dict('fit', polyfit.isChecked(), plotnum-1)

        polyorder = QSpinBox(self.sumDialog) #polynomial order
        polyorder.valueChanged.connect(lambda: self.update_summary_dict('order',
                                                                      polyorder.value(),
                                                                      plotnum-1))
        polyorder.setRange(1, 10)
        polyorder.setValue(1)
        self.update_summary_dict('order', polyorder.value(), plotnum-1)
        
        layout.addWidget(plotLabel, vpos, 0, 1, 1)
        layout.addWidget(xVar, vpos, 1, 1, 1)
        layout.addWidget(yVar, vpos, 2, 1, 1)
        layout.addWidget(colorbarVar, vpos, 3, 1, 1)
        layout.addWidget(polyfit, vpos, 4, 1, 1, alignment = Qt.AlignCenter)
        layout.addWidget(polyorder, vpos, 5, 1, 1)

    def combine_toggled(self, groupVar, combine, okButton):
##        groupVar.setEnabled(combine.isChecked())
        oktext = "Select summary file.." if combine.isChecked() == False \
                 else "Select experiment list.."
        okButton.setText(oktext)

    def update_summary_dict(self, key, value, plotnum):
        self.summaryDict[key][plotnum] = value
        
    def combine_summary_data(self, combine, legend_parameter): #combine summary plots
##        self.sumDialog.reject()
##        legend_parameter = self.sumlistwidget.currentItem().text()
        self.reset_summary()
        
        if combine == True:
            self.summary = SummaryAnal()
            self.summary.combineSummary(self.summaryDict, legend_parameter)
            if self.summary.list_filepath != "":
                self.comb = True
                self.statusBar.showMessage("Summary Data combined!")
            else:
                self.statusBar.showMessage("No file selected")
                self.comb = False
        else:
            self.comb = False

        self.show_summary_plots(legend_parameter)
        
    def export_summary_plots(self): #export summary plots
        if self.comb == False and self.summary == None:
            self.reset_summary()
            self.summary = SummaryAnal()
            self.summary.importSummary()
##            if len(self.summary.roi_label_unique) == 2:
##                self.summary.roi_label_unique.remove("All")
##        self.summary.eq_count = [1,1,1,1]
            self.summary.plotSummary(self.summaryDict,
                                     self.summary.df_forcedata,
                                     self.summary.df_forcedata)
        #save summary plots in separate thread
        saveSummPlotThread = SummPlotThread(self.summary,
                                            self.summaryDict['format'][0])
        saveSummPlotThread.output.connect(self.process_indicate)
        saveSummPlotThread.finished.connect(self.save_plot_indicate)
        saveSummPlotThread.start()

    def save_plot_indicate(self):
        self.statusBar.showMessage("Summary Plots saved!")

    def show_summary_plots(self, group = "ROI Label"): #show summary plots
        if self.comb == False and self.summary == None:
            self.reset_summary()
            self.summary = SummaryAnal()
            self.summary.importSummary()
##            if len(self.summary.roi_label_unique) == 2:
##                self.summary.roi_label_unique.remove("All")
##        self.summary.eq_count = [1,1,1,1]
            self.summary.plotSummary(self.summaryDict,
                                     self.summary.df_forcedata,
                                     self.summary.df_forcedata,
                                     group)
        self.summary.showSummaryPlot()

    def reset_summary(self): #reset self.comb to False
        self.comb = False
        self.summary = None
##        self.summary_dialog_init()
        plt.clf()
        plt.cla()
        plt.close()
        gc.collect()
        self.statusBar.showMessage("Reset!")