import re

import utils


def preprocess(data):
    configuration, procedure = data.split('\n\n')
    crates = parse_configuration(configuration)
    moves = parse_procedure(procedure)
    return crates, moves


def parse_configuration(configuration):
    configuration = configuration.split('\n')[:-1]
    width = max([len(s) for s in configuration]) + 1
    return [reverse([unwrap(row, col) for row in configuration if not_empty(row, col)]) for col in range(0, width, 4)]


def reverse(l):
    return list(reversed(l))


def not_empty(row, col):
    return row[col:col + 4].strip() != ''


def unwrap(wrapped, col):
    (crate,) = re.search(r'\s*\[([A-Z])]\s*', wrapped[col:col + 4]).groups()
    return crate


def parse_procedure(procedure):
    procedure = procedure.split('\n')
    return [parse_procedure_step(step) for step in procedure]


def parse_procedure_step(step):
    N, fro, to = re.search(r'move (\d+) from (\d+) to (\d+)', step).groups()
    return int(N), int(fro) - 1, int(to) - 1


def perform_moves(crates, moves, mode):
    for N, fro, to in moves:
        for n in range(-N, 0):
            if mode == 9000: crates[to].append(crates[fro].pop())
            if mode == 9001: crates[to].append(crates[fro].pop(n))
    return crates


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    """
    timer.start()
    data = utils.read()
    crates = perform_moves(*preprocess(data), mode=9000)
    print(''.join([col.pop() for col in crates]))
    timer.stop()  # 2.09ms
    """

    # Part 2
    timer.start()
    data = utils.read()
    crates = perform_moves(*preprocess(data), mode=9001)
    print(''.join([col.pop() for col in crates]))
    timer.stop()  # 1.64ms
