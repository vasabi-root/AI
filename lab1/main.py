from PyQt5.QtWidgets import QApplication
import sys

from main_window import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.installEventFilter(window)
    app.exec_()