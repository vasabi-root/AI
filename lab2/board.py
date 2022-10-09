import enum
from operator import length_hint
from time import sleep
from typing import List
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, qApp
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import ( 
    Qt, QPoint, QRect, QSize, QPropertyAnimation, QThreadPool,
    QEasingCurve, QSequentialAnimationGroup, QParallelAnimationGroup
)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QRunnable
from PyQt5.QtGui import QMouseEvent, QKeyEvent

import heapq

import numpy as np
from cell import Cell
from shared import Colors

from shared import Config
from node import Node, PrioritizedItem
from node import solve_func, solve_step, manhattan_distance, fnnm_distance, cost_criterion

from XLSXmaker import XLSXmake


class Board:
    '''
    Доска 3х3 ячейки с 8 элементами
    '''
    
    widget: QWidget 
    matrix: [[Cell]]                # матрица ячеек (для фронта)
    root: Node                      # корень дерева решений
    node: Node                      # текущее состояние (для алгоритма)
    rect: QRect                     # полотно под ячейками
    topLeft: QPoint                 # позици доски
    fringer: [[Node]]               # кайма (нераскрытые узлы дерева)
    m: int                          # размерность доски
    solution: ([[Node]], int, int)  # [0]: путь от начала в конец (если существует) 
                                    # [1]: емкостная сложность
                                    # [2]: временная сложность
    
    
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
        self.solution = ([], 0, 0)
    
    def makeRoot(self, state: List[List]) -> None:
        '''
        Создание корня дерева
        '''
        self.fringer = []
        self.initZero(state)
        self.root = Node(state=state, i=self.z_row, j=self.z_col)
        self.node = self.root
        self.setMatrix(state)
        
    def initZero(self, state) -> None:
        for i in range (self.m):
            for j in range (self.m):
                if (state[i][j] == 0):
                    self.z_row = i
                    self.z_col = j
                    return

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
                    
    def initBoard(self, is_astar: bool, is_manh: bool) -> None:
        self.solution = [], 0, 0
        self.fringer: List[PrioritizedItem] = [PrioritizedItem(0, self.root)]  # Очередь с приоритетом
        self.root.children = []
        self.traversed = set()
        self.h = manhattan_distance if is_manh else fnnm_distance
        self.g = cost_criterion if is_astar else lambda x: 0
        heapq.heapify(self.fringer)
        self.node = self.root
        self.path = []
        
        self.makeStepRight()
        
    def makeStepRight(self) -> None:
        node = None
        if (not self.node.is_target(self.end)):
            if (len(self.fringer) > 0):
                while (node == None):
                    node = solve_step(
                        self.node,
                        self.end,
                        self.traversed,
                        self.fringer,
                        self.h,
                        self.g
                    )
                self.path.append(node)
                if (len(self.path) >= 2):
                    if (node.parent == self.node):
                        r1 = self.node.z_row 
                        c1 = self.node.z_col
                        
                        r2 = node.z_row
                        c2 = node.z_col
                        
                        self.node = node
                        self.matrix[r1][c1], self.matrix[r2][c2] = self.matrix[r2][c2], self.matrix[r1][c1]
                        self.animeStep(r1, c1)
                        self.anim.start()
                    else:
                        self.animeFull(start=self.node.state, end=node.state)
                        self.group.start()
                self.node = node
                self.setChildrenColor(self.node)
                
    def makeStepLeft(self) -> None:
        if (len(self.path) >= 2):
            self.node = self.path.pop()
            for child in self.node.children:
                for item in self.fringer:
                    if (child == item.node):
                        self.fringer.remove(item)
                # self.fringer.remove(child)
            heapq.heappush(self.fringer, PrioritizedItem(self.node.cost, self.node))
            self.traversed.remove(self.node.hashable_state)
            self.animeFull(start=self.node.state, end=self.path[-1].state)
            self.node = self.path[-1]
            self.group.start()
            self.setChildrenColor(self.node)
        
    def setChildrenColor(self, node: Node) -> None:
        self.refreshColors()
        if (len(node.children) > 0):
            for i,child in enumerate(node.children):
                cell = self.matrix[child.z_row][child.z_col]
                cell.setCost(child.colorCost)
                cell.h = child.h
                cell.g = child.g
                cell.depth = child.depth
                cell.cellClicked.connect(self.widget.cellClickedEvent)
                if (i == 0):
                    cell.clicked.emit()
        else:
            cell = self.matrix[(self.node.z_row+1) % 3][0]
            cell.h = 0
            cell.g = self.node.depth
            cell.depth = self.node.depth
            cell.cellClicked.connect(self.widget.cellClickedEvent)
            cell.clicked.emit()
        
    
            
    def refreshColors(self) -> None:
        for row in self.matrix:
            for cell in row:
                if cell != 0:
                    cell.setDefault()
    
    def refresh(self) -> None:
        if (self.node != None):
            self.refreshColors()
            self.animeFull(self.node.state, self.start)
            self.node = self.root

    def solve(self, isAstar: bool=False, isManh: bool=False) -> bool:
        '''
        Переход к следующей вершине (фронт)
        '''
        self.solution = solve_func(self.root, self.end, isAstar, isManh)
        if (len(self.solution[0]) > 0):
            self.makeAnime()
            self.node = self.solution[0][-1]
            return True # решение существует
        return False    # решения нет
    
    # def stepRight(self) -> None:
        
        
    # def chooseDFSDL_next(self, depth) -> bool:
    #     pass
        
    def makeAnime(self, isReversed: bool=False) -> None:
        if ( len(self.solution[0]) <= 10000 / Config.SLOW_ANIME): # len(self.solution[0]) > 0 and
            path = self.solution[0].copy()
            if isReversed: 
                path.reverse()
                self.solution = ([], 0, 0)
            path.remove(path[0])
            self.group = QSequentialAnimationGroup(self.widget)
            for node in path:
                r1 = self.node.z_row 
                c1 = self.node.z_col
                
                r2 = node.z_row
                c2 = node.z_col
                
                self.node = node
                self.matrix[r1][c1], self.matrix[r2][c2] = self.matrix[r2][c2], self.matrix[r1][c1]
                self.animeStep(r1, c1, isReversed)
        else:
            start = self.root.state
            end = self.end
            if (isReversed):
                start, end = end, start
            self.animeFull(start=start, end=end)
    
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
        
    def animeStep (self, row: int, col: int, isReversed: bool=False) -> None:
        t = Config.FAST_ANIME if (isReversed) else Config.SLOW_ANIME
        x = self.topLeft.x() + Config.CELL_SIZE*col
        y = self.topLeft.y() + Config.CELL_SIZE*row
        self.anim = QPropertyAnimation(self.matrix[row][col], b"pos")
        self.anim.setEndValue(QPoint(x, y))
        self.anim.setDuration(t)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.group.addAnimation(self.anim)

    def animeFull (self, start: [[int]], end: [[int]]) -> None:
            
        self.group = QParallelAnimationGroup(self.widget)
        matrix = []
        for row in range(self.m):
            matrix.append([])
            for col in range(self.m):
                (r, c) = Config.index2d(start, end[row][col])
                matrix[row].append(self.matrix[r][c])
                if (self.matrix[row][col] != 0):
                    (r, c) = Config.index2d(end, start[row][col])
                    x = self.topLeft.x() + Config.CELL_SIZE*c
                    y = self.topLeft.y() + Config.CELL_SIZE*r

                    self.anim = QPropertyAnimation(self.matrix[row][col], b"pos")
                    self.anim.setEndValue(QPoint(x, y))
                    self.anim.setDuration(Config.SLOW_ANIME)
                    self.anim.setEasingCurve(QEasingCurve.OutCubic)
                    self.group.addAnimation(self.anim)
        self.matrix = matrix
        

