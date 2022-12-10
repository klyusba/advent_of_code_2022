

def read(filename: str) -> list:
    with open(filename) as f:
        return [
            [list(map(int, elf.split('-'))) for elf in line.split(',')]
            for line in f.read().splitlines()
        ]


def main1(assignments: list):
    """
    In how many assignment pairs does one range fully contain the other?
    """
    res = 0
    for (b1, e1), (b2, e2) in assignments:
        if b1 >= b2 and e1 <= e2 or b2 >= b1 and e2 <= e1:
            res += 1
    return res


def main2(assignments: list):
    """
    In how many assignment pairs do the ranges overlap?
    """
    res = 0
    for (b1, e1), (b2, e2) in assignments:
        if e1 >= b2 and e2 >= b1:
            res += 1
    return res


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
