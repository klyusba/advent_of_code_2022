from pytest import fixture
from collections import Counter
import numpy as np
from scipy.ndimage import binary_fill_holes


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    res = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            res.append(
                list(map(int, line.split(',')))
            )
    return res


def faces(cube):
    # cube = coordinates of left bottom vertex
    # face = coordinates of left bottom vertex + normal axe
    x, y, z = cube
    return [
        (x, y, z, 'z'),
        (x, y, z+1, 'z'),
        (x, y, z, 'x'),
        (x + 1, y, z, 'x'),
        (x, y, z, 'y'),
        (x, y+1, z, 'y'),
    ]


def main1(positions: list):
    """
    What is the surface area of your scanned lava droplet?
    """
    unique_faces = Counter()
    for cube in positions:
        unique_faces.update(faces(cube))
    return sum(1 for f, c in unique_faces.items() if c == 1)


def test_part1(sample):
    assert main1(sample) == 64


def to_matrix(positions: list) -> np.ndarray:
    positions = np.asarray(positions, int).T  # axis-vice
    max_ = np.max(positions, axis=1) + 1
    M = np.zeros(max_, dtype=bool)
    ind = np.ravel_multi_index(positions, M.shape)
    np.put(M, ind, True)
    return M


def to_positions(M: np.ndarray) -> list:
    return list(zip(*np.where(M)))


def main2(positions: list):
    """
    What is the exterior surface area of your scanned lava droplet?
    """
    M = to_matrix(positions)
    M = binary_fill_holes(M)
    positions = to_positions(M)
    return main1(positions)


def test_part2(sample):
    assert main2(sample) == 58


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
