import copy
from typing import List, Tuple
from collections import deque
import heapq
from dataclasses import dataclass, field
from typing import Any


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

    def get_children(self) -> list:
        children: [Node] = []
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
            children.append(child)
            self.children.append(child)

        return children

    def is_target(self, target_state: List[List[int]]) -> bool:
        return self.state == target_state


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    node: Any = field(compare=False)


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
    result = 0
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            result = result + abs(current_state[i][j] - target_state[i][j])
    return result


def fnnm_distance(current_state: List[List[int]], target_state: List[List[int]]) -> int:
    """
    h(n)
    P.S.
    FNNM - Fishki ne na mestah
    """
    result = 0
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] != target_state[i][j]:
                result = result + 1
    return result


def cost_criterion(node: Node) -> int:
    """
    g(n) для A*
    """
    return node.depth


def solve_func(root: Node, target_state: List[List[int]], is_astar: bool, is_manh: bool) -> Tuple[List[Node], int, int]:
    """
    Решатель
    Формат выозвращаемого значения: tuple(
        путь из root в target или [],
        len(traversed)+len(fringer),
        len(traversed)
    )
    """
    fringer: List[PrioritizedItem] = [PrioritizedItem(0, root)]  # Очередь с приоритетом
    traversed = set()
    h = manhattan_distance if is_manh else fnnm_distance
    g = cost_criterion if is_astar else lambda x: 0
    node: Node
    heapq.heapify(fringer)
    while len(fringer) != 0:
        item = heapq.heappop(fringer)  # Выбирает с наименьшей стоимостью
        node = item.node
        if node.is_target(target_state):
            break
        if node.hashable_state in traversed:
            continue
        children = node.get_children()
        traversed.add(node.hashable_state)
        for child in children:
            cost = h(node.state, target_state) + g(node)
            heapq.heappush(fringer, PrioritizedItem(cost, child))
    else:
        return [], 0, 0
    path = _restore_path(root, node)
    return path, len(traversed) + len(fringer), len(traversed)

# def dfs(root: Node, target_state: [[int]]) -> ([[Node]], int, int):
#     fringer = deque([root])
#     traversed = set()
#     node: Node
#     while len(fringer) != 0:
#         node = fringer.pop()
#         if node.is_target(target_state):
#             break
#         if node.hashable_state in traversed:
#             continue
#         next_nodes = node.next_nodes()
#         traversed.add(node.hashable_state)
#         for state in next_nodes:
#             fringer.append(state)
#     else:
#         return [], 0, 0
#     path = _restore_path(root, node)
#     return path, len(traversed) + len(fringer), len(traversed)


# def dfs_depth(root: Node, target_state: [[int]], depth) -> ([[Node]], int, int):
#     fringer = deque([root])
#     traversed = set()
#     node: Node
#     while len(fringer) != 0:
#         node = fringer.pop()
#         if node.depth <= depth:
#             if node.is_target(target_state):
#                 break
#             if node.hashable_state in traversed:
#                 continue
#             traversed.add(node.hashable_state)
#             next_nodes = node.next_nodes()
#             for state in next_nodes:
#                 fringer.append(state)
#     else:
#         return [], 0, 0
#     path = _restore_path(root, node)
#     return path, len(traversed) + len(fringer), len(traversed)
