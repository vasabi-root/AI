from PyQt5.QtWidgets import QWidget, QPushButton, QStyleOptionButton
from PyQt5.QtCore import QPropertyAnimation, QPoint, QRect, QSize, pyqtSignal

from shared import Colors, Config

# class TestCell(QWidget):
#     def __init__(self, widget: QWidget) -> None:
#         super().__init__(widget)
#         self.setStyleSheet("background-color:" + Colors.GREEN_STR)
#         self.resize(100, 100)
#         # self.pos = QPoint(10, 10)
#         self.show()
        
#     def anime(self) -> None:
#         self.anim = QPropertyAnimation(self, b"pos")
#         self.anim.setEndValue(QPoint(400, 400))
#         self.anim.setDuration(1500)
#         self.anim.start()

class Cell(QPushButton):
    
    num: int # значение фишк
    cellClicked = pyqtSignal(int, int, int)
    
    def __init__(self, widget: QWidget, xpos: int=50, ypos: int=50, num: int=0):
        super().__init__(widget)
        self.h = 0
        self.g = 0
        self.depth = 0
        self.clicked.connect(lambda _: self.cellClicked.emit(self.h, self.g, self.depth))
        self.setGeometry(QRect(QPoint(xpos, ypos), QSize(Config.CELL_SIZE, Config.CELL_SIZE)))
        self.setNum(num)
        self.setDefault()
        
    def getDefStyle(self) -> str:
        return  "border-color:" + Colors.DARK_GREEN_STR + ";" + \
                "border-style: solid;" + \
                "border-radius: 2px;" + \
                "border-width: 1px;" + \
                "color: white;" + \
                "text-align: center;"
    
    def setNum (self, num: int) -> None:
        '''
        Задаёт число в фишке
        '''
        self.num = num
        self.setText(str(self.num))
    
    def setDefault(self) -> None:
        '''
        Была ли ячейка сдвинута? Если да, то меняем цвет ячейки на красный
        '''
        defStyle = self.getDefStyle()
        self.setStyleSheet(defStyle + "background-color: " + Colors.GREEN_STR)
            
    def setCost (self, cost: int) -> None:
        '''
        Была ли ячейка сдвинута? Если да, то меняем цвет ячейки на красный
        '''
        self.isMoved = False
        
        defStyle = self.getDefStyle()
        r = hex(235 - cost*40)[2:3]
        g = hex(195 - cost*40)[2:3]
        b = hex(0)[2:3]
        
        c = '#' + r+g+b
        
        self.setStyleSheet(defStyle + "background-color: " + c)
        
    def anime(self) -> None:
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setEndValue(QPoint(400, 400))
        self.anim.setDuration(1500)
        self.anim.start()
        
    # def draw(self) -> None:
    #     pass