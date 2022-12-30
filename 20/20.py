import utils


def mix(l, decryptinon_key=1, n_mixes=1):
    l = [shift * decryptinon_key for shift in l]
    positions = [(i, shift) for i, shift in enumerate(l)]
    for _ in range(n_mixes):
        for i, shift in enumerate(l):
            current_i = positions.index((i, shift))
            positions.pop(current_i)
            new_i = (current_i + shift) % (len(l) - 1)
            positions = positions[:new_i] + [(i, shift)] + positions[new_i:]
    return [x for _, x in positions]


def coords(l):
    idx = l.index(0)
    return tuple(l[(idx + i * 1000) % len(l)] for i in range(1, 4))


if __name__  == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read_int_lines()
    print(sum(coords(mix(data))))
    timer.stop()  # 1132.25ms
    """

    # Part 2
    timer.start()
    data = utils.read_int_lines()
    print(sum(coords(mix(data, decryptinon_key=811589153, n_mixes=10))))
    timer.stop()  # 3542.98ms
