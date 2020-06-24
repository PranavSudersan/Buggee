# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:15:06 2020

@author: adwait
"""
from PyQt5.QtWidgets import QPushButton, \
     QGridLayout, QDialog, QListWidget
from current.analyze_force import ForceAnal
     
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
        
##        self.measurmntList = [1,2,3,4,5]
        itemlist = ["Measurement-" + str(x) for x  in self.measurmntList]
        self.listwidget.addItems(itemlist)

        gridLayout.addWidget(self.listwidget, 1, 0, 1, 1)
        gridLayout.addWidget(okButton, 2, 0, 1, 1)
        self.MsrDialog.show()

    def set_measurement(self): #assign corresponding filenames of the measurement
        self.MsrDialog.reject()
        self.msrListMode = True 
        self.msrmnt_num_current = int(self.listwidget.currentItem().text().split("-")[1])
      
        self.videoPath = self.folderPath + "/Imaging/Bottom View/" + \
                         self.bottomviewList[self.msrmnt_num_current-1]       
        self.load_video()

    def load_measurement_data(self): #load force data of measurement
        self.forceData = ForceAnal()
        self.forceData.force_filepath = self.folderPath +  \
                                        "/Force curves/" + \
                                        self.forcedataList[self.msrmnt_num_current-1]
        print(self.forceData.force_filepath)
        self.import_force_data()

        self.configRecWindow.videoTextbox.setText(self.folderPath + \
                                                  "/Imaging/Side View/" +
                                                  self.sideviewList[self.msrmnt_num_current-1])
        print("end")
        self.msrListMode = False
        self.msrmnt_num = self.msrmnt_num_current
        self.definePaths()
        self.setWindowTitle(self.appVersion + " Measurement-" + str(self.msrmnt_num))