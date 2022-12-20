from pytest import fixture


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    with open(filename) as f:
        lines = f.read().splitlines()
        return list(map(int, lines))


def move(a: list, item: (int, int)):
    if item == 0:
        return
    n = len(a) - 1
    ind = a.index(item)
    new_ind = (ind + item[1]) % n
    a.pop(ind)
    if new_ind != 0:  # illogical behaviour at start
        a.insert(new_ind, item)
    else:
        a.append(item)


def mix(numbers: list, times=1) -> list:
    # assert len(set(numbers)) == len(numbers)  there are duplicates
    a = list(enumerate(numbers))  # add idx for uniqueness
    for _ in range(times):
        for item in enumerate(numbers):
            move(a, item)
    return [n for idx, n in a]


def main1(numbers: list):
    """
    What is the sum of the three numbers that form the grove coordinates?
    (1000th, 2000th, and 3000th numbers after the value 0)
    """
    n = len(numbers)
    numbers = mix(numbers)
    idx = numbers.index(0)
    return numbers[(idx + 1000) % n] + numbers[(idx + 2000) % n] + numbers[(idx + 3000) % n]


def test_part1(sample):
    assert main1(sample) == 3


def main2(numbers: list):
    """
    Same, but every number multiplied by 811589153 and mixing is repeated 10 times
    """
    numbers = [n * 811589153 for n in numbers]
    n = len(numbers)
    numbers = mix(numbers, times=10)
    idx = numbers.index(0)
    return numbers[(idx + 1000) % n] + numbers[(idx + 2000) % n] + numbers[(idx + 3000) % n]


def test_part2(sample):
    assert main2(sample) == 1623178306


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
