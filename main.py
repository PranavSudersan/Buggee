# %% Main Application Call

import sys
import traceback as tb
import os
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen


#include source dirctory into module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.app.mainwindow import MainWindow

# if __name__ == "__main__":
def except_hook(cls, exception, traceback): #display error message/print traceback
##    print(dir(traceback))   
    trace = 'Traceback:\n' + ''.join(tb.extract_tb(traceback).format())
    
    msgBox = QMessageBox()
    msgBox.setWindowTitle("ERROR!")
    msgBox.setText(cls.__name__)
    msgBox.setInformativeText(str(exception))
    msgBox.setDetailedText(trace)
    msgBox.exec()    
 
    sys.__excepthook__(cls, exception, traceback)
         
def run():
    app = QApplication(sys.argv)
    pixmap = QPixmap("images/splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()
    screen_resolution = app.desktop().screenGeometry()
    w, h = screen_resolution.width(), screen_resolution.height()
    app.setWindowIcon(QIcon('images/icon.ico'))
    file = QFile("style/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    Gui = MainWindow(0.9*w,0.9*h)
    Gui.setWindowIcon(QIcon('images/icon.ico'))
    # sys.exit(app.exec_())
    Gui.show()
    splash.finish(Gui)
    app.exec_()

sys.excepthook = except_hook
run()