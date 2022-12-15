import numpy as np

import utils


def preprocess(data: list[str]) -> tuple[np.array, np.array]:
    structures = [[tuple(int(elem) for elem in rock.split(',')) for rock in definition.split(' -> ')] for definition in data]
    X, Y = list(zip(*[(x, y) for structure in structures for x, y in structure]))
    minX, maxX = min(X), max(X)
    maxY = max(Y)
    ingress = np.array([0, 500 - minX])
    cave = np.zeros((maxY + 1, maxX - minX + 1))
    for structure in structures:
        for (sx, sy), (ex, ey) in zip(structure[:-1], structure[1:]):
            sx -= minX
            ex -= minX
            if ex < sx: ex, sx = sx, ex
            if ey < sy: ey, sy = sy, ey
            cave[sy:ey+1, sx:ex+1] = -1
    return cave, ingress


def sandfall(data: tuple[np.array, np.array]) -> np.array:
    cave, ingress = data
    down, downleft, downright = np.array([1, 0]), np.array([1, -1]), np.array([1, 1])
    while True:
        if cave[tuple(ingress)] == 1: break
        sand = ingress + np.array([-1, 0])
        while True:
            if (newpos := sand + down)[0] < cave.shape[0] and cave[tuple(newpos)] not in [-1, 1]:
                sand = newpos
                continue
            if (newpos := sand + downleft)[0] < cave.shape[0] and cave[tuple(newpos)] not in [-1, 1]:
                sand = newpos
                continue
            if (newpos := sand + downright)[0] < cave.shape[0] and cave[tuple(newpos)] not in  [-1, 1]:
                sand = newpos
                continue
            break
        if not any([(sand + direction)[0] < cave.shape[0] for direction in [down, downleft, downright]]): break
        cave[tuple(sand)] = 1
    return cave


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(np.sum(sandfall(data) == 1))
    timer.stop()  # 319.74ms
    """

    # Part 2
    timer.start()
    cave, ingress = preprocess(utils.read_str_lines())
    pad_l, pad_r = cave.shape[0] - ingress[1], cave.shape[0] - (cave.shape[1] - (ingress[1] + 1))
    cave = np.pad(cave, ((0, 2), (pad_l, pad_r)))
    cave[-1, :] = -1
    ingress[1] += pad_l
    print(np.sum(sandfall((cave, ingress)) == 1))
    timer.stop()  # 6261.63ms
