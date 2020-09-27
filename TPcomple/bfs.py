import networkx as nx
from collections import deque


def generic_edges(G, source, neighbors=None, depth_limit=None, sort_neighbors=None):
    if callable(sort_neighbors):
        _neighbors = neighbors
        neighbors = lambda node: iter(sort_neighbors(_neighbors(node)))

    visited = {source}
    if depth_limit is None:
        depth_limit = len(G)
    queue = deque([(source, depth_limit, neighbors(source))])
    while queue:
        parent, depth_now, children = queue[0]
        try:
            child = next(children)
            if child not in visited:
                yield parent, child
                visited.add(child)
                if depth_now > 1:
                    queue.append((child, depth_now - 1, neighbors(child)))
        except StopIteration:
            queue.popleft()


def bfs_edges(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    if reverse and G.is_directed():
        successors = G.predecessors
    else:
        successors = G.neighbors
    yield from generic_edges(G, source, successors, depth_limit, sort_neighbors)


def bfs_algorithm(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    T = nx.DiGraph()
    T.add_node(source)
    edges_gen = bfs_edges(
        G,
        source,
        reverse=reverse,
        depth_limit=depth_limit,
        sort_neighbors=sort_neighbors,
    )
    T.add_edges_from(edges_gen)
    return T
