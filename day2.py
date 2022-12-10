
def read(filename: str) -> list:
    with open(filename) as f:
        return [
            line.split()
            for line in f.read().splitlines()
        ]


ROCK = 0
PAPER = 1
SCISSORS = 2

LOST = 10
DRAW = 11
WIN = 12

game_score = {
    LOST: 0,
    DRAW: 3,
    WIN: 6
}

shape_score = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}


def score(elf, me):
    if elf == me:
        return DRAW
    elif (elf - me) % 3 == 1:
        return LOST
    else:
        return WIN


def main1(plan: list):
    elf_code = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
    me_code = {'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}
    res = 0
    for elf, me in plan:
        elf, me = elf_code[elf], me_code[me]
        res += game_score[score(elf, me)] + shape_score[me]
    return res


def main2(plan: list):
    elf_code = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
    me_code = {'X': LOST, 'Y': DRAW, 'Z': WIN}
    res = 0
    for elf, me in plan:
        elf, g = elf_code[elf], me_code[me]
        me = next(shape for shape in shape_score if score(elf, shape) == g)
        res += game_score[g] + shape_score[me]
    return res


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
