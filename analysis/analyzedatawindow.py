# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:29:38 2020

@author: adwait
"""
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, \
     QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, \
     QGroupBox, QGridLayout, QWidget
     
# %% Configure Plot Window
class AnalyizeDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 200)
        self.setWindowTitle("Analyze Datafile")
        self.layout = QGridLayout()
        
        # self.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
        #                                [0,100],[0,100],[0,1]]}
        self.dataAnalDict = {}
        # self.dataAnalDict['force settings'] = {}
        self.dataAnalDict['Vertical force'] = {}
        self.dataAnalDict['Lateral force'] = {}
        self.initialize_dict("Default", range_clear = True)
        self.dataAnalDict['misc settings'] = {}
        
        self.home()
        
    #call this when your are adding a new roi label. #initialize force settings in dict
    def initialize_dict(self, roi_label, range_clear = True):
        # self.dataAnalDict['force settings'][roi_label] = {}
        # self.init_force_dict(roi_label, "Vertical force")
        # self.init_force_dict(roi_label, "Lateral force")
        if range_clear == True:
            self.dataAnalDict["Vertical force"]["ranges"] = {}
            self.dataAnalDict["Lateral force"]["ranges"] = {}
        self.init_force_dict("Vertical force", roi_label)        
        self.init_force_dict("Lateral force", roi_label)
    
    #initialize sub properties of force
    def init_force_dict(self, force, roi_label):
        self.dataAnalDict[force]["ranges"][roi_label] = {}
        self.dataAnalDict[force]["ranges"][roi_label]["Zero"] = "100,200"
        self.dataAnalDict[force]["ranges"][roi_label]["Force"] = "100,200"
        self.dataAnalDict[force]["ranges"][roi_label]["Preload"] = "100,200"
        self.dataAnalDict[force]["transform"] = {}
        self.dataAnalDict[force]["transform"]["Filter"] = False
        self.dataAnalDict[force]["transform"]["Filter window"] = 43
        self.dataAnalDict[force]["transform"]["Filter order"] = 2
        self.dataAnalDict[force]["transform"]["Cross Talk"] = 0
        self.dataAnalDict[force]["transform"]["Zero subtract"] = False
        # self.dataAnalDict['force settings'][roi_label][force] = {}
        # self.dataAnalDict['force settings'][roi_label][force]["Zero"] = "0,10"
        # self.dataAnalDict['force settings'][roi_label][force]["Force"] = "0,10"
        # self.dataAnalDict['force settings'][roi_label][force]["Preload"] = "0,10"
        # self.dataAnalDict['force settings'][roi_label][force]["Filter"] = False
        # self.dataAnalDict['force settings'][roi_label][force]["Filter window"] = 43
        # self.dataAnalDict['force settings'][roi_label][force]["Filter order"] = 2
        # self.dataAnalDict['force settings'][roi_label][force]["Cross Talk"] = 0
    
    def home(self):

        # self.showContactArea = QCheckBox('contact area', self) #contact area
        # self.showContactArea.setChecked(True)

        # self.showROIArea = QCheckBox('ROI area', self) #roi area
        # self.showContactLength = QCheckBox('contact length', self) #contact length
        # self.showROILength = QCheckBox('ROI length', self) #roi length
        # self.showContactNumber = QCheckBox('contact number', self) #contact number
        # self.showEcc = QCheckBox('eccentricity', self) #median eccentricity

        # self.showLateralForce = QCheckBox('lateral force', self) #lateral force
        # self.showZPiezo = QCheckBox('vertical piezo', self) #z piezo
        # self.showXPiezo = QCheckBox('lateral piezo', self) #x piezo
        # self.showAdhesion = QCheckBox('adhesion calculation', self) #adhesion/preload calc line
        # self.showFriction = QCheckBox('friction calculation', self) #friction calc lines
        # self.showStress = QCheckBox('stress', self) #stress
        # self.showDeformation = QCheckBox('deformation', self) #deformation
        # self.showTitle = QCheckBox('title', self) #plt title
        # self.showTitle.setChecked(True)
        # self.showLegend2 = QCheckBox('legend2', self) #plt title
        # self.showLegend2.setChecked(True)
        
        # self.showWidgets = [self.showContactArea, self.showROIArea, self.showZPiezo, 
        #                     self.showXPiezo, self.showAdhesion, self.showFriction,
        #                     self.showLateralForce, self.showContactLength, self.showROILength,
        #                     self.showContactNumber, self.showEcc, self.showStress,
        #                     self.showDeformation, self.showTitle, self.showLegend2]
        
        # self.xAxisLabel = QLabel("<b>X Axis:</b>", self)
        # self.xAxisParam = QComboBox(self) #x axis parameter
        # self.xAxisParam.addItem("Time (s)")
        # self.xAxisParam.addItem("Vertical Position (μm)")
        # self.xAxisParam.addItem("Lateral Position (μm)")
        # self.xAxisParam.addItem("Deformation (μm)")
        
        # self.fontLabel = QLabel("Font Size:", self)
        # self.fontSize = QDoubleSpinBox(self) #vertical force zero range start
        # self.fontSize.setValue(12)
        # self.fontSize.setSingleStep(1)
        # self.fontSize.setRange(1, 100)
        
        roiChoiceLabel = QLabel("ROI Label:", self)
        self.roiChoice = QComboBox(self) #choose ROI
        self.roiChoice.addItem("Default")
        self.roiChoice.setCurrentIndex(0)
        self.roiChoice.currentIndexChanged.connect(self.update_widgets)
        
        dataChoiceLabel = QLabel("Data:", self)
        self.dataChoice = QComboBox(self) #force data
        self.dataChoiceDict = {"Vertical force" : "Adhesion",
                         "Lateral force" : "Friction"}
        self.dataChoice.addItems(list(self.dataChoiceDict.keys()))
        self.dataChoice.setCurrentIndex(0)
        self.dataChoice.currentIndexChanged.connect(self.update_widgets)
        
        self.zeroBtn = QPushButton("Zero Range", self) #zero
        self.zeroLabel = QLineEdit(self)
        self.zeroLabel.setReadOnly(True)        
        self.zeroLabel.setText("100,200")
        
        self.forceBtn = QPushButton(self.dataChoiceDict[self.dataChoice.currentText()] +
                                    " Range", self) #adhesion/friction
        self.forceLabel = QLineEdit(self) 
        self.forceLabel.setReadOnly(True)        
        self.forceLabel.setText("100,200")
        
        self.preloadBtn = QPushButton("Preload Range", self) #preload
        self.preloadLabel = QLineEdit(self)
        self.preloadLabel.setReadOnly(True)        
        self.preloadLabel.setText("100,200")
        
        
        
        # self.startLabel = QLabel("Start (%):", self)
        # self.endLabel = QLabel("End (%):", self)

        # self.zeroLabel = QLabel("Zero Range", self)
        # self.adhLabel = QLabel("Adhesion Range", self)
        # self.prl1Label = QLabel("Preload Range", self)
        
        # self.zeroRange1 = QDoubleSpinBox(self) #vertical force zero range start
        # self.zeroRange1.setValue(0)
        # self.zeroRange1.setSingleStep(1)
        # self.zeroRange1.setRange(0, 100)
        # self.zeroRange1.valueChanged.connect(self.update_dict)
        
        # self.zeroRange2 = QDoubleSpinBox(self) #vertical force zero range end
        # self.zeroRange2.setValue(1)
        # self.zeroRange2.setSingleStep(1)
        # self.zeroRange2.setRange(0, 100)
        # self.zeroRange2.valueChanged.connect(self.update_dict)

        # self.adhRange1 = QDoubleSpinBox(self) #adhesion peak range start
        # self.adhRange1.setValue(0)
        # self.adhRange1.setSingleStep(1)
        # self.adhRange1.setRange(0, 100)
        # self.adhRange1.valueChanged.connect(self.update_dict)

        # self.adhRange2 = QDoubleSpinBox(self) #adhesion peak range start
        # self.adhRange2.setValue(100)
        # self.adhRange2.setSingleStep(1)
        # self.adhRange2.setRange(0, 100)
        # self.adhRange2.valueChanged.connect(self.update_dict)

        # self.prl1Range1 = QDoubleSpinBox(self) #preload peak range start
        # self.prl1Range1.setValue(0)
        # self.prl1Range1.setSingleStep(1)
        # self.prl1Range1.setRange(0, 100)
        # self.prl1Range1.valueChanged.connect(self.update_dict)

        # self.prl1Range2 = QDoubleSpinBox(self) #preload peak range start
        # self.prl1Range2.setValue(100)
        # self.prl1Range2.setSingleStep(1)
        # self.prl1Range2.setRange(0, 100)
        # self.prl1Range2.valueChanged.connect(self.update_dict)

        # self.zero2Range1 = QDoubleSpinBox(self) #lateral force zero range start
        # self.zero2Range1.setValue(0)
        # self.zero2Range1.setSingleStep(1)
        # self.zero2Range1.setRange(0, 100)
        # self.zero2Range1.valueChanged.connect(self.update_dict)

        # self.zero2Range2 = QDoubleSpinBox(self) #lateral force zero range end
        # self.zero2Range2.setValue(1)
        # self.zero2Range2.setSingleStep(1)
        # self.zero2Range2.setRange(0, 100)
        # self.zero2Range2.valueChanged.connect(self.update_dict)

        # self.filterLatF = QCheckBox('Filter stress curve', self) #filter
        
        self.filter = QCheckBox('Filter', self) #filter
        # self.filter.stateChanged.connect(self.update_dict)
        
        windLabel = QLabel("Window Length:", self)
        self.filter_wind = QSpinBox(self) #filter window
        self.filter_wind.setValue(43)
        self.filter_wind.setSingleStep(20)
        self.filter_wind.setRange(3, 10001)
        # self.filter_wind.valueChanged.connect(self.filter_change)
        
        
        polyLabel = QLabel("Polynomial Order:", self)
        self.filter_poly = QSpinBox(self) #filter polynom
        self.filter_poly.setValue(2)
        self.filter_poly.setSingleStep(1)
        self.filter_poly.setRange(1, 20000)
        # self.filter_poly.valueChanged.connect(self.update_dict)
        
        self.zero_subtract = QCheckBox('Zero subtract', self) #filter
        
        # self.startLabel2 = QLabel("Start (%):", self)
        # self.endLabel2 = QLabel("End (%):", self)

        # self.frLabel = QLabel("Friction Range", self)
        # self.prl2Label = QLabel("Preload Range", self)
        # self.zero2Label = QLabel("Zero Range", self)
        
        eqLabel = QLabel("Lateral Calib. Equation (μN):", self)        
        self.latCalibEq = QLineEdit(self) #lateral force calib equation
        self.latCalibEq.setText("29181.73*x")

        noiseStepsLabel = QLabel("Noisy Steps:", self)        
        noiseSteps = QLineEdit(self) #remove first data point from steps
        noiseSteps.setText("")

        # self.legendPosLabel = QLabel("Legend:", self) #legend position        
        # self.legendPos = QLineEdit(self)
        # self.legendPos.setText("upper right")

        # self.startFullLabel = QLabel("Start (%):", self)
        # self.endFullLabel = QLabel("End (%):", self)

        # self.startFull = QDoubleSpinBox(self) #plot range start
        # self.startFull.setValue(0)
        # self.startFull.setSingleStep(1)
        # self.startFull.setRange(0, 100)

        # self.endFull = QDoubleSpinBox(self) #plot range end
        # self.endFull.setValue(100)
        # self.endFull.setSingleStep(1)
        # self.endFull.setRange(0, 100)
        
        # self.invertLatForce = QCheckBox('Invert Lateral Force', self) #invert

        applyCrossTalk = QCheckBox('Apply Cross Talk', self) #cross talk flag
        # self.zeroShift = QCheckBox('Shift to Zero', self) #force curve shift to zero

        # self.vertCrossTalk = QDoubleSpinBox(self) #vertical cross talk slope
        # self.vertCrossTalk.setValue(0)
        # self.vertCrossTalk.setSingleStep(0.1)
        # self.vertCrossTalk.setDecimals(4)
        # self.vertCrossTalk.setRange(-1000, 1000)
        # self.vertCTlabel = QLabel("Cross Talk (μN/μN):", self)

        # self.latCrossTalk = QDoubleSpinBox(self) #lateral cross talk slope
        # self.latCrossTalk.setValue(0)
        # self.latCrossTalk.setSingleStep(0.1)
        # self.latCrossTalk.setDecimals(4)
        # self.latCrossTalk.setRange(-1000, 1000)
        # self.latCTlabel = QLabel("Cross Talk (μN/μN):", self)
        
        CTlabel = QLabel("Cross Talk (μN/μN):", self) # cross talk slope
        self.crossTalk = QDoubleSpinBox(self) 
        self.crossTalk.setValue(0)
        self.crossTalk.setSingleStep(0.1)
        self.crossTalk.setDecimals(4)
        self.crossTalk.setRange(-1000, 1000)
        # self.crossTalk.valueChanged.connect(self.update_dict)
        
        
        # self.frictionRange1 = QDoubleSpinBox(self) #friction range start
        # self.frictionRange1.setValue(0)
        # self.frictionRange1.setSingleStep(1)
        # self.frictionRange1.setRange(0, 100)
        # self.frictionRange1.valueChanged.connect(self.update_dict)
        
        # self.frictionRange2 = QDoubleSpinBox(self) #friction range end
        # self.frictionRange2.setValue(100)
        # self.frictionRange2.setSingleStep(1)
        # self.frictionRange2.setRange(0, 100)
        # self.frictionRange2.valueChanged.connect(self.update_dict)

        # self.prl2Range1 = QDoubleSpinBox(self) #friction preload peak range start
        # self.prl2Range1.setValue(0)
        # self.prl2Range1.setSingleStep(1)
        # self.prl2Range1.setRange(0, 100)
        # self.prl2Range1.valueChanged.connect(self.update_dict)

        # self.prl2Range2 = QDoubleSpinBox(self) #friction preload peak range start
        # self.prl2Range2.setValue(100)
        # self.prl2Range2.setSingleStep(1)
        # self.prl2Range2.setRange(0, 100)
        # self.prl2Range2.valueChanged.connect(self.update_dict)

        # self.fitPosLabel = QLabel("Fit Position\n(x,y):", self) #fit eq. position        
        # self.fitPos = QLineEdit(self)
        # self.fitPos.setText('0.5,0.5')

        # self.showFitEq = QCheckBox('Show Slope', self) #display equation on plot
        
        kBeamLabel = QLabel("Beam Spring Constant (μN/μm):", self) #beam dpring constant       
        kBeam = QLineEdit(self)
        kBeam.setText('30,1')

        # deformStartLabel = QLabel("Deformation Start:", self) #contact start tolerance auto detect
        self.deformBtn = QPushButton("Deformation Range", self) #deformation
        self.deformLabel = QLineEdit(self)
        self.deformLabel.setReadOnly(True)
        # self.deformLabel.textChanged.connect(self.updateRange)
        self.deformLabel.setText("100,200")
        # self.deformStart = QSpinBox(self) 
        # self.deformStart.setValue(100)
        # self.deformStart.setSingleStep(1)
        # self.deformStart.setRange(0, 10000)
        
        # self.dataAnalDict['misc'] = {}
        self.dataAnalDict['misc settings']['apply cross talk'] = applyCrossTalk
        self.dataAnalDict['misc settings']['noise steps'] = noiseSteps
        self.dataAnalDict['misc settings']['deformation range'] = self.deformLabel
        self.dataAnalDict['misc settings']['beam spring constant'] = kBeam      
        
        self.okBtn = QPushButton("OK", self) #Close window

        self.updateBtn = QPushButton("Update", self) #Update
        
        
        #update dictionary on widget value change
        self.zeroLabel.textChanged.connect(self.update_dict)
        self.forceLabel.textChanged.connect(self.update_dict)
        self.preloadLabel.textChanged.connect(self.update_dict)
        self.filter.stateChanged.connect(self.update_dict)
        self.filter_wind.valueChanged.connect(self.filter_change)
        self.filter_poly.valueChanged.connect(self.update_dict)
        self.zero_subtract.stateChanged.connect(self.update_dict)
        self.crossTalk.valueChanged.connect(self.update_dict)
        self.zeroLabel.textChanged.connect(self.update_dict)
        self.forceLabel.textChanged.connect(self.update_dict)
        self.preloadLabel.textChanged.connect(self.update_dict)
        
        # self.zeroGroupBox = QGroupBox("Configure Vertical Force")
        # filterGroupBox = QGroupBox("Configure Plot")
        # flagGroupBox = QGroupBox("Show")
        # self.latCalibGroupBox = QGroupBox("Configure Lateral Force")
        # self.fittingGroupBox = QGroupBox("Fit Data")
        
        forceGroupBox = QGroupBox("Force")
        miscGroupBox = QGroupBox("Misc")
        buttonGroupBox = QGroupBox()
        
        forceGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        miscGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # self.zeroGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # filterGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # flagGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # self.latCalibGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # self.fittingGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        # self.fittingGroupBox.setCheckable(True)
        # self.fittingGroupBox.setChecked(False)

        # self.layout.addWidget(self.roiChoice, 0, 0, 1, 2)
        # self.layout.addWidget(self.zeroGroupBox, 1, 0)
        # self.layout.addWidget(filterGroupBox, 2, 1)
        # self.layout.addWidget(flagGroupBox, 2, 0)
        # self.layout.addWidget(self.latCalibGroupBox, 1, 1)
        # self.layout.addWidget(self.fittingGroupBox, 3, 0)
        self.layout.addWidget(forceGroupBox, 0, 0)
        self.layout.addWidget(miscGroupBox, 1, 0)
        self.layout.addWidget(buttonGroupBox, 2, 0)

        self.setLayout(self.layout)

        buttonVbox = QGridLayout()
        buttonGroupBox.setLayout(buttonVbox)
        buttonVbox.addWidget(self.updateBtn, 0, 0)
        buttonVbox.addWidget(self.okBtn, 0, 1)

        forceLayout = QGridLayout()
        forceGroupBox.setLayout(forceLayout)
        forceLayout.addWidget(roiChoiceLabel, 0, 0, 1, 1)
        forceLayout.addWidget(self.roiChoice, 0, 1, 1, 1)
        forceLayout.addWidget(dataChoiceLabel, 0, 2, 1, 1)
        forceLayout.addWidget(self.dataChoice, 0, 3, 1, 1)
        forceLayout.addWidget(self.zeroBtn, 1, 0, 1, 1)
        forceLayout.addWidget(self.zeroLabel, 1, 1, 1, 1)
        forceLayout.addWidget(self.forceBtn, 2, 0, 1, 1)
        forceLayout.addWidget(self.forceLabel, 2, 1, 1, 1)
        forceLayout.addWidget(self.preloadBtn, 3, 0, 1, 1)
        forceLayout.addWidget(self.preloadLabel, 3, 1, 1, 1)
        forceLayout.addWidget(self.filter, 1, 2, 1, 2)
        forceLayout.addWidget(windLabel, 2, 2, 1, 1)
        forceLayout.addWidget(self.filter_wind, 2, 3, 1, 1)
        forceLayout.addWidget(polyLabel, 3, 2, 1, 1)
        forceLayout.addWidget(self.filter_poly, 3, 3, 1, 1)
        forceLayout.addWidget(self.zero_subtract, 4, 2, 1, 2)
        forceLayout.addWidget(CTlabel, 4, 0, 1, 1)
        forceLayout.addWidget(self.crossTalk, 4, 1, 1, 1)
        
        miscLayout = QGridLayout()
        miscGroupBox.setLayout(miscLayout)
        miscLayout.addWidget(applyCrossTalk, 0, 0, 1, 2)
        miscLayout.addWidget(self.deformBtn, 1, 0, 1, 1)
        miscLayout.addWidget(self.deformLabel, 1, 1, 1, 1)
        miscLayout.addWidget(noiseStepsLabel, 0, 2, 1, 1)
        miscLayout.addWidget(noiseSteps, 0, 3, 1, 1)
        miscLayout.addWidget(kBeamLabel, 1, 2, 1, 1)
        miscLayout.addWidget(kBeam, 1, 3, 1, 1)
        miscLayout.addWidget(eqLabel, 2, 0, 1, 1) #remove
        miscLayout.addWidget(self.latCalibEq, 2, 1, 1, 1) #remove
        # miscLayout.addWidget(self.zeroShift, 2, 2, 1, 2) #remove
        
        
        # zeroVbox = QGridLayout()
        # self.zeroGroupBox.setLayout(zeroVbox)
        # zeroVbox.addWidget(self.zeroLabel, 0, 1, 1, 1)
        # zeroVbox.addWidget(self.adhLabel, 0, 2, 1, 1)
        # zeroVbox.addWidget(self.prl1Label, 0, 3, 1, 1)
        # zeroVbox.addWidget(self.startLabel, 1, 0, 1, 1)
        # zeroVbox.addWidget(self.endLabel, 2, 0, 1, 1)
        # zeroVbox.addWidget(self.zeroRange1, 1, 1, 1, 1)
        # zeroVbox.addWidget(self.zeroRange2, 2, 1, 1, 1)
        # zeroVbox.addWidget(self.adhRange1, 1, 2, 1, 1)
        # zeroVbox.addWidget(self.adhRange2, 2, 2, 1, 1)
        # zeroVbox.addWidget(self.prl1Range1, 1, 3, 1, 1)
        # zeroVbox.addWidget(self.prl1Range2, 2, 3, 1, 1)
        # zeroVbox.addWidget(self.vertCTlabel, 3, 0, 1, 1)
        # zeroVbox.addWidget(self.vertCrossTalk, 3, 1, 1, 1)

        # filterVbox = QGridLayout()
        # filterGroupBox.setLayout(filterVbox)
        # filterVbox.addWidget(self.filterLatF, 1, 0, 1, 2)
        # filterVbox.addWidget(self.windLabel, 2, 0, 1, 1)
        # filterVbox.addWidget(self.filter_wind, 2, 1, 1, 1)
        # filterVbox.addWidget(self.polyLabel, 3, 0, 1, 1)
        # filterVbox.addWidget(self.filter_poly, 3, 1, 1, 1)
        # # filterVbox.addWidget(self.fontLabel, 2, 2, 1, 1)
        # # filterVbox.addWidget(self.fontSize, 2, 3, 1, 1)
        # filterVbox.addWidget(self.eqLabel, 3, 2, 1, 1)
        # filterVbox.addWidget(self.latCalibEq, 3, 3, 1, 1)
        # # filterVbox.addWidget(self.invertLatForce, 0, 2, 1, 2)
        # filterVbox.addWidget(self.zeroShift, 0, 0, 1, 1)
        # filterVbox.addWidget(self.applyCrossTalk, 1, 2, 1, 2)
        # # filterVbox.addWidget(self.xAxisLabel, 0, 3, 1, 1)
        # # filterVbox.addWidget(self.xAxisParam, 1, 3, 1, 1)
        # filterVbox.addWidget(self.noiseStepsLabel, 4, 2, 1, 1)
        # filterVbox.addWidget(self.noiseSteps, 5, 2, 1, 1)
        # # filterVbox.addWidget(self.legendPosLabel, 4, 3, 1, 1)
        # # filterVbox.addWidget(self.legendPos, 5, 3, 1, 1)
        # # filterVbox.addWidget(self.startFullLabel, 4, 0, 1, 1)
        # # filterVbox.addWidget(self.endFullLabel, 5, 0, 1, 1)
        # # filterVbox.addWidget(self.startFull, 4, 1, 1, 1)
        # # filterVbox.addWidget(self.endFull, 5, 1, 1, 1)
        # filterVbox.addWidget(self.kBeamLabel, 6, 2, 1, 1)
        # filterVbox.addWidget(self.kBeam, 6, 3, 1, 1)
        # filterVbox.addWidget(self.deformStartLabel, 6, 0, 1, 1)
        # filterVbox.addWidget(self.deformStart, 6, 1, 1, 1)

        # flagVbox = QGridLayout()
        # flagGroupBox.setLayout(flagVbox)
        # flagVbox.addWidget(self.showContactArea, 0, 0)
        # flagVbox.addWidget(self.showROIArea, 0, 1)
        # flagVbox.addWidget(self.showZPiezo, 0, 2)
        # flagVbox.addWidget(self.showXPiezo, 1, 0)
        # flagVbox.addWidget(self.showAdhesion, 1, 1)
        # flagVbox.addWidget(self.showFriction, 1, 2)
        # flagVbox.addWidget(self.showLateralForce, 2, 0)
        # flagVbox.addWidget(self.showContactLength, 2, 1)
        # flagVbox.addWidget(self.showROILength, 2, 2)
        # flagVbox.addWidget(self.showContactNumber, 3, 0)
        # flagVbox.addWidget(self.showEcc, 3, 1)
        # flagVbox.addWidget(self.showStress, 3, 2)
        # flagVbox.addWidget(self.showDeformation, 4, 0)
        # flagVbox.addWidget(self.showTitle, 4, 1)
        # flagVbox.addWidget(self.showLegend2, 4, 2)

        # lastCalibVbox = QGridLayout()
        # self.latCalibGroupBox.setLayout(lastCalibVbox)
        # lastCalibVbox.addWidget(self.frLabel, 0, 1, 1, 1)
        # lastCalibVbox.addWidget(self.prl2Label, 0, 2, 1, 1)
        # lastCalibVbox.addWidget(self.zero2Label, 0, 3, 1, 1)
        # lastCalibVbox.addWidget(self.startLabel2, 1, 0, 1, 1)
        # lastCalibVbox.addWidget(self.frictionRange1, 1, 1, 1, 1)
        # lastCalibVbox.addWidget(self.endLabel2, 2, 0, 1, 1)
        # lastCalibVbox.addWidget(self.frictionRange2, 2, 1, 1, 1)
        # lastCalibVbox.addWidget(self.prl2Range1, 1, 2, 1, 1)
        # lastCalibVbox.addWidget(self.prl2Range2, 2, 2, 1, 1)
        # lastCalibVbox.addWidget(self.zero2Range1, 1, 3, 1, 1)
        # lastCalibVbox.addWidget(self.zero2Range2, 2, 3, 1, 1)
        # lastCalibVbox.addWidget(self.latCTlabel, 3, 0, 1, 1)
        # lastCalibVbox.addWidget(self.latCrossTalk, 3, 1, 1, 1)

        # fittingVbox = QGridLayout()
        # self.fittingGroupBox.setLayout(fittingVbox)
        # fittingVbox.addWidget(self.startFitLabel, 0, 0, 1, 1)
        # fittingVbox.addWidget(self.endFitLabel, 1, 0, 1, 1)
        # fittingVbox.addWidget(self.fitStart, 0, 1, 1, 1)
        # fittingVbox.addWidget(self.fitStop, 1, 1, 1, 1)
        # fittingVbox.addWidget(self.xFitLabel, 0, 2, 1, 1)
        # fittingVbox.addWidget(self.yFitLabel, 1, 2, 1, 1)
        # fittingVbox.addWidget(self.xFit, 0, 3, 1, 1)
        # fittingVbox.addWidget(self.yFit, 1, 3, 1, 1)
        # fittingVbox.addWidget(self.fitPosLabel, 0, 4, 1, 1)
        # fittingVbox.addWidget(self.fitPos, 0, 5, 1, 1)
        # fittingVbox.addWidget(self.showFitEq, 1, 4, 1, 2)

    def filter_change(self):
        if self.filter_wind.value() %2 == 0: #make sure its odd
            self.filter_wind.blockSignals(True)
            self.filter_wind.setValue(self.filter_wind.value() + 1)
            self.filter_wind.blockSignals(False)
        self.update_dict()

    # def update_range(self):
    #     key = self.roiChoice.currentText()
    #     if key not in self.rangeDict.keys():
    #         key = "Default"

    #     self.zeroRange1.blockSignals(True)
    #     self.zeroRange1.setValue(self.rangeDict[key][0][0])
    #     self.zeroRange1.blockSignals(False)
    #     self.zeroRange2.blockSignals(True)
    #     self.zeroRange2.setValue(self.rangeDict[key][0][1])
    #     self.zeroRange2.blockSignals(False)
    #     self.adhRange1.blockSignals(True)
    #     self.adhRange1.setValue(self.rangeDict[key][1][0])
    #     self.adhRange1.blockSignals(False)
    #     self.adhRange2.blockSignals(True)
    #     self.adhRange2.setValue(self.rangeDict[key][1][1])
    #     self.adhRange2.blockSignals(False)
    #     self.prl1Range1.blockSignals(True)
    #     self.prl1Range1.setValue(self.rangeDict[key][2][0])
    #     self.prl1Range1.blockSignals(False)
    #     self.prl1Range2.blockSignals(True)
    #     self.prl1Range2.setValue(self.rangeDict[key][2][1])
    #     self.prl1Range2.blockSignals(False)
    #     self.frictionRange1.blockSignals(True)
    #     self.frictionRange1.setValue(self.rangeDict[key][3][0])
    #     self.frictionRange1.blockSignals(False)
    #     self.frictionRange2.blockSignals(True)
    #     self.frictionRange2.setValue(self.rangeDict[key][3][1])
    #     self.frictionRange2.blockSignals(False)
    #     self.prl2Range1.blockSignals(True)
    #     self.prl2Range1.setValue(self.rangeDict[key][4][0])
    #     self.prl2Range1.blockSignals(False)
    #     self.prl2Range2.blockSignals(True)
    #     self.prl2Range2.setValue(self.rangeDict[key][4][1])
    #     self.prl2Range2.blockSignals(False)
    #     self.zero2Range1.blockSignals(True)
    #     self.zero2Range1.setValue(self.rangeDict[key][5][0])
    #     self.zero2Range1.blockSignals(False)
    #     self.zero2Range2.blockSignals(True)
    #     self.zero2Range2.setValue(self.rangeDict[key][5][1])
    #     self.zero2Range2.blockSignals(False)
    
    def update_widgets(self):
        self.forceBtn.setText(self.dataChoiceDict[self.dataChoice.currentText()] +
                       " Range")
        # range_dict = self.dataAnalDict['force settings'][self.roiChoice.currentText()][self.dataChoice.currentText()]
        range_dict = self.dataAnalDict[self.dataChoice.currentText()]["ranges"][self.roiChoice.currentText()]
        transform_dict = self.dataAnalDict[self.dataChoice.currentText()]["transform"]
        self.zeroLabel.blockSignals(True)
        self.zeroLabel.setText(range_dict["Zero"])
        self.zeroLabel.blockSignals(False)
        self.forceLabel.blockSignals(True)
        self.forceLabel.setText(range_dict["Force"])
        self.forceLabel.blockSignals(False)
        self.preloadLabel.blockSignals(True)
        self.preloadLabel.setText(range_dict["Preload"])
        self.preloadLabel.blockSignals(False)
        self.filter.blockSignals(True)
        self.filter.setChecked(transform_dict["Filter"])
        self.filter.blockSignals(False)
        self.filter_wind.blockSignals(True)
        self.filter_wind.setValue(transform_dict["Filter window"])
        self.filter_wind.blockSignals(False)
        self.filter_poly.blockSignals(True)
        self.filter_poly.setValue(transform_dict["Filter order"])
        self.filter_poly.blockSignals(False)
        self.zero_subtract.blockSignals(True)
        self.zero_subtract.setChecked(transform_dict["Zero subtract"])
        self.zero_subtract.blockSignals(False)
        self.crossTalk.blockSignals(True)
        self.crossTalk.setValue(transform_dict["Cross Talk"])
        self.crossTalk.blockSignals(False)
    
    def update_dict(self):
        # range_dict = self.dataAnalDict['force settings'][self.roiChoice.currentText()][self.dataChoice.currentText()]
        range_dict = self.dataAnalDict[self.dataChoice.currentText()]["ranges"][self.roiChoice.currentText()]
        transform_dict = self.dataAnalDict[self.dataChoice.currentText()]["transform"]
        range_dict["Zero"] = self.zeroLabel.text()
        range_dict["Force"] = self.forceLabel.text()
        range_dict["Preload"] = self.preloadLabel.text()
        transform_dict["Filter"] = self.filter.isChecked()
        transform_dict["Filter window"] = self.filter_wind.value()
        transform_dict["Filter order"] = self.filter_poly.value()
        transform_dict["Zero subtract"] = self.zero_subtract.isChecked()
        transform_dict["Cross Talk"] = self.crossTalk.value()
        # self.rangeDict[self.roiChoice.currentText()] = [[self.zeroRange1.value(),
        #                                                    self.zeroRange2.value()],
        #                                                 [self.adhRange1.value(),
        #                                                    self.adhRange2.value()],
        #                                                 [self.prl1Range1.value(),
        #                                                    self.prl1Range2.value()],
        #                                                 [self.frictionRange1.value(),
        #                                                    self.frictionRange2.value()],
        #                                                 [self.prl2Range1.value(),
        #                                                  self.prl2Range2.value()],
        #                                                 [self.zero2Range1.value(),
        #                                                    self.zero2Range2.value()]]
        print(self.dataAnalDict)
    def show_window(self): #show window
        # self.update_range()
        self.update_dict()
        self.show()
        