import networkx as nx

from util import *


class Player:
    def __init__(self, n_player, board):
        # Player positions
        #       1. Top
        #       2. Bottom
        #       3. Left
        #       4. Right

        self.n_player = n_player
        self.G = board.G.copy()
        self.x, self.y = board.n // 2, board.m - 1

        nx.set_node_attributes(self.G, False, 'is_winning_pos')
        for i in range(board.n):
            self.G.nodes[(0, i)]['is_winning_pos'] = True

        self.remove_node(board.n // 2, 0)
        self.remove_node(0, board.m // 2)
        self.remove_node(board.n - 1, board.m // 2)

    def update_position(self):
        algorithm = get_player_movement_algorithm(self.n_player)
        winning_nodes = [n for n, d in self.G.nodes(data=True) if d['is_winning_pos']]
        best_path = None
        for node in winning_nodes:
            path = algorithm(self.G, (self.y, self.x), node)
            if best_path is None or len(path) < len(best_path):
                best_path = path
        self.y, self.x = best_path[1]

    def is_in_winning_position(self):
        winning_nodes = [n for n, d in self.G.nodes(data=True) if d['is_winning_pos']]
        return (self.y, self.x) in winning_nodes

    def update_view(self, prev_pos, new_pos):
        # x, y represent the position of the opposite player relative to this
        # player
        self.add_node(prev_pos[0], prev_pos[1])
        self.remove_node(new_pos[0], new_pos[1])

    def add_node(self, x, y):
        add_node_util(self.G, (y, x))

        add_edge_util(self.G, (y, x), (y, x - 1))
        add_edge_util(self.G, (y, x), (y, x + 1))

        if (y + 1, x) in self.G.nodes and (y - 1, x) in self.G.nodes:
            remove_edge_util(self.G, (y - 1, x), (y + 1, x))
            add_edge_util(self.G, (y, x), (y + 1, x))
            add_edge_util(self.G, (y, x), (y - 1, x))
        elif (y + 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y, x), (y - 1, x))
            remove_edge_util(self.G, (y + 2, x), (y + 1, x - 1))
            remove_edge_util(self.G, (y + 2, x), (y + 1, x + 1))
            add_edge_util(self.G, (y, x), (y + 2, x))
        elif (y - 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y, x), (y + 1, x))
            remove_edge_util(self.G, (y + 1, x), (y, x - 1))
            remove_edge_util(self.G, (y + 1, x), (y, x + 1))
            add_edge_util(self.G, (y, x), (y - 2, x))

        if get_attr_val(self.G, (y, x + 1), 'is_winning_pos') or get_attr_val(self.G, (y, x - 1), 'is_winning_pos'):
            self.G.nodes[(y, x)]['is_winning_pos'] = True
        else:
            self.G.nodes[(y, x)]['is_winning_pos'] = False

    def remove_node(self, x, y):
        remove_node_util(self.G, (y, x))

        if (y - 1, x) in self.G.nodes and (y + 1, x) in self.G.nodes:
            add_edge_util(self.G, (y + 1, x), (y - 1, x))
        elif (y + 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y + 2, x), (y + 1, x - 1))
            add_edge_util(self.G, (y + 2, x), (y + 1, x + 1))
        elif (y - 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y + 1, x), (y, x - 1))
            add_edge_util(self.G, (y + 1, x), (y, x + 1))
