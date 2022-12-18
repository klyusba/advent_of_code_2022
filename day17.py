from pytest import fixture
import numpy as np
from itertools import cycle


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


ROCKS = [
    np.array([
        [0, 0, 1, 1, 1, 1, 0],
    ], dtype=bool),
    np.array([
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
    ], dtype=bool),
    np.array([
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
    ], dtype=bool),
    np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
    ], dtype=bool),
    np.array([
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
    ], dtype=bool),
]


def move_right(maze, rock, rock_position):
    if np.any(rock[:, -1]):  # rock touch wall
        return rock
    new_pos = rock.copy()
    new_pos[:, 1:] = new_pos[:, :-1]
    new_pos[:, 0] = 0

    if has_intersection(maze, new_pos, rock_position):
        return rock
    else:
        return new_pos


def move_left(maze, rock, rock_position):
    if np.any(rock[:, 0]):  # rock touch wall
        return rock
    new_pos = rock.copy()
    new_pos[:, :-1] = new_pos[:, 1:]
    new_pos[:, -1] = 0
    if has_intersection(maze, new_pos, rock_position):
        return rock
    else:
        return new_pos


def has_intersection(maze, rock, rock_position):
    h = rock.shape[0]
    return np.any(maze[rock_position: rock_position+h, :] & rock)


def fix_rock(maze, rock, rock_position):
    h = rock.shape[0]
    maze[rock_position: rock_position + h, :] |= rock

    y = maze[rock_position: rock_position + h, :].sum(axis=1)
    t, = np.where(y)
    return rock_position + np.max(t) + 1


def model(air_jets: str, width: int, rounds: int, callback: callable = None):
    air_jets = cycle(air_jets)
    rocks = cycle(ROCKS)
    maze = np.zeros((4 * rounds, width), dtype=bool)
    height = 0
    for _ in range(rounds):
        rock = next(rocks).copy()
        rock_position = height + 3
        while True:
            direction = next(air_jets)
            if direction == '>':
                rock = move_right(maze, rock, rock_position)
            else:
                rock = move_left(maze, rock, rock_position)

            rock_position -= 1
            if rock_position < 0 or has_intersection(maze, rock, rock_position):
                height = max(fix_rock(maze, rock, rock_position+1), height)
                break
        if callback and not callback(maze[:height, :]):
            break
    return maze[:height, :]


def main1(air_jets: str, width=7, rounds=2022):
    maze = model(air_jets, width, rounds)
    return maze.shape[0]


def test_part1(sample):
    assert main1(sample) == 3068


def encode(maze):
    return maze.dot(2 ** np.arange(maze.shape[1]))


def find_pattern(maze):
    x = encode(maze)
    fft = np.fft.rfft(x, norm="ortho")
    y = fft.real ** 2 + fft.imag ** 2
    c = np.fft.irfft(y, norm="ortho")
    c[:3] = 0
    period = np.argmax(c[:len(c)//2])

    # find start of repetition by bisection
    lower, upper = 0, maze.shape[0]-1
    while lower < upper:
        idx = lower + (upper - lower) // 2
        if np.all(x[idx:idx+period] == x[idx+period:idx+2*period]):
            upper = idx
        else:
            lower = idx + 1
    return x[lower:lower+period]


class Monitor:
    def __init__(self, pattern):
        self.pattern = pattern
        self._counter = 0
        self._first = 0
        self._second = 0
        self.profile = []

    def __call__(self, maze):
        self._counter += 1
        h, n = maze.shape[0], self.pattern.shape[0]
        self.profile.append(h)
        if h < n:
            return True
        x = encode(maze)
        if np.all(x[-n:] == self.pattern):
            if not self._first:
                self._first = self._counter
                return True
            else:
                self._second = self._counter
                return False
        else:
            return True

    def get_period(self):
        p = self._second - self._first
        return p, self._first - p


def main2(air_jets: str, width=7, rounds=1_000_000_000_000):
    period = len(air_jets) * len(ROCKS)
    maze = model(air_jets, width, period)
    pattern = find_pattern(maze)

    m = Monitor(pattern)
    model(air_jets, width, period, m)
    period, start = m.get_period()
    d, r = divmod(rounds - start, period)
    return m.profile[start + r - 1] + d * pattern.shape[0]


def test_part2(sample):
    assert main2(sample) == 1514285714288


def test_part2_2(sample):
    assert main2(sample, rounds=2022) == 3068
    assert main2(sample, rounds=3000) == main1(sample, rounds=3000)
    assert main2(sample, rounds=5000) == main1(sample, rounds=5000)


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
