from typing import List
import numpy as np

from shared import Config

class Node: # of tree
    state: List[List[int]]  # состояние (обычный интовый двумерный список)
    root: object            # указатель на корень дерева (мб надо перенести в Board)
    parrent: object         # указатель на родителя
    children: List          # список потомков
    depth: int              # глубина (надо ограничить максимальной из интерфейса)
    hash: int               # 
    z_row: int              # позиция пустой ячейки на доске (строка)
    z_col: int              # позиция пустой ячейки на доске (столбец)
    m: int
    
    def __init__(self, state: List[List[int]], parrent=None, fringer: List[List]=None, endHash: int=0) -> None:
        self.parrent = parrent
        if (self.parrent == None):
            self.depth = 0
            self.root = self
        else:
            self.depth = self.parrent.depth + 1
            self.root = self.parrent.root
        self.children = []
        self.state = state
        self.m = len(state)
        self.initZero()
        self.hash = Config.getHash(self.state)
        fringer.append(self)
        
    def initZero(self) -> None:
        for i in range (self.m):
            for j in range (self.m):
                if (self.state[i][j] == 0):
                    self.z_row = i
                    self.z_col = j
                    return
        
    def DFSopen(self, fringer: List[List[object]]) -> None:
        '''
        Метод раскрытия потомков вершины (с учётом того, что состояния не должны повторяться)
        По алгоритму DFS
        '''
        # TODO: добавить новые вершины в кайму (fringer) и удалять текущую из неё
        
        try:
            fringer.remove(self)
        except (ValueError):
            pass
        
        self.children = []
        
        # ЭТО НЕ УДАЛЯТЬ (С ОТСЮДА)

        for row in [self.z_row-1, self.z_row+1]:
            if (0 <= row < self.m):
                state = Config.swap(self.state, self.z_row, self.z_col, row, self.z_col)
                hash = Config.getHash(state)
                if (not Node.alreadyExists(self.root, hash)):
                    self.children.append(
                        Node(
                            state,
                            self,
                            fringer
                        )
                    )
        for col in [self.z_col-1, self.z_col+1]:
            if (0 <= col < self.m):
                state = Config.swap(self.state, self.z_row, self.z_col, self.z_row, col)
                hash = Config.getHash(state)
                if (not Node.alreadyExists(self.root, hash)):
                    self.children.append(
                        Node(
                            state,
                            self,
                            fringer
                        )
                    )
        
        # ДО СЮДА
        # TODO: возможно, надо поменять порядок добавления в кайму
        
        
        # for c in self.children:
        #     print(c.state)
        # print()
    def DFSnext(self):
        '''
        Стратегия перехода к следующей вершине (алгоритм DFS)
        '''
        # TODO: надо выбрать следующую вершину (тут переписать всё можно переписать, 
        # главное -- чтоб возвращалая найденная вершина, или None, 
        # если её не нашлось (даже в случае перехода в конечное состояние)
        if len(self.children) > 0:
            # fringer.remove(self)
            return self.children[0]
        else:
            return None
        
    def DFSDLopen(self, fringer: List[List[object]], depth: int) -> None:
        '''
        Метод раскрытия потомков вершины (с учётом того, что состояния не должны повторяться)
        По алгоритму DFS
        '''
        # TODO: добавить новые вершины в кайму (fringer) и удалять текущую из неё
        
        try:
            fringer.remove(self)
        except (ValueError):
            pass
        
        self.children = []
        
        # ЭТО НЕ УДАЛЯТЬ (С ОТСЮДА)

        for row in [self.z_row-1, self.z_row+1]:
            if (0 <= row < self.m):
                state = Config.swap(self.state, self.z_row, self.z_col, row, self.z_col)
                hash = Config.getHash(state)
                if (not Node.alreadyExists(self.root, hash)):
                    self.children.append(
                        Node(
                            state,
                            self,
                            fringer
                        )
                    )
        for col in [self.z_col-1, self.z_col+1]:
            if (0 <= col < self.m):
                state = Config.swap(self.state, self.z_row, self.z_col, self.z_row, col)
                hash = Config.getHash(state)
                if (not Node.alreadyExists(self.root, hash)):
                    self.children.append(
                        Node(
                            state,
                            self,
                            fringer
                        )
                    )
        
        # ДО СЮДА
        # TODO: возможно, надо поменять порядок добавления в кайму
        
    def DFSDLnext(self, depth: int):
        '''
        Стратегия перехода к следующей вершине (алгоритм DFS Depth Limit)
        '''
        # TODO: надо выбрать следующую вершину (тут переписать всё можно переписать, 
        # главное -- чтоб возвращалая найденная вершина, или None, 
        # если её не нашлось (даже в случае перехода в конечное состояние)
        if len(self.children) > 0:
            # fringer.remove(self)
            return self.children[0]
        else:
            return None
    
    @staticmethod
    def alreadyExists(root, hash) -> bool:
        node = root
        ans = False
        l = len(node.children)
        if (node.hash == hash):
            ans = True
        elif (l > 0):
            i = 0
            while (i < l and ans == False):
                ans = Node.alreadyExists(node.children[i], hash)
                i += 1
        return ans
                    
            
        
        
                        
        
    
    
    