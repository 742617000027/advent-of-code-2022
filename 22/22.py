import re

import utils


def preprocess(data):
    raw = data.split('\n\n')
    raw_board, raw_instructions = raw[0].split('\n'), raw[1]
    max_row_len = max([len(row) for row in raw_board])
    raw_board = [row + ' ' * (max_row_len - len(row)) for row in raw_board]
    board = dict()
    for r, row_str in enumerate(raw_board):
        actual_row = row_str.strip()
        row_start = row_str.find(actual_row)
        row_end = row_start + len(actual_row) - 1

        for c, char in enumerate(actual_row, start=row_start):
            col_str = ''.join([raw_board[i][c] for i in range(len(raw_board))])
            actual_col = col_str.strip()
            col_start = col_str.find(actual_col)
            col_end = col_start + len(actual_col) - 1

            if char == '.':
                board[(r, c)] = dict()

                # Right
                if c < row_end and row_str[c + 1] == '.': board[(r, c)][0] = ((r, c + 1), 0)
                if c == row_end and actual_row[0] == '.': board[(r, c)][0] = ((r, row_start), 0)

                # Down
                if r < col_end and col_str[r + 1] == '.': board[(r, c)][1] = ((r + 1, c), 1)
                if r == col_end and actual_col[0] == '.': board[(r, c)][1] = ((col_start, c), 1)

                # Left
                if c > row_start and row_str[c - 1] == '.': board[(r, c)][2] = ((r, c - 1), 2)
                if c == row_start and actual_row[-1] == '.': board[(r, c)][2] = ((r, row_end), 2)

                # Up
                if r > col_start and col_str[r - 1] == '.': board[(r, c)][3] = ((r - 1, c), 3)
                if r == col_start and actual_col[-1] == '.': board[(r, c)][3] = ((col_end, c), 3)

    steps = [int(step) for step in re.findall(r'(\d+)', raw_instructions)]
    facings = [step for step in re.findall(r'([LR])', raw_instructions)]

    return board, (steps, facings)


def move(data):
    change = {'L': -1, 'R': 1}
    board, (steps, facings) = data
    pos = list(board.keys())[0]
    facing = 0
    while len(steps):

        for _ in range(steps.pop(0)):
            if facing not in board[pos]: break
            pos, facing = board[pos][facing]

        if len(facings): facing = (facing + change[facings.pop(0)]) % 4

    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing


def fold(data, S=50):
    board, instructions = data
    cube = {
        'front': {'offset': {'Y': 0, 'X': S}},
        'back': {'offset': {'Y': 2 * S, 'X': S}},
        'left': {'offset': {'Y': 2 * S, 'X': 0}},
        'right': {'offset': {'Y': 0, 'X': 2 * S}},
        'top': {'offset': {'Y': 3 * S, 'X': 0}},
        'bottom': {'offset': {'Y': S, 'X': S}}
    }

    for name, face in cube.items():
        Y, X = face['offset'].values()
        cube[name]['points'] = {(y, x): neighbors for (y, x), neighbors in board.items() if
                                Y <= y < Y + S and X <= x < X + S}

    for name, face in cube.items():
        Y, X = face['offset'].values()

        for point, neighbors in face['points'].items():
            y, x = point
            y_norm, x_norm = y - Y, x - X

            match name:

                case 'front':
                    if y_norm == 0:
                        if 3 in board[point]: del board[point][3]
                        if (new_neighbor := (x_norm + cube['top']['offset']['Y'], cube['top']['offset']['X'])) in \
                                cube['top']['points']:
                            board[point][3] = (new_neighbor, 0)

                    if x_norm == 0:
                        if 2 in board[point]: del board[point][2]
                        if (
                        new_neighbor := (cube['left']['offset']['Y'] + S - 1 - y_norm, cube['left']['offset']['X'])) in \
                                cube['left']['points']:
                            board[point][2] = (new_neighbor, 0)

                case 'back':
                    if y_norm == S - 1:
                        if 1 in board[point]: del board[point][1]
                        if (
                        new_neighbor := (x_norm + cube['top']['offset']['Y'], cube['top']['offset']['X'] + S - 1)) in \
                                cube['top']['points']:
                            board[point][1] = (new_neighbor, 2)

                    if x_norm == S - 1:
                        if 0 in board[point]: del board[point][0]
                        if (new_neighbor := (
                        cube['right']['offset']['Y'] + S - 1 - y_norm, cube['right']['offset']['X'] + S - 1)) in \
                                cube['right']['points']:
                            board[point][0] = (new_neighbor, 2)

                case 'left':
                    if y_norm == 0:
                        if 3 in board[point]: del board[point][3]
                        if (new_neighbor := (x_norm + cube['bottom']['offset']['Y'], cube['bottom']['offset']['X'])) in \
                                cube['bottom']['points']:
                            board[point][3] = (new_neighbor, 0)

                    if x_norm == 0:
                        if 2 in board[point]: del board[point][2]
                        if (new_neighbor := (
                        cube['front']['offset']['Y'] + S - 1 - y_norm, cube['front']['offset']['X'])) in cube['front'][
                            'points']:
                            board[point][2] = (new_neighbor, 0)

                case 'right':
                    if y_norm == 0:
                        if 3 in board[point]: del board[point][3]
                        if (
                        new_neighbor := (cube['top']['offset']['Y'] + S - 1, x_norm + cube['top']['offset']['X'])) in \
                                cube['top']['points']:
                            board[point][3] = (new_neighbor, 3)

                    if y_norm == S - 1:
                        if 1 in board[point]: del board[point][1]
                        if (new_neighbor := (
                        x_norm + cube['bottom']['offset']['Y'], cube['bottom']['offset']['X'] + S - 1)) in \
                                cube['bottom']['points']:
                            board[point][1] = (new_neighbor, 2)

                    if x_norm == S - 1:
                        if 0 in board[point]: del board[point][0]
                        if (new_neighbor := (
                        cube['back']['offset']['Y'] + S - 1 - y_norm, cube['back']['offset']['X'] + S - 1)) in \
                                cube['back']['points']:
                            board[point][0] = (new_neighbor, 2)

                case 'top':
                    if y_norm == S - 1:
                        if 1 in board[point]: del board[point][1]
                        if (new_neighbor := (cube['right']['offset']['Y'], x_norm + cube['right']['offset']['X'])) in \
                                cube['right']['points']:
                            board[point][1] = (new_neighbor, 1)

                    if x_norm == 0:
                        if 2 in board[point]: del board[point][2]
                        if (new_neighbor := (cube['front']['offset']['Y'], y_norm + cube['front']['offset']['X'])) in \
                                cube['front']['points']:
                            board[point][2] = (new_neighbor, 1)

                    if x_norm == S - 1:
                        if 0 in board[point]: del board[point][0]
                        if (
                        new_neighbor := (cube['back']['offset']['Y'] + S - 1, y_norm + cube['back']['offset']['X'])) in \
                                cube['back']['points']:
                            board[point][0] = (new_neighbor, 3)

                case 'bottom':
                    if x_norm == 0:
                        if 2 in board[point]: del board[point][2]
                        if (new_neighbor := (cube['left']['offset']['Y'], y_norm + cube['left']['offset']['X'])) in \
                                cube['left']['points']:
                            board[point][2] = (new_neighbor, 1)

                    if x_norm == S - 1:
                        if 0 in board[point]: del board[point][0]
                        if (new_neighbor := (
                        cube['right']['offset']['Y'] + S - 1, y_norm + cube['right']['offset']['X'])) in cube['right'][
                            'points']:
                            board[point][0] = (new_neighbor, 3)

    return board, instructions


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read())
    print(move(data))
    timer.stop()  # 562.54ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read())
    print(move(fold(data)))
    timer.stop()  # 1091.46ms
