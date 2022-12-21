from pytest import fixture
import sympy


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> dict:
    res = {}
    with open(filename) as f:
        for line in f.read().splitlines():
            name, number = line.split(': ')
            if number.isnumeric():
                res[name] = int(number)
            else:
                res[name] = number.split()
    return res


def calc(left, op, right):
    if op == '+':
        return left + right
    if op == '-':
        return left - right
    if op == '*':
        return left * right
    if op == '/':
        return left / right


def propagate(monkeys, root):
    stack = [root, ]
    while stack:
        name = stack[-1]
        if not isinstance(monkeys[name], list):
            stack.pop()
        else:
            left, op, right = monkeys[name]
            if not isinstance(monkeys[left], list) and not isinstance(monkeys[right], list):
                monkeys[name] = calc(monkeys[left], op, monkeys[right])
                stack.pop()
            else:
                stack.append(left)
                stack.append(right)
    return monkeys[root]


def main1(monkeys: dict):
    """
    What number will the monkey named root yell?
    """
    return propagate(monkeys, 'root')


def test_part1(sample):
    assert main1(sample) == 152


def main2(monkeys: dict):
    """
    Same, but every number multiplied by 811589153 and mixing is repeated 10 times
    """
    # patch
    left, _, right = monkeys['root']
    monkeys['root'] = [left, '-', right]
    monkeys['humn'] = sympy.var('x')

    problem = propagate(monkeys, 'root')
    res, = sympy.solve(problem)
    return res


def test_part2(sample):
    assert main2(sample) == 301


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
