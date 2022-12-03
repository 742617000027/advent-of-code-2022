import utils


def part1(game):
    p1, p2 = ord(game[0]) - 64, ord(game[1]) - 23 - 64
    d = p2 - p1
    if d == 0: return p2 + 3
    if d > 0: return p2 + 6 if d == 1 else p2
    if d < 0: return p2 + 6 if d == -2 else p2


def part2(game):
    p1, p2 = ord(game[0]) - 64, game[1]
    if p2 == 'X': return ((p1 + 1) % 3) + 1
    if p2 == 'Y': return 3 + p1
    if p2 == 'Z': return 6 + (p1 % 3) + 1


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = [line.split() for line in utils.read_str_lines()]
    points = [part1(game) for game in data]
    print(sum(points))
    timer.stop()  # 2.86ms
    """

    # Part 2
    timer.start()
    data = [line.split() for line in utils.read_str_lines()]
    points = [part2(game) for game in data]
    print(sum(points))
    timer.stop()  # 5.25ms