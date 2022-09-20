from cProfile import label
from ctypes import alignment
from email.charset import QP
from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QObject
from PyQt5.QtGui import QMouseEvent, QKeyEvent
import string

from shared import Config
from shared import Colors

class Cell (QWidget):
    
    widget: QWidget
    label: QLabel
    topLeft: QPoint
    # size: QSize
    # rect: QWidget
    num: int
    ifMoved: bool
    
    pen: QPen       # границы
    brush: QBrush   # заливка
    qp: QPainter    # рисовалка
    
    def __init__(self, widget: QWidget, xpos: int=50, ypos: int=50, num: int=0, ifMoved: bool=False):
        super().__init__(widget)
        # self.widget = widget
        self.pos = QPoint(xpos, ypos)
        # self.size = QSize
        # super().pos = 
        
        # self.topLeft = QPoint(xpos, ypos)
        self.resize(Config.CELL_SIZE, Config.CELL_SIZE)
        self.setStyleSheet("background-color:" + Colors.GREEN_STR)
        # self.rect = QWidget(self.pos, self.size)
        # self.rect.pos = self.pos
        
        self.label = QLabel(self)
        # self.label.setGeometry(self.rect)
        self.label.setGeometry(self.frameGeometry())
        # self.label.pos = self.pos
        # self.label.setAutoFillBackground(True)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.pen = QPen(Colors.DARK_GREEN) 
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(Colors.GREEN)
        
        self.setNum(num)
        self.setIfMoved(ifMoved)
        # self.initPainter()
    
    # def setPos(self, pos: QPoint) -> None:
    #     self.pos = pos
        # self.rect.setTopLeft(self.pos)
        # self.label.setGeometry(self.rect)
        
    def draw(self) -> None:
        pass
        # self.initPainter()
        
        # self.qp.drawRect(self.rect)
        # self.show()
        # self.label.setVisible(True)
        # self.qp.end()
    
    def initPainter(self) -> None:
        '''
        Инициализация рисовалки
        '''
        self.qp = QPainter(self.widget)
        self.qp.setPen(self.pen)
        self.qp.setBrush(self.brush)
        self.qp.setRenderHints(QPainter.Antialiasing)
        
    def setNum (self, num: int) -> None:
        '''
        Задаёт число в ячейке
        Если число 0, значит ячейка пуста
        '''
        self.num = num
        # if self.num != 0:
        self.label.setText("<font color='white'>" + str(self.num) + "</font>")
        # else:
        #     self.label.setText("")
        #     self.brush.setColor(Colors.DARK_GREEN)
        
    def setIfMoved (self, ifMoved: bool) -> None:
        '''
        Была ли ячейка сдвинута? Если да, от меняем цвет ячейки на красный
        '''
        self.ifMoved = ifMoved
        if (not self.ifMoved):
            self.brush.setColor(Colors.GREEN)
        else:
            self.brush.setColor(Colors.RED)
        
            
        ####