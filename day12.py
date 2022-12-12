from pytest import fixture
import numpy as np


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> (np.array, (int, int), (int, int)):
    with open(filename) as f:
        heightmap = [
            list(map(ord, line))
            for line in f.read().splitlines()
        ]

    heightmap = np.asarray(heightmap, dtype=int) - 97
    (x,), (y,) = np.where(heightmap == -14)  # S - start
    start = (x, y)
    heightmap[x, y] = 0  # replace S with a
    (x, ), (y, ) = np.where(heightmap == -28)  # E - destination
    dest = (x, y)
    heightmap[x, y] = 25  # replace E with z
    return heightmap, start, dest


def main1(heightmap: np.array, start: (int, int), dest: (int, int)):
    """
    What is the fewest steps required to move from your current position to the location that should get the best signal?
    """
    n, m = heightmap.shape
    inf = n * m
    stepmap = np.zeros_like(heightmap) + inf
    stepmap[start] = 0
    visitedmap = np.zeros_like(heightmap, dtype=bool)

    def neighbors(x, y):
        h = heightmap[x, y]
        res = []
        if x > 0 and heightmap[x-1, y] - h <= 1 and not visitedmap[x-1, y]:
            res.append((x-1, y))
        if x < n-1 and heightmap[x+1, y] - h <= 1 and not visitedmap[x+1, y]:
            res.append((x+1, y))
        if y > 0 and heightmap[x, y-1] - h <= 1 and not visitedmap[x, y-1]:
            res.append((x, y-1))
        if y < m-1 and heightmap[x, y+1] - h <= 1 and not visitedmap[x, y+1]:
            res.append((x, y+1))
        return res

    while stepmap[dest] == inf:
        idx = np.argmin(stepmap + inf * visitedmap)
        x, y = idx // m, idx % m
        visitedmap[x, y] = True
        d = stepmap[x, y]
        for x, y in neighbors(x, y):
            stepmap[x, y] = min(stepmap[x, y], d + 1)

    return stepmap[dest]


def test_part1(sample):
    assert main1(*sample) == 31


def main2(heightmap: np.array, start: (int, int), dest: (int, int)):
    """
    What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
    """
    n, m = heightmap.shape
    inf = n * m
    stepmap = np.zeros_like(heightmap) + inf
    stepmap[dest] = 0
    visitedmap = np.zeros_like(heightmap, dtype=bool)

    def neighbors(x, y):
        h = heightmap[x, y]
        res = []
        if x > 0 and heightmap[x-1, y] - h >= -1 and not visitedmap[x-1, y]:
            res.append((x-1, y))
        if x < n-1 and heightmap[x+1, y] - h >= -1 and not visitedmap[x+1, y]:
            res.append((x+1, y))
        if y > 0 and heightmap[x, y-1] - h >= -1 and not visitedmap[x, y-1]:
            res.append((x, y-1))
        if y < m-1 and heightmap[x, y+1] - h >= -1 and not visitedmap[x, y+1]:
            res.append((x, y+1))
        return res

    for _ in range(n * m):
        idx = np.argmin(stepmap + inf * visitedmap)
        x, y = idx // m, idx % m
        visitedmap[x, y] = True
        d = stepmap[x, y]
        if d == inf:  # there are isolated areas
            break

        for x, y in neighbors(x, y):
            stepmap[x, y] = min(stepmap[x, y], d + 1)

    return np.min(stepmap[heightmap == 0])


def test_part2(sample):
    assert main2(*sample) == 29


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(*data))
    print(main2(*data))
