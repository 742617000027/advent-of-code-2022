import re

import utils


def preprocess(data):
    regex = r'Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)'
    return [tuple(int(i) for i in re.match(regex, row).groups()) for row in data]


def compute_coverage_at_row(data, row):
    coverage_at_row = set()
    sensors, beacons = [set(devices) for devices in zip(*[[(sx, sy), (bx, by)] for sx, sy, bx, by in data])]
    for sx, sy, bx, by in data:
        distance_beacon, distance_row = manhatten(sx, sy, bx, by), abs(sy - row)
        if (x_range := distance_beacon - distance_row) < 0: continue
        coverage_at_row |= set(utils.product([sx + dx for dx in range(-x_range, x_range + 1)], [row])).difference(sensors | beacons)
    return coverage_at_row


def make_hulls(data):
    hulls = []
    for sx, sy, bx, by in data:
        distance_beacon = manhatten(sx, sy, bx, by) + 1
        hull = set()
        for dx in range(-distance_beacon, distance_beacon + 1):
            dy = distance_beacon - abs(dx)
            hull |= {(sx + dx, sy + dy), (sx + dx, sy - dy)}
        hulls.append(hull)
    return hulls


def manhatten(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)


def tuning_freq(hulls, lower, upper):
    for perm in utils.combinations(hulls, 4):
        intersection = set.intersection(*perm)
        if len(intersection) == 1:
            (point, ) = intersection
            x, y = point
            if lower <= x <= upper and lower <= y <= upper and not covered(hulls, point): return x * 4000000 + y


def covered(hulls, point):
    ret = False
    px, py = point
    for hull in hulls:
        limits = sorted([(x, y) for x, y in hull if y == py], key=lambda point: point[0])
        if len(limits) < 2: continue
        (lx, ly), (ux, uy) = limits
        if lx < px < ux:
            ret = True
            break
    return ret


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(len(compute_coverage_at_row(data, 2000000)))
    timer.stop()  # 5813.13ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(tuning_freq(make_hulls(data), 0, 4000000))
    timer.stop()  # 104601.50ms
