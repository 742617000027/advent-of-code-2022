import utils


def build(data):
    history = [clear(cmd.split('\n')) for cmd in clear(data.split('$ '))]
    cwd = filesystem
    for cmd in history:
        if 'cd' in cmd[0]: cwd = cd(cwd, cmd[0].split()[1])
        if 'ls' in cmd[0]: cwd = ls(cwd, cmd[1:])


def ls(cwd, output):
    for line in output:
        a, b = line.split()
        if a == 'dir':
            cwd['/'][b] = mkdir(cwd)
        else:
            cwd['/'][b] = int(a)
            cwd['size'] += int(a)
            update_parent(cwd, int(a))
    return cwd


def cd(cwd, dir):
    if dir == '..': return cwd['parent']
    if dir == '/': return filesystem
    return cwd['/'][dir]


def mkdir(parent=None):
    return {'parent': parent , 'size': int(), '/': dict()}


def update_parent(cwd, size):
    parent = cwd['parent']
    if parent:
        parent['size'] += size
        update_parent(parent, size)


def clear(l):
    return [e for e in l if e]


def find(cwd, hits, threshold, mode):
    for val in cwd['/'].values():
        if isinstance(val, dict):
            if mode == 'smaller' and val['size'] <= threshold: hits.append(val)
            if mode == 'bigger' and val['size'] >= threshold: hits.append(val)
            hits.extend(find(val, [], threshold, mode))
    return hits


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read()
    filesystem = mkdir()
    build(data)
    hits = find(filesystem, [], 100000, 'smaller')
    print(sum([hit['size'] for hit in hits]))
    timer.stop()  # 1.79ms
    """

    # Part 2
    timer.start()
    data = utils.read()
    filesystem = mkdir()
    build(data)
    unused_diskspace = 70000000 - filesystem['size']
    hits = sorted(find(filesystem, [], 30000000 - unused_diskspace, 'bigger'), key=lambda x: x['size'])
    print(hits[0]['size'])
    timer.stop()  # 1.58ms