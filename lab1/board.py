from operator import length_hint
from time import sleep
from typing import List
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, qApp
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import ( 
    Qt, QPoint, QRect, QSize, QPropertyAnimation, QThreadPool,
    QEasingCurve, QSequentialAnimationGroup, QRunnable, QAbstractAnimation
)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QRunnable
from PyQt5.QtGui import QMouseEvent, QKeyEvent


import numpy as np
from cell import Cell
from search import Search
from shared import Colors

from shared import Config
from node import Node, dfs, dfs_depth

from XLSXmaker import XLSXmake


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
    path: List[List[Node]]      # путь от начала в конец (если существует)
    
    
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
        self.path = []
    
    def makeRoot(self, state: List[List]) -> None:
        '''
        Создание корня дерева
        '''
        self.fringer = []
        self.root = Node(state=state, i=2, j=2)
        self.node = self.root
        self.setMatrix(state)

    def setMatrix(self, state: List[List]) -> None:
        '''
        Инициализация матрицы фишек (фронт)
        '''
        self.matrix = []
        for i in range(self.m):
            self.matrix.append([])
            ypos = self.topLeft.y() + i*Config.CELL_SIZE
            for j in range(self.m):
                xpos = self.topLeft.x() + j*Config.CELL_SIZE
                if (state[i][j] == 0):
                    self.matrix[i].append(0)
                else:
                    self.matrix[i].append(Cell(self.widget, xpos, ypos, state[i][j]))
                    
    def solve(self, DFSDL: bool, depth: int=50) -> bool:
        '''
        Переход к следующей вершине (фронт)
        '''
        if (len(self.path) == 0):
            if not DFSDL:
                self.path = dfs(self.root, self.end)
                XLSXmake(self.path, "DFS.xlsx")
            else:
                self.path = dfs_depth(self.root, self.end, depth)
                XLSXmake(self.path, "DFS_DL.xlsx")
                # self.node.DFSDLopen(self.fringer, depth)
                # next = self.node.DFSDLnext(depth)
        if (len(self.path) > 0):
            # Текущее положение пустой клетки
            self.makeAnime()
            return True # решение существует
        return False    # решения нет
        
    # def chooseDFSDL_next(self, depth) -> bool:
    #     pass
        
    def makeAnime(self, isReversed: bool=False) -> None:
        path = self.path.copy()
        if isReversed: 
            path.reverse()
            self.path = []
        path.remove(path[0])
        self.group = QSequentialAnimationGroup(self.widget)
        for node in path:
            r1 = self.node.z_row 
            c1 = self.node.z_col
            
            r2 = node.z_row
            c2 = node.z_col
            
            self.node = node
            self.matrix[r1][c1], self.matrix[r2][c2] = self.matrix[r2][c2], self.matrix[r1][c1]
            self.anime(r1, c1, isReversed)
    
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
        
    def anime (self, row: int, col: int, isReversed: bool) -> None:
        t = 50 if (isReversed) else 150
        x = self.topLeft.x() + Config.CELL_SIZE*col
        y = self.topLeft.y() + Config.CELL_SIZE*row
        self.anim = QPropertyAnimation(self.matrix[row][col], b"pos")
        self.anim.setEndValue(QPoint(x, y))
        self.anim.setDuration(t)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.group.addAnimation(self.anim)
        
