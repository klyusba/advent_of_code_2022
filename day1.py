from pytest import fixture


@fixture
def sample():
    return read('sample.txt')


def read(filename: str):
    with open(filename, 'r') as f:
        item_list = f.read()

    return [
        [int(item) for item in elf_items.split()]
        for elf_items in item_list.split('\n\n')
    ]


def main_part1(item_list: list) -> int:
    """
    Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
    """
    return max(
        sum(elf_items)
        for elf_items in item_list
    )


def test_part1(sample):
    assert main_part1(sample) == 24000


def main_part2(item_list: list) -> int:
    """
    Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
    """
    calories_elf = [
        sum(elf_items)
        for elf_items in item_list
    ]
    top_three = sorted(calories_elf, reverse=True)[:3]
    return sum(top_three)


def test_part2(sample):
    assert main_part2(sample) == 45000


if __name__ == "__main__":
    input_data = read('input.txt')
    print(main_part1(input_data))
    print(main_part2(input_data))
