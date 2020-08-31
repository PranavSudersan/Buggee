# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 23:03:32 2020

@author: adwait
"""

# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.lines as lines
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# from matplotlib.figure import Figure
# from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
# import sys

class Plot2Widget(FigureCanvasQTAgg):

    def __init__(self, fig, xdata, cursor1_init = None,
                 cursor2_init = None, parent=None):
        
##        fig = Figure(figsize=(width, height), dpi=dpi)
##        self.axes = fig.add_subplot(111)
        self.axes = fig.get_axes()[0]
        super(Plot2Widget, self).__init__(fig)
        self.xdata = xdata
        self.clickState = False
        self.add_cursors(cursor1_init, cursor2_init)

    #set init value as None for no cursor   
    def add_cursors(self, cursor1_init, cursor2_init):
        if cursor1_init != None:
            self.cursor1 = self.cursor_initialize(cursor1_init)
        else:
            self.cursor1 = None
        if cursor2_init != None:
            self.cursor2 = self.cursor_initialize(cursor2_init)
        else:
            self.cursor2 = None

    def cursor_initialize(self, XorY):
        x = [XorY, XorY]
        y = self.axes.get_ybound()
        line = lines.Line2D(x, y, picker=5)
        self.axes.add_line(line)
        self.draw_idle()
        self.sid = self.mpl_connect('pick_event', self.clickonline)
        return line
    
    def clickonline(self, event):
        print("click event")
        print(event.artist)
        if event.artist in [self.cursor1, self.cursor2] and event.mouseevent.button == 1 \
            and self.clickState == False:
            print("line selected ", event.artist)
            self.clickState = True
            self.follower = self.mpl_connect("motion_notify_event",
                                               lambda event, line=event.artist: self.followmouse(event,line))
            self.releaser = self.mpl_connect("button_release_event",self.releaseonclick)
            # self.releaser2 = self.mpl_connect("button_press_event",self.releaseonclick2)

    def followmouse(self, event,line):
        print(event.xdata, line)
        if event.xdata != None:
            x = event.xdata
            line.set_xdata([x, x])
            self.draw_idle()
            # indx = np.searchsorted(self.xdata, [event.xdata])[0]
            # if indx != self.xdata.shape[0]: 
            #     x = self.xdata[indx] #restrict cursor to data points
            #     x = event.xdata
            #     line.set_xdata([x, x])
            #     self.draw_idle()

    def releaseonclick(self, event):
        if event.button == 1:
            # print(self.cursor1.get_xdata(),self.cursor2.get_xdata())
            # if self.cursor1.get_xdata()[0] == self.cursor2.get_xdata()[0]:
            #     print("equal")
            #     indx = np.searchsorted(self.xdata, [self.cursor1.get_xdata()[0]])[0]
            #     x = self.xdata[indx-3]
            #     self.cursor1.set_xdata([x, x])
##            self.xval = line.get_xdata()[0]
##
##            print (self.xval)
            print(event.button)
            self.mpl_disconnect(self.follower)
            self.mpl_disconnect(self.releaser)
            self.clickState = False
            
#     def releaseonclick2(self, event):
#         if event.button == 3:
# ##            self.xval = line.get_xdata()[0]
# ##
# ##            print (self.xval)
#             print(event.button)
#             self.mpl_disconnect(self.follower)
#             self.mpl_disconnect(self.releaser)

##class MainWindow(QtWidgets.QMainWindow):
##
##    def __init__(self, *args, **kwargs):
##        super(MainWindow, self).__init__(*args, **kwargs)
##
##        fig = Figure(figsize=(5, 4), dpi=100)
##        axes = fig.add_subplot(111)
##
##        t = np.arange(-2, 3.5, 0.01)
##        s = np.sin(2*2*np.pi*t)
##        axes.plot(t, s, 'r')
##
##        self.sc = MplCanvas(fig, t)
##
##        buttonwid = QtWidgets.QPushButton("OK", self)
##        buttonwid.clicked.connect(self.button)
##        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
##        toolbar = NavigationToolbar(self.sc, self)
##
##        layout = QtWidgets.QVBoxLayout()
##        layout.addWidget(toolbar)
##        layout.addWidget(self.sc)
##        layout.addWidget(buttonwid)
##
##        # Create a placeholder widget to hold our toolbar and canvas.
##        widget = QtWidgets.QWidget()
##        widget.setLayout(layout)
##        self.setCentralWidget(widget)
##
##        self.show()
##
##    def button(self):
##        print("hello")
##        print(self.sc.Tline.get_xdata()[0], self.sc.Tline2.get_xdata()[0])

##app = QtWidgets.QApplication(sys.argv)
##w = MainWindow()
##app.exec_()

