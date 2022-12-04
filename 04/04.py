import utils


def preprocess(data):
    return [[setlify(*section) for section in split('-', *split(',', [pair]))] for pair in data]


def split(sep, *args):
    return [inner.split(sep) for outer in args for inner in outer]


def setlify(lower, upper):
    return {i for i in range(int(lower), int(upper) + 1)}


def diff(a, b):
    if a > b: a, b = b, a
    return a.difference(b)


def intersect(a, b):
    return a.intersection(b)


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(sum([len(diff(*pair)) == 0 for pair in data]))
    timer.stop()  # 13.60ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(sum([len(intersect(*pair)) > 0 for pair in data]))
    timer.stop()  # 24.75ms
