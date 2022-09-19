import enum
from typing import List
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

# class  Swap (enum):
#     TL

class Config:
    '''
    Настройки проекта
    '''
    WINDOW_TOP_PAD = 300
    WINDOW_LEFT_PAD = 300
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400

    R_LEFT_X = 0
    R_LEFT_Y = 0
    R_RIGHT_X = 180
    R_RIGHT_Y = 100
    
    CELL_SIZE = 30
    
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
                
    


class Colors:
    '''
    Основные цвета
    '''
    YELLOW = QColor("#FFD800")
    BLUE = QColor("#0057B8")
    GREEN = QColor("#50AB91")
    DARK_GREEN = QColor("#106B51")
    
    GREY = QColor("#E0E0E0")
    # GREY = QColor("#909090")
    RED = Qt.red
    RED_A120 = QColor(255, 0, 0, 120)
    BLACK = Qt.black
    BLACK_A100 = QColor(0, 0, 0, 100)
    
    GREEN_STR = "#50AB91"
    DARK_GREEN_STR = "#106B51"