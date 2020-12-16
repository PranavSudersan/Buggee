# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:31:37 2020

@author: adwait
"""
import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import logging

# %% Video frame count thread
class CountFrameThread(QThread):
    output = pyqtSignal('PyQt_PyObject')
    def __init__(self, cap):
        QThread.__init__(self)
        self.cap = cap

    def __del__(self):
        self.wait()

    def run(self):
        i = 1
        while(True):
            ret, frame = self.cap.read()
##            self.emit(SIGNAL('frame_number'), i)
            self.output.emit(i)
            i += 1
            if ret ==False:
                self.frameCount = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                logging.debug('%s, %s', 'framecount', self.frameCount)
##                self.cap.release()
                break