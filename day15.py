from pytest import fixture
import re
from itertools import product


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    res = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            match = re.findall(r'=(-?\d+)', line)
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, match)
            res.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))
    return res


def expand(ranges: list):
    res = []
    ranges.sort()
    start, end = ranges[0]
    for s, e in ranges[1:]:
        if s > end:
            res.append((start, end))
            start, end = s, e
        elif e > end:
            end = e
    res.append((start, end))
    return res


def main1(positions: list, y_of_interest=2000000):
    """
    In the row where y=2000000, how many positions cannot contain a beacon?
    """
    checked_ranges = []
    for (sx, sy), (bx, by) in positions:
        l = abs(sx-bx) + abs(sy-by) - abs(sy-y_of_interest)
        if l >= 0:
            checked_ranges.append((sx-l, sx+l))

    checked_ranges = expand(checked_ranges)
    sum_ranges = sum(
        end-start+1
        for start, end in checked_ranges
    )
    beacons_in_range = set()
    for _, (bx, by) in positions:
        if by != y_of_interest:
            continue
        for start, end in checked_ranges:
            if start <= bx <= end:
                beacons_in_range.add(bx)
                break
    return sum_ranges - len(beacons_in_range)


def test_part1(sample):
    assert main1(sample, 10) == 26


def rotate(positions):
    """
    return squares in new space x' = x + y; y' = x - y
    """
    res = []
    for (sx, sy), (bx, by) in positions:
        l = abs(sx-bx) + abs(sy-by)
        x_range = sx+sy-l, sx+sy+l
        y_range = sx-sy-l, sx-sy+l
        res.append((x_range, y_range))
    return res


def inverse_rotate(positions):
    res = []
    for x, y in positions:
        center = (x.start + x.end) / 2, (y.start + y.end) / 2
        center = (center[0] + center[1]) / 2, (center[0] - center[1]) / 2
        res.append(tuple(map(int, center)))
    return res


class Range1D:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __and__(self, other):
        return self.end >= other.start and self.start <= other.end

    def __contains__(self, other):
        return self.start <= other.start and self.end >= other.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __truediv__(self, other):
        res = []
        if self.start < other.start <= self.end:
            res.append(Range1D(self.start, other.start-1))

        if self & other:
            res.append(Range1D(
                max(self.start, other.start), min(self.end, other.end)
            ))

        if self.start <= other.end < self.end:
            res.append(Range1D(other.end + 1, self.end))
        return res

    def __str__(self):
        return f"[{self.start}, {self.end}]"

    def __repr__(self):
        return f"[{self.start}, {self.end}]"


class Range2D:
    def __init__(self, ranges):
        self.ranges = ranges

    def exclude(self, x_range, y_range):
        res = []
        a, b = Range1D(*x_range), Range1D(*y_range)
        for x, y in self.ranges:
            if not ((x & a) and (y & b)):
                res.append((x, y))
                continue
            for x, y in product(x / a, y / b):
                if not (x in a and y in b):  # intersection
                    res.append((x, y))
        return Range2D(res)


def main2(positions: list, range_of_search=4000000):
    """
    Find the only possible position for the distress beacon. What is its tuning frequency?
    """
    squares = rotate(positions)
    x_range, y_range = (0, 2 * range_of_search), (-range_of_search, range_of_search)
    free_space = Range2D([(Range1D(*x_range), Range1D(*y_range)), ])
    for s in squares:
        free_space = free_space.exclude(*s)

    points = inverse_rotate(free_space.ranges)
    res = 0, 0
    for x, y in points:
        if 0 <= x <= range_of_search and 0 <= y <= range_of_search:
            res = x, y
    return res[0] * 4000000 + res[1]


def test_part2(sample):
    assert main2(sample, 20) == 56000011


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
