from string import ascii_letters


def read(filename: str) -> list:
    with open(filename) as f:
        return [
            (set(line[:len(line)//2]), set(line[len(line)//2:]))
            for line in f.read().splitlines()
        ]


def main1(rucksacks: list):
    res = 0
    for c1, c2 in rucksacks:
        common, = c1 & c2
        priority = ascii_letters.index(common) + 1
        res += priority
    return res


def main2(rucksacks: list):
    res = 0
    for (c11, c12), (c21, c22), (c31, c32) in zip(rucksacks[::3], rucksacks[1::3], rucksacks[2::3]):
        common, = (c11 | c12) & (c21 | c22) & (c31 | c32)
        priority = ascii_letters.index(common) + 1
        res += priority
    return res


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
