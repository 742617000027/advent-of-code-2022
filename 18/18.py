import utils


def preprocess(data):
    return {(x, y, z): 0 for x, y, z in [[int(i) for i in droplet.split(',')] for droplet in data]}


def surface(data, limits):
    for point, direction in utils.product(data, utils.DIRS3D):
        neighbor = tuple(xn + dxn for xn, dxn in zip(point, direction))
        if neighbor not in data and \
                all([l <= xn <= u for xn, (l, u) in zip(neighbor, tuple(zip(*limits)))]):
            data[point] += 1
    return data


def inner_surface(data, limits):
    return surface(steamfill(data), limits)


def outer_surface(data):
    complete = surface(utils.deepcopy(data), get_limits(data, 1))
    inner = inner_surface(utils.deepcopy(data), get_limits(data))
    for droplet in complete:
        complete[droplet] -= inner[droplet]
    return complete


def steamfill(data, init=(0, 0, 0)):
    (lx, ly, lz), (ux, uy, uz) = get_limits(data, 1)
    data[init] = 0
    q = utils.deque([init])
    while q:
        point = q.popleft()
        x, y, z = point
        for dx, dy, dz in utils.DIRS3D:
            if lx <= x + dx <= ux and ly <= y + dy <= uy and lz <= z + dz <= uz:
                neighbor = (x + dx, y + dy, z + dz)
                if neighbor not in data:
                    data[neighbor] = 0
                    q.append(neighbor)
    return data


def get_limits(data, expansion=0):
    return tuple([0 - expansion] * 3), tuple(max(axis) + expansion for axis in zip(*list(data.keys())))


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(sum([val for val in surface(data, get_limits(data, 1)).values()]))
    timer.stop()  # 15.51ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(sum([val for val in outer_surface(data).values()]))
    timer.stop()  # 76.35ms
