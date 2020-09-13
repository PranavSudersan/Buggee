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
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import QWidget, QGridLayout

class Plot2Widget(FigureCanvasQTAgg):

    def __init__(self, fig, xdata = None, cursor1_init = None,
                 cursor2_init = None, parent=None, fixYLimits = False):
        
##        fig = Figure(figsize=(width, height), dpi=dpi)
##        self.axes = fig.add_subplot(111)
        self.axes = fig.get_axes()[-1] #get last axes to draw cursors
        super(Plot2Widget, self).__init__(fig)
        self.xdata = xdata
        self.clickState = False
        self.fixYLimits = fixYLimits
        self.artistDict = {} #artists for animation
        self.add_cursors(cursor1_init, cursor2_init)
        self.sid = self.mpl_connect('pick_event', self.clickonline)
        self.mpl_connect("resize_event", self.resizeWindow)

    #set init value as None for no cursor   
    def add_cursors(self, cursor1_init, cursor2_init):
        if cursor1_init != None:
            self.cursor1 = self.cursor_initialize(cursor1_init)
            self.artistDict["cursor1"] = self.cursor1
        else:
            self.cursor1 = None
            # del self.artistDict["cursor1"]
        if cursor2_init != None:
            self.cursor2 = self.cursor_initialize(cursor2_init)
            self.artistDict["cursor2"] = self.cursor2
        else:
            self.cursor2 = None
            # del self.artistDict["cursor2"]

    def cursor_initialize(self, XorY):
        print("XorY")
        x = [XorY, XorY]
        y = self.axes.get_ybound()
        line = lines.Line2D(x, y, picker=5)
        self.axes.add_line(line)
        self.draw_idle()
        # self.sid = self.mpl_connect('pick_event', self.clickonline)
        return line
    
    def clickonline(self, event):
        print("click event")
        # print(event.artist)
        if self.clickState == False and event.mouseevent.button == 1:
            self.clickState = True
            #detect cursor
            if event.artist in [self.cursor1, self.cursor2]:
                print("line selected ", event.artist)
                
                self.follower = self.mpl_connect("motion_notify_event",
                                                   lambda event, artist=event.artist: self.followmouse(event,artist))
                self.releaser = self.mpl_connect("button_release_event",
                                                 lambda event, artist=event.artist: self.releaseonclick(event,artist))
            #detect text box
            elif event.artist.__class__.__name__ == "Text":
                self.follower = self.mpl_connect("motion_notify_event",
                                                   lambda event, artist=event.artist: self.followmouse(event,artist))
                self.releaser = self.mpl_connect("button_release_event",
                                                 lambda event, artist=event.artist: self.releaseonclick(event,artist))
                # event.artist.set_position([2,1])
                # self.draw_idle()
                # self.releaser2 = self.mpl_connect("button_press_event",self.releaseonclick2)
            #blitting for faster updates
            event.artist.set_animated(True)
            self.draw()
            self.background = self.copy_from_bbox(self.axes.bbox)

    def followmouse(self, event, artist):
        print(event.xdata, event.ydata, artist)
        if event.xdata != None:
            x = event.xdata
            y = event.ydata
            if artist.__class__.__name__ == 'Line2D':
                self.updateCursor(artist, x)
            elif artist.__class__.__name__ == 'Text':
                #using axes coordinates to set position
                artist.set_position(self.axes.transLimits.transform((x,y)))
            
            # restore the background region
            self.restore_region(self.background)
            # redraw just the current rectangle
            self.axes.draw_artist(artist)
            # blit just the redrawn area
            self.blit(self.axes.bbox)

            # self.draw_idle()
            # indx = np.searchsorted(self.xdata, [event.xdata])[0]
            # if indx != self.xdata.shape[0]: 
            #     x = self.xdata[indx] #restrict cursor to data points
            #     x = event.xdata
            #     line.set_xdata([x, x])
            #     self.draw_idle()
    
    def updateCursor(self, cursor, x):
        # if ybound == None:
        ymin, ymax = [], []
        for line in self.axes.lines:
            if line in [self.cursor1, self.cursor2]:
                continue
            ydata = line.get_ydata()
            ymin.append(min(ydata))
            ymax.append(max(ydata))
            
        # yticks = self.axes.get_yaxis().get_ticklocs()
        ybound = [min(ymin), max(ymax)]
        print("ybound", ybound)
        cursor.set_xdata([x, x])
        cursor.set_ydata(ybound)
    
    def releaseonclick(self, event, artist):
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
            # turn off the rect animation property and reset the background
            artist.set_animated(False)
            self.background = None
            # redraw the full figure
            self.draw()
            self.draw_idle()
            self.updateBackground()
            
    def resizeWindow(self, event):
        print("resize")
        # self.tight_layout()
        self.draw()
        self.draw_idle()
        self.updateBackground()
    
    def toggleAnimation(self, state):
        for key in self.artistDict.keys():
            self.artistDict[key].set_animated(state)
        # if self.cursor1 != None:
        #     self.cursor1.set_animated(state)
        # if self.cursor2 != None:
        #     self.cursor2.set_animated(state)
        # self.draw()
    
    def updateBackground(self):        
        self.axes.get_figure().tight_layout()        
        self.toggleAnimation(True)
        self.draw()
        if self.fixYLimits == True:
            self.background = self.copy_from_bbox(self.axes.bbox)
        else:
            self.background = self.copy_from_bbox(self.axes.get_tightbbox(self.get_renderer()))
        # self.background = self.copy_from_bbox(self.axes.bbox)
        self.toggleAnimation(False)
        self.draw()
            
#complete figure widget with toolbar
class PlotWidget(QWidget):
    
    def __init__(self, fig, xdata = None, cursor1_init = None,
                 cursor2_init = None, *args, **kwargs):
##        super(QWidget, self).__init__(*args, **kwargs)
        super().__init__()
        # self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle("Plot")
        self.fig = fig
        self.xdata = xdata
        self.cursor1_init = cursor1_init
        self.cursor2_init = cursor2_init
        self.fig_close = True
        self.home()
        
    def home(self):
        self.wid = Plot2Widget(fig = self.fig,
                               xdata = self.xdata,
                               cursor1_init = self.cursor1_init,
                               cursor2_init = self.cursor2_init)
        plotToolbar = NavigationToolbar(self.wid, self)
        
        # plotGroupBox = QGroupBox()
        # plotlayout=QGridLayout()
        # plotGroupBox.setLayout(plotlayout)
        # plotlayout.addWidget(plotToolbar, 0, 0, 1, 1)
        # plotlayout.addWidget(self.wid, 1, 0, 1, 1)
        
        layout=QGridLayout()
        layout.addWidget(plotToolbar, 0, 0, 1, 1)
        layout.addWidget(self.wid, 1, 0, 1, 1)
        
        self.setLayout(layout)
        # self.show()
        # startFitLabel = QLabel("Start (%):")
    
    def closeEvent(self, event): #close widget
        print("closing plot")
        self.fig_close = True
        
