import re

from numpy import prod
from tqdm import tqdm

import utils


def preprocess(data):
    monkeys = {i: {
        'n_inspections': 0,
        'items': [int(item) for item in re.findall(r'(\d+)', monkey[0])],
        'op': monkey[1][17:],
        'test': int(re.search(r'(\d+)', monkey[2]).group()),
        True: int(re.search(r'(\d+)', monkey[3]).group()),
        False: int(re.search(r'(\d+)', monkey[4]).group())
    } for i, monkey in enumerate([
        [attribute.strip()
         for attribute
         in monkey.split('\n')[1:]]
        for monkey
        in data.split('\n\n')
    ])}
    magic = prod([monkey['test'] for monkey in monkeys.values()])
    return monkeys, magic


def run(data, n_rounds, relief=1):
    monkeys, magic = data

    for round in tqdm(range(n_rounds)):

        for m, monkey in monkeys.items():
            monkey['n_inspections'] += len(monkey['items'])

            for item in monkey['items']:
                item = inspect(item, monkey['op'], magic, relief)
                to = monkey[test(item, monkey['test'])]
                monkeys[to]['items'].append(item)
            monkey['items'] = []

    return monkeys


def inspect(old, op, magic, relief):
    return (eval(op) // relief) % magic


def test(item, test):
    return item % test == 0


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = preprocess(utils.read())
    monkeys = run(data, n_rounds=20, relief=3)
    print(prod(sorted([monkey['n_inspections'] for monkey in monkeys.values()])[-2:]))
    timer.stop()  # 26.12ms
    """

    # Part 2
    timer.start()
    data = preprocess(utils.read())
    monkeys = run(data, n_rounds=10000)
    print(prod(sorted([monkey['n_inspections'] for monkey in monkeys.values()])[-2:]))
    timer.stop()  # 5496.42ms
