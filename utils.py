from time import process_time


class Timer:
    def __init__(self):
        self.tic = 0
        self.toc = 0
        self.dur = 0

    def start(self):
        self.tic = process_time()

    def stop(self):
        self.toc = process_time()
        self.dur = self.toc - self.tic
        print(f'finished in {1000 * self.dur:.2f}ms')


def read_int_lines(file='input'):
    with open(file, 'r') as fp:
        sequence = [int(n) for n in fp.read().splitlines()]
    return sequence


def read_int_sequence(file='input'):
    with open(file, 'r') as fp:
        sequence = [int(n) for n in fp.read().split(',')]
    return sequence


def read_str_lines(file='input'):
    with open(file, 'r') as fp:
        sequence = fp.read().splitlines()
    return sequence


def read(file='input'):
    with open(file, 'r') as fp:
        content = fp.read()
    return content
