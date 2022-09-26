import enum
from typing import List
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

# class  Swap (enum):
#     TL

class Colors:
    '''
    Основные цвета
    '''
    YELLOW = QColor("#FFD800")
    BLUE = QColor("#0057B8")
    GREEN = QColor("#50AB91")
    DARK_GREEN = QColor("#106B51")
    LIGHT_GREEN = QColor("#80DBC1")
    
    GREY = QColor("#E0E0E0")
    RED = QColor("#D00000")
    RED_A120 = QColor(255, 0, 0, 120)
    BLACK = Qt.black
    BLACK_A100 = QColor(0, 0, 0, 100)
    
    GREEN_STR = "#50AB91"
    DARK_GREEN_STR = "#106B51"
    RED_STR = "#D00000"
    LIGHT_GREEN_STR = "#80DBC1"
    
    GREEN_xlsSTR = "FF50AB91"
    DARK_GREEN_xlsSTR = "FF106B51"
    RED_STR_xlsSTR = "FFD00000"

class Config:
    '''
    Настройки проекта
    '''
    WINDOW_TOP_PAD = 300
    WINDOW_LEFT_PAD = 300
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 450

    R_LEFT_X = 0
    R_LEFT_Y = 0
    R_RIGHT_X = 180
    R_RIGHT_Y = 100
    
    CELL_SIZE = 30

    SLOW_ANIME = 300 # ms
    FAST_ANIME = 50  # ms
    
    BUTTON_CONF = \
    f'''
        QPushButton:hover {{
            border: none;
            outline: none;
        }}
        QPushButton {{
            border-color: {Colors.DARK_GREEN_STR};
            border-style: solid;
            border-radius: 2px;
            border-width: 3px;
            color: white;
            text-align: center;
            background-color: {Colors.GREEN_STR}
        }}
        QPushButton:pressed {{
            border: none;
            outline: none;
            color: white;
            text-align: center;
            background-color: {Colors.DARK_GREEN_STR}
        }}
        QPushButton:disabled {{
            border-color: {Colors.DARK_GREEN_STR};
            border-style: solid;
            border-radius: 2px;
            border-width: 3px;
            color: white;
            text-align: center;
            background-color: {Colors.RED_STR}
        }}
    '''
    LABEL_CONF = \
    f'''
        QLabel {{
            color: black
        }}
    '''

    @staticmethod
    def index2d(myList: List[List], v) -> int:
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v))
    
    @staticmethod
    def getHash(matrix: List[List]) -> int:
        hash = 0
        m = len(matrix)
        k = 1
        for i in range (m):
            for j in range (m):
                n = j+1
                hash += matrix[i][j]*k
                k += 1
        return hash
    
    @staticmethod
    def swap(matrix: List[List], row_1: int, col_1: int, row_2: int, col_2: int) -> List[List]:
        m = len(matrix)
        mat_copy = []
        for i in range (m):
            mat_copy.append([])
            for j in range (m):
                if (i == row_1 and j == col_1):
                    mat_copy[i].append(matrix[row_2][col_2])
                elif (i == row_2 and j == col_2):
                    mat_copy[i].append(matrix[row_1][col_1])
                else:
                    mat_copy[i].append(matrix[i][j])
        return mat_copy