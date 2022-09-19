from operator import length_hint
from time import sleep
from typing import List
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, qApp
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtGui import QMouseEvent, QKeyEvent

import numpy as np
from cell import Cell
from node import Node
from shared import Colors

from shared import Config

class Board:
    '''
    Доска 3х3 ячейки с 8 элементами
    '''
    
    widget: QWidget 
    matrix: List[List[Cell]]    # матрица ячеек (для фронта)
    root: Node                  # корень дерева решений
    node: Node                  # текущее состояние (для алгоритма)
    rect: QRect                 # полотно под ячейками
    topLeft: QPoint             # позици доски
    fringer: List[List[Node]]   # кайма (нераскрытые узлы дерева)
    m: int                      # размерность доски
    
    
    def __init__(self, widget: QWidget, topLeft: QPoint, start: List[List[int]], end: List[List[int]]=None):
        self.widget = widget
        self.topLeft = topLeft
        self.start = start
        self.end = end
        self.m = len(self.start)
        
        self.makeRoot(self.start)
        
        self.rect = QRect(self.topLeft, QSize(self.m * Config.CELL_SIZE, self.m * Config.CELL_SIZE))
        
        self.pen = QPen(Colors.DARK_GREEN)
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(Colors.DARK_GREEN)
        self.group = QSequentialAnimationGroup(self.widget)
    
    def makeRoot(self, ar: List[List]) -> None:
        '''
        Создание корня дерева
        '''
        self.fringer = []
        self.root = Node(ar, fringer=self.fringer)
        self.node = self.root
        self.setMatrix(ar)

    def setMatrix(self, ar: List[List]) -> None:
        '''
        Инициализация матрицы фишек (фронт)
        '''
        self.matrix = []
        for i in range(self.m):
            self.matrix.append([])
            ypos = self.topLeft.y() + i*Config.CELL_SIZE
            for j in range(self.m):
                xpos = self.topLeft.x() + j*Config.CELL_SIZE
                if (ar[i][j] == 0):
                    self.matrix[i].append(0)    
                else:
                    self.matrix[i].append(Cell(self.widget, xpos, ypos, ar[i][j]))
                    
    def chooseNext(self, DFSDL: bool, depth: int=50) -> bool:
        '''
        Переход к следующей вершине (фронт)
        '''
        if not DFSDL:
            self.node.DFSopen(self.fringer)
            next = self.node.DFSnext()
        else:
            self.node.DFSDLopen(self.fringer, depth)
            next = self.node.DFSDLnext(depth)
            
        if next != None:
            # Текущее положение пустой клетки
            r1 = self.node.z_row 
            c1 = self.node.z_col
            
            r2 = next.z_row
            c2 = next.z_col
            self.node = next
            
            self.matrix[r1][c1], self.matrix[r2][c2] = self.matrix[r2][c2], self.matrix[r1][c1]
            self.anime(r1, c1)
            return True
        return False
        
    def chooseDFSDL_next(self, depth) -> bool:
        pass
        
    
    def draw(self) -> None:
        self.initPainter()
        self.qp.drawRect(self.rect)
            
        self.qp.end()
        
    # def getState(self) -> int
    
    def initPainter(self) -> None:
        '''
        Инициализация рисовалки
        '''
        self.qp = QPainter(self.widget)
        self.qp.setPen(self.pen)
        self.qp.setBrush(self.brush)
        self.qp.setRenderHints(QPainter.Antialiasing)
        
    def anime (self, row, col) -> None:
        x = self.topLeft.x() + Config.CELL_SIZE*col
        y = self.topLeft.y() + Config.CELL_SIZE*row
        self.anim = QPropertyAnimation(self.matrix[row][col], b"pos")
        self.anim.setEndValue(QPoint(x, y))
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.group.addAnimation(self.anim)
        # self.anim.start()
        
        