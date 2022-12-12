import networkx as nx
import numpy as np
from itertools import product

import utils


Vector = tuple[int, int]


def make_graph(data: list[str]) -> tuple[nx.DiGraph, Vector, Vector]:
    terrain = np.array([[ord(c) for c in line] for line in data])
    start = tuple(np.argwhere(terrain == ord('S')).squeeze())
    end = tuple(np.argwhere(terrain == ord('E')).squeeze())
    terrain[terrain == ord('S')] = ord('a')
    terrain[terrain == ord('E')] = ord('z')

    Y, X = terrain.shape
    G = nx.DiGraph()

    for current in product(range(Y), range(X)):
        y, x = current
        G.add_node(current, height=terrain[current])
        for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if 0 <= (yy := y + dy) < Y and 0 <= (xx := x + dx) < X:
                neighbor = (yy, xx)
                if terrain[neighbor] - 1 <= terrain[current]:
                    G.add_edge(current, neighbor)

    return G, start, end


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read_str_lines()
    G, start, end = make_graph(data)
    print(len(nx.shortest_path_length(G, node, end))
    timer.stop()  # 74.96ms
    """

    # Part 2
    timer.start()
    data = utils.read_str_lines()
    G, _, end = make_graph(data)
    print(min([
        nx.shortest_path_length(G, node, end)
        for node
        in G.nodes
        if G.nodes[node]['height'] == ord('a')
        and nx.has_path(G, node, end)
    ]))
    timer.stop()  # 1918.52ms
