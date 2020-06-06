# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:33:08 2020

@author: adwait
"""
from PyQt5.QtCore import QThread, pyqtSignal

# %% Save summary plots thread
class SummPlotThread(QThread): 
    output = pyqtSignal('PyQt_PyObject')
    def __init__(self, summary, pltformat):
        QThread.__init__(self)
        self.summary = summary
        self.pltformat = pltformat

    def __del__(self):
        self.wait()

    def run(self):
        self.output.emit("Saving summary plots..")
        self.summary.saveSummaryPlot(self.pltformat)