import utils


def subroutine(data, window):
    for i in range(len(data) - window):
        substr = data[i:i+window]
        if len(setlify(substr)) < len(substr):
            continue
        return i + window


def setlify(substr):
    return {c for c in substr}


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read()
    print(subroutine(data, window=4))
    timer.stop()  # 0.93ms
    """

    # Part 2
    timer.start()
    data = utils.read()
    print(subroutine(data, window=14))
    timer.stop()  # 3.57ms
