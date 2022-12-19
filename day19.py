from pytest import fixture
import re
import pyomo.environ as pyo


@fixture
def sample():
    return read('sample.txt')


def read(filename: str) -> list:
    res = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            match = re.findall(r'\d+', line)
            blueprint_id, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian = map(int, match)
            res.append((blueprint_id, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian))
    return res


def pprint(model, production, costs):
    resource_name = {
        1: 'ore',
        2: 'clay',
        3: 'obsidian',
        4: 'geode',
    }

    def str_cost(robot):
        return ' and '.join(
            f'{c} {resource_name[j]}' for j, c in zip(model.resources, costs[robot-1])
            if c > 0
        )

    for m in model.minutes:
        if m == len(model.minutes):
            break

        print(f'== Minute {m} ==')
        for j in model.robots:
            x = int(model.x[m, j].value)
            if x > 0:
                print(f'Spend {str_cost(j)} to start building a {resource_name[j]}-collecting robot')
        for j in model.robots:
            r = int(model.r[m, j].value)
            a = int(model.a[m+1, j].value + sum(x.value * cost[j-1] for x, cost in zip(model.x[m+1, :], costs)))
            if r > 0:
                print(f'{r} {resource_name[j]}-collecting robots collect {r} {resource_name[j]}; you now have {a} {resource_name[j]}')
        for j in model.robots:
            x = int(model.x[m, j].value)
            r = int(model.r[m+1, j].value)
            if x > 0:
                print(f'The new {resource_name[j]}-collecting robot is ready; you now have {r} of them.')
        print('')


def compile_and_solve(target, production, costs, time_total, start_robots, start_resources, verbose=0):
    model = pyo.ConcreteModel()
    model.minutes = pyo.RangeSet(time_total+1)
    model.resources = pyo.RangeSet(len(start_resources))
    model.robots = pyo.RangeSet(len(start_robots))
    D = pyo.NonNegativeIntegers
    model.x = pyo.Var(model.minutes, model.resources, domain=D, name='x')  # buy on i-th minute j-th robot
    model.r = pyo.Var(model.minutes, model.resources, domain=D, name='r')  # j-th robot count at the beginning of i-th minute
    model.a = pyo.Var(model.minutes, model.resources, domain=D, name='a')  # j-th resource count at the beginning of i-th minute

    def obj(model):
        return sum(c * model.a[time_total+1, r] for r, c in zip(model.robots, target))
    model.obj = pyo.Objective(rule=obj, sense=pyo.maximize)

    def robot_construction(model, i, j):
        if i == 1:
            return model.r[i, j] == start_robots[j-1]
        else:
            return model.r[i, j] == model.r[i-1, j] + model.x[i-1, j]
    model.RobotConstraint = pyo.Constraint(model.minutes, model.robots, rule=robot_construction)

    def resources_usage(model, i, j):
        if i == 1:
            return model.a[i, j] == (
                    start_resources[j-1]
                    - sum(r * p[j - 1] for r, p in zip(model.x[i, :], costs))
                )
        else:
            return model.a[i, j] == (
                    model.a[i-1, j]
                    + sum(r * p[j-1] for r, p in zip(model.r[i-1, :], production))
                    - sum(r * p[j-1] for r, p in zip(model.x[i, :], costs))
                )
    model.ResourceConstraint = pyo.Constraint(model.minutes, model.resources, rule=resources_usage)

    def factory_capacity(model, i):
        return sum(model.x[i, :]) <= 1
    model.FactoryConstraint = pyo.Constraint(model.minutes, rule=factory_capacity)

    opt = pyo.SolverFactory('cplex_direct')
    opt.solve(model)
    if verbose:
        pprint(model, production, costs)
    return int(pyo.value(model.obj))


def main1(blueprints: list, time_total=24, verbose=0):
    """
    What do you get if you add up the quality level of all of the blueprints in your list?
    quality level = id * the largest number of geodes that can be opened
    """
    start_robots = [1, 0, 0, 0]
    start_resources = [0, 0, 0, 0]
    target = [0, 0, 0, 1]
    production = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    res = 0
    for blueprint_id, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian in blueprints:
        costs = [
            [ore_robot_ore, 0, 0, 0],
            [clay_robot_ore, 0, 0, 0],
            [obsidian_robot_ore, obsidian_robot_clay, 0, 0],
            [geode_robot_ore, 0, geode_robot_obsidian, 0],
        ]
        n_geodes = compile_and_solve(target, production, costs, time_total, start_robots, start_resources, verbose)
        res += blueprint_id * n_geodes
    return res


def test_part1(sample):
    assert main1(sample, verbose=True) == 33


def main2(blueprints: list, time_total=32):
    """
    What do you get if you multiply these numbers together?
    """
    start_robots = [1, 0, 0, 0]
    start_resources = [0, 0, 0, 0]
    target = [0, 0, 0, 1]
    production = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    res = 1
    for blueprint_id, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian in blueprints[:3]:
        costs = [
            [ore_robot_ore, 0, 0, 0],
            [clay_robot_ore, 0, 0, 0],
            [obsidian_robot_ore, obsidian_robot_clay, 0, 0],
            [geode_robot_ore, 0, geode_robot_obsidian, 0],
        ]
        n_geodes = compile_and_solve(target, production, costs, time_total, start_robots, start_resources)
        res *= n_geodes
    return res


def test_part2(sample):
    assert main2(sample) == 56 * 62


if __name__ == "__main__":
    data = read('input.txt')
    # print(main1(data))
    print(main2(data))
