import copy
from collections import deque


class Node:
    def __init__(self, state=None, parent=None, children=None, depth=0, i=None, j=None):
        self.state: [[int]] = [[0]*3]*3 if not state else state
        self.parent: Node = parent
        self.children: [Node] = [] if not children else children
        self.depth: int = depth
        self.z_row: int = i
        self.z_col: int = j
        # self.traversed: [Node] = set() # пройденные


    @property
    def hashable_state(self):
        return tuple(tuple(row) for row in self.state)

    def available_moves(self) -> (int, int):
        if self.z_row - 1 >= 0:
            yield self.z_row - 1, self.z_col
        if self.z_row + 1 <= 2:
            yield self.z_row + 1, self.z_col
        if self.z_col - 1 >= 0:
            yield self.z_row, self.z_col - 1
        if self.z_col + 1 <= 2:
            yield self.z_row, self.z_col + 1

    def next_states(self) -> []:
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

    def is_target(self, target_state: [[int]]) -> bool:
        return self.state == target_state


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
        return ([], 0, 0)
    path = []
    while node != root:
        path.append(node)
        node = node.parent
    return ([root] + list(reversed(path)), len(traversed)+len(fringer), len(traversed))


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
        return ([], 0, 0)
    path = []
    while node != root:
        path.append(node)
        node = node.parent
    return ([root] + list(reversed(path)), len(traversed)+len(fringer), len(traversed))
