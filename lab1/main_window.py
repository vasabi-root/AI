from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QKeyEvent, QResizeEvent, QMouseEvent, QWheelEvent
from PyQt5.QtCore import QEvent, Qt

from shared import Config
from interface import Interface

class Window(QMainWindow):
    '''
    Класс окна приложения. В нем содержится ссылка на интерфейс,
    который реализует всю анимацию и логику приложения.
    '''
    
    def __init__(self) -> None:
        super().__init__()
        self.title = "VECTOR-SQUAD AI LAB-1"
        
        self.interface = Interface()
        # self.interface = Test()
        self.initWindow()
        
        self.setCentralWidget(self.interface)
        
    def initWindow(self):
        '''
        Инициализация окна. Устанавливаем отступы и размеры.
        '''
        self.setWindowTitle(self.title)

        self.setGeometry(
            Config.WINDOW_TOP_PAD, 
            Config.WINDOW_LEFT_PAD, 
            Config.WINDOW_WIDTH, 
            Config.WINDOW_HEIGHT
        )
        self.setFixedSize(
            Config.WINDOW_WIDTH, 
            Config.WINDOW_HEIGHT
        )
        self.show()
    
    # def mousePressEvent(self, mouse: QMouseEvent) -> None:
    #     '''
    #     Ловим события нажатия мышки и передаем обработку события интерфейсу.
    #     '''
    #     self.interface.mousePressEvent(mouse)
    
    # def keyPressEvent(self, key: QKeyEvent) -> None:
    #     '''
    #     Ловим события нажатия на клавишы и передаем обработку события интерфейсу.
    #     '''
    #     self.interface.keyPressEvent(key)

    # def keyReleaseEvent(self, key: QKeyEvent) -> None:
    #     self.interface.keyReleaseEvent(key)

    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     self.interface.axis.setCenterCoords(
    #         self.width() // 2,
    #         self.height() // 2,
    #     )
    
    # def wheelEvent(self, wheel: QWheelEvent) -> None:
    #     self.interface.wheelEvent(wheel)
        

