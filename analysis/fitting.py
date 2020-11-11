# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 22:49:48 2020

@author: adwait
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel,\
    QComboBox,QLineEdit, QTextEdit, QCheckBox, QPushButton, QGroupBox
# from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
##from sympy import *
import sympy as sp
import numpy as np
from scipy.optimize import curve_fit
from source.analysis.plot2widget import PlotWidget

class MathTextLabel(QWidget):

    def __init__(self, mathText, parent=None, **kwargs):
        super(QWidget, self).__init__(parent, **kwargs)
        _l=QVBoxLayout(self)
        _l.setContentsMargins(0,0,0,0)

        _r,_g,_b,_a=self.palette().base().color().getRgbF()

        self._figure=Figure(edgecolor=(_r,_g,_b), facecolor=(_r,_g,_b))
        self._canvas=FigureCanvas(self._figure)
        _l.addWidget(self._canvas)
        self.drawFigure(mathText)
        
    def drawFigure(self, mathText):
        self._figure.clear()
        _text=self._figure.suptitle(mathText,
                                    x=0.0,
                                    y=1.0,
                                    horizontalalignment='left',
                                    verticalalignment='top',
                                    size=QFont().pointSize()*2
                                    )
        self._canvas.draw()

        (_x0,_y0),(_x1,_y1)=_text.get_window_extent().get_points()
        _w=_x1-_x0; _h=_y1-_y0

        self._figure.set_size_inches(_w/80, _h/80)
        self.setFixedSize(_w,_h)

# if __name__=='__main__':
# from sys import argv, exit

class FitDataWindow(QWidget):
    def __init__(self, *args, **kwargs):
##        super(QWidget, self).__init__(*args, **kwargs)
        super().__init__()
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle("Data Fitting")
        self.home()
        
    def home(self):
        
        # startFitLabel = QLabel("Start (%):")
        # endFitLabel = QLabel("End (%):")

        # self.fitStart = QDoubleSpinBox(self) #fitting range start
        # self.fitStart.setValue(0)
        # self.fitStart.setSingleStep(1)
        # self.fitStart.setRange(0, 100)

        # self.fitStop = QDoubleSpinBox(self) #fitting range end
        # self.fitStop.setValue(100)
        # self.fitStop.setSingleStep(1)
        # self.fitStop.setRange(0, 100)
        
        params_list = ["Index", "Time", "Vertical piezo", "Lateral piezo",
                       "Deformation", "Vertical force", "Lateral force"]
        
        xPlotLabel = QLabel("X Axis:", self)
        self.xPlot = QComboBox(self) #x param
        self.xPlot.addItems(params_list)
        self.xPlot.setCurrentIndex(0)
        self.xPlot.currentIndexChanged.connect(self.plotSequence)
        
        self.enableFitting = QCheckBox("Enable", self)
        self.enableFitting.stateChanged.connect(lambda: self.fitData(True))
        
        xFitLabel = QLabel("X Parameter:", self)
        yFitLabel = QLabel("Y Parameter:", self)

        self.xFit = QComboBox(self) #x param
        self.xFit.addItems(params_list)
        self.xFit.setCurrentIndex(4)
        self.xFit.currentIndexChanged.connect(self.plotSequence)

        self.yFit = QComboBox(self) #x param
        self.yFit.addItems(params_list)
        self.yFit.setCurrentIndex(5)
        self.yFit.currentIndexChanged.connect(self.plotSequence)
        
        # self.xDict = {'Vertical piezo':None,
        #          'Lateral piezo':None,
        #          'Deformation':None,
        #          'Time':None,
        #          'Index':None}
        # self.yDict = {'Vertical force':None,
        #              'Lateral force':None}
        self.fileDataDict = {}
        
        fitparamLabel = QLabel("Fit Parameters:", self)
        self.fittingParams = QLineEdit(self)
        self.fittingParams.setText('m,c')
        self.fittingParams.textChanged.connect(self.updateTEX)
        self.params_old = self.fittingParams.text().split(',')
        
        guessValLabel = QLabel("Initial Guess:", self)
        self.guessValues = QLineEdit(self)
        self.guessValues.setText('0,0')
        
        lowBoundLabel = QLabel("Lower Bouond:", self)
        self.lowBound = QLineEdit(self)
        self.lowBound.setText(',')
        
        upBoundLabel = QLabel("Upper Bouond:", self)
        self.upBound = QLineEdit(self)
        self.upBound.setText(',')
        
        constantsLabel = QLabel("Constants:", self)
        self.constantParams = QLineEdit(self)
        self.constantParams.setText('p=1,q=2,r=3')
        self.constantParams.textChanged.connect(self.updateTEX)
        self.constants_old = [_x.split('=')[0] for _x in self.constantParams.text().split(',')]
        
        fitfunctionLabel = QLabel("Fitting Function:", self)
        self.fittingFunctionType = QComboBox(self)
        self.fittingFunctionType.addItem("Linear")
        self.fittingFunctionType.addItem("Quadratic")
        self.fittingFunctionType.addItem("Custom")
        self.fittingFunctionType.currentIndexChanged.connect(self.updateFitFunction)

        #standard functions: equation, params, guess, l_bound, u_bound
        self.functionDict = {'Linear': ['m*x+c', 'm,c', '0,0', ',', ','],
                             'Quadratic': ['a*x**2+b*x+c', 'a,b,c', '0,0,0', ',,', ',,'],
                             'Custom': ['a*x', 'a', '0', '', '']}
        
        self.fittingFunctionText = QTextEdit(self)
        self.fittingFunctionText.setText('m*x+c')
        self.fittingFunctionText.textChanged.connect(self.updateTEX)
        
        self.generateFunction()
        
        self.fittingFunctionTEX = MathTextLabel(self.mathText, self)
        
        self.applyFitBtn = QPushButton("Fit!", self)
        # self.applyFitBtn.clicked.connect(lambda: self.fitData(True))

        self.fitResult = QTextEdit(self)
        self.fitResult.setText("Result:\n")
        self.fitResult.setReadOnly(True)
        # self.fitResult.setStyleSheet("QLabel { font-weight: bold; font-size: 16px;} ")

        self.plotInitialize()
        
        plot = PlotWidget(self.fig,
                          cursor1_init = self.axes.get_xbound()[0],
                          cursor2_init = self.axes.get_xbound()[1])
        self.plotWidget = plot.wid
        # plotToolbar = NavigationToolbar(self.plotWidget, self)

        # self.fitPosLabel = QLabel("Fit Position\n(x,y):", self) #fit eq. position        
        # self.fitPos = QLineEdit(self)
        # self.fitPos.setText('0.5,0.5')

        # self.showFitEq = QCheckBox('Show Slope', self) #display equation on plot
        
        paramGroupBox = QGroupBox()
        paramlayout=QGridLayout()
        paramGroupBox.setLayout(paramlayout)
        paramlayout.addWidget(xPlotLabel, 0, 0, 1, 1)
        paramlayout.addWidget(self.xPlot, 0, 1, 1, 1)
        paramlayout.addWidget(self.enableFitting, 0, 3, 1, 1)
        paramlayout.addWidget(xFitLabel, 1, 0, 1, 1)
        paramlayout.addWidget(self.xFit, 1, 1, 1, 1)
        paramlayout.addWidget(yFitLabel, 1, 2, 1, 1)
        paramlayout.addWidget(self.yFit, 1, 3, 1, 1)
        paramlayout.addWidget(fitparamLabel, 2, 0, 1, 1)
        paramlayout.addWidget(self.fittingParams, 2, 1, 1, 1)
        paramlayout.addWidget(guessValLabel, 2, 2, 1, 1)
        paramlayout.addWidget(self.guessValues, 2, 3, 1, 1)
        paramlayout.addWidget(lowBoundLabel, 3, 0, 1, 1)
        paramlayout.addWidget(self.lowBound, 3, 1, 1, 1)
        paramlayout.addWidget(upBoundLabel, 3, 2, 1, 1)
        paramlayout.addWidget(self.upBound, 3, 3, 1, 1)
        paramlayout.addWidget(constantsLabel, 4, 0, 1, 1)
        paramlayout.addWidget(self.constantParams, 4, 1, 1, 1)
        paramlayout.addWidget(fitfunctionLabel, 4, 2, 1, 1)
        paramlayout.addWidget(self.fittingFunctionType, 4, 3, 1, 1)
        paramlayout.addWidget(self.fittingFunctionText, 5, 0, 1, 4)
        paramlayout.addWidget(self.fittingFunctionTEX, 6, 0, 3, 4)
        paramlayout.addWidget(self.fitResult, 9,0, 1, 4)
        paramlayout.addWidget(self.applyFitBtn, 10, 1, 1, 2)
        # layout.addWidget(plotToolbar, 0, 4, 1, 6)
        # layout.addWidget(self.plotWidget, 1, 4, 9, 6)
        
        
        # plotGroupBox = QGroupBox()
        # plotlayout=QGridLayout()
        # plotGroupBox.setLayout(plotlayout)
        # plotlayout.addWidget(plot, 0, 0, 1, 1)
        # plotlayout.addWidget(plotToolbar, 0, 0, 1, 1)
        # plotlayout.addWidget(self.plotWidget, 1, 0, 1, 1)
        
        layout=QGridLayout()
        layout.addWidget(paramGroupBox, 0, 0, 1, 1)
        layout.addWidget(plot, 0, 1, 1, 1)
        
        self.setLayout(layout)
        # self.show()
      
            
    def updateFitFunction(self):
        print('test0')
        _key = self.fittingFunctionType.currentText()
        self.fittingFunctionText.blockSignals(True)
        self.fittingFunctionText.setText(self.functionDict[_key][0])
        self.fittingFunctionText.blockSignals(False)
        print('test')
        self.fittingParams.blockSignals(True)
        self.fittingParams.setText(self.functionDict[_key][1])
        self.fittingParams.blockSignals(False)
        print('test2')
        self.guessValues.setText(self.functionDict[_key][2])
        self.lowBound.setText(self.functionDict[_key][3])
        self.upBound.setText(self.functionDict[_key][4])

        self.updateTEX()
    
    def updateTEX(self):
        #delete old variables
        for _x in self.params_old:
            if _x != '':
                exec('del ' + _x, globals())

        for _x in self.constants_old:
            if _x != '':
                exec('del ' + _x, globals())

        #update function        
        self.generateFunction()

        self.params_old = self.fittingParams.text().split(',')
        self.constants_old = [_x.split('=')[0] for _x in self.constantParams.text().split(',')]

        #draw equation
        if self.mathText != None:
            self.fittingFunctionTEX.drawFigure(self.mathText)
            #below optional, remove later: CHECK!
            # self.plotRawData()
            # self.plotWidget.cursor1.set_ydata(self.axes.get_ybound()) #CHECK
            # self.plotWidget.cursor2.set_ydata(self.axes.get_ybound()) #CHECK
    ##        self.plotWidget.add_cursors()
            # self.fitData(False)
            # self.updatePlot()
        

    #create fitting function and TEX format for display
    def generateFunction(self):
        try:
            math_functions = ['re','im','sign','Abs','arg','conjugate',
                              'polar_lift','periodic_argument',
                              'principal_branch','sin','cos','tan',
                              'cot','sec','csc','sinc','asin','acos',
                              'atan','acot','asec','acsc','atan2',
                              'sinh','cosh','tanh','coth','sech',
                              'csch','asinh','acosh','atanh','acoth',
                              'asech','acsch','ceiling','floor','frac',
                              'exp','LambertW','log','exp_polar','Min',
                              'Max','root','sqrt','cbrt','real_root','pi']
            
            x_param = 'x'
            y_param = 'y'
            fit_params = self.fittingParams.text()
            constants = self.constantParams.text()
            # constant_vals = '1,2,3'
            equation_fit = self.fittingFunctionText.toPlainText()

            variables = x_param + ',' + fit_params
            
            global var
            var = sp.symbols(variables.replace(',',' '))
            exec(variables +  ' = var', globals())
            for _x in constants.split(','):
                exec(_x, globals())
    ##        print(p+q)
            for item in math_functions:
                equation_fit = equation_fit.replace(item,'sp.'+item)

         
            self.mathText = r'$' + y_param + '=' + sp.latex(eval(equation_fit),
                                                            ln_notation = True) + '$'

            self.func = sp.lambdify(list(var),eval(equation_fit))
            print(self.mathText)
        except Exception as e:
            print('error', e)
            self.mathText = None

    def plotInitialize(self):

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.ax_raw = None
        # self.ax_norm = None
        self.ax_constr = None

        # #generate random data (for testing)
        xdata = np.linspace(0, 4, 50)
        self.fileDataDict[self.xFit.currentText()] = xdata
        self.fileDataDict[self.xPlot.currentText()] = xdata
        y = self.func(xdata, 2.5, 1.3)
        np.random.seed(1729)
        y_noise = 0.2 * np.random.normal(size=xdata.size)
        self.fileDataDict[self.yFit.currentText()] = y + y_noise
        
        self.plotRawData()
        self.updatePlot()
        self.fit_range = [None,None]

    def plotRawData(self):
                
        self.plotxdata= self.fileDataDict[self.xPlot.currentText()]

        self.xdata = self.fileDataDict[self.xFit.currentText()]
        self.ydata = self.fileDataDict[self.yFit.currentText()]

        if self.ax_raw != None: #check
            self.axes.lines.remove(self.ax_raw)
        
        # if self.xdata != None and self.ydata != None:
        self.ax_raw, = self.axes.plot(self.plotxdata, self.ydata, 'ro',
                                      linewidth=1, markersize=1)  
        self.axes.relim()
        self.axes.autoscale()
        self.axes.set_xlabel(self.xPlot.currentText())
        self.axes.set_ylabel(self.yFit.currentText())
        
        # self.updatePlot()
        # self.plotWidget.cursor1.set_xdata(self.axes.get_xbound()[0]) #CHECK
        # self.plotWidget.cursor2.set_xdata(self.axes.get_xbound()[1]) #CHECK
        
    def updatePlot(self):
        self.axes.relim()
        self.axes.autoscale()
        self.fig.tight_layout()
        self.fig.canvas.draw()
       
    def plotSequence(self):
        self.plotRawData()         
        self.update_cursor()
        self.fitData(False)
        # self.updatePlot()

    def update_cursor(self):
        if self.fit_range ==  [None,None]:
            self.fit_range[:] = [0,len(self.plotxdata)-1]
        if self.plotWidget.cursor1 != None:
            # x = self.plotxdata.min()
            x = self.plotxdata[self.fit_range[0]]
            y = [self.ydata.min(), self.ydata.max()]
            self.plotWidget.cursor1.set_xdata([x,x])
            self.plotWidget.cursor1.set_ydata(y) #CHECK
        if self.plotWidget.cursor2 != None:
            # x = self.plotxdata.max()
            x = self.plotxdata[self.fit_range[1]-1]
            y = [self.ydata.min(), self.ydata.max()]
            self.plotWidget.cursor2.set_xdata([x,x])
            self.plotWidget.cursor2.set_ydata(y) #CHECK
        # self.axes.relim()
        # self.axes.autoscale()
        self.updatePlot()
        self.plotWidget.draw_idle()
        
            
    # data fitting
    def fitData(self, update_slice = True):
        print("fit data")
        if self.enableFitting.isChecked() == True:
            self.generateFunction()
            #draw equation
            # if self.mathText != None:
            #     self.fittingFunctionTEX.drawFigure(self.mathText)
            # self.updateTEX()
            
            if update_slice == True:
                xlim1 = min([self.plotWidget.cursor1.get_xdata()[0],
                             self.plotWidget.cursor2.get_xdata()[0]])
                xlim2 = max([self.plotWidget.cursor1.get_xdata()[0],
                             self.plotWidget.cursor2.get_xdata()[0]])
        
                self.fit_range[:] = [np.searchsorted(self.plotxdata, [xlim1])[0],
                                  np.searchsorted(self.plotxdata, [xlim2])[0]+1]
                print("inside")
            
            fit_slice = slice(*self.fit_range)
            print(fit_slice)
            
            guess_vals = self.guessValues.text()
            l_bounds = self.lowBound.text()
            u_bounds = self.upBound.text()
            
            l_bounds_val = [float(_x) if _x != '' else -np.inf \
                            for _x in l_bounds.split(',')] \
                            if l_bounds != '' else -np.inf
            u_bounds_val = [float(_x) if _x != '' else np.inf \
                            for _x in u_bounds.split(',')] \
                            if u_bounds != '' else np.inf
            
            labeltext = self.fittingParams.text().replace(',', '=%5.3f, ') + \
                        '=%5.3f'
                    
            
            # if self.ax_norm != None:
            #     self.axes.lines.remove(self.ax_norm)
    
            if self.ax_constr != None:
                self.axes.lines.remove(self.ax_constr)
    
            try:
                print("test")
                #normal fit
            
                # popt, pcov = curve_fit(self.func, self.xdata[fit_slice],
                #                        self.ydata[fit_slice],
                #                        [float(x) for x in guess_vals.split(',')])
    
                # print("normal", popt)
                # self.ax_norm, = self.axes.plot(self.xdata[fit_slice],
                #                                self.func(self.xdata[fit_slice], *popt), 'b-',
                #                          label= labeltext % tuple(popt))
                
                #contrained fit
                popt, pcov = curve_fit(self.func, self.xdata[fit_slice],
                                       self.ydata[fit_slice],
                                       [float(_x) for _x in guess_vals.split(',')],
                                       bounds=(l_bounds_val,u_bounds_val))
                print("constrained", popt)
                
                self.fit_ydata = self.func(self.xdata[fit_slice], *popt)
                fit_label = labeltext % tuple(popt)
                self.ax_constr, = self.axes.plot(self.plotxdata[fit_slice],
                                                 self.fit_ydata, 'g--',
                                                 label= fit_label)
                error_label = 'Std. Dev. Error:\n' + labeltext % tuple(np.sqrt(np.diag(pcov)))
                self.fitResult.setText('Fit values:\n' + fit_label + '\n' + error_label)
                self.fitParams = dict(zip(self.fittingParams.text().split(','),
                                          popt))
                print(self.fitParams)
    
            except Exception as e: #on fitting failure
                print(e)
                self.fitResult.setText(str(e))
                # self.ax_norm = None
                self.ax_constr = None
    
            # self.plotWidget.cursor1.set_ydata(self.axes.get_ybound()) #CHECK
            # self.plotWidget.cursor2.set_ydata(self.axes.get_ybound()) #CHECK
            self.axes.legend()
            # self.axes.text(1, 1, "Test", picker=5)
    ##        self.fig.canvas.draw()
        else:
            if self.ax_constr != None:
                self.axes.get_legend().remove()
                self.axes.lines.remove(self.ax_constr)
                self.ax_constr = None
            self.fitParams = {}
            self.fitResult.setText('Fit values:\n')
        
        self.updatePlot()
    ##        plt.show()

# _a=QApplication(argv)
# _w=FitDataWindow()
# # _w.show()
# _w.raise_()
# _a.exec_()
# QApplication.exit()
