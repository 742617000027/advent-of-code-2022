import re
from copy import deepcopy
from tqdm import tqdm
import networkx as nx

import utils


def preprocess(data):
    regex = r'Valve ([A-Z]+) has flow rate=(\d+)'
    G = nx.DiGraph()
    for line in data:
        head, tail = line.split('; ')
        (valve, flow) = re.match(regex, head).groups()
        neighbors = tail.replace('s', '').replace('tunnel lead to valve ', '').split(', ')
        G.add_node(valve, flow=int(flow), open=False)
        for neighbor in neighbors:
            G.add_edge(valve, neighbor)
    return G


def search(g, source, total, remaining, path, pbar):
    targets = [node for node, values in g.nodes.items() if values['flow'] > 0 and not values['open']]
    if len(targets) == 0:
        results.add(total)
    for target in targets:
        minutes = nx.shortest_path_length(g, source, target) + 1
        if (remaining - minutes) > 0:
            pbar.set_postfix(a=max(results), z=path)
            pbar.update(1)
            h = deepcopy(g)
            h.nodes[target]['open'] = True
            search(h, target, total + (remaining - minutes) * h.nodes[target]['flow'], remaining - minutes, path + (target, ), pbar)
            continue
        results.add(total)


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    timer.start()
    data = preprocess(utils.read_str_lines())
    results = {0}
    with tqdm(desc='Search') as pbar:
        search(data, 'AA', 0, 30, ('AA',), pbar)
    print(max(results))
    timer.stop()  # 236541.84ms
