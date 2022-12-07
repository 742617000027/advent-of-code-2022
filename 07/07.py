import operator

import utils


OP = {'<=': operator.le, '>=': operator.ge}


def build(data):
    history = [clear(cmd.split('\n')) for cmd in clear(data.split('$ '))]
    cwd = filesystem
    for cmd in history: cwd = execute(cwd, cmd)


def execute(cwd, cmd):
    return globals()[cmd[0].split().pop(0)](cwd, cmd)


def ls(cwd, cmd):
    output = cmd[1:]
    for line in output:
        info, name = line.split()
        if info == 'dir': mkdir(name, cwd)
        else: mkfile(name, info, cwd)
    return cwd


def cd(cwd, cmd):
    arg = cmd[0].split()[1]
    if arg == '..': return cwd['..']
    if arg == '/': return filesystem
    return cwd['/'][arg]


def mkdir(name, cwd):
    cwd['/'][name] = {'..': cwd , 'size': int(), '/': dict()}


def mkfile(name, info, cwd):
    cwd['/'][name] = int(info)
    cwd['size'] += int(info)
    update_parent(cwd, int(info))


def update_parent(cwd, size):
    parent = cwd['..']
    if parent:
        parent['size'] += size
        update_parent(parent, size)


def clear(l):
    return [e for e in l if e]


def find(cwd, threshold, mode):
    hits = []
    for val in cwd['/'].values():
        if isinstance(val, dict):
            if OP[mode](val['size'], threshold): hits.append(val)
            hits.extend(find(val, threshold, mode))
    return hits


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read()
    filesystem = {'..': None , 'size': int(), '/': dict()}
    build(data)
    hits = find(filesystem, [], 100000, '<=')
    print(sum([hit['size'] for hit in hits]))
    timer.stop()  # 1.79ms
    """

    # Part 2
    timer.start()
    data = utils.read()
    filesystem = {'..': None , 'size': int(), '/': dict()}
    build(data)
    unused_diskspace = 70000000 - filesystem['size']
    hits = sorted(find(filesystem, 30000000 - unused_diskspace, '>='), key=lambda x: x['size'])
    print(hits[0]['size'])
    timer.stop()  # 1.58ms