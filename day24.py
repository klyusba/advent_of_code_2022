from pytest import fixture
import numpy as np
import heapq as hp


@fixture
def sample():
    return read('sample.txt')


class Valley:
    def __init__(self, blizzards: list):
        M = []
        v = {'.': 0, '>': 1, 'v': 2, '<': 3, '^': 4, '#': 5}
        for line in blizzards:
            M.append([v[c] for c in line])

        M = np.asarray(M, dtype=int)
        self._R = M[1:-1, 1:-1] == 1
        self._D = M[1:-1, 1:-1] == 2
        self._L = M[1:-1, 1:-1] == 3
        self._U = M[1:-1, 1:-1] == 4

    @property
    def shape(self):
        return self._R.shape

    def __getitem__(self, item):
        s, x, y = item
        n, m = self._R.shape
        return (
            self._R[x, (y-s) % m]
            + self._D[(x-s) % n, y] * 2
            + self._L[x, (y+s) % m] * 4
            + self._U[(x+s) % n, y] * 8
        )

    def free_spaces(self, s, x, y):
        n, m = self._R.shape
        res = []
        if self[s, x, y] == 0:
            res.append((x, y))
        if x < n-1 and self[s, x+1, y] == 0:
            res.append((x+1, y))
        if x > 0 and self[s, x-1, y] == 0:
            res.append((x-1, y))
        if y < m-1 and self[s, x, y+1] == 0:
            res.append((x, y+1))
        if y > 0 and self[s, x, y-1] == 0:
            res.append((x, y-1))
        return res

    def print(self, s):
        n, m = self.shape
        for i in range(n):
            line = []
            for j in range(m):
                v = self[s, i, j]
                cnt = bin(v).count("1")
                if cnt >= 2:
                    line.append(str(cnt))
                elif v & 1:
                    line.append('>')
                elif v & 2:
                    line.append('v')
                elif v & 4:
                    line.append('<')
                elif v & 8:
                    line.append('^')
                else:
                    line.append('.')
            print(''.join(line))
        print('')


def read(filename: str) -> Valley:
    with open(filename) as f:
        return Valley(f.read().splitlines())


def shortest_path(blizzards: Valley, start, target):
    q = [start, ]
    visited = set()

    while q:
        node = hp.heappop(q)
        if node not in visited:
            visited.add(node)
            d, pos_x, pos_y = node
            if (pos_x, pos_y) == target:
                return d

            for x, y in blizzards.free_spaces(d, pos_x, pos_y):
                hp.heappush(q, (d+1, x, y))
    return 0


def main1(blizzards: Valley):
    """
    What is the fewest number of minutes required to avoid the blizzards and reach the goal?
    """
    n, m = blizzards.shape
    target = n-1, m-1
    start = 2, 0, 0
    return shortest_path(blizzards, start, target)


def test_part1(sample):
    assert main1(sample) == 18


def main2(blizzards: Valley):
    """
    What is the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again?
    """
    n, m = blizzards.shape
    target = n-1, m-1
    d1 = shortest_path(blizzards, (2, 0, 0), target)
    print(d1)
    # wait for open path
    while True:
        d1 += 1
        d2 = shortest_path(blizzards, (d1, *target), (0, 0))
        if d2:
            break

    print(d2 - d1)
    d3 = shortest_path(blizzards, (d2, 0, 0), target)
    print(d3 - d2)
    return d3


def test_part2(sample):
    assert main2(sample) == 54


if __name__ == "__main__":
    data = read('input.txt')
    # data = read('sample.txt')
    # print(main1(data))
    print(main2(data))
