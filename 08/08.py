import numpy as np

import utils


def tree_cover(forest):
    visible = set()
    X, Y = len(forest[0]), len(forest)

    for y in range(Y):
        for x in range(X):
            tree_under_test = forest[y, x]
            if np.any([np.all(line < tree_under_test) for line in lines(x, y, forest)]):
                visible.add((y, x))

    return visible


def scenic_scores(forest):
    scores = np.zeros_like(forest)
    X, Y = len(forest[0]), len(forest)

    for y in range(Y):
        for x in range(X):
            tree_under_test = forest[y, x]
            scores[y, x] = np.prod([calculate_distance(line, tree_under_test) for line in lines(x, y, forest)])

    return scores


def lines(x, y, forest):
    return np.flip(forest[:y, x]), forest[y, x + 1:], forest[y + 1:, x], np.flip(forest[y, :x])


def calculate_distance(line, tree_under_test):
    if len(line) == 0: return 0
    (hits, ) = np.where(line >= tree_under_test)
    if len(line) > 0 and len(hits) == 0: return len(line)
    return hits[0] + 1 if len(line) > 0 else 0


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = [[int(c) for c in line] for line in utils.read_str_lines()]
    forest = np.asarray(data, dtype=np.byte)
    print(len(tree_cover(forest)))
    timer.stop()  # 298.38ms
    """

    # Part 2
    timer.start()
    data = [[int(c) for c in line] for line in utils.read_str_lines()]
    forest = np.asarray(data, dtype=np.intc)
    print(np.max(scenic_scores(forest)))
    timer.stop()  # 228.97ms