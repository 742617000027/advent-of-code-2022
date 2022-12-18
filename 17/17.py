import numpy as np
from skimage.morphology import flood_fill

import utils

def make_rocks():
    horizontal = np.ones((1, 4), dtype=np.byte)
    cross = np.zeros((3, 3), dtype=np.byte)
    cross[:, 1], cross[1, :] = 1, 1
    L = np.zeros((3, 3), dtype=np.byte)
    L[:, 0], L[0, :] = 1, 1
    vertical = np.ones([4, 1], dtype=np.byte)
    box = np.ones((2, 2), dtype=np.byte)
    return utils.deque([horizontal, cross, L, vertical, box])


def preprocess(data):
    lookup = {'>': -1, '<': 1}
    return utils.deque([lookup[direction] for direction in data])


def tetris(data, N):

    directions, rocks = data
    max_height = np.sum([shape.shape[0] for shape in rocks]) + 6
    board = np.zeros((max_height, 7), dtype=np.byte)
    lookup = utils.defaultdict(dict)
    abs_top = rel_top = 0
    rock_idx = direction_idx = 0

    for step in range(N):

        idx = (rock_idx, direction_idx)
        board_hash = hash(tuplify(board[rel_top - 64:]))  # randomly chosen magic number 64
        if board_hash in lookup[idx]:
            that_step, that_top = lookup[idx][board_hash]
            remaining_steps, steps_since_that_step = N - step, step - that_step
            full_cycles_remaining, residual_steps = divmod(remaining_steps, steps_since_that_step)
            if residual_steps == 0:
                abs_top += (rel_top - find_floor(board, rel_top))
                return abs_top + (abs_top - that_top) * full_cycles_remaining
        else:
            lookup[idx][board_hash] = (step, abs_top + (rel_top - find_floor(board, rel_top)))

        rock = rocks[rock_idx]

        rock_pos_y, rock_pos_x = rel_top + 3, 7 - (2 +  rock.shape[1])

        while True:

            # Sideways
            direction = directions[direction_idx]
            if not collision(board, rock, (rock_pos_y, rock_pos_x), (0, direction)):
                rock_pos_x += direction

            direction_idx = (direction_idx + 1) % len(directions)

            # Up
            if collision(board, rock, (rock_pos_y, rock_pos_x), (-1, 0)):
                board = place(board, rock, (rock_pos_y, rock_pos_x))
                rel_top = max(rock_pos_y + rock.shape[0], rel_top)

                floor = find_floor(board, rel_top)
                abs_top += floor
                rel_top -= floor
                board = np.pad(board[floor:, :], ((0, max_height), (0, 0)))
                break

            rock_pos_y -= 1

        rock_idx = (rock_idx + 1) % len(rocks)

    return abs_top + (rel_top - find_floor(board, rel_top))


def tuplify(arr):
    return tuple(tuple(line) for line in arr)


def find_floor(board, rel_top):

    j = np.where(np.sum(flood_fill(board.copy(), (board.shape[0] - 1, 3), 1) - board, axis=1))[0][0] - 1
    for i in range(rel_top - 3, j, -1):
        if np.all(np.sum(board[i:i + 4], axis=0)):
            return max(i, j, 0)
    return max(j, 0)


def place(board, rock, rock_pos):
    rock_dim_y, rock_dim_x = rock.shape
    rock_pos_y, rock_pos_x = rock_pos
    board[rock_pos_y: rock_pos_y + rock_dim_y, rock_pos_x: rock_pos_x + rock_dim_x] += rock
    return board


def collision(board, rock, rock_pos, direction):
    rock_dim_y, rock_dim_x = rock.shape
    rock_pos_y, rock_pos_x = rock_pos
    dir_y, dir_x = direction
    new_pos_y, new_pos_x = rock_pos_y + dir_y, rock_pos_x + dir_x

    # Walls and floor
    if new_pos_x < 0 or new_pos_x + rock_dim_x > board.shape[1] or new_pos_y < 0:
        return True

    # Rocks
    if np.any(board[new_pos_y : new_pos_y + rock_dim_y, new_pos_x : new_pos_x + rock_dim_x] + rock > 1):
        return True

    return False


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read()), make_rocks()
    print(tetris(data, 2022))
    timer.stop()  # 12022.58ms
    """

    # Part 2
    timer.start()
    timer.start()
    data = preprocess(utils.read()), make_rocks()
    print(tetris(data, 1000000000000))
    timer.stop()  # 17253.65ms