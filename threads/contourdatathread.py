# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:32:37 2020

@author: adwait
"""
from PyQt5.QtCore import QThread, pyqtSignal

# %% Save contour data thread
class ContourDataThread(QThread): 
    output = pyqtSignal('PyQt_PyObject')
    def __init__(self, df_contour, contourDataPath, roi_labels):
        QThread.__init__(self)
        self.df_contour = df_contour
        self.contourDataPath = contourDataPath
        self.roi_labels = roi_labels

    def __del__(self):
        self.wait()

    def run(self):
        #delete old data in appended file
        self.output.emit("Creating contour dataset..")
        for r in self.df_contour['ROI_Label'].unique():
            if r not in self.roi_labels:
                self.df_contour = self.df_contour[self.df_contour['ROI_Label'] != r]
                continue
            for i in self.df_contour['Frame_no'].unique():
                ind_all = self.df_contour.index[(self.df_contour['Frame_no'] == i) &
                                           (self.df_contour['ROI_Label'] == r)].tolist()
                ind_0 = self.df_contour.index[(self.df_contour['Frame_no'] == i) &
                                         (self.df_contour['ROI_Label'] == r) &
                                         (self.df_contour['Contour_ID'] == 0)].tolist()
                ind_old = [a for a in ind_all if a < max(ind_0)]
                self.df_contour.drop(ind_old, inplace = True)
        self.output.emit("Saving contour data to excel..")
        self.df_contour.to_excel(self.contourDataPath) #save 
        del self.df_contour