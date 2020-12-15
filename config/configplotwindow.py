# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:29:38 2020

@author: adwait
"""
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, \
     QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, \
     QGroupBox, QGridLayout, QWidget, QColorDialog
from PyQt5.QtGui import QColor
     
# %% Configure Plot Window
class ConfigPlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.Window)
        self.setGeometry(100, 100, 900, 200)
        self.setWindowTitle("Configure Plot")
        self.layout = QGridLayout()
        
        # self.rangeDict = {"Default" : [[0,1],[0,100],[0,100],
        #                                [0,100],[0,100],[0,1]]}

        """self.plotDict defination rule. value can be a widget
        source -->> 'datafile', 'image'
                source: { category: {'combine': widget,
                                      'curves': { curve: {'show': widget,
                                                        'color': tuple,
                                                        'color button': widget,
                                                        'line style': widget,
                                                        'marker': widget,
                                                        'invert': widget,
                                                        'position': widget,
                                                        'shift': widget,
                                                        'y bounds': widget}
                                                 }
                                    }
                         }
                'extras': {curve: widget},
                'plot settings': {'x axis': widget,
                                  'font size': widget,
                                  'plot range': widget,
                                  ...}
        """        
        self.plotDict = {}
        self.plotDict['datafile'] = {}
        self.plotDict['image'] = {}
        self.plotDict['extras'] = {}
        self.plotDict['plot settings'] = {}
        
        self.home()

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
        showTitle = QCheckBox('Show title', self) #plt title
        showTitle.setChecked(True)
        showLegend2 = QCheckBox('Show step legend', self) #region legend
        showLegend2.setChecked(True)
        self.fixYBound = QCheckBox('Fix Y Bounds', self) #fix Y axis
        self.fixYBound.setChecked(True)
        zeroShiftY = QCheckBox('Zero shift Y', self) #shift Y axis to zero
        zeroShiftY.setChecked(False)
        self.setYBounds = QPushButton("Update Y Bounds", self) #set y bounds from current figure
        
        # #used for settings save
        # self.showWidgets = [self.showContactArea, self.showROIArea, self.showZPiezo, 
        #                     self.showXPiezo, self.showAdhesion, self.showFriction,
        #                     self.showLateralForce, self.showContactLength, self.showROILength,
        #                     self.showContactNumber, self.showEcc, self.showStress,
        #                     self.showDeformation, self.showTitle, self.showLegend2]
        
        plotStyleLabel = QLabel("Style", self) #plot style
        plotStyle = QComboBox(self) 
        styleList = ['default','bmh','classic','dark_background','fast','fivethirtyeight',
                     'ggplot','grayscale','seaborn-bright','seaborn-colorblind','seaborn-dark-palette',
                     'seaborn-dark','seaborn-darkgrid','seaborn-deep','seaborn-muted','seaborn-notebook',
                     'seaborn-paper','seaborn-pastel','seaborn-poster','seaborn-talk','seaborn-ticks',
                     'seaborn-white','seaborn-whitegrid','seaborn','Solarize_Light2','tableau-colorblind10',
                     '_classic_test']
        plotStyle.addItems(styleList)
        
        xAxisLabel = QLabel("<b>X Axis:</b>", self)
        xAxisParam = QComboBox(self) #x axis parameter
        xParams = ["Index", "Time", "Vertical piezo", "Lateral piezo", 
                   "Deformation", "Vertical force", "Lateral force"]
        xAxisParam.addItems(xParams)
        xAxisParam.setCurrentIndex(1)

        
        fontLabel = QLabel("Font Size:", self)
        fontSize = QDoubleSpinBox(self)
        fontSize.setValue(12)
        fontSize.setSingleStep(1)
        fontSize.setRange(1, 99)
        
        lineLabel = QLabel("Line Width:", self)
        lineWidth = QDoubleSpinBox(self)
        lineWidth.setValue(1)
        lineWidth.setSingleStep(1)
        lineWidth.setRange(1, 99)

        markerLabel = QLabel("Marker Size:", self)
        markerSize = QDoubleSpinBox(self)
        markerSize.setValue(1)
        markerSize.setSingleStep(1)
        markerSize.setRange(1, 99)
        
        opacityLabel = QLabel("Opacity:", self)
        opacity = QDoubleSpinBox(self)
        opacity.setValue(0.5)
        opacity.setSingleStep(0.1)
        opacity.setRange(0, 1)
        
        self.plotRangeButton = QPushButton("Plot Range", self) #plot range select
        plotRangeLabel= QLineEdit(self) #plot range select
        plotRangeLabel.setReadOnly(True)
        # self.plotRangeLabel.textChanged.connect(self.updateRange)
        plotRangeLabel.setText("0,1")
        self.plotDict['plot settings']['plot range'] = plotRangeLabel
        
        
        # self.roiChoice = QComboBox(self) #choose ROI #REMOVE!!!
        # self.roiChoice.addItem("Default")
        # self.roiChoice.setCurrentIndex(0)
        # self.roiChoice.currentIndexChanged.connect(self.update_range)
        
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
        
        # self.filter_wind = QSpinBox(self) #filter window
        # self.filter_wind.setValue(43)
        # self.filter_wind.setSingleStep(20)
        # self.filter_wind.setRange(3, 10001)
        # self.filter_wind.valueChanged.connect(self.filter_change)
        # self.windLabel = QLabel("Window Length:", self)
        
        # self.filter_poly = QSpinBox(self) #filter polynom
        # self.filter_poly.setValue(2)
        # self.filter_poly.setSingleStep(1)
        # self.filter_poly.setRange(1, 20000)
        # self.polyLabel = QLabel("Polynomial Order:", self)

        # self.startLabel2 = QLabel("Start (%):", self)
        # self.endLabel2 = QLabel("End (%):", self)

        # self.frLabel = QLabel("Friction Range", self)
        # self.prl2Label = QLabel("Preload Range", self)
        # self.zero2Label = QLabel("Zero Range", self)
        
        # self.eqLabel = QLabel("Lateral Calib. Equation (μN):", self)        
        # self.latCalibEq = QLineEdit(self) #lateral force calib equation
        # self.latCalibEq.setText("29181.73*x")

        # self.noiseStepsLabel = QLabel("Noisy Steps:", self)        
        # self.noiseSteps = QLineEdit(self) #remove first data point from steps
        # self.noiseSteps.setText("")

        legendPosLabel = QLabel("Legend:", self) #legend position        
        legendPos = QLineEdit(self)
        legendPos.setText("upper right")

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

        # self.applyCrossTalk = QCheckBox('Apply Cross Talk', self) #cross talk flag
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

        # self.startFitLabel = QLabel("Start (%):", self)
        # self.endFitLabel = QLabel("End (%):", self)

        # self.fitStart = QDoubleSpinBox(self) #fitting range start
        # self.fitStart.setValue(0)
        # self.fitStart.setSingleStep(1)
        # self.fitStart.setRange(0, 100)

        # self.fitStop = QDoubleSpinBox(self) #fitting range end
        # self.fitStop.setValue(100)
        # self.fitStop.setSingleStep(1)
        # self.fitStop.setRange(0, 100)

        # self.xFitLabel = QLabel("X Parameter:", self)
        # self.yFitLabel = QLabel("Y Parameter:", self)

        # self.xFit = QComboBox(self) #x param
        # self.xFit.addItems(['Deformation (μm)',
        #                     'Vertical Position (μm)',
        #                     'Lateral Position (μm)',
        #                     'Time (s)'])
        # self.xFit.setCurrentIndex(0)

        # self.yFit = QComboBox(self) #x param
        # self.yFit.addItems(['Vertical Force (μN)', 'Lateral Force (μN)'])
        # self.yFit.setCurrentIndex(0)

        # self.fitPosLabel = QLabel("Fit Position\n(x,y):", self) #fit eq. position        
        # self.fitPos = QLineEdit(self)
        # self.fitPos.setText('0.5,0.5')

        # self.showFitEq = QCheckBox('Show Slope', self) #display equation on plot
        
        # self.kBeamLabel = QLabel("Beam Spring Constant (μN/μm):", self) #beam dpring constant       
        # self.kBeam = QLineEdit(self)
        # self.kBeam.setText('30,1')

        # self.deformStartLabel = QLabel("Deformation Start:", self) #contact start tolerance auto detect
        # self.deformStart = QSpinBox(self) 
        # self.deformStart.setValue(100)
        # self.deformStart.setSingleStep(1)
        # self.deformStart.setRange(0, 10000)
     
        self.okBtn = QPushButton("OK", self) #Close window

        self.updateBtn = QPushButton("Update", self) #Update
       

        
        
        forceGroupBox = QGroupBox("Datafile Curves")
        forceGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        forceLayout = QGridLayout()
        forceGroupBox.setLayout(forceLayout)
        self.designLayoutTitles(forceLayout, style = True, y_bound = False)
        self.designLayout(forceLayout, 1, "datafile", "Force", False, "Vertical force", True, 
                          (255,0,0), "-", "", False, 'left', 0, None, 2)
        self.designLayout(forceLayout, 2, "datafile", "Force", None, "Lateral force", False, 
                          (0,255,255), "", "o", False, 'left', 6, None, 2)
        self.designLayout(forceLayout, 3, "datafile", "Displacement", True, "Vertical piezo", False, 
                          (255,0,255), "-", "", False, 'right', 6, None, 3)
        self.designLayout(forceLayout, 4, "datafile", "Displacement", None, "Lateral piezo", False, 
                          (255,0,255), "-.", "", False, 'right', 6, None, 3)
        self.designLayout(forceLayout, 5, "datafile", "Displacement", None, "Deformation", False, 
                          (255,0,255), "-", "o", False, 'right', 6, None, 3)
        
        imageGroupBox = QGroupBox("Image Curves")
        imageGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        imageLayout = QGridLayout()
        imageGroupBox.setLayout(imageLayout)
        self.designLayoutTitles(imageLayout, style = False, y_bound = True)
        self.designLayout(imageLayout, 1, "image", "Area", True, "Contact area", True, 
                          'Greens', None, None, False, 'right', 0, '50000,80000', 2)
        self.designLayout(imageLayout, 2, "image", "Area", None, "ROI area", False, 
                          'Blues', None, None, False, 'right', 0, '30000,50000', 2)
        self.designLayout(imageLayout, 3, "image", "Length", True, "Contact length", False, 
                          'Oranges', None, None, False, 'right', 0, '30000,50000', 2)
        self.designLayout(imageLayout, 4, "image", "Length", None, "ROI length", False, 
                          'Purples', None, None, False, 'right', 0, '30000,50000', 2)
        self.designLayout(imageLayout, 5, "image", "Number", True, "Contact number", False, 
                          'Oranges', None, None, False, 'right', 0, '30000,50000', 1)
        self.designLayout(imageLayout, 6, "image", "Eccentricity", True, "Eccentricity", False, 
                          'Oranges', None, None, False, 'right', 0, '30000,50000', 1)
        
        
        mixedGroupBox = QGroupBox("Extras")
        mixedGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        mixedLayout = QGridLayout()
        mixedGroupBox.setLayout(mixedLayout)
        showCurve = QLabel("Show")
        mixedLayout.addWidget(showCurve, 0, 1, 1, 1)
        # self.designLayoutTitles(mixedLayout, y_bound = True)
        self.designLayout(mixedLayout, 1, "extras", None, None, "Stress", False)
        self.designLayout(mixedLayout, 2, "extras", None, None, "Adhesion", False)
        self.designLayout(mixedLayout, 3, "extras", None, None, "Friction", False)
        self.designLayout(mixedLayout, 4, "extras", None, None, "Steps", False)
        self.designLayout(mixedLayout, 5, "extras", None, None, "Fit", False)
        
        plotGroupBox = QGroupBox("Plot Settings")
        plotGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        plotLayout = QGridLayout()
        plotGroupBox.setLayout(plotLayout)
        # showLabel = QLabel("Show")
        # plotLayout.addWidget(showLabel, 0, 1, 1, 1)
        # self.designLayout(plotLayout, 1, None, None, "Title", False)
        # self.designLayout(plotLayout, 2, None, None, "Legend2", False)
        plotLayout.addWidget(showTitle, 0, 2, 1, 1)        
        plotLayout.addWidget(showLegend2, 1, 2, 1, 1)
        plotLayout.addWidget(zeroShiftY, 2, 2, 1, 1)
        plotLayout.addWidget(self.fixYBound, 3, 2, 1, 1)
        plotLayout.addWidget(self.setYBounds, 4, 2, 1, 1)
        plotLayout.addWidget(xAxisLabel, 0, 0, 1, 1)
        plotLayout.addWidget(xAxisParam, 0, 1, 1, 1)
        plotLayout.addWidget(fontLabel, 2, 0, 1, 1)
        plotLayout.addWidget(fontSize, 2, 1, 1, 1)
        plotLayout.addWidget(lineLabel, 3, 0, 1, 1)
        plotLayout.addWidget(lineWidth, 3, 1, 1, 1)
        plotLayout.addWidget(markerLabel, 4, 0, 1, 1)
        plotLayout.addWidget(markerSize, 4, 1, 1, 1)
        plotLayout.addWidget(opacityLabel, 5, 0, 1, 1)
        plotLayout.addWidget(opacity, 5, 1, 1, 1)
        plotLayout.addWidget(legendPosLabel, 6, 0, 1, 1)
        plotLayout.addWidget(legendPos, 6, 1, 1, 1)
        plotLayout.addWidget(plotStyleLabel, 7, 0, 1, 1)
        plotLayout.addWidget(plotStyle, 7, 1, 1, 1)           
        plotLayout.addWidget(self.plotRangeButton, 1, 0, 1, 1)
        plotLayout.addWidget(plotRangeLabel, 1, 1, 1, 1)
                           
        # self.zeroGroupBox = QGroupBox("Configure Vertical Force")
        # filterGroupBox = QGroupBox("Configure Plot")
        # flagGroupBox = QGroupBox("Show")
        # self.latCalibGroupBox = QGroupBox("Configure Lateral Force")
        # self.fittingGroupBox = QGroupBox("Fit Data")
        buttonGroupBox = QGroupBox()
        
        
        self.plotDict['plot settings']['x axis'] = xAxisParam
        self.plotDict['plot settings']['style'] = plotStyle
        self.plotDict['plot settings']['font size'] = fontSize
        self.plotDict['plot settings']['line width'] = lineWidth
        self.plotDict['plot settings']['marker size'] = markerSize
        self.plotDict['plot settings']['opacity'] = opacity
        self.plotDict['plot settings']['legend position'] = legendPos
        self.plotDict['plot settings']['show title'] = showTitle
        self.plotDict['plot settings']['show step legend'] = showLegend2
        self.plotDict['plot settings']['fix y bounds'] = self.fixYBound
        self.plotDict['plot settings']['zero shift Y'] = zeroShiftY
        # self.plotDict['plot settings']['plot range'] = slice(0,1) #CHECK!!
        
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
        self.layout.addWidget(imageGroupBox, 1, 0)
        self.layout.addWidget(mixedGroupBox, 0, 1)
        self.layout.addWidget(plotGroupBox, 1, 1)
        self.layout.addWidget(buttonGroupBox, 2, 0, 1, 2)

        self.setLayout(self.layout)

        buttonVbox = QGridLayout()
        buttonGroupBox.setLayout(buttonVbox)
        buttonVbox.addWidget(self.updateBtn, 0, 0)
        buttonVbox.addWidget(self.okBtn, 0, 1)
        
        # print(self.plotDict)
    #axis_combine = None means it wont draw xategory and combine widgets
    def designLayout(self, layout, row, source, category, combine, curve, show,  
                     color = None, line_style = None, marker = None, axis_inv = None,
                      axis_pos = None, axis_shift = None, y_bound = None, 
                      axis_combine = None):
        widgetDict = {}
        if combine != None:
            categoryLabel = QLabel(category)
            layout.addWidget(categoryLabel, row, 0, axis_combine, 1)
            combineCurve = QCheckBox()
            combineCurve.setChecked(combine)
            combineCurve.stateChanged.connect(lambda: self.disableAxisSettings(source, 
                                                                               category))
            layout.addWidget(combineCurve, row, 1, axis_combine, 1)
            self.plotDict[source][category] = {}
            self.plotDict[source][category]['combine'] = combineCurve
            self.plotDict[source][category]['curves'] = {}
                                    
        if axis_combine == None:
            pos = 0
        else:
            pos = 2
            
        curveLabel = QLabel(curve)
        layout.addWidget(curveLabel, row, pos, 1, 1)
        pos += 1
        showCurve = QCheckBox()
        showCurve.setChecked(show)
        layout.addWidget(showCurve, row, pos, 1, 1)
        pos += 1
        widgetDict['show'] = showCurve
        
        #case of extra plots
        if source ==  "extras":
            self.plotDict[source][curve] = showCurve
        
        if color != None:
            if source in ['datafile', 'extras']:
                colorWidget = QPushButton()
                colorVal = QColor(*color)
                colorWidget.setStyleSheet("QPushButton {background-color: %s}"
                                       % colorVal.name()) #set background color
                widgetDict['color'] = tuple([x/255 for x in color])
                widgetDict['color button'] = colorWidget #stored to update bg later
                
                colorWidget.clicked.connect(lambda: self.colorPicker(colorWidget, 
                                                                     source,
                                                                     category, 
                                                                     curve))
                
                # colorlist = ['black','blue','brown','cyan','green','grey',
                #              'magenta','orange','purple','red','violet','yellow']                
            elif source == 'image': #colormaps                
                colorlist = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
                colorWidget = QComboBox()
                colorWidget.addItems(colorlist)
                colorWidget.setCurrentIndex(colorWidget.findText(color))
                widgetDict['color'] = colorWidget
                
            layout.addWidget(colorWidget, row, pos, 1, 1)
            pos += 1
            
        if line_style != None:              
            linelist = ["", ":", "-.", "--", "-", ":", "-.", "--", "-", ":", "-."]
            lineWidget = QComboBox()
            lineWidget.addItems(linelist)
            lineWidget.setCurrentIndex(lineWidget.findText(line_style))
            layout.addWidget(lineWidget, row, pos, 1, 1)
            pos += 1
            widgetDict['line style'] = lineWidget
        if marker != None:              
            markerlist = ["", "o", "v", "^", "s", "P", "*", "D", "<", "X", ">"]
            markerWidget = QComboBox()
            markerWidget.addItems(markerlist)
            markerWidget.setCurrentIndex(markerWidget.findText(marker))
            layout.addWidget(markerWidget, row, pos, 1, 1)
            pos += 1
            widgetDict['marker'] = markerWidget
        if axis_inv != None:
            axisInvert = QCheckBox()
            axisInvert.setChecked(axis_inv)
            layout.addWidget(axisInvert, row, pos, 1, 1)
            pos += 1
            widgetDict['invert'] = axisInvert
        if axis_pos != None:
            axisPosition = QComboBox()
            axisPosition.addItems(["left", "right"])
            axisPosition.setCurrentIndex(axisPosition.findText(axis_pos))
            layout.addWidget(axisPosition, row, pos, 1, 1)
            pos += 1
            widgetDict['position'] = axisPosition
        if axis_shift != None:
            axisShift = QSpinBox() 
            axisShift.setSingleStep(1)
            axisShift.setRange(0, 99)
            axisShift.setValue(axis_shift)
            layout.addWidget(axisShift, row, pos, 1, 1)
            pos += 1
            widgetDict['shift'] = axisShift
        if y_bound != None:
            yBound = QLineEdit()
            yBound.setText(y_bound)
            layout.addWidget(yBound, row, pos, 1, 1)
            pos += 1
            widgetDict['y bounds'] = yBound
        
        if category != None:
            self.plotDict[source][category]['curves'][curve] = widgetDict
            self.disableAxisSettings(source, category)
    
    def designLayoutTitles(self, layout, style = False, y_bound = False):
        categoryLabel = QLabel("Category")
        layout.addWidget(categoryLabel, 0, 0, 1, 1)
        combineLabel = QLabel("Combine")
        layout.addWidget(combineLabel, 0, 1, 1, 1)
        curveyLabel = QLabel("Curve")
        layout.addWidget(curveyLabel, 0, 2, 1, 1)
        showLabel = QLabel("Show")
        layout.addWidget(showLabel, 0, 3, 1, 1)
        colorLabel = QLabel("Color")
        layout.addWidget(colorLabel, 0, 4, 1, 1)
        pos = 5
        if style == True:
            lineLabel = QLabel("Line Style")
            layout.addWidget(lineLabel, 0, pos, 1, 1)
            pos += 1
            markerLabel = QLabel("Marker")
            layout.addWidget(markerLabel, 0, pos, 1, 1)
            pos += 1
            
        invertLabel = QLabel("Invert")
        layout.addWidget(invertLabel, 0, pos, 1, 1)
        pos += 1
        axposLabel = QLabel("Axis Position")
        layout.addWidget(axposLabel, 0, pos, 1, 1)
        pos += 1
        axshiftLabel = QLabel("Axis Shift")
        layout.addWidget(axshiftLabel, 0, pos, 1, 1)
        pos += 1
        if y_bound == True:
            yboundLabel = QLabel("Y Bounds")
            layout.addWidget(yboundLabel, 0, pos, 1, 1)
            pos += 1

    
    def disableAxisSettings(self, source, category):
        # print(category)
        state = not self.plotDict[source][category]['combine'].isChecked()
        curves = list(self.plotDict[source][category]['curves'].keys())[1:]
        for curve in curves:
            keys =  self.plotDict[source][category]['curves'][curve].keys()
            ax_property = ['invert', 'position', 'shift', 'y bounds']
            for prop in ax_property:   
                if prop in keys:
                    self.plotDict[source][category]['curves'][curve][prop].setEnabled(state)

    # def updateRange(self):
    #     cursor_pos = self.plotRangeLabel.text().split(',')
    #     self.plotDict['plot settings']['plot range'] = slice(int(cursor_pos[0]),
    #                                                          int(cursor_pos[1])+1)

    def colorPicker(self, button, source, category, curve): #color picker dialog
        
        color = QColorDialog.getColor()
        color_tuple = tuple([x/255 for x in color.getRgb()])
        self.updateColor(color_tuple, button, source, category, curve)
    
    #update color button and dictionary
    def updateColor(self, color_tuple, button, source, category, curve):
        c = [round(255*x) for x in color_tuple]
        color = QColor(*c)
        button.setStyleSheet("QPushButton {background-color: %s}"
                                           % color.name()) #set background color
        self.plotDict[source][category]['curves'][curve]['color'] = color_tuple
        
    #update color tuples for "datafile' curves in plotDict
    def updateColorTuple(self):
        for category in self.plotDict['datafile']:
            for curve in self.plotDict['datafile'][category]['curves']:
                btn = self.plotDict['datafile'][category]['curves'][curve]['color button']
                color = btn.palette().color(1).getRgb()
                color_tuple = tuple([x/255 for x in color])
                self.plotDict['datafile'][category]['curves'][curve]['color'] = color_tuple 
    
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
        # filterVbox.addWidget(self.fontLabel, 2, 2, 1, 1)
        # filterVbox.addWidget(self.fontSize, 2, 3, 1, 1)
        # filterVbox.addWidget(self.eqLabel, 3, 2, 1, 1)
        # filterVbox.addWidget(self.latCalibEq, 3, 3, 1, 1)
        # filterVbox.addWidget(self.invertLatForce, 0, 2, 1, 2)
        # filterVbox.addWidget(self.zeroShift, 0, 0, 1, 1)
        # filterVbox.addWidget(self.applyCrossTalk, 1, 2, 1, 2)
        # filterVbox.addWidget(self.xAxisLabel, 0, 3, 1, 1)
        # filterVbox.addWidget(self.xAxisParam, 1, 3, 1, 1)
        # filterVbox.addWidget(self.noiseStepsLabel, 4, 2, 1, 1)
        # filterVbox.addWidget(self.noiseSteps, 5, 2, 1, 1)
        # filterVbox.addWidget(self.legendPosLabel, 4, 3, 1, 1)
        # filterVbox.addWidget(self.legendPos, 5, 3, 1, 1)
        # filterVbox.addWidget(self.startFullLabel, 4, 0, 1, 1)
        # filterVbox.addWidget(self.endFullLabel, 5, 0, 1, 1)
        # filterVbox.addWidget(self.startFull, 4, 1, 1, 1)
        # filterVbox.addWidget(self.endFull, 5, 1, 1, 1)
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
        # # fittingVbox.addWidget(self.startFitLabel, 0, 0, 1, 1)
        # # fittingVbox.addWidget(self.endFitLabel, 1, 0, 1, 1)
        # # fittingVbox.addWidget(self.fitStart, 0, 1, 1, 1)
        # # fittingVbox.addWidget(self.fitStop, 1, 1, 1, 1)
        # # fittingVbox.addWidget(self.xFitLabel, 0, 2, 1, 1)
        # # fittingVbox.addWidget(self.yFitLabel, 1, 2, 1, 1)
        # # fittingVbox.addWidget(self.xFit, 0, 3, 1, 1)
        # # fittingVbox.addWidget(self.yFit, 1, 3, 1, 1)
        # fittingVbox.addWidget(self.fitPosLabel, 0, 4, 1, 1)
        # fittingVbox.addWidget(self.fitPos, 0, 5, 1, 1)
        # fittingVbox.addWidget(self.showFitEq, 1, 4, 1, 2)

    # def filter_change(self):
    #     if self.filter_wind.value() %2 == 0: #make sure its odd
    #         self.filter_wind.blockSignals(True)
    #         self.filter_wind.setValue(self.filter_wind.value() + 1)
    #         self.filter_wind.blockSignals(False)

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

    # def update_dict(self):
    #     self.rangeDict[self.roiChoice.currentText()] = [[self.zeroRange1.value(),
    #                                                        self.zeroRange2.value()],
    #                                                     [self.adhRange1.value(),
    #                                                        self.adhRange2.value()],
    #                                                     [self.prl1Range1.value(),
    #                                                        self.prl1Range2.value()],
    #                                                     [self.frictionRange1.value(),
    #                                                        self.frictionRange2.value()],
    #                                                     [self.prl2Range1.value(),
    #                                                      self.prl2Range2.value()],
    #                                                     [self.zero2Range1.value(),
    #                                                        self.zero2Range2.value()]]
    #     print(self.rangeDict)
    def show_window(self): #show window
        # self.update_range()
        # self.update_dict()
        self.show()

# test = ConfigPlotWindow()