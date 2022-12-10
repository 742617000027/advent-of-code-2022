import numpy as np

import utils


def move_rope(data, n_knots):

    vecs = {
        'U': np.array([-1, 0]),
        'R': np.array([0, 1]),
        'D': np.array([1, 0]),
        'L': np.array([0, -1]),
    }

    rope = [np.array([0, 0]) for _ in range(n_knots)]
    tail_visited = {(0, 0)}

    for direction, distance in data:
        for _ in range(distance):
            rope[0] += vecs[direction]
            for k, knot in enumerate(rope[1:]):
                following = rope[k]
                if np.any(np.abs(following - knot) >= 2):
                    move_knot(knot, following)
                    if k == len(rope) - 2: tail_visited.add(tuple(rope[-1]))
                else:
                    break

    return tail_visited


def move_knot(knot, following):
    idx = np.abs(following - knot) >= 2
    knot[idx] += (following[idx] - knot[idx]) // 2
    knot[~idx] = following[~idx]
    return knot


if __name__ == '__main__':
    timer = utils.Timer()

    """
    # Part 1
    timer.start()
    data = [(line.split()[0], int(line.split()[1])) for line in utils.read_str_lines()]
    print(len(move_rope(data, 2)))
    timer.stop()  # 230.23ms
    """

    # Part 2
    timer.start()
    data = [(line.split()[0], int(line.split()[1])) for line in utils.read_str_lines()]
    print(len(move_rope(data, 10)))
    timer.stop()  # 769.24ms
