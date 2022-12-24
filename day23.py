from pytest import fixture
import numpy as np
from itertools import count


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> np.ndarray:
    res = []
    with open(filename) as f:
        for line in f.read().splitlines():
            res.append([
                c == '#' for c in line
            ])
    return np.asarray(res, dtype=bool)


def expand(elves: np.ndarray, add=1):
    if np.any(elves[0, :]) or np.any(elves[-1, :]) or np.any(elves[:, 0]) or np.any(elves[:, -1]):
        n, m = elves.shape
        new = np.zeros((n+2*add, m+2*add), dtype=elves.dtype)
        new[add:-add, add:-add] = elves
        return new
    else:
        return elves


def trunc(elves: np.ndarray):
    x, y = np.where(elves)
    x_min, x_max = x.min(), x.max()+1
    y_min, y_max = y.min(), y.max()+1
    return elves[x_min:x_max, y_min:y_max]


def find_duplicates(a):
    u = set()
    add = u.add
    return {item for item in a if item in u or add(item)}


def move(elves: np.ndarray, directions):
    steps = []
    for x, y in zip(*np.where(elves)):  # for each elf choose step
        # If no other Elves
        if elves[x-1:x+2, y-1:y+2].sum() == 1:
            steps.append((x, y))
            continue
        # Otherwise, the Elf looks in each of four directions
        for dx, dy in directions:
            if elves[x+dx, y+dy].sum() == 0:
                steps.append((x+dx[1], y+dy[1]))
                break
        else:
            steps.append((x, y))

    dup = find_duplicates(steps)
    moved = 0
    # Simultaneously, each Elf moves to their proposed destination tile
    for x, y, new_pos in zip(*np.where(elves), steps):
        pos = x, y
        # if they were the only Elf to propose moving to that position
        if new_pos not in dup and pos != new_pos:
            elves[pos] = False
            elves[new_pos] = True
            moved += 1
    return moved


def main1(elves: np.ndarray, rounds=10):
    """
    Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds.
    How many empty ground tiles does that rectangle contain?
    """
    directions = [
        (np.array([-1, -1, -1]), np.array([-1, 0, 1])),  # north
        (np.array([1, 1, 1]), np.array([-1, 0, 1])),     # south
        (np.array([-1, 0, 1]), np.array([-1, -1, -1])),  # west
        (np.array([-1, 0, 1]), np.array([1, 1, 1])),     # east
    ]
    elves = expand(elves, add=rounds)  # add free space to move
    for _ in range(rounds):
        move(elves, directions)
        directions.append(directions.pop(0))  # the first direction is moved to the end of the list of directions
    elves = trunc(elves)
    return np.sum(~elves)


def test_part1(sample):
    assert main1(sample) == 110


def main2(elves: np.ndarray):
    """
    Figure out where the Elves need to go. What is the number of the first round where no Elf moves?
    """
    directions = [
        (np.array([-1, -1, -1]), np.array([-1, 0, 1])),  # north
        (np.array([1, 1, 1]), np.array([-1, 0, 1])),     # south
        (np.array([-1, 0, 1]), np.array([-1, -1, -1])),  # west
        (np.array([-1, 0, 1]), np.array([1, 1, 1])),     # east
    ]
    for round in count(1):
        elves = expand(elves, add=10)  # add free space to move
        moved = move(elves, directions)
        directions.append(directions.pop(0))  # the first direction is moved to the end of the list of directions
        if not moved:
            return round
    return 0


def test_part2(sample):
    assert main2(sample) == 20


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
