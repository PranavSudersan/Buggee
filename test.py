# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:14:23 2020

@author: adwait
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, \
     QSlider, QFileDialog, QCheckBox, QLabel, QPushButton, \
     QMessageBox, QAction, QComboBox, QGraphicsScene, QGraphicsView, \
     QGraphicsPixmapItem, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QStatusBar, \
     QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, \
     QDialog, QListWidget,QTabWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage, QBrush, \
     QPolygonF, QPainter, QPalette, QColor
from PyQt5.QtCore import Qt,QFile,QTextStream,QRect
import sys
    
class MainWindow(QMainWindow): #also try inherit Effect, unify self.frame everywhere
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1200, 900)
        self.appVersion = "V-Scope v6.1"
        self.setWindowTitle(self.appVersion)
        self.layout = QGridLayout(self)

        quitWindow = QAction("&Quit", self) #quit program
##        quitWindow.setShortcut("Ctrl+Q") 
        quitWindow.setStatusTip('Quit Program')
        
        openVideoFile = QAction("&Open Video File...", self) #open video file
##        openVideoFile.setShortcut("Ctrl+V")
        openVideoFile.setStatusTip("Select the required video file")

        openImageFile = QAction("&Open Image File...", self) #open image file
##        openImageFile.setShortcut("Ctrl+I")
        openImageFile.setStatusTip("Select the required image file")

        openForceFile = QAction("&Open Force Data...", self) #open force file
##        openForceFile.setShortcut("Ctrl+F")
        openForceFile.setStatusTip("Select the corresponding force data file")

        self.openZeroForceFile = QAction("&Open Zero-Force Data...", self) #open zero force file
        self.openZeroForceFile.setStatusTip("Select the zeroline force data file")

        openFileList = QAction("&Open File List...", self) #open file list spreadhsheet
##        openFileList.setShortcut("Ctrl+O")
        openFileList.setStatusTip("Select file list spreadhsheet")

        self.chooseMsrmnt = QAction("&Choose Measurement...", self) #choose measurement from file list
##        self.chooseMsrmnt.setShortcut("Ctrl+M")
        self.chooseMsrmnt.setStatusTip("Select measurement from list")

        recordVideo = QAction("&Record", self) #configure recording
##        recordVideo.setShortcut("Ctrl+R")
        recordVideo.setStatusTip("Configure Record")

        plot = QAction("&Plot/Force", self) #configure plot
##        plot.setShortcut("Ctrl+P")
        plot.setStatusTip("Configure plot and force curves")

        paths = QAction("&Filepath", self) #configure export file paths
        paths.setStatusTip("Configure Filepaths")

        showSummary = QAction("&Display Summary Plots", self) #show summary Plots
        showSummary.setStatusTip("Displays summary plots based on summary data file")

        exportSummary = QAction("&Export Summary Plots", self) #export summary Plots
        exportSummary.setStatusTip("Exports summary plots based on summary data file")

        configureSummary = QAction("&Configure", self) #configure summary plots
        configureSummary.setStatusTip("Configure Summary Plot")
        
        mainMenu = self.menuBar() #create main menu
        
        fileMenu = mainMenu.addMenu("&File") #File menu
        fileMenu.addAction(openVideoFile)
        fileMenu.addAction(openImageFile)
        fileMenu.addAction(openForceFile)
        fileMenu.addAction(self.openZeroForceFile)
        fileMenu.addAction(openFileList)
        fileMenu.addAction(self.chooseMsrmnt)
        fileMenu.addAction(quitWindow)

        self.chooseMsrmnt.setEnabled(False)
        self.openZeroForceFile.setEnabled(False)

        configureMenu = mainMenu.addMenu("&Configure") #Configure menu
        configureMenu.addAction(recordVideo)
        configureMenu.addAction(plot)
        configureMenu.addAction(paths)

        plotMenu = mainMenu.addMenu("&Summarize") #Plot menu
        plotMenu.addAction(configureSummary)
        plotMenu.addAction(showSummary)
        plotMenu.addAction(exportSummary)
##        plotMenu.addAction(combineSummary)

        self.statusBar = QStatusBar() #status bar
        self.setStatusBar(self.statusBar)
        
        self.home()
        
        
        
    def home(self):
        print(self.size())
        self.roiBtn = QPushButton("Draw ROI", self) #Draw ROI Manually
        # self.roiBtn.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px;} ")

        
        self.videoEffect = QComboBox(self) #video effect dropdown
        self.videoEffect.addItem("Binary")
        self.videoEffect.addItem("Masked")
        self.videoEffect.addItem("Contours")
        self.videoEffect.addItem("Transformed")
        self.videoEffect.addItem("Background")
        self.videoEffect.addItem("Auto ROI")
        self.videoEffect.addItem("Force/Area Plot")
        self.videoEffect.setStyleSheet("QComboBox { font-weight: bold; font-size: 14px;} ")
        # self.videoEffect.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
##        self.videoEffect.move(650, 85)
##        self.videoEffect.resize(self.videoEffect.minimumSizeHint())
        self.videoEffect.model().item(5).setEnabled(False)
        self.videoEffect.model().item(6).setEnabled(False)

        self.analyzeVideo = QCheckBox('Analyze Video', self) #Perform Analysis
##        self.analyzeVideo.move(500, 30)
        # self.analyzeVideo.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.analyzeVideo.setStyleSheet("QCheckBox { font-weight: bold; font-size: 16px;} ")

        self.showEffect = QCheckBox('Show Effect', self) #show contours
##        self.showContours.move(300, 60)
        # self.showEffect.setStyleSheet("QCheckBox { font-weight: bold; font-size: 16px;} ")

        self.showContours = QCheckBox('Show Contours', self) #show contours
        # self.showContours.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
##        self.showContours.move(300, 60)
        # self.showContours.setStyleSheet("QCheckBox { font-weight: bold; font-size: 16px;} ")
        
        self.blankPixmap = QPixmap('images/blank.png')
        
        self.rawScene = QGraphicsScene(self) #raw video feed
        self.rawPixmapItem = QGraphicsPixmapItem(self.blankPixmap)
        self.rawScene.addItem(self.rawPixmapItem)
        self.rawView = MyQGraphicsView(self.rawScene)
        # self.rawView.setMinimumSize(600,400)
        # self.rawView.setGeometry(0,0,500,700)
        # self.rawView.setGeometry(QRect(50, 120, 480, 360))
        # self.rawView.setSizePolicy(700, 500)
        self.rawView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rawView.setBackgroundBrush(QBrush(Qt.black,
                                                       Qt.SolidPattern))

        self.effectScene = QGraphicsScene(self) #analysis video feed
##        self.effectPixmap = QPixmap('images/blank.png')
        self.effectPixmapItem = QGraphicsPixmapItem(self.blankPixmap)
        self.effectScene.addItem(self.effectPixmapItem)
        self.effectView = MyQGraphicsView(self.effectScene)
        # self.effectView.setMinimumSize(600,400)
        # self.effectView.resize(700,500)
        # self.effectView.setGeometry(QRect(560, 120, 480, 360))
        # self.effectView.setGeometry(500,0,500,700)
        # self.effectView.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.effectView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effectView.setBackgroundBrush(QBrush(Qt.black,
                                                          Qt.SolidPattern))
        
        self.playBtn = QPushButton("Play", self) #Play/Pause action       
        # self.playBtn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.stopBtn = QPushButton("Stop", self) #Stop video       
        # self.playBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.seekSlider = QSlider(Qt.Horizontal, self) #seek bar
##        self.seekSlider.setGeometry(30, 60, 200, 30)
        self.seekSlider.setMinimum(0)
        self.seekSlider.setMaximum(100)
        self.seekSlider.setValue(0)
        self.seekSlider.setTickInterval(10)
        self.seekSlider.setSingleStep(2)
        self.seekSlider.setTickPosition(QSlider.TicksBelow)

        self.videoFileNameLabel = QLabel("Select video from file menu", self)
##        self.videoFileNameLabel.setGeometry(10, 650, 400, 60)
##        self.videoFileNameLabel.setTextFormat(Qt.RichText)
        self.videoFileNameLabel.setWordWrap(True)

        self.forceFileNameLabel = QLabel("Select force data from file menu", self)
##        self.forceFileNameLabel.setGeometry(10, 700, 400, 60)
        self.forceFileNameLabel.setWordWrap(True)

        self.zeroForceFileNameLabel = QLabel("Select zero-force data from file menu", self)
        self.zeroForceFileNameLabel.setWordWrap(True)
        
        
        
        wid = QWidget(self)
        self.setCentralWidget(wid)

        topleftGroupBox = QGroupBox()
        # topleftGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        topleftGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        topleftVbox = QGridLayout(self)
        # topleftVbox.setColumnStretch(0, 1.5)
        topleftGroupBox.setLayout(topleftVbox)
        topleftVbox.addWidget(self.showContours, 0, 0, 1, 1)
        topleftVbox.addWidget(self.showEffect, 1, 0, 1, 1)
        topleftVbox.addWidget(self.roiBtn, 2, 0, 1, 1)

        toprightGroupBox = QGroupBox()
        # toprightGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        toprightGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        toprightVbox = QGridLayout(self)
        # toprightVbox.setColumnStretch(0, 1.5)
        toprightGroupBox.setLayout(toprightVbox)
        toprightVbox.addWidget(self.analyzeVideo, 0, 0, 1, 1)
        toprightVbox.addWidget(self.videoEffect, 1, 0, 1, 1)
        
        displayGroupBox = QGroupBox()
        # displayGroupBox.setSizePolicy(1400,500)
        displayGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        displayVbox = QGridLayout(self)
        displayGroupBox.setLayout(displayVbox)
        displayVbox.addWidget(self.rawView, 0, 0, 1, 1)
        displayVbox.addWidget(self.effectView, 0, 1, 1, 1)

        playbackGroupBox = QGroupBox()
        # playbackGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        playbackGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        playbackVbox = QGridLayout(self)
        # playbackVbox.setRowStretch(1, 1.5)
        playbackGroupBox.setLayout(playbackVbox)
        playbackVbox.addWidget(self.seekSlider, 0, 0, 1, 2)
        playbackVbox.addWidget(self.playBtn, 1, 0, 1, 1)
        playbackVbox.addWidget(self.stopBtn, 1, 1, 1, 1)      

        fileGroupBox = QGroupBox("Filenames")
        # fileGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # fileGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        fileVbox = QGridLayout(self)
        fileGroupBox.setLayout(fileVbox)
        fileVbox.addWidget(self.videoFileNameLabel, 0, 0, 1, 1)
        fileVbox.addWidget(self.forceFileNameLabel, 1, 0, 1, 1)
        fileVbox.addWidget(self.zeroForceFileNameLabel, 2, 0, 1, 1)
 
    
        inputsGroupBox = QGroupBox()
        # inputsGroupBox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        inputsGroupBox.setStyleSheet("QGroupBox { font-weight: bold; } ")
        inputsLayout = QGridLayout(self)
        inputsGroupBox.setLayout(inputsLayout)
        inputsLayout.addWidget(topleftGroupBox, 0, 0, 3, 1)
        inputsLayout.addWidget(toprightGroupBox, 3, 0, 1, 1)
        # inputsLayout.addWidget(playbackGroupBox, 4, 0, 1, 1)
        # inputsLayout.addWidget(fileGroupBox, 5, 0, 1, 1)
        effectsTab = QTabWidget()
        effectsTab.addTab(topleftGroupBox,"Brightness/Contrast")
        effectsTab.addTab(toprightGroupBox,"Filtering")
        
        # self.layout.addWidget(topleftGroupBox, 0, 0, 1, 1)
        # self.layout.addWidget(toprightGroupBox, 0, 1, 1, 1)
        
        # self.layout.addWidget(self.rawView, 1, 0, 1, 1)
        # self.layout.addWidget(self.effectView, 1, 1, 1, 1)
        self.layout.addWidget(displayGroupBox, 0, 0, 2, 1)
        self.layout.addWidget(effectsTab, 2, 0, 1, 1)
        # self.layout.addWidget(playbackGroupBox, 1, 0, 1, 1)
        # self.layout.addWidget(fileGroupBox, 6, 0, 1, 1)
        
        print("minimum",self.showContours.minimumSize().height())
        
        wid.setLayout(self.layout)
        
    def closeEvent(self, event): #close application
        msg = QMessageBox()
        msg.setStyleSheet("QLabel{min-width:500 px; font-size: 24px;} QPushButton{ width:500px; font-size: 24px; }");
        choice = msg.question(self, 'Closing...',
                                      "Really Quit?",
                                      msg.Yes | msg.No)        
        if choice == msg.Yes:
            if type(event) is not bool:
                event.accept()
            QApplication.exit()
        else:
            if type(event) is not bool:
                event.ignore()
                
# %% Zoomable QGraphicsView Display
class MyQGraphicsView(QGraphicsView): #zoom QFraphicsView
    def __init__ (self, parent=None):
        super(MyQGraphicsView, self).__init__ (parent)

    def wheelEvent(self, event):
       
        zoomInFactor = 1.25  # Zoom Factor
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())
if __name__ == "__main__":
    def run():
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('images/icon.ico'))
        # file = QFile("style/dark.qss")
        # file.open(QFile.ReadOnly | QFile.Text)
        # stream = QTextStream(file)
        # app.setStyleSheet(stream.readAll())
        Gui = MainWindow()
        Gui.setWindowIcon(QIcon('images/icon.ico'))
        # sys.exit(app.exec_())
        Gui.show()
        app.exec_()
    
    run()