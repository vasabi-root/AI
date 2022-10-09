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
    QSequentialAnimationGroup, QRunnable, QPropertyAnimation
)
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtGui import QMouseEvent, QKeyEvent
import numpy as np
import os

from board import Board
from XLSXmaker import XLSXmake
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
        # self.click = QSound("bass.wav")
        self.depth = 50
        self.initBoards()
        self.initButtons()
        self.initLabels()
        
        
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
                  [7, 1, 0] ] # variant
        # start = [ [0, 4, 3],
        #           [6, 2, 1],
        #           [7, 5, 8] ]
        # start = [ [7, 2, 4],
        #           [5, 0, 6],
        #           [8, 3, 2] ]        
        self.startBoard = Board(self, QPoint(Config.CELL_SIZE, Config.CELL_SIZE*3), start)
        ends = list()
        ends.append( [ [2, 3, 4], [0, 6, 1], [7, 8, 5] ])
        ends.append( [ [3, 6, 4], [2, 5, 8], [7, 0, 1] ])
        ends.append( [ [3, 6, 4], [2, 5, 0], [7, 1, 8] ])
        ends.append(start) # depth = 0
        ends.append( [ [1, 2, 3], [4, 0, 5], [6, 7, 8] ]) # depth =  19942
        ends.append( [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]) # variant
        ends.append( [ [0, 2, 1], [3, 4, 5], [6, 7, 8] ]) # variant 1,2 = 2,1
        ends.append( [ [6, 4, 3], [5, 0, 1], [2, 7, 8] ]) # depth = 400
        end = ends[-2]
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
        
        # self.depthLabel = QLabel("DEPTH:", self)
        # self.depthLabel.setGeometry(QRect(
        #     QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*2), Config.CELL_SIZE*3-2).toPoint(), 
        #     QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        # ))
        # self.depthLabel.setAlignment(Qt.AlignCenter)
        # self.depthLabel.setStyleSheet(Config.LABEL_CONF)
        
        # self.depthText = QTextEdit(str(self.depth) ,self)
        # self.depthText.setGeometry(QRect(
        #     QPointF(Config.WINDOW_WIDTH/2, Config.CELL_SIZE*3).toPoint(), 
        #     QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        # ))
        # # self.depthText.enterEvent.connect()
        # self.depthLabel.setVisible(False)
        # self.depthText.setVisible(False)
        
        
        self.GSLabel = QLabel("GS", self)
        self.GSLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (len(self.GSLabel.text())*9+ Config.CELL_SIZE), self.toggleAlgor.pos().y()+3).toPoint(), 
            QSize(len(self.GSLabel.text())*9, Config.CELL_SIZE)
        ))
        self.GSLabel.setAlignment(Qt.AlignRight)
        self.GSLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.AstarLabel = QLabel("A*", self)
        self.AstarLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 + (Config.CELL_SIZE), self.toggleAlgor.pos().y()+3).toPoint(), 
            QSize(len(self.AstarLabel.text())*10, Config.CELL_SIZE)
        ))
        self.AstarLabel.setAlignment(Qt.AlignLeft)
        self.AstarLabel.setStyleSheet(Config.LABEL_CONF)


        self.ChipsLabel = QLabel("Chips position", self)
        self.ChipsLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (len(self.ChipsLabel.text())*9+Config.CELL_SIZE), self.toggleHevr.pos().y()+3).toPoint(), 
            QSize(len(self.ChipsLabel.text())*9, Config.CELL_SIZE)
        ))
        self.ChipsLabel.setAlignment(Qt.AlignRight)
        self.ChipsLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.ManhLabel = QLabel("Manhattan distance", self)
        self.ManhLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 + (Config.CELL_SIZE), self.toggleHevr.pos().y()+3).toPoint(), 
            QSize(len(self.ManhLabel.text())*9, Config.CELL_SIZE)
        ))
        self.ManhLabel.setAlignment(Qt.AlignLeft)
        self.ManhLabel.setStyleSheet(Config.LABEL_CONF)
        
        self.stepLabel = QLabel("STEP MODE", self)
        self.stepLabel.setGeometry(QRect(
            QPointF(Config.CELL_SIZE, self.toggleStep.pos().y()-Config.CELL_SIZE/1.5).toPoint(), 
            QSize(Config.CELL_SIZE*3, Config.CELL_SIZE)
        ))
        self.stepLabel.setAlignment(Qt.AlignCenter)
        self.stepLabel.setStyleSheet(Config.LABEL_CONF)
        
        
        self.gLabel = QLabel("g: ", self)
        self.gLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*4, Config.CELL_SIZE*11).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.gLabel.setAlignment(Qt.AlignRight)
        self.gLabel.setStyleSheet(Config.LABEL_CONF)
        self.gLabel.setVisible(False)
        
        self.hLabel = QLabel("h: ", self)
        self.hLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*4, Config.CELL_SIZE*12).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.hLabel.setAlignment(Qt.AlignRight)
        self.hLabel.setStyleSheet(Config.LABEL_CONF)
        self.hLabel.setVisible(False)
        
        self.depthLabel = QLabel("depth: ", self)
        self.depthLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*5, Config.CELL_SIZE*13).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        self.depthLabel.setAlignment(Qt.AlignRight)
        self.depthLabel.setStyleSheet(Config.LABEL_CONF)
        self.depthLabel.setVisible(False)
        
        self.gNumLabel = QLabel("0", self)
        self.gNumLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*3, Config.CELL_SIZE*11).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.gNumLabel.setAlignment(Qt.AlignLeft)
        self.gNumLabel.setStyleSheet(Config.LABEL_CONF)
        self.gNumLabel.setVisible(False)
        
        self.hNumLabel = QLabel("0", self)
        self.hNumLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*3, Config.CELL_SIZE*12).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.hNumLabel.setAlignment(Qt.AlignLeft)
        self.hNumLabel.setStyleSheet(Config.LABEL_CONF)
        self.hNumLabel.setVisible(False)
        
        self.depthNumLabel = QLabel("0", self)
        self.depthNumLabel.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*3, Config.CELL_SIZE*13).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.depthNumLabel.setAlignment(Qt.AlignLeft)
        self.depthNumLabel.setStyleSheet(Config.LABEL_CONF)
        self.depthNumLabel.setVisible(False)
        
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
        
        self.leftStepButton = QPushButton(self)
        self.leftStepButton.setText("<")
        self.leftStepButton.setGeometry(QRect(
            QPointF(Config.CELL_SIZE*3, Config.CELL_SIZE*8).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.leftStepButton.setStyleSheet(Config.BUTTON_CONF)
        self.leftStepButton.setVisible(False)
        self.leftStepButton.pressed.connect(self.leftPressedEvent)
        
        self.rightStepButton = QPushButton(self)
        self.rightStepButton.setText(">")
        self.rightStepButton.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH - Config.CELL_SIZE*4, Config.CELL_SIZE*8).toPoint(), 
            QSize(Config.CELL_SIZE, Config.CELL_SIZE)
        ))
        self.rightStepButton.setStyleSheet(Config.BUTTON_CONF)
        self.rightStepButton.setVisible(False)
        self.rightStepButton.pressed.connect(self.rightPressedEvent)
        
        
        self.toggleAlgor = AnimatedToggle(self)
        self.toggleAlgor.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE), Config.CELL_SIZE/3).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))

        self.toggleHevr = AnimatedToggle(self)
        self.toggleHevr.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE), Config.CELL_SIZE).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        
        self.toggleStep = AnimatedToggle(self)
        self.toggleStep.setGeometry(QRect(
            QPointF(Config.WINDOW_WIDTH/2 - (Config.CELL_SIZE*5), self.solveButton.pos().y()).toPoint(), 
            QSize(Config.CELL_SIZE*2, Config.CELL_SIZE)
        ))
        self.toggleStep.stateChanged.connect(self.stepShow)
    
    def stepShow(self) -> None:
        self.rightStepButton.setVisible(not self.rightStepButton.isVisible())
        # self.leftStepButton.setVisible(not self.leftStepButton.isVisible())
        
        self.hLabel.setVisible(not self.hLabel.isVisible())
        self.hNumLabel.setVisible(not self.hNumLabel.isVisible())
        self.depthLabel.setVisible(not self.depthLabel.isVisible())
        self.depthNumLabel.setVisible(not self.depthNumLabel.isVisible())
        
        self.toggleAlgor.setEnabled(not self.toggleAlgor.isEnabled())
        self.toggleHevr.setEnabled(not self.toggleHevr.isEnabled())
        
        isAstar = int(self.toggleAlgor.handle_position) == 1
        isManh = int(self.toggleHevr.handle_position) == 1
        
        if (isAstar):
            self.gLabel.setVisible(not self.gLabel.isVisible())
            self.gNumLabel.setVisible(not self.gNumLabel.isVisible())
        
        if (int(self.toggleStep.handle_position) == 0):
            self.refreshPressedEvent()
            self.solveButton.setEnabled(False)
            self.refreshButton.setEnabled(True)
            self.animeBoard.initBoard(isAstar, isManh)
        else:
            self.solveButton.setEnabled(True)
            self.refreshButton.setEnabled(False)
            self.animeBoard.refresh()
            self.animeBoard.group.start()
    
    def leftPressedEvent(self) -> None:
        self.animeBoard.makeStepLeft()
        # print("<")
    
    def rightPressedEvent(self) -> None:
        self.animeBoard.makeStepRight()
        # print(">")
    
    def cellClickedEvent(self, h: int, g: int, depth: int) -> None:
        self.hNumLabel.setText(str(h))
        self.gNumLabel.setText(str(g))
        self.depthNumLabel.setText(str(depth))
    
    def solvePressedEvent(self) -> None:
        '''
        Обработка нажатия на солв
        '''
        self.animeBoard.group = QSequentialAnimationGroup(self)
        isAstar = int(self.toggleAlgor.handle_position) == 1
        isManh = int(self.toggleHevr.handle_position) == 1
        solutionExists = self.animeBoard.solve(isAstar, isManh)
            
        if (len(self.animeBoard.solution[0]) <= Config.MAX_XLSX_PATH):
            saveFunc = self.saveMessage
            sA = "A_star" if isAstar else "Greedy_search"
            sH = "Manhattan_dist" if isManh else "Chips_pos"
            if (not XLSXmake(self.animeBoard.solution, sA + '_' + sH + '.xlsx')):
                saveFunc = self.saveErrorMessage
            self.animeBoard.group.finished.connect(saveFunc)
        else:
            self.animeBoard.group.finished.connect(self.largePathMessage)
        
        if (solutionExists):
            # self.animeBoard.node = self.animeBoard.solution[0][-1]
            self.solveButton.setDisabled(True)
            self.refreshButton.setDisabled(False)
            self.animeBoard.group.start()
            if (self.animeBoard.group.__class__ == QSequentialAnimationGroup):
                self.animeBoard.group.currentAnimationChanged.connect(self.soundOn)
            else:
                self.animeBoard.group.stateChanged.connect(self.soundOn)
            
        else:
            self.solveButton.setDisabled(False)
            QMessageBox.warning(self, "Solution ERROR", "There is no solution!")
        
    def refreshPressedEvent(self) -> None:
        '''
        Обработка нажатия на рефреш
        '''
        if (self.animeBoard.node != None and self.animeBoard.node.hashable_state != self.startBoard.root.hashable_state):
            if (len(self.animeBoard.solution[0]) > 0):
                self.animeBoard.makeAnime(isReversed=True)
                self.animeBoard.node = self.animeBoard.root
            else:
                isAstar = int(self.toggleAlgor.handle_position) == 1
                isManh = int(self.toggleHevr.handle_position) == 1
                self.animeBoard.refresh()
                self.animeBoard.initBoard(isAstar, isManh)
            self.animeBoard.group.start()
            if (self.animeBoard.group.__class__ == QSequentialAnimationGroup):
                self.animeBoard.group.currentAnimationChanged.connect(self.soundOn)
            else:
                self.animeBoard.group.stateChanged.connect(self.soundOn)
            if (int(self.toggleStep.handle_position) == 0):
                self.solveButton.setEnabled(True)
                self.refreshButton.setEnabled(False)
        
    def crunchAnimeStart(self) -> None:
        size = QSize(self.refreshButton.size())
        self.crunchAnime = QPropertyAnimation(self.refreshButton, b"size")
        self.crunchAnime.setEndValue(size)
        self.crunchAnime.setDuration(10)
        self.crunchAnime.start()    
    
    def saveMessage(self) -> None:
        QMessageBox.information(self, "Solution found", "Path was saved to the .xslx-file!")
        self.crunchAnimeStart()
        
    def saveErrorMessage(self) -> None:
        isAstar = int(self.toggleAlgor.handle_position) == 1
        isManh = int(self.toggleHevr.handle_position) == 1
        sA = "A_star" if isAstar else "Greedy_search"
        sH = "Manhattan_dist" if isManh else "Chips_pos"
        
        QMessageBox.warning(self, "Save ERROR", "Please, close the file: "+"'"+sA + '_' + sH + ".xlsx"+"'" + " and try again")
        self.crunchAnimeStart()
        
    def largePathMessage(self) -> None:
        QMessageBox.warning(self, "Solution found", 
        f'Path too large!\
        \n path len:              {len(self.animeBoard.solution[0])-1}\
        \n capacitive difficulty: {self.animeBoard.solution[1]}\
        \n timing difficulty:     {self.animeBoard.solution[2]}')
        self.crunchAnimeStart()

    def soundOn(self) -> None:
        self.click.play()
        # QThreadPool.globalInstance().start(Run(self.click))
        
class Run(QRunnable):
    def __init__(self, s: QSound) -> None:
        super().__init__()
        self.s = s
    def run(self):
        self.s.play()

            
        