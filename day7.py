

def read(filename: str) -> list:
    with open(filename) as f:
        return f.read().splitlines()


ROOT = '/'
SEP = '/'


def parse_terminal(terminal: list) -> dict:
    fs = {ROOT: {}}
    cwd = fs
    for line in terminal:
        if line.startswith('$ cd'):
            _, dirname = line.rsplit(' ', 1)
            cwd = cwd[dirname]
        elif line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            _, dirname = line.split(' ')
            cwd[dirname] = {'..': cwd}
        else:
            size, filename = line.split(' ')
            cwd[filename] = int(size)
    return fs


def disk_usage(fs: dict):
    stack = [(ROOT, fs[ROOT]), ]
    res = {}
    visited = set()
    while stack:
        path, cdw = stack[-1]
        # there are folders with same name, we use absolute path to distinct them
        subdirs = [(path + SEP + d, v) for d, v in cdw.items() if d != '..' and isinstance(v, dict)]

        if path in visited or not subdirs:  # if we counted all folder content or reached leef node
            dirsize = (
                sum(size for fn, size in cdw.items() if isinstance(size, int))  # count files
                + sum(res[p] for p, v in subdirs)  # count subdirs
            )
            res[path] = dirsize
            stack.pop()
        else:
            visited.add(path)
            stack.extend(subdirs)
    return res


def print_fs(fs):
    stack = [(0, ROOT, fs[ROOT]), ]
    res = []
    while stack:
        lvl, dirname, cwd = stack.pop()
        res.append('  ' * lvl + '+ ' + dirname)
        lvl += 1
        # files first
        res.extend('  ' * lvl + '- ' + fn for fn, v in cwd.items() if isinstance(v, int))
        stack.extend((lvl, dn, v) for dn, v in cwd.items() if dn != '..' and isinstance(v, dict))
    print('\n'.join(res))


def main1(terminal: list):
    """
    Find all of the directories with a total size of at most 100000.
    """
    fs = parse_terminal(terminal)
    # print_fs(fs)
    dir_sizes = disk_usage(fs)
    return sum(
        size for size in dir_sizes.values()
        if size <= 100_000
    )


def main2(terminal: list, total_space=70_000_000, space_needed=30_000_000):
    """
    Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update.
    """
    fs = parse_terminal(terminal)
    dir_sizes = disk_usage(fs)
    total_size = dir_sizes[ROOT]
    space_to_free = space_needed - (total_space - total_size)
    return min(
        size for size in dir_sizes.values()
        if size >= space_to_free
    )


if __name__ == "__main__":
    data = read('input.txt')
    print(main1(data))
    print(main2(data))
