from pytest import fixture


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    with open(filename) as f:
        return f.read().splitlines()


def to_decimal(n: str):
    r = 0
    v = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    for p, c in enumerate(reversed(n)):
        r += v[c] * pow(5, p)
    return r


def to_snafu(n: int):
    r = []
    v = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}
    while n:
        n, a = divmod(n, 5)
        if a >= 3:
            n, a = n+1, a-5
        r.append(v[a])
    return ''.join(reversed(r))


def test_to_snafu():
    assert to_snafu(1) == '1'
    assert to_snafu(2) == '2'
    assert to_snafu(3) == '1='
    assert to_snafu(4) == '1-'
    assert to_snafu(5) == '10'
    assert to_snafu(6) == '11'
    assert to_snafu(7) == '12'
    assert to_snafu(8) == '2='
    assert to_snafu(9) == '2-'
    assert to_snafu(10) == '20'
    assert to_snafu(15) == '1=0'
    assert to_snafu(20) == '1-0'
    assert to_snafu(2022) == '1=11-2'
    assert to_snafu(12345) == '1-0---0'
    assert to_snafu(314159265) == '1121-1110-1=0'


def main1(numbers: list):
    """
    What SNAFU number do you supply to Bob's console?
    """
    d = sum(map(to_decimal, numbers))
    return to_snafu(d)


def test_part1(sample):
    assert main1(sample) == '2=-1=0'


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
