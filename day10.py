import numpy as np
from itertools import product
from pytest import fixture


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    with open(filename) as f:
        return f.read().splitlines()


def main1(instructions: list):
    """
    What is the sum of these six signal strengths? 20th, 60th, 100th, 140th, 180th, and 220th cycles
    """
    cycles = [1, 1, ]
    for cmd in instructions:
        if cmd == 'noop':
            cycles.append(cycles[-1])
        elif cmd.startswith('addx'):
            _, v = cmd.split()
            v = int(v)
            cycles.append(cycles[-1])
            cycles.append(cycles[-1] + v)

    s = sum(
        i * cycles[i]
        for i in (20, 60, 100, 140, 180, 220)
    )
    return s


def test_part1(sample):
    assert main1(sample) == 21


def main2(instructions: list):
    cycles = [1, ]
    for cmd in instructions:
        if cmd == 'noop':
            cycles.append(cycles[-1])
        elif cmd.startswith('addx'):
            _, v = cmd.split()
            v = int(v)
            cycles.append(cycles[-1])
            cycles.append(cycles[-1] + v)

    crt = [' ', ] * 240
    for i, x in enumerate(cycles):
        if abs(i % 40 - x) <= 1:
            crt[i] = '#'

    print(''.join(crt[:40]))
    print(''.join(crt[40:80]))
    print(''.join(crt[80:120]))
    print(''.join(crt[120:160]))
    print(''.join(crt[160:200]))
    print(''.join(crt[200:240]))


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
