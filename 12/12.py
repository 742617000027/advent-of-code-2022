import networkx as nx
import numpy as np

import utils


def preprocess(data):
    terrain = np.array([[ord(c) for c in line] for line in data])
    start = np.argwhere(terrain == 83).squeeze()
    end = np.argwhere(terrain == 69).squeeze()
    terrain[terrain == 83] = ord('a')
    terrain[terrain == 69] = ord('z')

    Y, X = terrain.shape
    G = nx.DiGraph()

    for y in range(Y):
        for x in range(X):
            current = (y, x)
            if current not in G: G.add_node(current, coords=str(current), height=int(terrain[current]))
            for yy, xx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                if 0 <= (y + yy) < Y and 0 <= (x + xx) < X:
                    neighbor = (y + yy, x + xx)
                    if terrain[neighbor] - 1 <= terrain[current]:
                        if neighbor not in G: G.add_node(neighbor, coords=str(neighbor), height=int(terrain[neighbor]))
                        G.add_edge(current, neighbor)

    return G, tuple(start), tuple(end)


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    G, start, end = data
    print(len(nx.shortest_path(G, start, end)) - 1)
    timer.stop()  # 74.96ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    G, _, end = data
    print(min([
        len(nx.shortest_path(G, node, end)) - 1
        for node
        in G.nodes
        if G.nodes[node]['height'] == 97
        and nx.has_path(G, node, end)
    ]))
    timer.stop()  # 1918.52ms
