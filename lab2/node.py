import copy
from typing import List, Tuple
from collections import deque
import heapq


class Node:
    def __init__(self, state=None, parent=None, children=None, depth=0, i=None, j=None):
        self.state: List[List[int]] = [[0 for _ in range(3)] for _ in range(3)] if not state else state
        self.parent: Node = parent
        self.children: List[Node] = [] if not children else children
        self.depth: int = depth
        self.z_row: int = i
        self.z_col: int = j

    @property
    def hashable_state(self):
        return tuple(tuple(row) for row in self.state)

    def available_moves(self) -> Tuple[int, int]:
        if self.z_row - 1 >= 0:
            yield self.z_row - 1, self.z_col
        if self.z_row + 1 <= 2:
            yield self.z_row + 1, self.z_col
        if self.z_col - 1 >= 0:
            yield self.z_row, self.z_col - 1
        if self.z_col + 1 <= 2:
            yield self.z_row, self.z_col + 1

    def next_states(self) -> list:
        states: [Node] = []
        for x, y in self.available_moves():
            state = copy.deepcopy(self.state)
            state[x][y], state[self.z_row][self.z_col] = state[self.z_row][self.z_col], state[x][y]
            child = Node(
                state=state,
                parent=self,
                depth=self.depth + 1,
                i=x,
                j=y
            )
            states.append(child)
            self.children.append(child)

        return states

    def is_target(self, target_state: List[List[int]]) -> bool:
        return self.state == target_state


def _restore_path(root: Node, node: Node) -> List[Node]:
    path: List[Node] = []
    while node != root:
        path.append(node)
        node = node.parent
    return [root, *reversed(path)]


def manhattan_distance(current_state: List[List[int]], target_state: List[List[int]]) -> int:
    """
    h(n)
    """
    pass


def fnnm_distance(current_state: List[List[int]], target_state: List[List[int]]) -> int:
    """
    h(n)
    P.S.
    FNNM - Fishki ne na mestah
    """
    pass


def cost_criterion(current_state: List[List[int]], target_state: List[List[int]]) -> int:
    """
    g(n) для A*
    """
    pass


def solve_func(root: Node, target_state: List[List[int]], is_astar: bool, is_manh: bool) -> Tuple[List[Node], int, int]:
    """
    Решатель
    Формат выозвращаемого значения: tuple(
        путь из root в target или [],
        len(traversed)+len(fringer),
        len(traversed)
    )
    """
    fringer: List[Tuple[int, Node]] = [(0, root)]  # Очередь с приоритетом
    traversed = set()
    h = manhattan_distance if is_manh else fnnm_distance
    g = cost_criterion if is_astar else lambda x, y: 0
    node: Node
    while len(fringer) != 0:
        _, node = heapq.heappop(fringer)  # Выбирает с наименьшей стоимостью
        if node.is_target(target_state):
            break
        if node.hashable_state in traversed:
            continue
        next_states = node.next_states()
        traversed.add(node.hashable_state)
        for state in next_states:
            cost = h(node.state, target_state) + g(node.state, target_state)
            heapq.heappush(fringer, (cost, state))
    else:
        return [], 0, 0
    path = _restore_path(root, node)
    return path, len(traversed) + len(fringer), len(traversed)


def dfs(root: Node, target_state: [[int]]) -> ([[Node]], int, int):
    fringer = deque([root])
    traversed = set()
    node: Node
    while len(fringer) != 0:
        node = fringer.pop()
        if node.is_target(target_state):
            break
        if node.hashable_state in traversed:
            continue
        next_states = node.next_states()
        traversed.add(node.hashable_state)
        for state in next_states:
            fringer.append(state)
    else:
        return [], 0, 0
    path = _restore_path(root, node)
    return path, len(traversed) + len(fringer), len(traversed)


def dfs_depth(root: Node, target_state: [[int]], depth) -> ([[Node]], int, int):
    fringer = deque([root])
    traversed = set()
    node: Node
    while len(fringer) != 0:
        node = fringer.pop()
        if node.depth <= depth:
            if node.is_target(target_state):
                break
            if node.hashable_state in traversed:
                continue
            traversed.add(node.hashable_state)
            next_states = node.next_states()
            for state in next_states:
                fringer.append(state)
    else:
        return [], 0, 0
    path = _restore_path(root, node)
    return path, len(traversed) + len(fringer), len(traversed)
