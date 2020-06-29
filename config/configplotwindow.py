# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:29:38 2020

@author: adwait
"""
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, \
     QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, \
     QGroupBox, QGridLayout, QWidget
     
# %% Configure Plot Window
class ConfigPlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 200)
        self.setWindowTitle("Configure Plot")
        self.layout = QGridLayout()
        self.home()
        self.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
                                       [0,100],[0,100],[0,1]]}

    def home(self):

        self.showContactArea = QCheckBox('contact area', self) #contact area
        self.showContactArea.setChecked(True)

        self.showROIArea = QCheckBox('ROI area', self) #roi area
        self.showContactLength = QCheckBox('contact length', self) #contact length
        self.showROILength = QCheckBox('ROI length', self) #roi length
        self.showContactNumber = QCheckBox('contact number', self) #contact number
        self.showEcc = QCheckBox('eccentricity', self) #median eccentricity

        self.showLateralForce = QCheckBox('lateral force', self) #lateral force
        self.showZPiezo = QCheckBox('vertical piezo', self) #z piezo
        self.showXPiezo = QCheckBox('lateral piezo', self) #x piezo
        self.showAdhesion = QCheckBox('adhesion calculation', self) #adhesion/preload calc line
        self.showFriction = QCheckBox('friction calculation', self) #friction calc lines
        self.showStress = QCheckBox('stress', self) #stress
        self.showDeformation = QCheckBox('deformation', self) #deformation

        self.xAxisLabel = QLabel("<b>X Axis:</b>", self)
        self.xAxisParam = QComboBox(self) #x axis parameter
        self.xAxisParam.addItem("Time (s)")
        self.xAxisParam.addItem("Vertical Position (μm)")
        self.xAxisParam.addItem("Lateral Position (μm)")
        self.xAxisParam.addItem("Deformation (μm)")
        
        self.roiChoice = QComboBox(self) #choose ROI
        self.roiChoice.addItem("Default")
        self.roiChoice.setCurrentIndex(0)
        self.roiChoice.currentIndexChanged.connect(self.update_range)
        
        self.startLabel = QLabel("Start (%):", self)
        self.endLabel = QLabel("End (%):", self)

        self.zeroLabel = QLabel("Zero Range", self)
        self.adhLabel = QLabel("Adhesion Range", self)
        self.prl1Label = QLabel("Preload Range", self)
        
        self.zeroRange1 = QDoubleSpinBox(self) #vertical force zero range start
        self.zeroRange1.setValue(0)
        self.zeroRange1.setSingleStep(1)
        self.zeroRange1.setRange(0, 100)
        self.zeroRange1.valueChanged.connect(self.update_dict)
        
        self.zeroRange2 = QDoubleSpinBox(self) #vertical force zero range end
        self.zeroRange2.setValue(1)
        self.zeroRange2.setSingleStep(1)
        self.zeroRange2.setRange(0, 100)
        self.zeroRange2.valueChanged.connect(self.update_dict)

        self.adhRange1 = QDoubleSpinBox(self) #adhesion peak range start
        self.adhRange1.setValue(0)
        self.adhRange1.setSingleStep(1)
        self.adhRange1.setRange(0, 100)
        self.adhRange1.valueChanged.connect(self.update_dict)

        self.adhRange2 = QDoubleSpinBox(self) #adhesion peak range start
        self.adhRange2.setValue(100)
        self.adhRange2.setSingleStep(1)
        self.adhRange2.setRange(0, 100)
        self.adhRange2.valueChanged.connect(self.update_dict)

        self.prl1Range1 = QDoubleSpinBox(self) #preload peak range start
        self.prl1Range1.setValue(0)
        self.prl1Range1.setSingleStep(1)
        self.prl1Range1.setRange(0, 100)
        self.prl1Range1.valueChanged.connect(self.update_dict)

        self.prl1Range2 = QDoubleSpinBox(self) #preload peak range start
        self.prl1Range2.setValue(100)
        self.prl1Range2.setSingleStep(1)
        self.prl1Range2.setRange(0, 100)
        self.prl1Range2.valueChanged.connect(self.update_dict)

        self.zero2Range1 = QDoubleSpinBox(self) #lateral force zero range start
        self.zero2Range1.setValue(0)
        self.zero2Range1.setSingleStep(1)
        self.zero2Range1.setRange(0, 100)
        self.zero2Range1.valueChanged.connect(self.update_dict)

        self.zero2Range2 = QDoubleSpinBox(self) #lateral force zero range end
        self.zero2Range2.setValue(1)
        self.zero2Range2.setSingleStep(1)
        self.zero2Range2.setRange(0, 100)
        self.zero2Range2.valueChanged.connect(self.update_dict)

        self.filterLatF = QCheckBox('Filter cyan curve', self) #filter
        
        self.filter_wind = QSpinBox(self) #filter window
        self.filter_wind.setValue(43)
        self.filter_wind.setSingleStep(20)
        self.filter_wind.setRange(3, 10001)
        self.filter_wind.valueChanged.connect(self.filter_change)
        self.windLabel = QLabel("Window Length:", self)
        
        self.filter_poly = QSpinBox(self) #filter polynom
        self.filter_poly.setValue(2)
        self.filter_poly.setSingleStep(1)
        self.filter_poly.setRange(1, 20000)
        self.polyLabel = QLabel("Polynomial Order:", self)

        self.startLabel2 = QLabel("Start (%):", self)
        self.endLabel2 = QLabel("End (%):", self)

        self.frLabel = QLabel("Friction Range", self)
        self.prl2Label = QLabel("Preload Range", self)
        self.zero2Label = QLabel("Zero Range", self)
        
        self.eqLabel = QLabel("Lateral Calib. Equation (μN):", self)        
        self.latCalibEq = QLineEdit(self) #lateral force calib equation
        self.latCalibEq.setText("29181.73*x")

        self.noiseStepsLabel = QLabel("Noisy Steps:", self)        
        self.noiseSteps = QLineEdit(self) #remove first data point from steps
        self.noiseSteps.setText("")

        self.legendPosLabel = QLabel("Legend:", self) #legend position        
        self.legendPos = QLineEdit(self)
        self.legendPos.setText("upper right")

        self.startFullLabel = QLabel("Start (%):", self)
        self.endFullLabel = QLabel("End (%):", self)

        self.startFull = QDoubleSpinBox(self) #plot range start
        self.startFull.setValue(0)
        self.startFull.setSingleStep(1)
        self.startFull.setRange(0, 100)

        self.endFull = QDoubleSpinBox(self) #plot range end
        self.endFull.setValue(100)
        self.endFull.setSingleStep(1)
        self.endFull.setRange(0, 100)
        
        self.invertLatForce = QCheckBox('Invert Lateral Force', self) #invert

        self.applyCrossTalk = QCheckBox('Apply Cross Talk', self) #cross talk flag
        self.zeroShift = QCheckBox('Shift to Zero', self) #force curve shift to zero

        self.vertCrossTalk = QDoubleSpinBox(self) #vertical cross talk slope
        self.vertCrossTalk.setValue(0)
        self.vertCrossTalk.setSingleStep(0.1)
        self.vertCrossTalk.setDecimals(4)
        self.vertCrossTalk.setRange(-1000, 1000)
        self.vertCTlabel = QLabel("Cross Talk (μN/μN):", self)

        self.latCrossTalk = QDoubleSpinBox(self) #lateral cross talk slope
        self.latCrossTalk.setValue(0)
        self.latCrossTalk.setSingleStep(0.1)
        self.latCrossTalk.setDecimals(4)
        self.latCrossTalk.setRange(-1000, 1000)
        self.latCTlabel = QLabel("Cross Talk (μN/μN):", self)

        self.frictionRange1 = QDoubleSpinBox(self) #friction range start
        self.frictionRange1.setValue(0)
        self.frictionRange1.setSingleStep(1)
        self.frictionRange1.setRange(0, 100)
        self.frictionRange1.valueChanged.connect(self.update_dict)
        
        self.frictionRange2 = QDoubleSpinBox(self) #friction range end
        self.frictionRange2.setValue(100)
        self.frictionRange2.setSingleStep(1)
        self.frictionRange2.setRange(0, 100)
        self.frictionRange2.valueChanged.connect(self.update_dict)

        self.prl2Range1 = QDoubleSpinBox(self) #friction preload peak range start
        self.prl2Range1.setValue(0)
        self.prl2Range1.setSingleStep(1)
        self.prl2Range1.setRange(0, 100)
        self.prl2Range1.valueChanged.connect(self.update_dict)

        self.prl2Range2 = QDoubleSpinBox(self) #friction preload peak range start
        self.prl2Range2.setValue(100)
        self.prl2Range2.setSingleStep(1)
        self.prl2Range2.setRange(0, 100)
        self.prl2Range2.valueChanged.connect(self.update_dict)

        self.startFitLabel = QLabel("Start (%):", self)
        self.endFitLabel = QLabel("End (%):", self)

        self.fitStart = QDoubleSpinBox(self) #fitting range start
        self.fitStart.setValue(0)
        self.fitStart.setSingleStep(1)
        self.fitStart.setRange(0, 100)

        self.fitStop = QDoubleSpinBox(self) #fitting range end
        self.fitStop.setValue(100)
        self.fitStop.setSingleStep(1)
        self.fitStop.setRange(0, 100)

        self.xFitLabel = QLabel("X Parameter:", self)
        self.yFitLabel = QLabel("Y Parameter:", self)

        self.xFit = QComboBox(self) #x param
        self.xFit.addItems(['Deformation (μm)',
                            'Vertical Position (μm)',
                            'Lateral Position (μm)',
                            'Time (s)'])
        self.xFit.setCurrentIndex(0)

        self.yFit = QComboBox(self) #x param
        self.yFit.addItems(['Vertical Force (μN)', 'Lateral Force (μN)'])
        self.yFit.setCurrentIndex(0)

        self.fitPosLabel = QLabel("Fit Position\n(x,y):", self) #fit eq. position        
        self.fitPos = QLineEdit(self)
        self.fitPos.setText('0.5,0.5')

        self.showFitEq = QCheckBox('Show Slope', self) #display equation on plot
        
        self.kBeamLabel = QLabel("Beam Spring Constant (μN/μm):", self) #beam dpring constant       
        self.kBeam = QLineEdit(self)
        self.kBeam.setText('30,1')

        self.deformStartLabel = QLabel("Deformation Start:", self) #contact start tolerance auto detect
        self.deformStart = QSpinBox(self) 
        self.deformStart.setValue(100)
        self.deformStart.setSingleStep(1)
        self.deformStart.setRange(0, 10000)
        
        self.okBtn = QPushButton("OK", self) #Close window

        self.updateBtn = QPushButton("Update", self) #Update
        
        self.zeroGroupBox = QGroupBox("Configure Vertical Force")
        filterGroupBox = QGroupBox("Configure Plot")
        flagGroupBox = QGroupBox("Show")
        self.latCalibGroupBox = QGroupBox("Configure Lateral Force")
        self.fittingGroupBox = QGroupBox("Fit Data")
        buttonGroupBox = QGroupBox()

        self.zeroGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        filterGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        flagGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.latCalibGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.fittingGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.fittingGroupBox.setCheckable(True)
        self.fittingGroupBox.setChecked(False)

        self.layout.addWidget(self.roiChoice, 0, 0, 1, 2)
        self.layout.addWidget(self.zeroGroupBox, 1, 0)
        self.layout.addWidget(filterGroupBox, 2, 1)
        self.layout.addWidget(flagGroupBox, 2, 0)
        self.layout.addWidget(self.latCalibGroupBox, 1, 1)
        self.layout.addWidget(self.fittingGroupBox, 3, 0)
        self.layout.addWidget(buttonGroupBox, 3, 1)

        self.setLayout(self.layout)

        buttonVbox = QGridLayout()
        buttonGroupBox.setLayout(buttonVbox)
        buttonVbox.addWidget(self.updateBtn, 0, 0)
        buttonVbox.addWidget(self.okBtn, 0, 1)
        
        zeroVbox = QGridLayout()
        self.zeroGroupBox.setLayout(zeroVbox)
        zeroVbox.addWidget(self.zeroLabel, 0, 1, 1, 1)
        zeroVbox.addWidget(self.adhLabel, 0, 2, 1, 1)
        zeroVbox.addWidget(self.prl1Label, 0, 3, 1, 1)
        zeroVbox.addWidget(self.startLabel, 1, 0, 1, 1)
        zeroVbox.addWidget(self.endLabel, 2, 0, 1, 1)
        zeroVbox.addWidget(self.zeroRange1, 1, 1, 1, 1)
        zeroVbox.addWidget(self.zeroRange2, 2, 1, 1, 1)
        zeroVbox.addWidget(self.adhRange1, 1, 2, 1, 1)
        zeroVbox.addWidget(self.adhRange2, 2, 2, 1, 1)
        zeroVbox.addWidget(self.prl1Range1, 1, 3, 1, 1)
        zeroVbox.addWidget(self.prl1Range2, 2, 3, 1, 1)
        zeroVbox.addWidget(self.vertCTlabel, 3, 0, 1, 1)
        zeroVbox.addWidget(self.vertCrossTalk, 3, 1, 1, 1)

        filterVbox = QGridLayout()
        filterGroupBox.setLayout(filterVbox)
        filterVbox.addWidget(self.filterLatF, 1, 0, 1, 2)
        filterVbox.addWidget(self.windLabel, 2, 0, 1, 1)
        filterVbox.addWidget(self.filter_wind, 2, 1, 1, 1)
        filterVbox.addWidget(self.polyLabel, 3, 0, 1, 1)
        filterVbox.addWidget(self.filter_poly, 3, 1, 1, 1)
        filterVbox.addWidget(self.eqLabel, 2, 2, 1, 2)
        filterVbox.addWidget(self.latCalibEq, 3, 2, 1, 2)
        filterVbox.addWidget(self.invertLatForce, 0, 2, 1, 2)
        filterVbox.addWidget(self.zeroShift, 0, 0, 1, 1)
        filterVbox.addWidget(self.applyCrossTalk, 1, 2, 1, 2)
        filterVbox.addWidget(self.xAxisLabel, 0, 3, 1, 1)
        filterVbox.addWidget(self.xAxisParam, 1, 3, 1, 1)
        filterVbox.addWidget(self.noiseStepsLabel, 4, 2, 1, 1)
        filterVbox.addWidget(self.noiseSteps, 5, 2, 1, 1)
        filterVbox.addWidget(self.legendPosLabel, 4, 3, 1, 1)
        filterVbox.addWidget(self.legendPos, 5, 3, 1, 1)
        filterVbox.addWidget(self.startFullLabel, 4, 0, 1, 1)
        filterVbox.addWidget(self.endFullLabel, 5, 0, 1, 1)
        filterVbox.addWidget(self.startFull, 4, 1, 1, 1)
        filterVbox.addWidget(self.endFull, 5, 1, 1, 1)
        filterVbox.addWidget(self.kBeamLabel, 6, 2, 1, 1)
        filterVbox.addWidget(self.kBeam, 6, 3, 1, 1)
        filterVbox.addWidget(self.deformStartLabel, 6, 0, 1, 1)
        filterVbox.addWidget(self.deformStart, 6, 1, 1, 1)

        flagVbox = QGridLayout()
        flagGroupBox.setLayout(flagVbox)
        flagVbox.addWidget(self.showContactArea, 0, 0)
        flagVbox.addWidget(self.showROIArea, 0, 1)
        flagVbox.addWidget(self.showZPiezo, 0, 2)
        flagVbox.addWidget(self.showXPiezo, 1, 0)
        flagVbox.addWidget(self.showAdhesion, 1, 1)
        flagVbox.addWidget(self.showFriction, 1, 2)
        flagVbox.addWidget(self.showLateralForce, 2, 0)
        flagVbox.addWidget(self.showContactLength, 2, 1)
        flagVbox.addWidget(self.showROILength, 2, 2)
        flagVbox.addWidget(self.showContactNumber, 3, 0)
        flagVbox.addWidget(self.showEcc, 3, 1)
        flagVbox.addWidget(self.showStress, 3, 2)
        flagVbox.addWidget(self.showDeformation, 4, 0)

        lastCalibVbox = QGridLayout()
        self.latCalibGroupBox.setLayout(lastCalibVbox)
        lastCalibVbox.addWidget(self.frLabel, 0, 1, 1, 1)
        lastCalibVbox.addWidget(self.prl2Label, 0, 2, 1, 1)
        lastCalibVbox.addWidget(self.zero2Label, 0, 3, 1, 1)
        lastCalibVbox.addWidget(self.startLabel2, 1, 0, 1, 1)
        lastCalibVbox.addWidget(self.frictionRange1, 1, 1, 1, 1)
        lastCalibVbox.addWidget(self.endLabel2, 2, 0, 1, 1)
        lastCalibVbox.addWidget(self.frictionRange2, 2, 1, 1, 1)
        lastCalibVbox.addWidget(self.prl2Range1, 1, 2, 1, 1)
        lastCalibVbox.addWidget(self.prl2Range2, 2, 2, 1, 1)
        lastCalibVbox.addWidget(self.zero2Range1, 1, 3, 1, 1)
        lastCalibVbox.addWidget(self.zero2Range2, 2, 3, 1, 1)
        lastCalibVbox.addWidget(self.latCTlabel, 3, 0, 1, 1)
        lastCalibVbox.addWidget(self.latCrossTalk, 3, 1, 1, 1)

        fittingVbox = QGridLayout()
        self.fittingGroupBox.setLayout(fittingVbox)
        fittingVbox.addWidget(self.startFitLabel, 0, 0, 1, 1)
        fittingVbox.addWidget(self.endFitLabel, 1, 0, 1, 1)
        fittingVbox.addWidget(self.fitStart, 0, 1, 1, 1)
        fittingVbox.addWidget(self.fitStop, 1, 1, 1, 1)
        fittingVbox.addWidget(self.xFitLabel, 0, 2, 1, 1)
        fittingVbox.addWidget(self.yFitLabel, 1, 2, 1, 1)
        fittingVbox.addWidget(self.xFit, 0, 3, 1, 1)
        fittingVbox.addWidget(self.yFit, 1, 3, 1, 1)
        fittingVbox.addWidget(self.fitPosLabel, 0, 4, 1, 1)
        fittingVbox.addWidget(self.fitPos, 0, 5, 1, 1)
        fittingVbox.addWidget(self.showFitEq, 1, 4, 1, 2)

    def filter_change(self):
        if self.filter_wind.value() %2 == 0: #make sure its odd
            self.filter_wind.blockSignals(True)
            self.filter_wind.setValue(self.filter_wind.value() + 1)
            self.filter_wind.blockSignals(False)

    def update_range(self):
        key = self.roiChoice.currentText()
        if key not in self.rangeDict.keys():
            key = "Default"

        self.zeroRange1.blockSignals(True)
        self.zeroRange1.setValue(self.rangeDict[key][0][0])
        self.zeroRange1.blockSignals(False)
        self.zeroRange2.blockSignals(True)
        self.zeroRange2.setValue(self.rangeDict[key][0][1])
        self.zeroRange2.blockSignals(False)
        self.adhRange1.blockSignals(True)
        self.adhRange1.setValue(self.rangeDict[key][1][0])
        self.adhRange1.blockSignals(False)
        self.adhRange2.blockSignals(True)
        self.adhRange2.setValue(self.rangeDict[key][1][1])
        self.adhRange2.blockSignals(False)
        self.prl1Range1.blockSignals(True)
        self.prl1Range1.setValue(self.rangeDict[key][2][0])
        self.prl1Range1.blockSignals(False)
        self.prl1Range2.blockSignals(True)
        self.prl1Range2.setValue(self.rangeDict[key][2][1])
        self.prl1Range2.blockSignals(False)
        self.frictionRange1.blockSignals(True)
        self.frictionRange1.setValue(self.rangeDict[key][3][0])
        self.frictionRange1.blockSignals(False)
        self.frictionRange2.blockSignals(True)
        self.frictionRange2.setValue(self.rangeDict[key][3][1])
        self.frictionRange2.blockSignals(False)
        self.prl2Range1.blockSignals(True)
        self.prl2Range1.setValue(self.rangeDict[key][4][0])
        self.prl2Range1.blockSignals(False)
        self.prl2Range2.blockSignals(True)
        self.prl2Range2.setValue(self.rangeDict[key][4][1])
        self.prl2Range2.blockSignals(False)
        self.zero2Range1.blockSignals(True)
        self.zero2Range1.setValue(self.rangeDict[key][5][0])
        self.zero2Range1.blockSignals(False)
        self.zero2Range2.blockSignals(True)
        self.zero2Range2.setValue(self.rangeDict[key][5][1])
        self.zero2Range2.blockSignals(False)

    def update_dict(self):
        self.rangeDict[self.roiChoice.currentText()] = [[self.zeroRange1.value(),
                                                           self.zeroRange2.value()],
                                                        [self.adhRange1.value(),
                                                           self.adhRange2.value()],
                                                        [self.prl1Range1.value(),
                                                           self.prl1Range2.value()],
                                                        [self.frictionRange1.value(),
                                                           self.frictionRange2.value()],
                                                        [self.prl2Range1.value(),
                                                         self.prl2Range2.value()],
                                                        [self.zero2Range1.value(),
                                                           self.zero2Range2.value()]]
    def show_window(self): #show window
        self.update_dict()
        self.show()