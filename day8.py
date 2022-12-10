import numpy as np
from itertools import product
from pytest import fixture


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> np.array:
    with open(filename) as f:
        return np.asarray([
            list(map(int, line))
            for line in f.read().splitlines()
        ], dtype=int)


def calc_visibility(heights: np.array) -> np.array:
    rows, cols = heights.shape

    cumm_max = np.zeros_like(heights)
    # mb replace with np.maximum.accumulate
    cumm_max[0, :] = -1
    for i in range(1, rows):
        cumm_max[i, :] = np.maximum(heights[i - 1, :], cumm_max[i - 1, :])
    top_visibility = heights > cumm_max

    cumm_max[-1, :] = -1
    for i in range(rows-2, -1, -1):
        cumm_max[i, :] = np.maximum(heights[i + 1, :], cumm_max[i + 1, :])
    bottom_visibility = heights > cumm_max

    cumm_max[:, 0] = -1
    for j in range(1, cols):
        cumm_max[:, j] = np.maximum(heights[:, j - 1], cumm_max[:, j - 1])
    left_visibility = heights > cumm_max

    cumm_max[:, -1] = -1
    for j in range(cols - 2, -1, -1):
        cumm_max[:, j] = np.maximum(heights[:, j + 1], cumm_max[:, j + 1])
    right_visibility = heights > cumm_max
    return top_visibility | bottom_visibility | left_visibility | right_visibility


def main1(heights: np.array):
    """
    How many trees are visible from outside the grid?
    """
    v = calc_visibility(heights)
    return np.sum(v)


def test_part1(sample):
    assert main1(sample) == 21


def calc_scenic_score(heights: np.array) -> np.array:
    rows, cols = heights.shape

    def _score(arr, t):
        res = 0
        for x in arr:
            res += 1
            if x >= t:
                break
        return res

    score_left = np.zeros_like(heights)
    score_right = np.zeros_like(heights)
    score_top = np.zeros_like(heights)
    score_bottom = np.zeros_like(heights)
    for row, col in product(range(1, rows-1), range(1, cols-1)):
        h = heights[row, col]
        score_left[row, col] = _score(heights[row, col-1::-1], h)
        score_right[row, col] = _score(heights[row, col+1:], h)
        score_top[row, col] = _score(heights[row-1::-1, col], h)
        score_bottom[row, col] = _score(heights[row+1:, col], h)

    return score_left * score_right * score_top * score_bottom


def main2(heights: np.array):
    """
    What is the highest scenic score possible for any tree?
    """
    v = calc_scenic_score(heights)
    return np.max(v)


def test_part2(sample):
    assert main2(sample) == 8


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
