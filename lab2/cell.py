from PyQt5.QtWidgets import QWidget, QPushButton, QStyleOptionButton
from PyQt5.QtCore import QPropertyAnimation, QPoint, QRect, QSize

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
    
    num: int # значение фишки
    
    def __init__(self, widget: QWidget, xpos: int=50, ypos: int=50, num: int=0, isMoved: bool=False):
        super().__init__(widget)
        self.setGeometry(QRect(QPoint(xpos, ypos), QSize(Config.CELL_SIZE, Config.CELL_SIZE)))
        self.setNum(num)
        self.setIsMoved(isMoved)
        
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
    
    def setIsMoved (self, isMoved: bool) -> None:
        '''
        Была ли ячейка сдвинута? Если да, то меняем цвет ячейки на красный
        '''
        self.isMoved = isMoved
        defStyle = self.getDefStyle()
        if (not self.isMoved):
            self.setStyleSheet(defStyle + "background-color: " + Colors.GREEN_STR)
        else:
            self.setStyleSheet(defStyle + "background-color: " + Colors.RED_STR)
        
    def anime(self) -> None:
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setEndValue(QPoint(400, 400))
        self.anim.setDuration(1500)
        self.anim.start()
        
    # def draw(self) -> None:
    #     pass