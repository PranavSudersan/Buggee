# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:26:33 2020

@author: adwait
"""
from PyQt5.QtWidgets import QLabel, QPushButton, \
      QLineEdit, QSpinBox, QGridLayout, QWidget
     
# %% Configure ROIs window for analysis
class ConfigROIWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.setGeometry(720, 140, 100, 100)
        self.setWindowTitle("Configure ROI")
        self.layout = QGridLayout()
        self.roiDict = {}
        self.home()

    def home(self):
        self.roiNum = QSpinBox(self) #no. of ROI
        self.roiNum.setValue(1)
        self.roiNum.setSingleStep(1)
        self.roiNum.setRange(1, 100)
        self.roiNum.valueChanged.connect(self.num_change)
        self.label1 = QLabel("ROI Number", self)

        self.roiLabel =  QLineEdit(self) #Name of ROI
##        self.roiLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.roiLabel.setText("")
        self.roiLabel.textChanged.connect(self.label_change)
        self.label2 = QLabel("ROI Name", self)

        self.roiDrawBtn = QPushButton("Draw ROI", self) #Draw ROI
        self.roiDrawBtn.setEnabled(False)
##        self.roiDrawBtn.clicked.connect(self.roi_draw)

        self.roiDef = QLabel("ROI Definition:", self) #display definitions

        self.delBtn = QPushButton("Delete", self) #Delete current definition
        self.delBtn.clicked.connect(self.del_roi)

        self.okBtn = QPushButton("OK", self) #Close window
        
        self.layout.addWidget(self.roiNum, 1, 0, 1, 1)
        self.layout.addWidget(self.label1, 0, 0, 1, 1)
        self.layout.addWidget(self.roiLabel, 1, 1, 1, 1)
        self.layout.addWidget(self.label2, 0, 1, 1, 1)
        self.layout.addWidget(self.roiDrawBtn, 2, 0, 1, 1)
        self.layout.addWidget(self.delBtn, 2, 1, 1, 1)
        self.layout.addWidget(self.roiDef, 0, 2, 3, 1)
        self.layout.addWidget(self.okBtn, 3, 0, 1, 2)

        self.setLayout(self.layout)

    def num_change(self):
        key = self.roiNum.value()
        self.roiLabel.blockSignals(True)
        if key in self.roiDict.keys():
            self.roiLabel.setText(self.roiDict[key])
            self.roiDrawBtn.setEnabled(True)
        else:
            self.roiLabel.setText("")
            self.roiDrawBtn.setEnabled(False)
        self.roiLabel.blockSignals(False)

    def label_change(self):
        if self.roiLabel.text() in ["Dict", "dict", "All", "all"]: #banned keywords
            self.roiLabel.blockSignals(True)
            self.roiLabel.setText("")
            self.roiLabel.blockSignals(False)
            self.roiDict[self.roiNum.value()] = self.roiLabel.text()
            self.update_def()
            self.roiDrawBtn.setEnabled(False)
        else:
            self.roiDict[self.roiNum.value()] = self.roiLabel.text()
            self.update_def()
            self.roiDrawBtn.setEnabled(True)

    def del_roi(self): #delete current definition
        del self.roiDict[self.roiNum.value()]
        self.roiNum.setValue(self.roiNum.value()-1)
        self.update_def()

    def update_def(self): #update definition label
        defString = "ROI Definition:"
        for k in self.roiDict.keys():
            defString += "\nROI " + str(k) + ":\t" + self.roiDict[k]

        self.roiDef.setText(defString)
        
    def roi_draw(self):
        pass

    def showWindow(self):
        self.show()