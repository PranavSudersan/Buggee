# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:27:34 2020

@author: adwait
"""
from PyQt5.QtWidgets import QFileDialog, QPushButton, QTextEdit, \
     QGroupBox, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
      
# %% Configure file paths window
class ConfigPathWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Configure Paths")
        self.home()

    def home(self):
        self.browseBtn0 = QPushButton("Browse..", self) #root folder
        self.browseBtn0.clicked.connect(self.browse_folder)
        self.rootFolder =  QTextEdit(self) #data
        self.rootFolder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.browseBtn1 = QPushButton("Browse..", self) #data
        self.browseBtn1.clicked.connect(lambda: self.browse_file('data'))
        self.dataPath =  QTextEdit(self) #data
        self.dataPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.browseBtn2 = QPushButton("Browse..", self) #plots
        self.browseBtn2.clicked.connect(lambda: self.browse_file('plot'))        
        self.plotPath =  QTextEdit(self) #plots
        self.plotPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.browseBtn3 = QPushButton("Browse..", self) #recording
        self.browseBtn3.clicked.connect(lambda: self.browse_file('recording'))
        self.recordingPath =  QTextEdit(self) #recording
        self.recordingPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.browseBtn4 = QPushButton("Browse..", self) #summary
        self.browseBtn4.clicked.connect(lambda: self.browse_file('summary'))
        self.summaryPath =  QTextEdit(self) #summary
        self.summaryPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.browseBtn5 = QPushButton("Browse..", self) #contours
        self.browseBtn5.clicked.connect(lambda: self.browse_file('contours'))
        self.contourDataPath =  QTextEdit(self) #contours
        self.contourDataPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.okBtn = QPushButton("OK", self) #Close window

        rootGroupBox = self.createGroup("Output folder", self.rootFolder,
                                             self.browseBtn0)
        rootGroupBox.setCheckable(False)

        self.dataGroupBox = self.createGroup("Data", self.dataPath,
                                             self.browseBtn1)
        self.plotGroupBox = self.createGroup("Plot", self.plotPath,
                                             self.browseBtn2)
        self.recordingGroupBox = self.createGroup("Recording", self.recordingPath,
                                             self.browseBtn3)
        self.summaryGroupBox = self.createGroup("Summary", self.summaryPath,
                                             self.browseBtn4)
        self.contourGroupBox = self.createGroup("Contour Data", self.contourDataPath,
                                             self.browseBtn5)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(rootGroupBox)
        self.layout.addWidget(self.dataGroupBox)
        self.layout.addWidget(self.plotGroupBox)
        self.layout.addWidget(self.recordingGroupBox)
        self.layout.addWidget(self.summaryGroupBox)
        self.layout.addWidget(self.contourGroupBox)
        self.layout.addWidget(self.okBtn)

    def createGroup(self, title, path, button): #create groupbox
        groupBox = QGroupBox(title)
        groupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)
        hbox = QHBoxLayout(self)
        groupBox.setLayout(hbox)
        hbox.addWidget(path)
        hbox.addWidget(button)
        return groupBox
    
    def browse_file(self, filetype):
        name, _ = QFileDialog.getSaveFileName(self, "Save " + filetype + " file")
        if name != '':
            if filetype == 'data':
                self.dataPath.setText(name + '.txt')
            elif filetype == 'plot':
                self.plotPath.setText(name + '.svg')
            elif filetype == 'recording':
                self.recordingPath.setText(name + '.avi')
            elif filetype == 'summary':
                self.summaryPath.setText(name + '.txt')
            elif filetype == 'contours':
                self.contourDataPath.setText(name + '.xlsx')
    
    def browse_folder(self):
        folderpath = QFileDialog.getExistingDirectory(caption = f'Select output folder')
        if folderpath != '':
            self.rootFolder.setText(folderpath)

    def showWindow(self):
        self.show()
