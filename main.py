# %% Main Application Call

import sys
import traceback as tb
import os
import logging
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen

__app__ = 'Buggee'
__version__ = '1.6'
__author__ = 'Pranav Sudersan'
__email__ = 'pranavsudersan@gmail.com'
__license__ = 'MIT'

#include source dirctory into module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# configure logger
file_handler = logging.FileHandler(filename='LOG.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s <%(filename)s line %(lineno)d> %(levelname)s:: %(message)s')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter('<%(filename)s line %(lineno)d> %(levelname)s:: %(message)s')
stream_handler.setFormatter(stream_formatter)
stream_handler.setLevel(logging.DEBUG)

logging.basicConfig(handlers=[file_handler, stream_handler],
                    level = logging.DEBUG)

from source.app.mainwindow import MainWindow

# if __name__ == "__main__":
def except_hook(cls, exception, traceback): #display error message/print traceback
    
    trace = 'Traceback:\n' + ''.join(tb.extract_tb(traceback).format())
    
    logging.error(cls.__name__ + ':' + str(exception) + '\n\n' + trace)
    
    msgBox = QMessageBox()
    msgBox.setWindowTitle("ERROR!")
    msgBox.setText(cls.__name__)
    msgBox.setInformativeText(str(exception))
    msgBox.setDetailedText(trace)
    msgBox.exec()
    sys.__excepthook__(cls, exception, traceback)
         
def run():
    logging.info('APP OPENED ' + __app__ + ' v' + __version__)
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
    Gui = MainWindow(width = 0.95*w,
                     height = 0.9*h,
                     appname = __app__,
                     version = __version__)
    Gui.setWindowIcon(QIcon('images/icon.ico'))

    Gui.show()
    splash.finish(Gui)
    app.exec_()

sys.excepthook = except_hook

try:
    run()
except Exception as e:
    logging.exception('APP CRASHED!\n' + str(e) + '\n\n' + str(tb.format_exc()))
finally:
    logging.info('APP CLOSED')   
    logger = logging.getLogger()
    while logger.hasHandlers():
        for hdl in logger.handlers:
            hdl.close()
            logger.removeHandler(hdl)
    logging.shutdown()