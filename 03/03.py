import utils


def split(r):
    return {c for c in r[:len(r) // 2]}, {c for c in r[len(r) // 2:]}


def group(rucksacks):
    return [{c for c in rucksack} for rucksack in rucksacks]


def common(*args):
    a, b = args[:2]
    i = a.intersection(b)
    if len(args) > 2: i = common(i, *args[2:])
    if len(i) == 1: (i, ) = i
    return i


def prio(i):
    p = ord(i) - 96
    return p if p > 0 else p + 58


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read_str_lines()
    print(sum([prio(common(*split(rucksack))) for rucksack in data]))
    timer.stop()  # 4.83ms
    """

    # Part 2
    timer.start()
    data = utils.read_str_lines()
    print(sum([prio(common(*group(data[i:i+3]))) for i in range(0, len(data), 3)]))
    timer.stop()  # 3.85ms
