import utils


def preprocess(data):
    return {(r, c): None for r, row in enumerate(data) for c, char in enumerate(row) if char == '#'}


def reposition(elves, N):
    directions = [
        ((-1, 0), [(dy, dx) for dy, dx in utils.DIAGDIRS if dy == -1]),
        ((1, 0), [(dy, dx) for dy, dx in utils.DIAGDIRS if dy == 1]),
        ((0, -1), [(dy, dx) for dy, dx in utils.DIAGDIRS if dx == -1]),
        ((0, 1), [(dy, dx) for dy, dx in utils.DIAGDIRS if dx == 1])
    ]

    round = 1
    while True:

        for y, x in elves:
            if not any([(y + dy, x + dx) in elves for dy, dx in utils.DIAGDIRS]): continue
            for (dy, dx), check in directions:
                move_to = (y + dy, x + dx) if not any([(y + dyy, x + dxx) in elves for dyy, dxx in check]) else None
                elves[(y, x)] = move_to
                if move_to is not None: break

        if all([move_to is None for move_to in elves.values()]): return elves, round
        counts = utils.Counter(elves.values())
        elves = {(elf if move_to is None or counts[move_to] > 1 else move_to): None for elf, move_to in elves.items()}
        directions = directions[1:] + [directions[0]]
        if N is not None and round == N: break
        round += 1

    return elves, round


def empty(elves):
    Y, X = list(zip(*elves.keys()))
    min_Y, max_Y = min(Y), max(Y)
    min_X, max_X = min(X), max(X)
    return abs(max_Y + 1 - min_Y) * abs(max_X + 1 - min_X) - len(elves)


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    elves, _ = reposition(data, N=10)
    print(empty(elves))
    timer.stop()  # 664.78ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    _, round = reposition(data, N=None)
    print(round)
    timer.stop()  # 4124.44ms
