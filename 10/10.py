import utils


def run_cycles(data):
    X = 1
    cycles = []
    for line in data:
        split = line.split()
        op = split.pop(0)
        if op == 'noop':
            cycles.append(X)
        if op =='addx':
            cycles.extend([X] * 2)
            X += int(split.pop())
    return cycles


def draw(cycles):
    crt = ['' for _ in range(6)]
    for i, sprite_pos in enumerate(cycles):
        row, pixel_pos = divmod(i, 40)
        crt[row] += '#' if sprite_pos - 1 <= pixel_pos <= sprite_pos + 1 else '.'
    return '\n'.join([''.join(row) for row in crt])


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read_str_lines()
    cycles = run_cycles(data)
    print(sum([cycles[idx - 1] * idx for idx in [20, 60, 100, 140, 180, 220]]))
    timer.stop()  # 0.20ms
    """

    # Part 2
    timer.start()
    data = utils.read_str_lines()
    cycles = run_cycles(data)
    crt = draw(cycles)
    print(crt)
    timer.stop()  # 0.31ms
