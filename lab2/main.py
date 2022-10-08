from PyQt5.QtWidgets import QApplication
import sys

from main_window import Window

def exception_hook(ectype, val, traceback):
    print(ectype, val, traceback)
    sys._excepthook(ectype, val, traceback)
    sys.exit(1)

if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.installEventFilter(window)
    app.exec_()

