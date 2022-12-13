import networkx as nx

import utils

Vector = tuple[int, int]


def process(data: list[str]) -> tuple[nx.DiGraph, Vector, Vector]:
    terrain = [[ord(c) for c in line] for line in data]
    [(sy, sx)], [(ey, ex)] = [[(y, x.index(c)) for y, x in enumerate(terrain) if c in x] for c in [ord('S'), ord('E')]]
    terrain[sy][sx], terrain[ey][ex] = ord('a'), ord('z')
    Y, X = len(terrain), len(terrain[0])
    G = nx.DiGraph()

    for y, x in utils.product(range(Y), range(X)):
        G.add_node((y, x), height=terrain[y][x])
        for dy, dx in utils.DIRS:
            if 0 <= (yy := y + dy) < Y and 0 <= (xx := x + dx) < X and terrain[yy][xx] - 1 <= terrain[y][x]:
                G.add_edge((y, x), (yy, xx))
    return G, (sy, sx), (ey, ex)


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    G, start, end = process(utils.read_str_lines())
    print(nx.shortest_path_length(G, start, end))
    timer.stop()  # 65.14ms
    """

    # Part 2
    timer.start()
    G, _, end = process(utils.read_str_lines())
    print(nx.multi_source_dijkstra(G, {node for node in G.nodes if G.nodes[node]['height'] == ord('a')}, end)[0])
    timer.stop()  # 91.56ms
