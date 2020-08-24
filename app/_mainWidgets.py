# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 21:04:04 2020

@author: adwait
"""

"""IMPORTANT!! Any new widget added should be included in update_settings_dict 
of mainwindow.py if you want its parameters to be saved in settings file
"""

from PyQt5.QtGui import QPixmap, QIcon, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QCheckBox, QLabel, QPushButton, \
     QComboBox, QGraphicsScene, \
     QGraphicsPixmapItem, QSpinBox, QDoubleSpinBox, \
     QGroupBox, QGridLayout, QWidget, \
     QTabWidget
from source.app.myqgraphicsview import MyQGraphicsView

class MainWidgets:
    
    def home(self):

        self.blankPixmap = QPixmap('images/blank.png')
        
        
        self.rawScene = QGraphicsScene(self) #raw video feed
        self.rawPixmapItem = QGraphicsPixmapItem(self.blankPixmap)
        self.rawScene.addItem(self.rawPixmapItem)
        # self.rawView = MyQGraphicsView(self.rawScene) #REMOVE!!!!
        # self.rawView.setMinimumSize(600,300)
##        self.rawView.setGeometry(QRect(50, 120, 480, 360))
        #original view
        self.rawView1 = MyQGraphicsView(self.rawScene)
        self.rawView1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView1.setBackgroundBrush(QBrush(Qt.black,
                                                       Qt.SolidPattern))
        
        #contour view
        self.rawView2 = MyQGraphicsView(self.rawScene)
        self.rawView2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView2.setBackgroundBrush(QBrush(Qt.black,
                                                       Qt.SolidPattern))
        
        #effect view
        self.rawView3 = MyQGraphicsView(self.rawScene)
        self.rawView3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView3.setBackgroundBrush(QBrush(Qt.black,
                                                       Qt.SolidPattern))

        self.effectScene = QGraphicsScene(self) #analysis video feed
##        self.effectPixmap = QPixmap('images/blank.png')
        self.effectPixmapItem = QGraphicsPixmapItem(self.blankPixmap)
        self.effectScene.addItem(self.effectPixmapItem)
        # self.effectView = MyQGraphicsView(self.effectScene) #REMOVE
        # self.effectView.setMinimumSize(600,300)
##        self.effectView.setGeometry(QRect(560, 120, 480, 360))
        
        self.effectView1 = MyQGraphicsView(self.effectScene)
        self.effectView1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView1.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))

        self.effectView2 = MyQGraphicsView(self.effectScene)
        self.effectView2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView2.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))

        self.effectView3 = MyQGraphicsView(self.effectScene)
        self.effectView3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView3.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))

        self.effectView4 = MyQGraphicsView(self.effectScene)
        self.effectView4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView4.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))

        self.effectView5 = MyQGraphicsView(self.effectScene)
        self.effectView5.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView5.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))

        self.effectView6 = MyQGraphicsView(self.effectScene)
        self.effectView6.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView6.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView6.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))
        
        self.playBtn = QPushButton("", self) #Play/Pause action
        self.playBtn.clicked.connect(self.playback)
        self.playBtn.setIcon(QIcon('images/play.png'))
##        self.playBtn.resize(self.playBtn.minimumSizeHint())
##        self.playBtn.move(100,500)

        self.stopBtn = QPushButton("", self) #Stop video
        self.stopBtn.clicked.connect(self.stop_video)
        self.stopBtn.setIcon(QIcon('images/stop.png'))
##        self.stopBtn.resize(self.stopBtn.minimumSizeHint())
##        self.stopBtn.move(150,500)

        self.prevBtn = QPushButton("", self) #Previous frame
        self.prevBtn.clicked.connect(self.previous_frame)
        self.prevBtn.setIcon(QIcon('images/previous.png'))
##        self.prevBtn.resize(self.prevBtn.minimumSizeHint())
##        self.prevBtn.move(200,500)

        self.nextBtn = QPushButton("", self) #Next frame
        self.nextBtn.clicked.connect(self.next_frame)
        self.nextBtn.setIcon(QIcon('images/next.png'))
##        self.nextBtn.resize(self.nextBtn.minimumSizeHint())
##        self.nextBtn.move(250,500)

        self.repeatBtn = QPushButton("", self) #Repeat playback
        self.repeatBtn.clicked.connect(self.next_frame)
        self.repeatBtn.setIcon(QIcon('images/repeat.png'))
        self.repeatBtn.setCheckable(True)
        
        self.recordBtn = QPushButton("", self) #Record video
        self.recordBtn.clicked.connect(self.record_frame)
        self.recordBtn.setIcon(QIcon('images/record.png'))
##        self.recordBtn.resize(self.recordBtn.minimumSizeHint())
##        self.recordBtn.move(300,500)
        self.recordBtn.setEnabled(False)
        
        self.seekSlider = QSlider(Qt.Horizontal, self) #seek bar
##        self.seekSlider.setGeometry(30, 60, 200, 30)
        self.seekSlider.setMinimum(0)
        self.seekSlider.setMaximum(100)
        self.seekSlider.setValue(0)
        self.seekSlider.setTickInterval(10)
        self.seekSlider.setSingleStep(2)
        self.seekSlider.setTickPosition(QSlider.TicksBelow)
        self.seekSlider.setStyleSheet("QSlider::groove:horizontal {height:2.5ex;}")
        self.seekSlider.valueChanged.connect(self.seek_video)
        
        self.roiBtn = QPushButton("Draw ROI", self) #Draw ROI Manually
        self.roiBtn.clicked.connect(self.configROIWindow.showWindow)
        self.roiBtn.setStyleSheet("QPushButton { font-weight: bold; font-size: 14px;} ")
        self.configROIWindow.roiDrawBtn.clicked.connect(self.roiMerge)
        self.configROIWindow.okBtn.clicked.connect(self.closeROIWindow)
##        self.roiBtn.resize(self.roiBtn.minimumSizeHint())
##        self.roiBtn.move(375,500)

        self.measureBtn = QPushButton("Measure", self) #Measure pixel length
        self.measureBtn.clicked.connect(self.measureScale)
        self.measureBtn.setStyleSheet("QPushButton { font-weight: bold; font-size: 18px;} ")
##        self.measureBtn.resize(self.measureBtn.minimumSizeHint())
##        self.measureBtn.move(375,575)

        self.pixelValue = QDoubleSpinBox(self)
        self.pixelValue.setRange(0, 3000)
        self.pixelValue.setValue(168.67)
        self.pixelValue.setSingleStep(10)
        self.pixelValue.valueChanged.connect(self.update_calib)
##        self.pixelValue.move(375, 550)
##        self.pixelValue.resize(50, 20)

        self.pixelLabel = QLabel("px equals ", self) #pixel
##        self.pixelLabel.move(430, 545)
        
        self.lengthValue = QDoubleSpinBox(self)
        self.lengthValue.setRange(0, 1000)
        self.lengthValue.setValue(100)
        self.lengthValue.setSingleStep(1)
        self.lengthValue.valueChanged.connect(self.update_calib)

        self.lengthUnit = QComboBox(self) #length unit
        self.lengthUnit.addItem("px")
        self.lengthUnit.addItem("cm")
        self.lengthUnit.addItem("mm")
        self.lengthUnit.addItem("μm")
        self.lengthUnit.addItem("nm")
        self.lengthUnit.setCurrentIndex(3)
        self.lengthUnit.currentIndexChanged.connect(self.update_calib)
        
#         self.videoEffect = QComboBox(self) #video effect dropdown
#         self.videoEffect.addItem("Binary")
#         self.videoEffect.addItem("Masked")
#         self.videoEffect.addItem("Contours")
#         self.videoEffect.addItem("Transformed")
#         self.videoEffect.addItem("Background")
#         self.videoEffect.addItem("Auto ROI")
#         self.videoEffect.addItem("Force/Area Plot")
#         self.videoEffect.setStyleSheet("QComboBox { font-weight: bold; font-size: 14px;} ")
# ##        self.videoEffect.move(650, 85)
# ##        self.videoEffect.resize(self.videoEffect.minimumSizeHint())
#         # self.videoEffect.currentIndexChanged.connect(self.effect_change)
#         self.videoEffect.model().item(5).setEnabled(False)
#         self.videoEffect.model().item(6).setEnabled(False)

        self.analyzeVideo = QCheckBox('Analyze Video', self) #Perform Analysis
##        self.analyzeVideo.move(500, 30)
        self.analyzeVideo.stateChanged.connect(self.anal_change)
        self.analyzeVideo.setStyleSheet("QCheckBox { font-weight: bold; font-size: 14px;} ")

        self.correctZeroForce = QCheckBox('Zero-force correct', self) #Perform Analysis
        self.correctZeroForce.stateChanged.connect(self.plotSequence)
        self.correctZeroForce.setEnabled(False)

#         self.showContours = QCheckBox('Show Contours', self) #show contours
# ##        self.showContours.move(300, 60)
#         self.showContours.stateChanged.connect(self.anal_change)
#         self.showContours.setStyleSheet("QCheckBox { font-weight: bold; font-size: 16px;} ")

#         self.showEffect = QCheckBox('Show Effect', self) #show contours
# ##        self.showContours.move(300, 60)
#         self.showEffect.stateChanged.connect(self.anal_change)
#         self.showEffect.setStyleSheet("QCheckBox { font-weight: bold; font-size: 16px;} ")
        
        self.bgButton = QPushButton("Set Background", self) #Set background
        self.bgButton.clicked.connect(self.bgFrame)
        self.bgButton.setStyleSheet("QPushButton { font-weight: bold; font-size: 14px;} ")
        # self.bgButton.resize(self.bgButton.minimumSizeHint())
        # self.bgButton.clicked.connect(self.bg_change)
        
        self.bgShowButton = QPushButton("Show", self) #Set background
        self.bgShowButton.setStyleSheet("QPushButton { font-weight: bold; font-size: 14px;} ")
        self.bgShowButton.setCheckable(True)
        self.bgShowButton.clicked.connect(self.bgShow)
        # self.bgShowButton.resize(self.bgShowButton.minimumSizeHint())
##        self.bgButton.move(420,80)

##        self.bgSubtract = QCheckBox('Subtract Background', self) #background subtract
##        self.bgSubtract.move(300, 80)
##        self.bgSubtract.stateChanged.connect(self.bg_change)
        
        self.backgroundCorrectionLabel = QLabel("Type:", self) #background blur
        self.backgroundCorrection =  QComboBox(self) #Background correction type
        self.backgroundCorrection.addItem("Average Correction")
        self.backgroundCorrection.addItem("Direct Subtract")
        self.backgroundCorrection.addItem("Gaussian Correction")
        self.backgroundCorrection.addItem("Rolling Ball")
        self.backgroundCorrection.addItem("Rolling Paraboloid")
        self.backgroundCorrection.currentIndexChanged.connect(self.bg_change)        
        
        self.bgBlurLabel = QLabel("Blur Size:", self) #background blur
        self.bgSlider = QSlider(Qt.Horizontal, self) #background blur
        self.bgSlider.setMinimum(3)
        self.bgSlider.setMaximum(1001)
        self.bgSlider.setValue(30)
        self.bgSlider.setTickInterval(200)
        self.bgSlider.setTickPosition(QSlider.TicksBelow)
        self.bgSlider.valueChanged.connect(self.bg_change)
        self.bgSlider.setSingleStep(5)
        self.bgSpinBox = QSpinBox(self)
        self.bgSpinBox.setRange(3, 1001)
        self.bgSpinBox.setValue(self.bgSlider.value())
        self.bgSpinBox.setSingleStep(1)
        self.bgSpinBox.valueChanged.connect(self.bg_change)

        self.bgAlphaLabel = QLabel("Blend:", self) #background alpha
        self.bgAlphaSpinBox = QDoubleSpinBox(self) 
        self.bgAlphaSpinBox.setRange(0, 1)
        self.bgAlphaSpinBox.setValue(0.45)
        self.bgAlphaSpinBox.setSingleStep(0.01)
        self.bgAlphaSpinBox.valueChanged.connect(self.bg_change)
        
        threshTypeLabel = QLabel("Threshold Type:\t", self) #threshold cutoff
        self.threshType = QComboBox(self) #threshold type
        self.threshType.addItem("Global")
        self.threshType.addItem("Adaptive")
        self.threshType.addItem("Otsu")
        self.threshType.addItem("Canny")
##        self.threshType.move(900, 35)
##        self.threshType.resize(self.threshType.minimumSizeHint())
        self.threshType.currentIndexChanged.connect(self.threshold_change)
        
        
        self.binaryInvert =  QCheckBox('Invert', self) #invert binary
        self.binaryInvert.stateChanged.connect(self.threshold_change)
        
        self.thresh1Label = QLabel("Threshold:\t", self) #threshold cutoff
        self.threshSlider1 = QSlider(Qt.Horizontal, self) 
##        self.threshSlider1.setGeometry(800, 60, 200, 30)
        self.threshSlider1.setMinimum(3)
        self.threshSlider1.setMaximum(701)
        self.threshSlider1.setValue(128)
        self.threshSlider1.setTickInterval(50)
        self.threshSlider1.setTickPosition(QSlider.TicksBelow)
        self.threshSlider1.valueChanged.connect(self.threshold_change)
        self.threshSlider1.setSingleStep(4)
        self.threshSpinBox1 = QSpinBox(self)
        self.threshSpinBox1.setRange(3, 701)
        self.threshSpinBox1.setValue(self.threshSlider1.value())
        self.threshSpinBox1.setSingleStep(2)
        self.threshSpinBox1.valueChanged.connect(self.threshold_change)
##        self.threshSpinBox1.move(1010, 60)
##        self.threshSpinBox1.resize(45, 20)

        self.thresh2Label = QLabel("Constant:\t", self) #threshold constant
        self.threshSlider2 = QSlider(Qt.Horizontal, self) 
##        self.threshSlider2.setGeometry(800, 90, 200, 30)
        self.threshSlider2.setMinimum(-10)
        self.threshSlider2.setMaximum(10)
        self.threshSlider2.setValue(2)
        self.threshSlider2.setTickInterval(1)
        self.threshSlider2.setTickPosition(QSlider.TicksBelow)
        self.threshSlider2.valueChanged.connect(self.threshold_change)
        self.threshSlider2.setSingleStep(2)
        self.threshSpinBox2 = QSpinBox(self)
        self.threshSpinBox2.setRange(-10, 10)
        self.threshSpinBox2.setValue(self.threshSlider2.value())
        self.threshSpinBox2.setSingleStep(1)
        self.threshSpinBox2.valueChanged.connect(self.threshold_change)
##        self.threshSpinBox2.move(1010, 90)
##        self.threshSpinBox2.resize(45, 20)

        self.applyMorph = QCheckBox('Morph', self) #Morph 
        self.applyMorph.setChecked(False)
        self.applyMorph.stateChanged.connect(self.video_analysis)
        
        morphTypeLabel = QLabel("Morph Type: ", self) 
        self.morphType = QComboBox(self) #morph type
        self.morphType.addItem("Erosion")
        self.morphType.addItem("Dilation")
        self.morphType.addItem("Opening")
        self.morphType.addItem("Closing")
        self.morphType.addItem("Gradient")
        self.morphType.addItem("Top Hat")
        self.morphType.addItem("Black Hat")
        self.morphType.currentIndexChanged.connect(self.video_analysis)
        
        morphSizeLabel = QLabel("Size: ", self)
        self.morphSize = QSpinBox(self) #morph kernel size (square)
        self.morphSize.setRange(1, 1000)
        self.morphSize.setValue(5)
        self.morphSize.setSingleStep(1)
        self.morphSize.valueChanged.connect(self.video_analysis)
        # self.morphXSpinBox.setEnabled(False)

        morphIterationsLabel = QLabel("Iterations: ", self)
        self.morphIterations = QSpinBox(self) #morph iterations
        self.morphIterations.setRange(1, 1000)
        self.morphIterations.setValue(1)
        self.morphIterations.setSingleStep(1)
        self.morphIterations.valueChanged.connect(self.video_analysis)
        # self.morphYSpinBox.setEnabled(False)

        # Features Settings  
        
        topTemplateLabel = QLabel("Top Template:\t", self) 
        
        topTemplateBtn = QPushButton("Select", self) #top template image
        topTemplateBtn.clicked.connect(lambda: self.selectTemplateImage("Top"))
        
        lineTypeTopLabel = QLabel("Line Type:", self) 
        self.lineTypeTop = QComboBox(self) #line type
        self.lineTypeTop.addItem("Longest")
        self.lineTypeTop.addItem("Shortest")
        self.lineTypeTop.addItem("Top most")
        self.lineTypeTop.addItem("Bottom most")
        self.lineTypeTop.addItem("Best fit")
        self.lineTypeTop.currentIndexChanged.connect(self.video_analysis)
        
        markerWindowTopLabel = QLabel("Marker Window:", self) 
        self.markerWindowTop = QSpinBox(self)
        self.markerWindowTop.setRange(1, 99)
        self.markerWindowTop.setValue(5)
        self.markerWindowTop.setSingleStep(1)
        self.markerWindowTop.valueChanged.connect(self.video_analysis)
        
        #display edges top
        self.displayFeatureEdgesTop = QPushButton("Display Edges", self)
        self.displayFeatureEdgesTop.setCheckable(True)
        self.displayFeatureEdgesTop.clicked.connect(self.video_analysis)        

        #display lines top
        self.displayFeatureLinesTop = QPushButton("Display Lines", self)
        self.displayFeatureLinesTop.setCheckable(True)
        self.displayFeatureLinesTop.clicked.connect(self.video_analysis)
        
        bottomTemplateLabel = QLabel("Bottom Template:\t", self)
        
        bottomTemplateBtn = QPushButton("Select", self) #bottom template image
        bottomTemplateBtn.clicked.connect(lambda: self.selectTemplateImage("Bottom"))
        
        lineTypeBottomLabel = QLabel("Line Type:", self) 
        self.lineTypeBottom = QComboBox(self) #line type
        self.lineTypeBottom.addItem("Longest")
        self.lineTypeBottom.addItem("Shortest")
        self.lineTypeBottom.addItem("Top most")
        self.lineTypeBottom.addItem("Bottom most")
        self.lineTypeBottom.addItem("Best fit")
        self.lineTypeBottom.currentIndexChanged.connect(self.video_analysis)
        
        markerWindowBottomLabel = QLabel("Marker Window:", self) 
        self.markerWindowBottom = QSpinBox(self)
        self.markerWindowBottom.setRange(1, 99)
        self.markerWindowBottom.setValue(5)
        self.markerWindowBottom.setSingleStep(1)
        self.markerWindowBottom.valueChanged.connect(self.video_analysis)

        #display edges bottom
        self.displayFeatureEdgesBottom = QPushButton("Display Edges", self)
        self.displayFeatureEdgesBottom.setCheckable(True)
        self.displayFeatureEdgesBottom.clicked.connect(self.video_analysis) 

        #display lines bottom
        self.displayFeatureLinesBottom = QPushButton("Display Lines", self)
        self.displayFeatureLinesBottom.setCheckable(True)
        self.displayFeatureLinesBottom.clicked.connect(self.video_analysis)

        lineThreshLabel = QLabel("Line Threshold:", self) 
        self.lineThreshSlider = QSlider(Qt.Horizontal, self)
        self.lineThreshSlider.setMinimum(1)
        self.lineThreshSlider.setMaximum(999)
        self.lineThreshSlider.setValue(30)
        # self.edgeMinSlider.setTickInterval(5)
        self.lineThreshSlider.setTickPosition(QSlider.TicksBelow)
        self.lineThreshSlider.valueChanged.connect(self.feature_param_change)
        # self.edgeMinSlider.setSingleStep(2)
        self.lineThresh = QSpinBox(self)
        self.lineThresh.setRange(1, 999)
        self.lineThresh.setValue(self.lineThreshSlider.value())
        self.lineThresh.setSingleStep(1)
        self.lineThresh.valueChanged.connect(self.feature_param_change)

        lineLengthLabel = QLabel("Line Length:", self) 
        self.lineLengthSlider = QSlider(Qt.Horizontal, self)
        self.lineLengthSlider.setMinimum(1)
        self.lineLengthSlider.setMaximum(999)
        self.lineLengthSlider.setValue(50)
        # self.edgeMinSlider.setTickInterval(5)
        self.lineLengthSlider.setTickPosition(QSlider.TicksBelow)
        self.lineLengthSlider.valueChanged.connect(self.feature_param_change)
        # self.edgeMinSlider.setSingleStep(2)
        self.lineLength = QSpinBox(self)
        self.lineLength.setRange(1, 999)
        self.lineLength.setValue(self.lineLengthSlider.value())
        self.lineLength.setSingleStep(1)
        self.lineLength.valueChanged.connect(self.feature_param_change)

        lineGapLabel = QLabel("Line Gap:", self) 
        self.lineGapSlider = QSlider(Qt.Horizontal, self)
        self.lineGapSlider.setMinimum(1)
        self.lineGapSlider.setMaximum(999)
        self.lineGapSlider.setValue(200)
        # self.edgeMinSlider.setTickInterval(5)
        self.lineGapSlider.setTickPosition(QSlider.TicksBelow)
        self.lineGapSlider.valueChanged.connect(self.feature_param_change)
        # self.edgeMinSlider.setSingleStep(2)
        self.lineGap = QSpinBox(self)
        self.lineGap.setRange(1, 999)
        self.lineGap.setValue(self.lineGapSlider.value())
        self.lineGap.setSingleStep(1)
        self.lineGap.valueChanged.connect(self.feature_param_change)
        
        #Image Segment settings
        
        self.useDistTransfrom = QCheckBox('Distance Transform', self) #apply distance transform
        self.useDistTransfrom.stateChanged.connect(self.segment_param_change)
        
        self.showSegment = QPushButton("Display Segment", self) #display segment
        self.showSegment.setCheckable(True)
        self.showSegment.clicked.connect(self.segment_show)
        # self.showSegment.setEnabled(False)
        
        #display foreground
        self.segmentFGButton = QPushButton("Disply Foreground", self)
        self.segmentFGButton.setCheckable(True)
        self.segmentFGButton.clicked.connect(self.segment_show_fg)
        # self.segmentFGButton.setEnabled(False)

        #display background
        self.segmentBGButton = QPushButton("Display Background", self) #segment background parameter
        self.segmentBGButton.setCheckable(True)
        self.segmentBGButton.clicked.connect(self.segment_show_bg)
        # self.segmentBGButton.setEnabled(False)
        
        #segment foreground parameter
        self.segmentFGLabel = QLabel("Foreground:\t", self)  
        self.segmentFGSlider = QSlider(Qt.Horizontal, self)
        self.segmentFGSlider.setMinimum(1)
        self.segmentFGSlider.setMaximum(100)
        self.segmentFGSlider.setValue(3)
        self.segmentFGSlider.setTickInterval(5)
        self.segmentFGSlider.setTickPosition(QSlider.TicksBelow)
        self.segmentFGSlider.valueChanged.connect(self.segment_param_change)
        self.segmentFGSlider.setSingleStep(2)
        # self.segmentFGSlider.setEnabled(False)
        self.segmentFGSpinBox = QSpinBox(self)
        self.segmentFGSpinBox.setRange(1, 100)
        self.segmentFGSpinBox.setValue(self.segmentFGSlider.value())
        self.segmentFGSpinBox.setSingleStep(1)
        self.segmentFGSpinBox.valueChanged.connect(self.segment_param_change)
        # self.segmentFGSpinBox.setEnabled(False)
        
        #segment background parameter
        self.segmentBGLabel = QLabel("Background:\t", self) 
        self.segmentBGSlider = QSlider(Qt.Horizontal, self)
        self.segmentBGSlider.setMinimum(1)
        self.segmentBGSlider.setMaximum(100)
        self.segmentBGSlider.setValue(3)
        self.segmentBGSlider.setTickInterval(5)
        self.segmentBGSlider.setTickPosition(QSlider.TicksBelow)
        self.segmentBGSlider.valueChanged.connect(self.segment_param_change)
        self.segmentBGSlider.setSingleStep(2)
        # self.segmentBGSlider.setEnabled(False)
        self.segmentBGSpinBox = QSpinBox(self)
        self.segmentBGSpinBox.setRange(1, 100)
        self.segmentBGSpinBox.setValue(self.segmentBGSlider.value())
        self.segmentBGSpinBox.setSingleStep(1)
        self.segmentBGSpinBox.valueChanged.connect(self.segment_param_change)
        # self.segmentBGSpinBox.setEnabled(False)

        self.brightnessLabel = QLabel("Brightness:\t", self) #brightness
        self.brightnessSlider = QSlider(Qt.Horizontal, self) 
##        self.brightnessSlider.setGeometry(30, 580, 200, 30)
        self.brightnessSlider.setMinimum(-127)
        self.brightnessSlider.setMaximum(127)
        self.brightnessSlider.setValue(0)
        self.brightnessSlider.setTickInterval(50)
        self.brightnessSlider.setTickPosition(QSlider.TicksBelow)
        self.brightnessSlider.valueChanged.connect(self.bc_change)
        self.brightnessSlider.setSingleStep(5)
        self.brightnessSpinBox = QSpinBox(self)
        self.brightnessSpinBox.setRange(-127, 127)
        self.brightnessSpinBox.setValue(self.brightnessSlider.value())
        self.brightnessSpinBox.setSingleStep(1)
        self.brightnessSpinBox.valueChanged.connect(self.bc_change)
##        self.brightnessSpinBox.move(250, 580)
##        self.brightnessSpinBox.resize(45, 20)

        self.contrastLabel = QLabel("Contrast:\t", self) #contrast
        self.contrastSlider = QSlider(Qt.Horizontal, self) 
##        self.contrastSlider.setGeometry(30, 630, 200, 30)
        self.contrastSlider.setMinimum(-64)
        self.contrastSlider.setMaximum(64)
        self.contrastSlider.setValue(0)
        self.contrastSlider.setTickInterval(50)
        self.contrastSlider.setTickPosition(QSlider.TicksBelow)
        self.contrastSlider.valueChanged.connect(self.bc_change)
        self.contrastSlider.setSingleStep(5)
        self.contrastSpinBox = QSpinBox(self)
        self.contrastSpinBox.setRange(-64, 64)
        self.contrastSpinBox.setValue(self.contrastSlider.value())
        self.contrastSpinBox.setSingleStep(1)
        self.contrastSpinBox.valueChanged.connect(self.bc_change)
##        self.contrastSpinBox.move(250, 630)
##        self.contrastSpinBox.resize(45, 20)

##        self.applyFilter = QCheckBox('Apply Filter', self) #apply filter
##        self.applyFilter.move(700, 525)
##        self.applyFilter.stateChanged.connect(self.dft_change)

        self.minAreaFilter = QSpinBox(self)
        self.minAreaFilter.setRange(1, 10000)
        self.minAreaFilter.setValue(25)
        self.minAreaFilter.setSingleStep(1)
        self.minAreaFilter.valueChanged.connect(self.video_analysis)
        self.minAreaLabel = QLabel("Min Area:", self)

        self.maxAreaFilter = QSpinBox(self)
        self.maxAreaFilter.setRange(1, 1000000)
        self.maxAreaFilter.setValue(1000000)
        self.maxAreaFilter.setSingleStep(100)
        self.maxAreaFilter.valueChanged.connect(self.video_analysis)
        self.maxAreaLabel = QLabel("Max Area:", self)
        
        self.filterType =  QComboBox(self) #Filter Type
        self.filterType.addItem("Average Filter")
        self.filterType.addItem("Fourier Filter")
        self.filterType.addItem("Gaussian Filter")
        self.filterType.addItem("Median Filter")
        self.filterType.addItem("Bilateral Filter")
        self.filterType.addItem("Morph Open")
        self.filterType.addItem("Morph Close")
        self.filterType.currentIndexChanged.connect(self.dft_change)

        self.lowPassLabel = QLabel("Parameter 1:\t", self) #low pass filter
        self.lowPassSlider = QSlider(Qt.Horizontal, self) 
##        self.lowPassSlider.setGeometry(800, 500, 200, 30)
        self.lowPassSlider.setMinimum(0)
        self.lowPassSlider.setMaximum(1000)
        self.lowPassSlider.setValue(6)
        self.lowPassSlider.setTickInterval(50)
        self.lowPassSlider.setTickPosition(QSlider.TicksBelow)
        self.lowPassSlider.valueChanged.connect(self.dft_change)
        self.lowPassSlider.setSingleStep(1)
        self.lowPassSpinBox = QSpinBox(self)
        self.lowPassSpinBox.setRange(0, 1000)
        self.lowPassSpinBox.setValue(self.lowPassSlider.value())
        self.lowPassSpinBox.setSingleStep(1)
        self.lowPassSpinBox.valueChanged.connect(self.dft_change)
##        self.lowPassSpinBox.move(1020, 500)
##        self.lowPassSpinBox.resize(45, 20)

        self.highPassLabel = QLabel("Parameter 2:\t", self) #high pass filter
        self.highPassSlider = QSlider(Qt.Horizontal, self) 
##        self.highPassSlider.setGeometry(800, 550, 200, 30)
        self.highPassSlider.setMinimum(0)
        self.highPassSlider.setMaximum(1000)
        self.highPassSlider.setValue(0)
        self.highPassSlider.setTickInterval(50)
        self.highPassSlider.setTickPosition(QSlider.TicksBelow)
        self.highPassSlider.valueChanged.connect(self.dft_change)
        self.highPassSlider.setSingleStep(5)
        self.highPassSpinBox = QSpinBox(self)
        self.highPassSpinBox.setRange(0, 1000)
        self.highPassSpinBox.setValue(self.highPassSlider.value())
        self.highPassSpinBox.setSingleStep(1)
        self.highPassSpinBox.valueChanged.connect(self.dft_change)
##        self.highPassSpinBox.move(1020, 550)
##        self.highPassSpinBox.resize(45, 20)

##        self.autoDetectROI = QCheckBox('Auto detect ROI', self) #Auto detect ROI
##        self.autoDetectROI.move(430, 605)
##        self.autoDetectROI.stateChanged.connect(self.auto_roi_change)

        self.distinctAutoROI = QCheckBox('Distinct ROI', self) #Distinct auto ROI (one for each manual roi)
        self.distinctAutoROI.setChecked(True)
        self.distinctAutoROI.stateChanged.connect(self.distinct_roi_change)

        self.combineROI = QCheckBox('Combine', self) #combine multiple contour data sets of ROI
        self.combineROI.stateChanged.connect(self.distinct_roi_change)

        self.morphROI = QCheckBox('Morph', self) #Morph ROI (remove holes)
        self.morphROI.setChecked(True)
        self.morphROI.stateChanged.connect(self.roi_morph_change)

        self.morphXLabel = QLabel("Morph X:\t", self)
        self.morphXSpinBox = QSpinBox(self) #morph kernel X
        self.morphXSpinBox.setRange(1, 1000)
        self.morphXSpinBox.setValue(28)
        self.morphXSpinBox.setSingleStep(1)
        self.morphXSpinBox.valueChanged.connect(self.roi_morph_change)
        # self.morphXSpinBox.setEnabled(False)

        self.morphYLabel = QLabel("Morph Y:\t", self)
        self.morphYSpinBox = QSpinBox(self) #morph kernel Y
        self.morphYSpinBox.setRange(1, 1000)
        self.morphYSpinBox.setValue(62)
        self.morphYSpinBox.setSingleStep(1)
        self.morphYSpinBox.valueChanged.connect(self.roi_morph_change)
        # self.morphYSpinBox.setEnabled(False)
        
        self.applyHullROI = QCheckBox('Apply Hull', self) #Apply convex hull on ROI
        self.applyHullROI.stateChanged.connect(self.epsilon_change)

        self.applybgROI = QCheckBox('BG Correct', self) #Apply background correction on ROI
        self.applybgROI.stateChanged.connect(self.bg_roi_change)
        
        self.threshROIType = QComboBox(self) #auto roi threshold type
        self.threshROIType.addItem("Global")
        self.threshROIType.addItem("Adaptive")
        self.threshROIType.addItem("Otsu")
        self.threshROIType.addItem("Canny")
##        self.threshROIType.move(550, 610)
##        self.threshROIType.resize(self.threshROIType.minimumSizeHint())
        self.threshROIType.currentIndexChanged.connect(self.threshold_roi_change)
        
        self.epsilonROILabel = QLabel("Resolution:\t", self) #adjust resolution of roi polyfit
        self.epsilonSlider = QSlider(Qt.Horizontal, self) 
##        self.epsilonSlider.setGeometry(400, 650, 200, 30)
        self.epsilonSlider.setMinimum(-50)
        self.epsilonSlider.setMaximum(0)
        self.epsilonSlider.setValue(-30)
        self.epsilonSlider.setTickInterval(10)
        self.epsilonSlider.setTickPosition(QSlider.TicksBelow)
        self.epsilonSlider.valueChanged.connect(self.epsilon_change)
        self.epsilonSlider.setSingleStep(5)
        self.epsilonSpinBox = QSpinBox(self)
        self.epsilonSpinBox.setRange(-50, 0)
        self.epsilonSpinBox.setValue(self.epsilonSlider.value())
        self.epsilonSpinBox.setSingleStep(1)
        self.epsilonSpinBox.valueChanged.connect(self.epsilon_change)
##        self.epsilonSpinBox.move(620, 650)
##        self.epsilonSpinBox.resize(45, 20)

        self.roiMinLabel = QLabel("Minimum:", self) #minimum area of roi contours
        self.roiMinSpinBox = QSpinBox(self)
        self.roiMinSpinBox.setRange(0, 1000)
        self.roiMinSpinBox.setValue(3)
        self.roiMinSpinBox.setSingleStep(1)
        self.roiMinSpinBox.valueChanged.connect(self.roi_min_change)

        self.resizeROILabel = QLabel("Resize factor:", self) #resize roi
        self.resizeROISpinBox = QDoubleSpinBox(self)
        self.resizeROISpinBox.setRange(0, 10)
        self.resizeROISpinBox.setValue(0.96)
        self.resizeROISpinBox.setSingleStep(0.1)
        self.resizeROISpinBox.valueChanged.connect(self.video_analysis)
        
        self.threshROI1Label = QLabel("Cutoff:\t", self) #threshold cutoff (roi)
        self.threshROISlider1 = QSlider(Qt.Horizontal, self)
##        self.threshROISlider1.setGeometry(400, 700, 200, 30)
        self.threshROISlider1.setMinimum(1)
        self.threshROISlider1.setMaximum(1001)
        self.threshROISlider1.setValue(148)
        self.threshROISlider1.setTickInterval(50)
        self.threshROISlider1.setTickPosition(QSlider.TicksBelow)
        self.threshROISlider1.valueChanged.connect(self.threshold_roi_change)
        self.threshROISlider1.setSingleStep(4)
        self.threshROISpinBox1 = QSpinBox(self)
        self.threshROISpinBox1.setRange(1, 1001)
        self.threshROISpinBox1.setValue(self.threshROISlider1.value())
        self.threshROISpinBox1.setSingleStep(2)
        self.threshROISpinBox1.valueChanged.connect(self.threshold_roi_change)
##        self.threshROISpinBox1.move(620, 700)
##        self.threshROISpinBox1.resize(45, 20)

        self.threshROI2Label = QLabel("Constant:\t", self) #threshold constant (roi)
        self.threshROISlider2 = QSlider(Qt.Horizontal, self)
##        self.threshROISlider2.setGeometry(400, 750, 200, 30)
        self.threshROISlider2.setMinimum(-10)
        self.threshROISlider2.setMaximum(700)
        self.threshROISlider2.setValue(2)
        self.threshROISlider2.setTickInterval(50)
        self.threshROISlider2.setTickPosition(QSlider.TicksBelow)
        self.threshROISlider2.valueChanged.connect(self.threshold_roi_change)
        self.threshROISlider2.setSingleStep(2)
        self.threshROISpinBox2 = QSpinBox(self)
        self.threshROISpinBox2.setRange(-10, 700)
        self.threshROISpinBox2.setValue(self.threshROISlider2.value())
        self.threshROISpinBox2.setSingleStep(1)
        self.threshROISpinBox2.valueChanged.connect(self.threshold_roi_change)
##        self.threshROISpinBox2.move(620, 750)
##        self.threshROISpinBox2.resize(45, 20)

        self.blurROILabel = QLabel("Blur:\t", self) #blur for auto roi detection (roi)
        self.blurROISlider = QSlider(Qt.Horizontal, self)
##        self.threshROISlider2.setGeometry(400, 750, 200, 30)
        self.blurROISlider.setMinimum(3)
        self.blurROISlider.setMaximum(1000)
        self.blurROISlider.setValue(7)
        self.blurROISlider.setTickInterval(100)
        self.blurROISlider.setTickPosition(QSlider.TicksBelow)
        self.blurROISlider.valueChanged.connect(self.blur_roi_change)
        self.blurROISlider.setSingleStep(2)
        self.blurROISpinBox = QSpinBox(self)
        self.blurROISpinBox.setRange(3, 1000)
        self.blurROISpinBox.setValue(self.blurROISlider.value())
        self.blurROISpinBox.setSingleStep(1)
        self.blurROISpinBox.valueChanged.connect(self.blur_roi_change)
##        self.threshROISpinBox2.move(620, 750)
##        self.threshROISpinBox2.resize(45, 20)

        self.bgblurROILabel = QLabel("BG Blur:\t", self) #blur background for auto roi detection (roi)
        self.bgblurROISlider = QSlider(Qt.Horizontal, self)
##        self.threshROISlider2.setGeometry(400, 750, 200, 30)
        self.bgblurROISlider.setMinimum(3)
        self.bgblurROISlider.setMaximum(1000)
        self.bgblurROISlider.setValue(3)
        self.bgblurROISlider.setTickInterval(100)
        self.bgblurROISlider.setTickPosition(QSlider.TicksBelow)
        self.bgblurROISlider.valueChanged.connect(self.bg_blur_roi_change)
        self.bgblurROISlider.setSingleStep(2)
        self.bgblurROISlider.setEnabled(False)
        self.bgblurROISpinBox = QSpinBox(self)
        self.bgblurROISpinBox.setRange(3, 1000)
        self.bgblurROISpinBox.setValue(self.bgblurROISlider.value())
        self.bgblurROISpinBox.setSingleStep(1)
        self.bgblurROISpinBox.valueChanged.connect(self.bg_blur_roi_change)
        self.bgblurROISpinBox.setEnabled(False)

        self.bgblendROILabel = QLabel("BG Blend:\t", self) #blend background for auto roi detection (roi)
        self.bgblendROISlider = QSlider(Qt.Horizontal, self)
##        self.threshROISlider2.setGeometry(400, 750, 200, 30)
        self.bgblendROISlider.setMinimum(0)
        self.bgblendROISlider.setMaximum(100)
        self.bgblendROISlider.setValue(50)
        self.bgblendROISlider.setTickInterval(10)
        self.bgblendROISlider.setTickPosition(QSlider.TicksBelow)
        self.bgblendROISlider.valueChanged.connect(self.bg_blend_roi_change)
        self.bgblendROISlider.setSingleStep(10)
        self.bgblendROISlider.setEnabled(False)
        self.bgblendROISpinBox = QDoubleSpinBox(self)
        self.bgblendROISpinBox.setRange(0, 1)
        self.bgblendROISpinBox.setValue(self.bgblendROISlider.value()/100)
        self.bgblendROISpinBox.setSingleStep(0.01)
        self.bgblendROISpinBox.valueChanged.connect(self.bg_blend_roi_change)
        self.bgblendROISpinBox.setEnabled(False)

        self.analysisMode = QComboBox(self) #change analysis type
        self.analysisMode.addItem("Contact Area Analysis")
        self.analysisMode.addItem("Contact Angle Analysis")
        self.analysisMode.currentIndexChanged.connect(self.video_analysis)
        self.analysisMode.setStyleSheet("QComboBox { font-weight: bold; font-size: 14px;} ")
        
        # self.effectContrast = QCheckBox('Enhance Contrast', self) #enhance effect contrast
        # self.effectContrast.stateChanged.connect(self.video_analysis)
        # self.effectContrast.setStyleSheet("QCheckBox { font-weight: bold; font-size: 14px;} ")

        self.showPlot = QPushButton("Live Plot", self) #Show Plot
        self.showPlot.clicked.connect(self.plot_data)
##        self.showPlot.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showPlot.setStyleSheet("QPushButton { font-weight: bold; font-size: 14px;} ")
##        self.showPlot.resize(self.showPlot.minimumSizeHint())
##        self.showPlot.move(800,600)

        self.saveBtn = QPushButton("Save Data", self) #Save area data
        self.saveBtn.clicked.connect(self.save_prompt)
        # self.saveBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.saveBtn.setStyleSheet("QPushButton { font-weight: bold; font-size: 14px;} ")
##        self.saveBtn.resize(self.saveBtn.minimumSizeHint())
##        self.saveBtn.move(900,600)

        self.clearData = QPushButton("Clear Data", self) #Clear area data
        self.clearData.clicked.connect(self.clear_prompt)
        # self.clearData.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.clearData.setStyleSheet("QPushButton { font-weight: bold; font-size: 14px;} ")
##        self.clearData.resize(self.clearData.minimumSizeHint())
##        self.clearData.move(900,650)
        self.clearData.setEnabled(False)

        self.fpsSpinBox = QDoubleSpinBox(self) #fps input
        self.fpsSpinBox.setMinimum(0)
        self.fpsSpinBox.setValue(1)
##        self.fpsSpinBox.move(650,55)
##        self.fpsSpinBox.resize(45, 20)
        self.fpsSpinBox.valueChanged.connect(self.fps_change)
        self.fpsLabel = QLabel("Enter FPS", self)
##        self.fpsLabel.move(595,50)
        
        self.videoFileNameLabel = QLabel("Select video from file menu", self)
##        self.videoFileNameLabel.setGeometry(10, 650, 400, 60)
##        self.videoFileNameLabel.setTextFormat(Qt.RichText)
        self.videoFileNameLabel.setWordWrap(True)

        self.forceFileNameLabel = QLabel("Select force data from file menu", self)
##        self.forceFileNameLabel.setGeometry(10, 700, 400, 60)
        self.forceFileNameLabel.setWordWrap(True)

        self.zeroForceFileNameLabel = QLabel("Select zero-force data from file menu", self)
        self.zeroForceFileNameLabel.setWordWrap(True)
        

        ################ Adjust window layout #######################
        
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # topleftGroupBox = QGroupBox()
        # # topleftGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # topleftGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # topleftVbox = QGridLayout(self)
        # topleftVbox.setColumnStretch(0, 1.5)
        # topleftGroupBox.setLayout(topleftVbox)
        # topleftVbox.addWidget(self.showContours, 0, 0, 1, 1)
        # topleftVbox.addWidget(self.showEffect, 0, 1, 1, 1)
        # topleftVbox.addWidget(self.roiBtn, 0, 2, 1, 1)

        # toprightGroupBox = QGroupBox()
        # # toprightGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # toprightGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # toprightVbox = QGridLayout(self)
        # # toprightVbox.setColumnStretch(0, 1.5)
        # toprightGroupBox.setLayout(toprightVbox)
        # toprightVbox.addWidget(self.analyzeVideo, 0, 0, 1, 1)
        # toprightVbox.addWidget(self.effectContrast, 0, 1, 1, 1)
        # toprightVbox.addWidget(self.videoEffect, 0, 2, 1, 1)
        # toprightVbox.addWidget(self.showPlot, 0, 3, 1, 1)
        

        # displayGroupBox = QGroupBox()
        # displayGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # displayGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # displayVbox = QGridLayout(self)
        # displayGroupBox.setLayout(displayVbox)
        # displayVbox.addWidget(self.rawView, 0, 0, 1, 1)
        # displayVbox.addWidget(self.effectView, 0, 1, 1, 1)
        
        playbackGroupBox = QGroupBox()
        # playbackGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        playbackGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        playbackVbox = QGridLayout(self)
        # playbackVbox.setRowStretch(1, 1.5)
        playbackGroupBox.setLayout(playbackVbox)
        playbackVbox.addWidget(self.seekSlider, 0, 0, 1, 6)
        playbackVbox.addWidget(self.playBtn, 1, 0, 1, 1)
        playbackVbox.addWidget(self.stopBtn, 1, 1, 1, 1)
        playbackVbox.addWidget(self.prevBtn, 1, 2, 1, 1)
        playbackVbox.addWidget(self.nextBtn, 1, 3, 1, 1)
        playbackVbox.addWidget(self.repeatBtn, 1, 4, 1, 1)
        playbackVbox.addWidget(self.recordBtn, 1, 5, 1, 1)        

        self.bgGroupBox = QGroupBox("Enable")
        # self.bgGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.bgGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.bgGroupBox.setCheckable(True)
        self.bgGroupBox.setChecked(False)        
        self.bgGroupBox.toggled.connect(self.bg_change)
        bgVbox = QGridLayout(self)
        self.bgGroupBox.setLayout(bgVbox)
##        bgVbox.addWidget(self.bgSubtract, 0, 0, 1, 1)
        bgVbox.addWidget(self.bgButton, 0, 0, 1, 2)
        bgVbox.addWidget(self.bgShowButton, 0, 2, 1, 2)
        bgVbox.addWidget(self.backgroundCorrectionLabel, 1, 0, 1, 1)
        bgVbox.addWidget(self.backgroundCorrection, 1, 1, 1, 1)
        bgVbox.addWidget(self.bgBlurLabel, 2, 0, 1, 1)
        bgVbox.addWidget(self.bgSlider, 2, 1, 1, 2)
        bgVbox.addWidget(self.bgSpinBox, 2, 3, 1, 1)
        bgVbox.addWidget(self.bgAlphaLabel, 1, 2, 1, 1,alignment=Qt.AlignRight)
        bgVbox.addWidget(self.bgAlphaSpinBox, 1, 3, 1, 1)
        
        
        measureGroupBox = QGroupBox("Length Calibration")
        # measureGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        measureGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        measureVbox = QGridLayout(self)
        measureGroupBox.setLayout(measureVbox)
        measureVbox.addWidget(self.pixelValue, 0, 0, 1, 1)
        measureVbox.addWidget(self.pixelLabel, 0, 1, 1, 1)
        measureVbox.addWidget(self.lengthValue, 0, 2, 1, 1)
        measureVbox.addWidget(self.lengthUnit, 0, 3, 1, 1)
        measureVbox.addWidget(self.measureBtn, 1, 1, 1, 2)

        fpsGroupBox = QGroupBox("Adjust")
        # fpsGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        fpsGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        fpsVbox = QGridLayout(self)
        fpsGroupBox.setLayout(fpsVbox)
        fpsVbox.addWidget(self.fpsLabel, 0, 0, 1, 1)
        fpsVbox.addWidget(self.fpsSpinBox, 0, 1, 1, 1)
        fpsVbox.addWidget(self.correctZeroForce, 1, 0, 1, 2)

        self.bcGroupBox = QGroupBox()
        # self.bcGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.bcGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        bcVbox = QGridLayout(self)
        self.bcGroupBox.setLayout(bcVbox)
        bcVbox.addWidget(self.brightnessLabel, 0, 0, 1, 1)
        bcVbox.addWidget(self.brightnessSlider, 0, 1, 1, 1)
        bcVbox.addWidget(self.brightnessSpinBox, 0, 3, 1, 1)
        bcVbox.addWidget(self.contrastLabel, 1, 0, 1, 1)
        bcVbox.addWidget(self.contrastSlider, 1, 1, 1, 1)
        bcVbox.addWidget(self.contrastSpinBox, 1, 3, 1, 1)

        self.dftGroupBox = QGroupBox("Enable")
        # self.dftGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.dftGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.dftGroupBox.setCheckable(True)
        self.dftGroupBox.setChecked(False)        
        self.dftGroupBox.toggled.connect(self.dft_change)
        dftVbox = QGridLayout(self)
        self.dftGroupBox.setLayout(dftVbox)
##        dftVbox.addWidget(self.applyFilter, 0, 0, 1, 1)
        dftVbox.addWidget(self.filterType, 0, 0, 1, 1)
        dftVbox.addWidget(self.maxAreaLabel, 0, 7, 1, 1)
        dftVbox.addWidget(self.maxAreaFilter, 0, 8, 1, 1)
        dftVbox.addWidget(self.minAreaLabel, 0, 9, 1, 1)
        dftVbox.addWidget(self.minAreaFilter, 0, 10, 1, 1)
        dftVbox.addWidget(self.lowPassLabel, 1, 0, 1, 1)
        dftVbox.addWidget(self.lowPassSlider, 1, 1, 1, 9)
        dftVbox.addWidget(self.lowPassSpinBox, 1, 10, 1, 1)
        dftVbox.addWidget(self.highPassLabel, 2, 0, 1, 1)
        dftVbox.addWidget(self.highPassSlider, 2, 1, 1, 9)
        dftVbox.addWidget(self.highPassSpinBox, 2, 10, 1, 1)

        fileGroupBox = QGroupBox("Filenames")
        # fileGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        fileGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        fileVbox = QGridLayout(self)
        fileGroupBox.setLayout(fileVbox)
        fileVbox.addWidget(self.videoFileNameLabel, 0, 0, 1, 1)
        fileVbox.addWidget(self.forceFileNameLabel, 1, 0, 1, 1)
        fileVbox.addWidget(self.zeroForceFileNameLabel, 2, 0, 1, 1)

        # middlerightGroupBox = QGroupBox()
        # middlerightGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # middlerightVbox = QGridLayout(self)
        # middlerightVbox.setColumnStretch(0, 1)
        # middlerightVbox.setColumnStretch(2, 1.5)
        # middlerightGroupBox.setLayout(middlerightVbox)
        # middlerightVbox.addWidget(self.showPlot, 0, 1, 1, 1)
        # middlerightVbox.addWidget(self.effectContrast, 0, 0, 1, 1)
        
        self.threshGroupBox = QGroupBox()
        # self.threshGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.threshGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        threshVbox = QGridLayout(self)
        self.threshGroupBox.setLayout(threshVbox)
        # threshVbox.addWidget(self.applySegment, 0, 0, 1, 1)
        threshVbox.addWidget(threshTypeLabel, 0, 0, 1, 1)
        threshVbox.addWidget(self.threshType, 0, 1, 1, 1)
        threshVbox.addWidget(self.binaryInvert, 0, 2, 1, 1)
        threshVbox.addWidget(self.thresh1Label, 1, 0, 1, 1)
        threshVbox.addWidget(self.threshSlider1, 1, 1, 1, 8)
        threshVbox.addWidget(self.threshSpinBox1, 1, 9, 1, 1)
        threshVbox.addWidget(self.thresh2Label, 2, 0, 1, 1)
        threshVbox.addWidget(self.threshSlider2, 2, 1, 1, 8)
        threshVbox.addWidget(self.threshSpinBox2, 2, 9, 1, 1)
        threshVbox.addWidget(self.applyMorph, 3, 0, 1, 1)
        threshVbox.addWidget(morphTypeLabel, 3, 1, 1, 1)
        threshVbox.addWidget(self.morphType, 3, 2, 1, 1)
        threshVbox.addWidget(morphSizeLabel, 3, 4, 1, 1)
        threshVbox.addWidget(self.morphSize, 3, 5, 1, 1)
        threshVbox.addWidget(morphIterationsLabel, 3, 7, 1, 1)
        threshVbox.addWidget(self.morphIterations, 3, 8, 1, 1)

        self.segmentGroupBox = QGroupBox("Enable")
        # self.threshGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.threshGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.segmentGroupBox.setCheckable(True)
        self.segmentGroupBox.setChecked(False)        
        self.segmentGroupBox.toggled.connect(self.segment_change)
        segmentVbox = QGridLayout(self)
        self.segmentGroupBox.setLayout(segmentVbox)
        segmentVbox.addWidget(self.useDistTransfrom, 0, 0, 1, 1)
        segmentVbox.addWidget(self.showSegment, 0, 1, 1, 1)
        segmentVbox.addWidget(self.segmentFGButton, 0, 2, 1, 1)
        segmentVbox.addWidget(self.segmentBGButton, 0, 3, 1, 1)
        # segmentVbox.addWidget(chooseTemplateBtn, 0, 4, 1, 1)
        segmentVbox.addWidget(self.segmentFGLabel, 1, 0, 1, 1)
        segmentVbox.addWidget(self.segmentFGSlider, 1, 1, 1, 8)
        segmentVbox.addWidget(self.segmentFGSpinBox, 1, 9, 1, 1)
        segmentVbox.addWidget(self.segmentBGLabel, 2, 0, 1, 1)
        segmentVbox.addWidget(self.segmentBGSlider, 2, 1, 1, 8)
        segmentVbox.addWidget(self.segmentBGSpinBox, 2, 9, 1, 1)


        self.featuresGroupBox = QGroupBox()
        # self.featuresGroupBox.setCheckable(True)
        # self.featuresGroupBox.setChecked(False)        
        # self.featuresGroupBox.toggled.connect(self.video_analysis)
        featuresVbox = QGridLayout(self)
        self.featuresGroupBox.setLayout(featuresVbox)
        featuresVbox.addWidget(topTemplateLabel, 0, 0, 1, 1)
        featuresVbox.addWidget(topTemplateBtn, 0, 1, 1, 1)
        featuresVbox.addWidget(lineTypeTopLabel, 0, 2, 1, 1)
        featuresVbox.addWidget(self.lineTypeTop, 0, 3, 1, 1)
        featuresVbox.addWidget(markerWindowTopLabel, 0, 4, 1, 1)
        featuresVbox.addWidget(self.markerWindowTop, 0, 5, 1, 1)
        featuresVbox.addWidget(self.displayFeatureEdgesTop, 0, 6, 1, 1)
        featuresVbox.addWidget(self.displayFeatureLinesTop, 0, 7, 1, 1)
        featuresVbox.addWidget(bottomTemplateLabel, 1, 0, 1, 1)
        featuresVbox.addWidget(bottomTemplateBtn, 1, 1, 1, 1)
        featuresVbox.addWidget(lineTypeBottomLabel, 1, 2, 1, 1)
        featuresVbox.addWidget(self.lineTypeBottom, 1, 3, 1, 1)
        featuresVbox.addWidget(markerWindowBottomLabel, 1, 4, 1, 1)
        featuresVbox.addWidget(self.markerWindowBottom, 1, 5, 1, 1)
        featuresVbox.addWidget(self.displayFeatureEdgesBottom, 1, 6, 1, 1)
        featuresVbox.addWidget(self.displayFeatureLinesBottom, 1, 7, 1, 1)
        featuresVbox.addWidget(lineThreshLabel, 2, 0, 1, 1)
        featuresVbox.addWidget(self.lineThreshSlider, 2, 1, 1, 1)
        featuresVbox.addWidget(self.lineThresh, 2, 2, 1, 1)
        featuresVbox.addWidget(lineLengthLabel, 2, 3, 1, 1)
        featuresVbox.addWidget(self.lineLengthSlider, 2, 4, 1, 1)
        featuresVbox.addWidget(self.lineLength, 2, 5, 1, 1)
        featuresVbox.addWidget(lineGapLabel, 2, 6, 1, 1)
        featuresVbox.addWidget(self.lineGapSlider, 2, 7, 1, 1)
        featuresVbox.addWidget(self.lineGap, 2, 8, 1, 1)
        
        self.threshROIGroupBox = QGroupBox("Enable")
        # self.threshROIGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.threshROIGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.threshROIGroupBox.setCheckable(True)
        self.threshROIGroupBox.setChecked(False)        
        self.threshROIGroupBox.toggled.connect(self.auto_roi_change)
        threshROIVbox = QGridLayout(self)
        self.threshROIGroupBox.setLayout(threshROIVbox)
##        threshROIVbox.addWidget(self.autoDetectROI, 0, 0, 1, 1)
        threshROIVbox.addWidget(self.distinctAutoROI, 0, 0, 1, 1)
        threshROIVbox.addWidget(self.combineROI, 0, 1, 1, 1)
        threshROIVbox.addWidget(self.applyHullROI, 0, 2, 1, 1)
        threshROIVbox.addWidget(self.applybgROI, 0, 3, 1, 1)
        threshROIVbox.addWidget(self.roiMinLabel, 0, 5, 1, 1)
        threshROIVbox.addWidget(self.roiMinSpinBox, 0, 6, 1, 1)
        threshROIVbox.addWidget(self.resizeROILabel, 0, 7, 1, 1)
        threshROIVbox.addWidget(self.resizeROISpinBox, 0, 8, 1, 1)        
        threshROIVbox.addWidget(self.threshROIType, 0, 9, 1, 1)
        threshROIVbox.addWidget(self.epsilonROILabel, 1, 0, 1, 1)
        threshROIVbox.addWidget(self.epsilonSlider, 1, 1, 1, 3)
        threshROIVbox.addWidget(self.epsilonSpinBox, 1, 4, 1, 1)
        threshROIVbox.addWidget(self.morphROI, 1, 5, 1, 1)
        threshROIVbox.addWidget(self.morphXLabel, 1, 6, 1, 1)
        threshROIVbox.addWidget(self.morphXSpinBox, 1, 7, 1, 1)
        threshROIVbox.addWidget(self.morphYLabel, 1, 8, 1, 1)
        threshROIVbox.addWidget(self.morphYSpinBox, 1, 9, 1, 1)
        threshROIVbox.addWidget(self.threshROI1Label, 2, 0, 1, 1)
        threshROIVbox.addWidget(self.threshROISlider1, 2, 1, 1, 8)
        threshROIVbox.addWidget(self.threshROISpinBox1, 2, 9, 1, 1)
        threshROIVbox.addWidget(self.threshROI2Label, 3, 0, 1, 1)
        threshROIVbox.addWidget(self.threshROISlider2, 3, 1, 1, 8)
        threshROIVbox.addWidget(self.threshROISpinBox2, 3, 9, 1, 1)
        threshROIVbox.addWidget(self.blurROILabel, 4, 0, 1, 1)
        threshROIVbox.addWidget(self.blurROISlider, 4, 1, 1, 8)
        threshROIVbox.addWidget(self.blurROISpinBox, 4, 9, 1, 1)
        threshROIVbox.addWidget(self.bgblurROILabel, 5, 0, 1, 1)
        threshROIVbox.addWidget(self.bgblurROISlider, 5, 1, 1, 3)
        threshROIVbox.addWidget(self.bgblurROISpinBox, 5, 4, 1, 1)
        threshROIVbox.addWidget(self.bgblendROILabel, 5, 5, 1, 1)
        threshROIVbox.addWidget(self.bgblendROISlider, 5, 6, 1, 3)
        threshROIVbox.addWidget(self.bgblendROISpinBox, 5, 9, 1, 1)
        
        self.dataGroupBox = QGroupBox()
        # self.dataGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.dataGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        dataVbox = QGridLayout(self)
        self.dataGroupBox.setLayout(dataVbox)
        dataVbox.addWidget(self.analyzeVideo, 0, 0, 1, 1)
        dataVbox.addWidget(self.roiBtn, 0, 1, 1, 1)
        dataVbox.addWidget(self.saveBtn, 0, 2, 1, 1)
        dataVbox.addWidget(self.analysisMode, 1, 0, 1, 1)
        dataVbox.addWidget(self.showPlot, 1, 1, 1, 1)
        dataVbox.addWidget(self.clearData, 1, 2, 1, 1)
        
        effectsTab = QTabWidget() #B&C and flitering tabs
        effectsTab.addTab(self.bgGroupBox,"Background Correct")
        effectsTab.addTab(self.bcGroupBox,"Brightness/Contrast")
        effectsTab.addTab(self.dftGroupBox,"Filtering")
        effectsTab.setStyleSheet("QTabWidget { font-weight: bold; } ")
        
        thresholdTab = QTabWidget() #manual and auto threshold function tabs
        thresholdTab.addTab(self.threshGroupBox,"Binarize")
        thresholdTab.addTab(self.threshROIGroupBox,"Auto ROI detect")
        thresholdTab.addTab(self.segmentGroupBox,"Segment")
        thresholdTab.addTab(self.featuresGroupBox,"Features")
        thresholdTab.setStyleSheet("QTabWidget { font-weight: bold; } ")

        self.middleleftGroupBox = QGroupBox()
        # self.middleleftGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        middleleftVbox = QGridLayout(self)
        self.middleleftGroupBox.setLayout(middleleftVbox)
        # middleleftVbox.addWidget(self.bgGroupBox, 0, 0, 1, 2)
        middleleftVbox.addWidget(effectsTab, 0, 0, 2, 2)
        middleleftVbox.addWidget(measureGroupBox, 0, 2, 1, 1)
        middleleftVbox.addWidget(fpsGroupBox, 1, 2, 1, 1)
        
        
        # self.layout.addWidget(topleftGroupBox, 0, 0, 1, 1)
        # self.layout.addWidget(toprightGroupBox, 0, 1, 1, 1)
        
        self.rawViewDict = {"Original":self.rawView1, 
                            "Processed":self.rawView2,
                            "Transformed":self.rawView3}
        self.rawViewTab = QTabWidget() #B&C and flitering tabs
        for key in self.rawViewDict.keys():
            self.rawViewTab.addTab(self.rawViewDict[key],key)
        self.rawViewTab.currentChanged.connect(self.rawViewTabChanged)
        self.rawViewTab.setStyleSheet("QTabWidget { font-weight: bold; } ")
        # rawViewResize = QSizeGrip(self.rawViewTab)
        
        self.effectViewDict = {"Binary":self.effectView1, 
                            "Masked":self.effectView2,
                            "Processed":self.effectView3,
                            "Transformed":self.effectView4,
                            "Auto ROI":self.effectView5,
                            "Plot":self.effectView6}
        self.effectViewTab = QTabWidget() #B&C and flitering tabs
        for key in self.effectViewDict.keys():
            self.effectViewTab.addTab(self.effectViewDict[key],key)
        self.effectViewTab.currentChanged.connect(self.effectViewTabChanged)
        self.effectViewTab.setStyleSheet("QTabWidget { font-weight: bold; } ")
        
        self.layout.addWidget(self.rawViewTab, 0, 0, 1, 1)
        self.layout.addWidget(self.effectViewTab, 0, 1, 1, 1)
        # self.layout.addWidget(displayGroupBox, 1, 0, 4, 2)
        
        self.layout.addWidget(playbackGroupBox, 5, 0, 1, 1)
        # self.layout.addWidget(middlerightGroupBox, 5, 1, 1, 1)
        
        self.layout.addWidget(self.middleleftGroupBox, 6, 0, 2, 1)
        # self.layout.addWidget(effectsTab, 7, 0, 1, 1)
        # self.layout.addWidget(self.bcGroupBox, 8, 0, 2, 1)
        # self.layout.addWidget(self.dftGroupBox, 10, 0, 3, 1)

        self.layout.addWidget(fileGroupBox, 8, 0, 1, 1)

        # self.layout.addWidget(self.threshGroupBox, 6, 1, 3, 1)
        # self.layout.addWidget(self.threshROIGroupBox, 9, 1, 5, 1)
        self.layout.addWidget(thresholdTab, 6, 1, 3, 1)

        self.layout.addWidget(self.dataGroupBox, 5, 1, 1, 1)

        wid.setLayout(self.layout)
         