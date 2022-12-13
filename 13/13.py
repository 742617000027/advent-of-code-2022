import utils


def preprocess(data):
    return [[eval(packet) for packet in pair.split('\n')] for pair in data.split('\n\n')]


def compare(l, r):
    for a, b in zip(*[l, r]):
        while True:
             match (a, b):
                case (int(), int()):
                    if a < b: return 1
                    if b < a: return -1
                    break
                case (list(), list()):
                    ret = compare(a[:len(b)], b[:len(a)])
                    if ret is not None: return ret
                    if len(a) < len(b): return 1
                    if len(b) < len(a): return -1
                    break
                case _:
                    if isinstance(a, int): a = [a]
                    if isinstance(b, int): b = [b]
    if len(l) < len(r): return 1
    if len(r) < len(l): return -1


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read())
    print(sum([i if compare(a, b) > 0 else 0 for i, (a, b) in enumerate(data, start=1)]))
    timer.stop()  # 14.26ms
    """

    # Part 2
    timer.start()
    divider = [[[2]], [[6]]]
    data = sorted(preprocess(utils.read().replace('\n\n', '\n')).pop() + divider,
                  key=utils.cmp_to_key(compare),
                  reverse=True)
    print(utils.reduce(lambda a, b: a * b, [i for i, elem in enumerate(data, start=1) if elem in divider]))
    timer.stop()  # 27.70ms
