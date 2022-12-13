import utils


def preprocess(data):
    return [[eval(packet) for packet in pair.split('\n')] for pair in data.split('\n\n')]


def compare(pair):
    for a, b in zip(*pair):
        while True:
             match (a, b):
                case (int(), int()):
                    if a < b: return True
                    if b < a: return False
                    break
                case (list(), list()):
                    ret = compare([a[:len(b)], b[:len(a)]])
                    if ret is not None: return ret
                    if len(a) < len(b): return True
                    if len(b) < len(a): return False
                    break
                case _:
                    swap = isinstance(a, list)
                    if swap: b, a = a, b
                    a = [a]
                    if swap: a, b = b, a
    a, b = pair
    if len(a) < len(b): return True
    if len(b) < len(a): return False


def sort(data):
    l = data[:]
    for i, j in zip(range(1, len(l)), range(len(l) - 1)):
        key = l[i]
        while j >= 0 and compare([key, l[j]]):
            l[j+1] = l[j]
            j -= 1
        l[j+1] = key
    return l


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read())
    print(sum([i if compare(pair) else 0 for i, pair in enumerate(data, start=1)]))
    timer.stop()  # 14.26ms
    """

    # Part 2
    timer.start()
    divider = [[[2]], [[6]]]
    data = preprocess(utils.read().replace('\n\n', '\n')).pop() + divider
    print(utils.reduce(lambda a, b: a * b, [i for i, elem in enumerate(sort(data), start=1) if elem in divider]))
    timer.stop()  # 59.21ms
