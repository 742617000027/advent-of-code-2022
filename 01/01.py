import utils


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    print(max([sum([int(i) for i in s.split('\n')]) for s in utils.read().split('\n\n')]))
    timer.stop()  # 7.09ms
    """

    # Part 2
    timer.start()
    ordered = sorted([sum([int(i) for i in s.split('\n')]) for s in utils.read().split('\n\n')], reverse=True)
    print(sum(ordered[:3]))
    timer.stop()  # 6.67ms

