from pytest import fixture
import numpy as np
import re


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> (np.ndarray, list):
    with open(filename) as f:
        map, path = f.read().split('\n\n')
    # parse map
    map = map.splitlines()
    max_x = max(len(line) for line in map)
    M = np.zeros((len(map), max_x), dtype=int)
    v = {' ': 0, '.': 1, '#': 2}
    for i, line in enumerate(map):
        for j, c in enumerate(line):
            M[i, j] = v[c]

    # parse path
    path = re.split(r'([RL])', path)
    for i in range(0, len(path), 2):
        path[i] = int(path[i])
    return M, path


def password(row, col, face):
    return 1000 * (row + 1) + 4 * (col + 1) + face


def get_slice(M, row=None, col=None):
    if row is not None:
        row = M[row, :]
        idx, = np.where(row)
        return row[idx], idx[0], idx[-1]
    if col is not None:
        col = M[:, col]
        idx, = np.where(col)
        return col[idx], idx[0], idx[-1]


def find_stop_point(field: np.ndarray, start: int, step: int) -> int:
    n = field.shape[0]
    pos = start
    for i in range(1, step+1):
        pos = (start + i) % n
        if field[pos] == 2:
            return (pos - 1) % n
    return pos


def move_right(M: np.ndarray, x: int, y: int, step: int) -> int:
    row, start, end = get_slice(M, row=x)
    y = find_stop_point(row, y-start, step) + start
    return y


def move_left(M: np.ndarray, x: int, y: int, step: int) -> int:
    row, start, end = get_slice(M, row=x)
    y = end - find_stop_point(row[::-1], end - y, step)
    return y


def move_down(M: np.ndarray, x: int, y: int, step: int) -> int:
    col, start, end = get_slice(M, col=y)
    x = find_stop_point(col, x-start, step) + start
    return x


def move_up(M: np.ndarray, x: int, y: int, step: int) -> int:
    col, start, end = get_slice(M, col=y)
    x = end - find_stop_point(col[::-1], end - x, step)
    return x


def move(M: np.ndarray, pos: list, step: int) -> list:
    row, col, face = pos
    if face == 0:
        col = move_right(M, row, col, step)
    elif face == 1:
        row = move_down(M, row, col, step)
    elif face == 2:
        col = move_left(M, row, col, step)
    elif face == 3:
        row = move_up(M, row, col, step)
    else:
        raise ValueError()
    return [row, col, face]


def main1(M: np.ndarray, path: list):
    """
    What is the final password?
    """
    faces = '>v<^'
    x, y = np.where(M)
    pos = [x[0], y[0], 0]  # row, col, >
    for step in path:
        if isinstance(step, int):
            pos = move(M, pos, step)
        elif step == 'L':
            pos[-1] = (pos[-1] - 1) % 4
        elif step == 'R':
            pos[-1] = (pos[-1] + 1) % 4
    return password(*pos)


def test_part1(sample):
    assert main1(*sample) == 6032


def main2(M: np.ndarray, path: list):
    """
    Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?
    """
    x, y = np.where(M)
    pos = [x[0], y[0], 0]  # row, col, >
    return password(*pos)


def test_part2(sample):
    assert main2(*sample) == 5031


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(*data))
    # print(main2(*data))
