from pytest import fixture
import re
import numpy as np
from itertools import product, combinations
from scipy.sparse.csgraph import floyd_warshall


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> (dict, dict):
    with open(filename) as f:
        maze, flow_rates = {}, {}
        for line in f.read().splitlines():
            m = re.search(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)', line)
            valve, flow_rate, vaves = m.groups()
            maze[valve] = vaves.split(', ')
            flow_rates[valve] = int(flow_rate)
    return maze, flow_rates


def to_matrix(maze: dict, flow_rates: dict, start: str) -> (np.ndarray, np.ndarray, int):
    valves = len(flow_rates)
    D = np.zeros((valves, valves), dtype=int)
    r = np.zeros((valves,), dtype=int)
    idx = {n: i for i, n in enumerate(flow_rates)}
    for n, i in idx.items():
        for valve in maze[n]:
            D[i, idx[valve]] = 1  # 1 minute to go to valve
        r[i] = flow_rates[n]

    D = floyd_warshall(D, True).astype(int)
    D += 1  # 1 minute to open valve
    return D, r, idx[start]


def main1(maze: dict, flow_rates: dict, start='AA', time_total=30):
    maze, flow_rates, start = to_matrix(maze, flow_rates, start)

    def get_neighbours(valve, path, time_left):
        res = []
        nodes = set(range(maze.shape[0])) - set(path)
        for i in nodes:
            d = maze[valve, i]
            if d <= time_left and flow_rates[i] > 0:
                res.append((i, d))
        return res

    max_obj = 0
    stack, path, obj = [(0, start, time_total), ], [], []
    while stack:
        lvl, valve, time_left = stack.pop()
        while len(path) > lvl:
            path.pop()
            obj.pop()

        path.append(valve)
        obj.append(flow_rates[valve] * time_left)
        neighbours = get_neighbours(valve, path, time_left)
        if neighbours:
            stack.extend((lvl+1, n, time_left-d) for n, d in neighbours)
        else:
            max_obj = max(max_obj, sum(obj))

    return max_obj


def test_part1(sample):
    assert main1(*sample) == 1651


def main2(maze: dict, flow_rates: dict, start='AA', time_total=26):
    maze, flow_rates, start = to_matrix(maze, flow_rates, start)

    def get_neighbours(valve, path, time_left):
        res = []
        nodes = set(range(maze.shape[0])) - set(path)
        for i in nodes:
            d = maze[valve, i]
            if d <= time_left and flow_rates[i] > 0:
                res.append((i, d))
        return res

    max_obj = 0
    path, obj = [], []
    neighbours = get_neighbours(start, path, time_total)
    stack = [  # optimisation self and elephant equal at start, replace product with combinations
        (0, n_self, n_elephant, time_total - d_self, time_total - d_elephant)
        for (n_self, d_self), (n_elephant, d_elephant) in combinations(neighbours, 2)
        if n_self != n_elephant
    ]

    while stack:
        lvl, valve_self, valve_elephant, time_left_self, time_left_elephant = stack.pop()
        while len(path) > 2 * lvl:
            path.pop()
            path.pop()
            obj.pop()

        path.append(valve_self)
        path.append(valve_elephant)
        obj.append(flow_rates[valve_self] * time_left_self + flow_rates[valve_elephant] * time_left_elephant)
        neighbours_self = get_neighbours(valve_self, path, time_left_self)
        neighbours_elephant = get_neighbours(valve_elephant, path, time_left_elephant)
        if neighbours_self or neighbours_elephant:
            neighbours_self = neighbours_self or [(start, time_total), ]
            neighbours_elephant = neighbours_elephant or [(start, time_total), ]
            stack.extend(
                (lvl+1, n_self, n_elephant, time_left_self-d_self, time_left_elephant-d_elephant)
                for (n_self, d_self), (n_elephant, d_elephant) in product(neighbours_self, neighbours_elephant)
                if n_self != n_elephant
            )
        else:
            max_obj = max(max_obj, sum(obj))

    return max_obj


def test_part2(sample):
    assert main2(*sample) == 1707


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(*data))
    print(main2(*data))
