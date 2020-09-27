import networkx as nx
from util import *


class Board:
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.G = nx.grid_2d_graph(m, n)

    def get_absolute_pos(self, relative_pos, n_player):
        rotations = n_player - 1

        board_center = self.m // 2, self.n // 2

        x, y = rotate(relative_pos[0], relative_pos[1], 90 * rotations, board_center)

        return x, y
