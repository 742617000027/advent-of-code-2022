import operator

import networkx as nx

import utils

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}


def preprocess(data):
    d = dict()
    for line in data:
        c, val = line.split(': ')
        try:
            d[c] = int(val)
        except ValueError:
            a, op, b = val.split()
            d[c] = {'a': a, 'b': b, 'op': op}
    return d


def solve(data):
    ret = utils.deepcopy(data)
    while True:
        for key, val in ret.items():
            if isinstance(val, dict) and isinstance(ret[val['a']], int) and isinstance(ret[val['b']], int):
                ret[key] = OPS[val['op']](ret[val['a']], ret[val['b']])
        if all([isinstance(val, int) for val in ret.values()]):
            return ret


def revsolve(data, solved):
    inv = {'+': '-', '-': '+', '*': '/', '/': '*'}
    G = nx.DiGraph()
    for key, val in data.items():
        if isinstance(val, dict):
            G.add_edge(val['a'], key)
            G.add_edge(val['b'], key)
    path = list(reversed(nx.shortest_path(G, 'humn', 'root')))[1:]
    a, b = data['root']['a'], data['root']['b']
    x = solved[b if a in path else a]
    for node in path[:-1]:
        a, b, op = data[node]['a'], data[node]['b'], data[node]['op']
        fixed, switch = solved[b if a in path else a], b in path
        if switch and op in ['-', '/']: x = OPS[op](fixed, x)
        else: x = OPS[inv[op]](x, fixed)
    return x


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read_str_lines())
    print(solve(data)['root'])
    timer.stop()  # 103.91ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read_str_lines())
    solved = solve(data)
    print(revsolve(data, solved))
    timer.stop()  # 218.53ms
