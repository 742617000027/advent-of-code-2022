import utils


def preprocess(data):
    directions = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
    blizzards = [
        ((r, c), directions[direction])
        for r, row
        in enumerate(data)
        for c, direction
        in enumerate(row)
        if direction in directions
    ]
    start, end = (0, data[0].index('.')), (len(data) - 1, data[-1].index('.'))
    return blizzards, start, end, len(data), len(data[0])


def run(data, trips=1):
    blizzards, start, end, Y, X = data
    universes = {start}
    trip = minute = 0

    while True:

        # Move blizzards
        blizzards = [
            ((wrap(dy + y, Y), wrap(dx + x, X)), (dy, dx))
            for (y, x), (dy, dx)
            in blizzards
        ]
        current_blizzards = {pos for pos, _ in blizzards}

        # Move self
        new = set()
        for y, x in universes:
            neighbors = [
                (dy + y, dx + x)
                for dy, dx
                in utils.DIRS
                if (0 < dy + y < Y - 1 and 0 < dx + x < X - 1) or (dy + y, dx + x) in [start, end]
            ]
            for neighbor in neighbors:
                if neighbor not in current_blizzards: new.add(neighbor)

        universes |= new
        universes = universes.difference(current_blizzards)
        minute += 1

        if end in universes:
            trip += 1
            if trip == trips: return minute
            start, end = end, start
            universes = {start}

def wrap(a, b):
    return ((a - 1) % (b - 2)) + 1


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(run(data))
    timer.stop()  # 1324.50ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(run(data, trips=3))
    timer.stop()  # 2407.73ms
