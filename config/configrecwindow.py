# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:28:19 2020

@author: adwait
"""
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QLabel, QPushButton, \
     QComboBox, QTextEdit, QSpinBox, QLineEdit, \
     QGroupBox, QGridLayout, QWidget, QSizePolicy
import time
     
# %% Recording Window
class ConfigRecWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 550, 250)
        self.setWindowTitle("Configure Record")
        self.layout = QGridLayout()
        self.cap2 = None
        self.home()

    def home(self):
        self.saveBtn = QPushButton("Browse..", self) #Save Video
        self.saveBtn.clicked.connect(self.save_dialog)

        self.openBtn = QPushButton("Open...", self) #Open 2nd Video
        self.openBtn.clicked.connect(self.open_video)

        self.videoTextbox =  QTextEdit(self) #2nd video filename diplayed
        self.videoTextbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.fourRec = QCheckBox('4 panel recording', self) #record 4 views

        self.textbox =  QTextEdit(self) #filename diplayed
##        selt.textbox.wordWrapMode()
        self.textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.codec = QComboBox(self) #length unit
        self.codec.addItem("MJPG")
        self.codec.addItem("DIVX")
        self.codec.addItem("FFV1")
        self.codec.setCurrentIndex(1)
        self.codecLabel = QLabel("Codec:", self)

        self.fps = QSpinBox(self) #playback fps of recorded file
        self.fps.setValue(1)
        self.fps.setSingleStep(1)
        self.fps.setRange(1, 100)
        self.fpsLabel = QLabel("Frames per second:", self)
        
        video1label = QLabel("Video-1 Title:", self)
        self.video1Title = QLineEdit(self)
        self.video1Title.setText("Bottom View")

        video2label = QLabel("Video-2 Title:", self)
        self.video2Title = QLineEdit(self) 
        self.video2Title.setText("Side View")
        
        self.okBtn = QPushButton("OK", self) #Close window

        fileGroupBox = QGroupBox("Save video in...")
        codecGroupBox = QGroupBox("Video settings")
        videoGroupBox = QGroupBox("Select 2nd video")
        titleGroupBox = QGroupBox("Titles")

        fileGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        codecGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        videoGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        titleGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        
        self.layout.addWidget(fileGroupBox, 0, 0)
        self.layout.addWidget(codecGroupBox, 2, 0)
        self.layout.addWidget(videoGroupBox, 0, 1)
        self.layout.addWidget(titleGroupBox, 2, 1)
        self.layout.addWidget(self.okBtn, 3, 0, 1, 2)

        self.setLayout(self.layout)
        
        fileVbox = QGridLayout()
        fileGroupBox.setLayout(fileVbox)
        fileVbox.addWidget(self.saveBtn, 0, 0, 1, 2)
        fileVbox.addWidget(self.textbox, 1, 0, 2, 2)

        videoVbox = QGridLayout()
        videoGroupBox.setLayout(videoVbox)
        videoVbox.addWidget(self.openBtn, 0, 0, 1, 1)
        videoVbox.addWidget(self.fourRec, 0, 1, 1, 1)
        videoVbox.addWidget(self.videoTextbox, 1, 0, 2, 2)

        codecVbox = QGridLayout()
        codecGroupBox.setLayout(codecVbox)
        codecVbox.addWidget(self.codecLabel, 0, 0, 1, 1)
        codecVbox.addWidget(self.codec, 0, 1, 1, 1)
        codecVbox.addWidget(self.fpsLabel, 1, 0, 1, 1)
        codecVbox.addWidget(self.fps, 1, 1, 1, 1)
        
        titleGrid = QGridLayout()
        titleGroupBox.setLayout(titleGrid)
        titleGrid.addWidget(video1label, 0, 0)
        titleGrid.addWidget(self.video1Title, 0, 1)
        titleGrid.addWidget(video2label, 1, 0)
        titleGrid.addWidget(self.video2Title, 1, 1)

    def save_dialog(self):
        name, _ = QFileDialog.getSaveFileName(self, "Save File")
        filename = time.strftime(name + "-%Y%m%d%H%M%S" + ".avi")
        self.textbox.setText(filename)

    def open_video(self):
        videofile, _ = QFileDialog.getOpenFileName(self, "Open Video")
        self.videoTextbox.setText(videofile)

    def showWindow(self, filepath):
##        self.filename = filepath + "-recording" + ".avi"
        self.textbox.setText(filepath)
        self.show()