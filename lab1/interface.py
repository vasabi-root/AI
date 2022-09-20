from asyncio import wait_for
from compileall import compile_file
from time import sleep
from typing import List
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import Qt, QPoint, QPointF, QSize, QRect, QSequentialAnimationGroup
from PyQt5.QtGui import QMouseEvent, QKeyEvent
import numpy as np

from board import Board
from shared import Config, Colors
from animated_toggle import AnimatedToggle

class Interface(QWidget):
    '''
    Главный класс приложения. В нем подключается и реализуется вся логика приложения.
    '''
    
    qp: QPainter
    
    board: Board
    
    def __init__(self) -> None:
        super().__init__()
        
        self.qp = QPainter()                # Просто специальная рисовалка
        # ar = [ [1, 2, 3],
        #        [4, 0, 5],
        #        [6, 7, 8] ]
        
        self.depth = 50
        self.initBoards()
        self.initLabels()
        self.initButtons()
        
        
    def paintEvent(self, event) -> None:
        '''
        Событие рисования на экране. Вызывается при вызове метода self.update()
        '''
        self.qp.begin(self)
        self.draw()
        self.qp.end()
        
    def draw(self) -> None:
        self.clearScreen()
        self.startBoard.draw()
        self.endBoard.draw()
        self.animeBoard.draw()
        # self.cell.draw()
        # self.board.draw()
        # self.table.drawFrame(self.qp)        
        
    def clearScreen(self) -> None:
        '''
        Очистка экрана
        '''
        w = self.size().width()
        h = self.size().height()

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        # brush.setColor(Colors.GREY)
        brush.setColor(Colors.LIGHT_GREEN)
        
        self.qp.setBrush(brush)
        self.qp.drawRect(-1, -1, w+1, h+1)
        
    def initBoards(self) -> None:
        start = [ [3, 6, 4],
                  [2, 5, 8],
                  [7, 1, 0] ]
        self.startBoard = Board(self, QPoint(Config.CELL_SIZE, Config.CELL_SIZE*3), start)
        end = [ [3, 6, 4],
                [2, 0, 1],
                [7, 8, 5] ]
        self.endBoard = Board(
            self, 
            QPoint(Config.WINDOW_WIDTH - (Config.CELL_SIZE*4), Config.CELL_SIZE*3), 
            end
        )
        self.animeBoard = Board(
            self, 
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*1.5), Config.CELL_SIZE*7).toPoint(), 
            start, 
            end
        )
        # self.animeBoard.matrix[0][0].setIsMoved(True)
    
    def initLabels(self) -> None:
        self.startLabel = QLabel("START", self)
        self.startLabel.setGeometry(QRect(
            QPoint(Config.CELL_SIZE, Config.CELL_SIZE*2),
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.startLabel.setAlignment(Qt.AlignCenter)
        
        self.endLabel = QLabel("END", self)
        self.endLabel.setGeometry(QRect(
            QPoint(Config.WINDOW_WIDTH - (Config.CELL_SIZE*4), Config.CELL_SIZE*2), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.endLabel.setAlignment(Qt.AlignCenter)
        
        self.solLabel = QLabel("SOLUTION", self)
        self.solLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*1.5), Config.CELL_SIZE*6).toPoint(), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.solLabel.setAlignment(Qt.AlignCenter)
        
        self.arrowLabel = QLabel("--------------->", self)
        self.arrowLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*2), Config.CELL_SIZE*4).toPoint(), 
            QSize(Config.CELL_SIZE*4, Config.CELL_SIZE)
        ))
        self.arrowLabel.setAlignment(Qt.AlignCenter)
        
        self.depthLabel = QLabel("DEPTH:", self)
        self.depthLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*2), Config.CELL_SIZE*3-2).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        self.depthLabel.setAlignment(Qt.AlignCenter)
        
        self.depthText = QTextEdit(str(self.depth) ,self)
        self.depthText.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2, Config.CELL_SIZE*3).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        # self.depthText.enterEvent.connect()
        self.depthLabel.setVisible(False)
        self.depthText.setVisible(False)
        
        
        self.DFSLabel = QLabel("DFS", self)
        self.DFSLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*2), Config.CELL_SIZE).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.DFSLabel.setAlignment(Qt.AlignCenter)
        
        self.DFSDLLabel = QLabel("DFS (depth limit)", self)
        self.DFSDLLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 + (Config.CELL_SIZE/2), Config.CELL_SIZE).toPoint(), 
            QSize(Config.CELL_SIZE*4, Config.CELL_SIZE)
        ))
        self.DFSDLLabel.setAlignment(Qt.AlignCenter)
        
    def initButtons(self) -> None:
        self.solveButton = QPushButton(self)
        self.solveButton.setText("SOLVE")
        self.solveButton.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*1.5), Config.CELL_SIZE*11).toPoint(), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.solveButton.setStyleSheet(
            "QPushButton:hover {" + \
                "border: none;" + \
                "outline: none;" + \
            "}" + \
            "QPushButton {" + \
                "border-color:" + Colors.DARK_GREEN_STR + ";" + \
                "border-style: solid;" + \
                "border-radius: 2px;" + \
                "border-width: 3px;" + \
                "color: white;" + \
                "text-align: center;" + \
                "background-color: " + Colors.GREEN_STR + \
            "}" + \
            "QPushButton:pressed {" + \
                "border: none;" + \
                "outline: none;" + \
                "color: white;" + \
                "text-align: center;" + \
                "background-color: " + Colors.DARK_GREEN_STR + \
            "}"
        )
        self.solveButton.pressed.connect(self.solvePressedEvent)
        
        
        self.toggle = AnimatedToggle(self)
        self.toggle.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE), Config.CELL_SIZE+2).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        self.toggle.stateChanged.connect(self.DFSDL_show)
    
    def DFSDL_show(self) -> None:
        self.depthLabel.setVisible(not self.depthLabel.isVisible())
        self.depthText.setVisible(not self.depthText.isVisible())
        
    
    def solvePressedEvent(self) -> None:
        '''
        Обработка нажатия на солв
        '''
        self.animeBoard.group = QSequentialAnimationGroup(self)
        if (int(self.toggle.handle_position) == 0):
            if (self.animeBoard.chooseNext(DFSDL=0)):
                self.animeBoard.group.start()
            else:
                print('Not solved!')
                pass
        else:
            self.depth = int(self.depthText.toPlainText())
            if (self.animeBoard.chooseNext(DFSDL=1,depth=self.depth)):
                self.animeBoard.group.start()
        