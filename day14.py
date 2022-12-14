from pytest import fixture
import numpy as np


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    res = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            path = []
            points = line.split(' -> ')
            for p in points:
                x, y = map(int, p.split(','))
                path.append((x, y))
            res.append(path)
    return res


WALL = 1
SAND = 2
SOURCE = 3


def draw(paths: list, source: (int, int)) -> np.ndarray:
    x_max, x_min, y_max, y_min = 0, 2**63, 0, 0
    for p in paths:
        for x, y in p:
            x_max = max(x_max, x)
            x_min = min(x_min, x)
            y_max = max(y_max, y)

    # expand
    x_max += 2
    x_min -= 1
    y_max += 1

    M = np.zeros((y_max-y_min, x_max-x_min), dtype=int)
    for p in paths:
        for (x1, y1), (x2, y2) in zip(p, p[1:]):
            if x1 == x2:
                y1, y2 = min(y1, y2) - y_min, max(y1, y2) - y_min + 1
                x = x1 - x_min
                M[y1:y2, x] = WALL
            elif y1 == y2:
                x1, x2 = min(x1, x2) - x_min, max(x1, x2) - x_min + 1
                y = y1 - y_min
                M[y, x1:x2] = WALL
            else:
                raise ValueError()
    M[source[1] - y_min, source[0] - x_min] = SOURCE
    return M


def show(cave_map: np.ndarray):
    lines = []
    s = {0: ' ', 1: '#', 2: 'o', 3: '+'}
    for row in cave_map:
        line = ''.join([
            s[p] for p in row
        ])
        lines.append(line)
    print('\n'.join(lines))


def put_sand(M: np.ndarray):
    try:
        (y,), (x,) = np.where(M == SOURCE)
    except:  # source is blocked
        return

    last_row = M.shape[0] - 1
    while y < last_row:
        if M[y+1, x] and M[y+1, x+1] and M[y+1, x-1]:  # all blocked
            M[y, x] = SAND
            return True
        elif M[y+1, x] and M[y+1, x-1]:
            y, x = y + 1, x + 1
        elif M[y+1, x]:
            y, x = y + 1, x - 1
        else:
            y += 1


def main1(paths: list, source=(500, 0)):
    """
    How many units of sand come to rest before sand starts flowing into the abyss below?
    """
    cave_map = draw(paths, source)
    show(cave_map)
    cnt = 0
    while put_sand(cave_map):
        # show(cave_map)
        cnt += 1
    show(cave_map)
    return cnt


def test_part1(sample):
    assert main1(sample) == 24


def main2(paths: list, source=(500, 0)):
    """
    How many units of sand come to rest?
    """
    floor = 2 + max(
        max(y for x, y in p)
        for p in paths
    )
    paths = paths + [[(500-floor-1, floor), (500+floor+1, floor)], ]
    cave_map = draw(paths, source)
    show(cave_map)
    cnt = 0
    while put_sand(cave_map):
        cnt += 1
    show(cave_map)
    return cnt


def test_part2(sample):
    assert main2(sample) == 93


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
