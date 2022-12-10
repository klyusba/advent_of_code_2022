from pytest import fixture


@fixture
def sample1():
    t = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
    return [
        line.split()
        for line in t.splitlines()
    ]


@fixture
def sample2():
    t = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
    return [
        line.split()
        for line in t.splitlines()
    ]


def read(filename: str) -> list:
    with open(filename) as f:
        return [
            line.split()
            for line in f.read().splitlines()
        ]


def _step_head(h, d):
    hx, hy = h
    if d == 'U':
        hy += 1
    elif d == 'R':
        hx += 1
    elif d == 'D':
        hy -= 1
    elif d == 'L':
        hx -= 1
    return hx, hy


def _step_tail(h, t):
    hx, hy, tx, ty = *h, *t
    if abs(hx - tx) <= 1 and abs(hy - ty) <= 1:  # adjacent
        return tx, ty
    elif abs(hx - tx) <= 1:
        return hx, (hy + ty) // 2
    elif abs(hy - ty) <= 1:
        return (tx + hx) // 2, hy
    else:
        return (tx + hx) // 2, (hy + ty) // 2


def main1(plan: list):
    head, tail = (0, 0), (0, 0)
    visited = {tail, }
    for direction, steps in plan:
        for _ in range(int(steps)):
            head = _step_head(head, direction)
            tail = _step_tail(head, tail)
            visited.add(tail)
    return len(visited)


def test_part1(sample1):
    assert main1(sample1) == 13


def show(head, tails):
    points = [(0, 0), head] + tails
    min_x, max_x = min(x for x, y in points)-2, max(x for x, y in points)+2
    min_y, max_y = min(y for x, y in points)-2, max(y for x, y in points)+2
    field = [
        ['.', ] * (max_x - min_x + 1)
        for _ in range(max_y - min_y + 1)
    ]
    field[-min_y][-min_x] = 's'  # start point
    for i, (x, y) in enumerate(tails, 1):
        field[y - min_y][x - min_x] = str(i)
    field[head[1] - min_y][head[0] - min_x] = 'H'  # head
    print('\n'.join(reversed([''.join(row) for row in field])))
    print('\n--------------------------------------------\n')


def main2(plan: list, tails_count=9):
    head = (0, 0)
    tails = [(0, 0) for _ in range(tails_count)]
    visited = {tails[-1], }
    for direction, steps in plan:
        for _ in range(int(steps)):
            head = _step_head(head, direction)
            tails[0] = _step_tail(head, tails[0])
            for i in range(1, tails_count):
                tails[i] = _step_tail(tails[i-1], tails[i])
            visited.add(tails[-1])
    return len(visited)


def test_part2(sample2):
    assert main2(sample2) == 36


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
