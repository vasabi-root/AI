from asyncio import wait_for
from compileall import compile_file
from email import message
import imp
from time import sleep
from typing import List
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import (
    Qt, QPoint, QPointF, QSize, QRect, 
    QSequentialAnimationGroup, QRunnable, QThreadPool
)
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtGui import QMouseEvent, QKeyEvent
import numpy as np
import os

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
        
        self.click = QSound("click1.wav")
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
        ends = list()
        ends.append( [ [2, 3, 4], [0, 6, 1], [7, 8, 5] ])
        ends.append( [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ])
        ends.append( [ [3, 6, 4], [2, 5, 8], [7, 0, 1] ])
        ends.append( [ [3, 6, 4], [2, 5, 0], [7, 1, 8] ])
        end = ends[0]
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
    
    def initLabels(self) -> None:
        self.startLabel = QLabel("START", self)
        self.startLabel.setGeometry(QRect(
            QPoint(Config.CELL_SIZE, Config.CELL_SIZE*2),
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.startLabel.setAlignment(Qt.AlignCenter)
        self.startLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.endLabel = QLabel("END", self)
        self.endLabel.setGeometry(QRect(
            QPoint(Config.WINDOW_WIDTH - (Config.CELL_SIZE*4), Config.CELL_SIZE*2), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.endLabel.setAlignment(Qt.AlignCenter)
        self.endLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.solLabel = QLabel("SOLUTION", self)
        self.solLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*1.5), Config.CELL_SIZE*6).toPoint(), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.solLabel.setAlignment(Qt.AlignCenter)
        self.solLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.arrowLabel = QLabel("--------------->", self)
        self.arrowLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*2), Config.CELL_SIZE*4).toPoint(), 
            QSize(Config.CELL_SIZE*4, Config.CELL_SIZE)
        ))
        self.arrowLabel.setAlignment(Qt.AlignCenter)
        self.arrowLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.depthLabel = QLabel("DEPTH:", self)
        self.depthLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*2), Config.CELL_SIZE*3-2).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        self.depthLabel.setAlignment(Qt.AlignCenter)
        self.depthLabel.setStyleSheet(Config.LABEL_CONF)
        
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
        self.DFSLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.DFSDLLabel = QLabel("DFS (depth limit)", self)
        self.DFSDLLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 + (Config.CELL_SIZE/1.5), Config.CELL_SIZE).toPoint(), 
            QSize(Config.CELL_SIZE*4, Config.CELL_SIZE)
        ))
        self.DFSDLLabel.setAlignment(Qt.AlignCenter)
        self.DFSDLLabel.setStyleSheet(Config.LABEL_CONF)
        
    def initButtons(self) -> None:
        self.solveButton = QPushButton(self)
        self.solveButton.setText("SOLVE")
        self.solveButton.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*1.5), Config.CELL_SIZE*11).toPoint(), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.solveButton.setStyleSheet(Config.BUTTON_CONF)
        self.solveButton.pressed.connect(self.solvePressedEvent)
        
        self.refreshButton = QPushButton(self)
        self.refreshButton.setText("REFRESH")
        self.refreshButton.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*1.5), Config.CELL_SIZE*12).toPoint(), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.refreshButton.setStyleSheet(Config.BUTTON_CONF)
        self.refreshButton.setDisabled(True)
        self.refreshButton.pressed.connect(self.refreshPressedEvent)
        
        
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
            solutionExists = self.animeBoard.solve(DFSDL=0)
        else:
            self.depth = int(self.depthText.toPlainText())
            solutionExists = self.animeBoard.solve(DFSDL=1, depth=self.depth)
        
        if (solutionExists):
            self.solveButton.setDisabled(True)
            self.animeBoard.group.start()
            self.refreshButton.setDisabled(False)
            self.animeBoard.group.stateChanged.connect(self.saveMessage)
            #self.animeBoard.group.currentAnimationChanged.connect(self.soundOn)
        else:
            self.solveButton.setDisabled(False)
            QMessageBox.warning(self, "Solution ERROR", "There is no solution!")
        
    def refreshPressedEvent(self) -> None:
        '''
        Обработка нажатия на рефреш
        '''
        self.refreshButton.setDisabled(True)
        self.animeBoard.makeAnime(True)
        self.animeBoard.group.start()
        self.solveButton.setDisabled(False)
        
    def saveMessage(self) -> None:
        QMessageBox.information(self, "Solution found", "Path was saved to the .xslx-file!")
    
    def soundOn(self) -> None:
        self.click.play()
        # QThreadPool.globalInstance().start(Run(self.click))
        
class Run(QRunnable):
    def __init__(self, s: QSound) -> None:
        super().__init__()
        self.s = s
    def run(self):
        self.s.play()

            
        