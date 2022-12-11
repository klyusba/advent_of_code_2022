from pytest import fixture
from dataclasses import dataclass


@dataclass
class Monkey:
    items: list
    operation: callable
    div_test: int
    if_true: int
    if_false: int
    items_inspected: int = 0


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    with open(filename) as f:
        monkeys_def = f.read().split('\n\n')

    monkeys = []
    for m in monkeys_def:
        lines = m.splitlines()
        # starting items
        _, items = lines[1].split(': ')
        items = list(map(int, items.split(', ')))
        # operation
        _, operation = lines[2].split('= ')
        operation = eval('lambda old: ' + operation)
        # div test
        _, div_test = lines[3].rsplit(' ', 1)
        div_test = int(div_test)
        # if true
        _, if_true = lines[4].rsplit(' ', 1)
        if_true = int(if_true)
        # if false
        _, if_false = lines[5].rsplit(' ', 1)
        if_false = int(if_false)

        monkeys.append(Monkey(items, operation, div_test, if_true, if_false))
    return monkeys


def main1(monkeys: list, rounds=20, boring_coef=3):
    """
    What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
    """
    for _ in range(rounds):
        for m in monkeys:  # type: Monkey
            while m.items:
                item = m.items.pop(0)
                m.items_inspected += 1
                v = m.operation(item)
                v = v // boring_coef
                throw_to = m.if_true if v % m.div_test == 0 else m.if_false
                monkeys[throw_to].items.append(v)

    monkeys.sort(key=lambda m: m.items_inspected, reverse=True)
    return monkeys[0].items_inspected * monkeys[1].items_inspected


def test_part1(sample):
    assert main1(sample) == 10605


def main2(monkeys: list, rounds=10000):
    """
    What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
    """
    base = 1
    for m in monkeys:
        base *= m.div_test

    for _ in range(rounds):
        for m in monkeys:  # type: Monkey
            while m.items:
                item = m.items.pop(0)
                m.items_inspected += 1
                v = m.operation(item) % base
                throw_to = m.if_true if v % m.div_test == 0 else m.if_false
                monkeys[throw_to].items.append(v)

    monkeys.sort(key=lambda m: m.items_inspected, reverse=True)
    return monkeys[0].items_inspected * monkeys[1].items_inspected


def test_part2(sample):
    assert main2(sample) == 2713310158


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data, rounds=20, boring_coef=3))
    print(main2(data, rounds=10000))
