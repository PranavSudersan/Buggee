# %% Main Application Call

import sys
import os
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from tkinter import messagebox, Tk

#include root dirctory into module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from current.app.mainwindow import MainWindow

if __name__ == "__main__":
    def except_hook(cls, exception, traceback): #display error message/print traceback
    ##    print(dir(traceback))   
        root = Tk()
        root.withdraw()
        messagebox.showinfo(cls.__name__, str(exception) + '\n\nTraceback: ' +
                            str(traceback.tb_frame))
        root.destroy()    
        sys.__excepthook__(cls, exception, traceback)
             
    def run():
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('images/icon.ico'))
        file = QFile("style/dark.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
        Gui = MainWindow()
        Gui.setWindowIcon(QIcon('images/icon.ico'))
        # sys.exit(app.exec_())
        Gui.show()
        app.exec_()
    
    sys.excepthook = except_hook
    run()