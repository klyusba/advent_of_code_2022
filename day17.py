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
    r = np.sum(rock[:, -1], axis=0)
    if r:  # rock touch wall
        return rock
    new_pos = rock.copy()
    new_pos[:, 1:] = new_pos[:, :-1]
    new_pos[:, 0] = 0

    if has_intersection(maze, new_pos, rock_position):
        return rock
    else:
        return new_pos


def move_left(maze, rock, rock_position):
    r = np.sum(rock[:, 0], axis=0)
    if r:  # rock touch wall
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

    y = maze.sum(axis=1)
    t, = np.where(y)
    return np.max(t) + 1


def main1(air_jets: str, width=7, rounds=2022):
    air_jets = cycle(air_jets)
    rocks = cycle(ROCKS)
    maze = np.zeros((10000, width), dtype=bool)
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
                height = fix_rock(maze, rock, rock_position+1)
                break

    return height


def test_part1(sample):
    assert main1(sample) == 3068


def main2(air_jets: str, width=7, rounds=1000000000000):
    return 0


def test_part2(sample):
    assert main2(sample) == 1514285714288


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    # print(main2(data))
