from pytest import fixture


@fixture
def sample1():
    return 'mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19


@fixture
def sample2():
    return 'bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23


@fixture
def sample3():
    return 'nppdvjthqldpwncqszvftbrmjlhg', 6, 23


@fixture
def sample4():
    return 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29


@fixture
def sample5():
    return 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26


def read(filename: str):
    with open(filename, 'r') as f:
        return f.read()


def main_part1(signal: str) -> int:
    """
    How many characters need to be processed before the first start-of-packet marker is detected?
    The start of a packet is indicated by a sequence of four characters that are all different.
    """
    return next(
        i + 4
        for i in range(len(signal))
        if len(set(signal[i:i+4])) == 4
    )


def test_part1_1(sample1):
    sample, ans, _ = sample1
    assert main_part1(sample) == ans


def test_part1_2(sample2):
    sample, ans, _ = sample2
    assert main_part1(sample) == ans


def test_part1_3(sample3):
    sample, ans, _ = sample3
    assert main_part1(sample) == ans


def main_part2(signal: str) -> int:
    """
    A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather than 4.
    """
    return next(
        i + 14
        for i in range(len(signal))
        if len(set(signal[i:i + 14])) == 14
    )


def test_part2_1(sample1):
    sample, _, ans = sample1
    assert main_part2(sample) == ans


def test_part2_2(sample2):
    sample, _, ans = sample2
    assert main_part2(sample) == ans


def test_part2_3(sample3):
    sample, _, ans = sample3
    assert main_part2(sample) == ans


if __name__ == "__main__":
    input_data = read('input.txt')
    print(main_part1(input_data))
    print(main_part2(input_data))
