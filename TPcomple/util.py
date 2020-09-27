from math import cos, sin, pi

from djikstra import dijkstra_algorithm
from bfs import bfs_algorithm
from dfs import dfs_algorithm


def get_attr_val(G, node, attribute):
    if node in G.nodes:
        return G.nodes[node][attribute]


def remove_node_util(G, node):
    if node in G.nodes:
        G.remove_node(node)


def add_node_util(G, node):
    if node not in G.nodes:
        G.add_node(node)


def remove_edge_util(G, u, v):
    if u in G.nodes and v in G.nodes:
        if (u, v) in G.edges:
            G.remove_edge(u, v)
        if (v, u) in G.edges:
            G.remove_edge(v, u)


def add_edge_util(G, u, v):
    if u in G.nodes and v in G.nodes:
        if (u, v) not in G.edges and (v, u) not in G.edges:
            G.add_edge(u, v)


def rotate(x, y, theta, c):
    x, y = x - c[0], y - c[1]

    _x = round(x * cos(theta * pi / 180) - y * sin(theta * pi / 180))
    _y = round(x * sin(theta * pi / 180) + y * cos(theta * pi / 180))

    x, y = c[0] + _x, c[1] + _y

    return x, y


def get_player_movement_algorithm(n_player):
    algorithms = {
        1: dijkstra_algorithm,
        2: dfs_algorithm,
        3: bfs_algorithm,
        4: dijkstra_algorithm
    }
    return algorithms[n_player]


def get_position_from_player_number(player, board):
    if 0 < player.n_player < 5:
        rotations = player.n_player - 1
        board_center = board.m // 2, board.n // 2
        _x, _y = rotate(player.x, player.y, 90 * rotations, board_center)
        return _x, _y
