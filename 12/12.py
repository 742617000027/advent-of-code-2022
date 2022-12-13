from itertools import product

import networkx as nx
import numpy as np

import utils

Vector = tuple[int, int]


def preprocess(data: list[str]) -> tuple[nx.DiGraph, Vector, Vector]:
    terrain, start, end = make_map(data)
    G = make_graph(terrain)
    return G, start, end


def make_map(data: list[str]) -> np.array:
    terrain = np.array([[ord(c) for c in line] for line in data])
    start, end = find('S', terrain), find('E', terrain)
    terrain[start], terrain[end] = ord('a'), ord('z')
    return terrain, start, end


def find(needle: str, haystack: np.array) -> Vector:
    return tuple(np.argwhere(haystack == ord(needle)).squeeze())


def make_graph(terrain: np.array) -> nx.DiGraph:
    G = nx.DiGraph()
    Y, X = terrain.shape

    for current in product(range(Y), range(X)):
        y, x = current
        G.add_node(current, height=terrain[current])
        for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if 0 <= (yy := y + dy) < Y and 0 <= (xx := x + dx) < X:
                neighbor = (yy, xx)
                if terrain[neighbor] - 1 <= terrain[current]:
                    G.add_edge(current, neighbor)
    return G


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    G, start, end = preprocess(utils.read_str_lines())
    print(nx.shortest_path_length(G, start, end))
    timer.stop()  # 65.14ms
    """

    # Part 2
    timer.start()
    G, _, end = preprocess(utils.read_str_lines())
    print(nx.multi_source_dijkstra(G, {node for node in G.nodes if G.nodes[node]['height'] == ord('a')}, end)[0])
    timer.stop()  # 91.56ms
