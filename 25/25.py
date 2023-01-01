import operator

import utils


def sna2dec(sna):
    ret, repl = 0, {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    for i, c in enumerate(sna[::-1]):
        ret += repl[c] * 5**i
    return ret


def dec2sna(dec):
    if dec in [-2, -1, 0, 1, 2]: return str(dec), 0
    E, head, repl, op = 0, '', {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}, {True: operator.ge, False: operator.le}
    sign = (2 * (dec >= 0) - 1)
    while True:
        for mult in [0, 1, 2]:
            if op[dec >= 0](sum([(sign * mult if e == E else sign * 2) * 5**e for e in range(E + 1)]), dec):
                head += repl[sign * mult]
                break
        if head != '': break
        E += 1

    tail, tail_E = dec2sna(dec - sna2dec(f'{head:0{E + 1}}'))
    body = head + f'{"0" * (E - tail_E - 1)}{tail}'
    return body, E


if __name__ == '__main__':
    timer = utils.Timer()

    # Part 1
    timer.start()
    data = utils.read_str_lines()
    print(dec2sna(sum([sna2dec(line) for line in data]))[0])
    timer.stop()  # 10.08ms
