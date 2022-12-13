from pytest import fixture
from itertools import chain
from functools import cmp_to_key


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    res = []
    with open(filename) as f:
        groups = f.read().split('\n\n')
        for line1, line2 in map(str.splitlines, groups):
            res.append((eval(line1), eval(line2)))
    return res


def compare(packet1, packet2):
    """1 if packet2 > packet1; -1 if packet2 < packet1; 0 if packet2 == packet1"""
    if isinstance(packet1, int) and isinstance(packet2, int):
        if packet2 > packet1:
            return 1
        elif packet2 < packet1:
            return -1
        else:
            return 0
    elif isinstance(packet1, list) and isinstance(packet2, list):
        for v1, v2 in zip(packet1, packet2):
            c = compare(v1, v2)
            if c != 0:
                return c
        else:
            return compare(len(packet1), len(packet2))
    elif isinstance(packet1, int) and isinstance(packet2, list):
        return compare([packet1, ], packet2)
    elif isinstance(packet1, list) and isinstance(packet2, int):
        return compare(packet1, [packet2, ])


def main1(pairs: list):
    """
    How many pairs of packets are in the right order.
    What is the sum of the indices of those pairs?
    """
    return sum(
        i
        for i, (packet1, packet2) in enumerate(pairs, start=1)
        if compare(packet1, packet2) == 1
    )


def test_part1(sample):
    assert main1(sample) == 13


def main2(pairs: list):
    """
    Put all of the packets in the right order
    What is the decoder key for the distress signal?
    """
    divider_packets = [[2]], [[6]]
    pairs = pairs + [divider_packets, ]
    packets = chain.from_iterable(pairs)
    packets = sorted(packets, key=cmp_to_key(compare), reverse=True)
    ind1, ind2 = map(packets.index, divider_packets)
    return (ind1 + 1) * (ind2 + 1)


def test_part2(sample):
    assert main2(sample) == 140


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
