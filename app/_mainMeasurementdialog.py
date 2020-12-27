# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:15:06 2020

@author: adwait
"""
from PyQt5.QtWidgets import QPushButton, \
     QGridLayout, QDialog, QListWidget
import logging
     
class MainMeasurementDialog:

    def choose_measurement(self): #choose measurement
        self.MsrDialog = QDialog(self)
        foldername = self.folderPath.split("/")[-1]
        self.MsrDialog.setWindowTitle("Measurement Picker: " + foldername)
        self.MsrDialog.resize(400, 500)
        gridLayout = QGridLayout(self.MsrDialog)
        self.listwidget = QListWidget(self.MsrDialog)
        okButton = QPushButton("Select", self.MsrDialog)
        okButton.clicked.connect(self.set_measurement)
        okButton.setDefault(True)
        
        #TODO: make this into table showing filenames
        itemlist = ["Measurement-" + str(x) for x  in self.fileListDf.index]
        self.listwidget.addItems(itemlist)

        gridLayout.addWidget(self.listwidget, 1, 0, 1, 1)
        gridLayout.addWidget(okButton, 2, 0, 1, 1)
        self.MsrDialog.show()
    
    #TODO: make column names more generic instead of 'Video 1', 'Data 1', 'Video 2'
    def set_measurement(self): #assign corresponding filenames of the measurement
        self.MsrDialog.reject()
        self.msrListMode = True 
        self.msrmnt_num_current = int(self.listwidget.currentItem().text().split("-")[1])
      
        # self.videoPath = self.folderPath + "/Imaging/Bottom View/" + \
        #                  self.bottomviewList[self.msrmnt_num_current-1]
        self.videoPath = self.fileListDf.loc[self.msrmnt_num_current]['Video 1']
        self.load_video()

    def load_measurement_data(self): #load force data of measurement
        # self.forceData = ForceAnal(self.fitWindow, self.configPlotWindow,
        #                            self.analyzeDataWindow)
        # self.forceData.force_filepath = self.folderPath +  \
        #                                 "/Force curves/" + \
        #                                 self.forcedataList[self.msrmnt_num_current-1]
        self.forceData.force_filepath = self.fileListDf.loc[self.msrmnt_num_current]['Data 1']
        logging.debug(self.forceData.force_filepath)
        self.import_force_data()

        # self.configRecWindow.videoTextbox.setText(self.folderPath + \
        #                                           "/Imaging/Side View/" +
        #                                           self.sideviewList[self.msrmnt_num_current-1])
        if 'Video 2' in self.fileListDf.columns:
            video2_path = self.fileListDf.loc[self.msrmnt_num_current]['Video 2']
        else:
            video2_path = ''
        self.configRecWindow.videoTextbox.setText(video2_path)
        logging.debug("end")
        self.msrListMode = False
        self.msrmnt_num = self.msrmnt_num_current
        self.definePaths()
        self.setWindowTitle(self.appVersion + " Measurement-" + str(self.msrmnt_num))