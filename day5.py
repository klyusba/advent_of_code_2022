import re


def read(filename: str):
    with open(filename) as f:
        stacks, commands = f.read().split('\n\n')
        # stacks:
        stacks = stacks.splitlines()
        columns_num = len(stacks.pop()[1::4])  # numbers
        parsed = []
        for i in range(columns_num):
            stack = []
            for line in reversed(stacks):
                try:
                    crate = line[1 + i*4]
                    if crate != ' ':
                        stack.append(crate)
                except IndexError:
                    pass
            parsed.append(stack)
        stacks = parsed

        parsed = []
        for cmd in commands.splitlines():
            m = re.search(r'move (\d+) from (\d+) to (\d+)', cmd)
            m, f, t = map(int, m.groups())
            parsed.append((m, f-1, t-1))  # zero based

        return stacks, parsed


def main1(stacks: list, commands: list):
    """
    After the rearrangement procedure completes, what crate ends up on top of each stack?
    """
    for cnt, f, t in commands:
        for _ in range(cnt):
            stack_to, stack_from = stacks[t], stacks[f]
            stack_to.append(stack_from.pop())
    return ''.join([stack[-1] for stack in stacks])


def main2(stacks: list, commands: list):
    """
    After the rearrangement procedure completes, what crate ends up on top of each stack?
    """
    for cnt, f, t in commands:
        stack_to, stack_from = stacks[t], stacks[f]
        crates = stack_from[-cnt:]
        stack_to += crates
        stack_from[-cnt:] = []
    return ''.join([stack[-1] for stack in stacks])


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(*data))
    print(main2(*data))
