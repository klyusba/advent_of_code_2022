from pytest import fixture
import numpy as np
import re
from scipy.spatial.transform import Rotation


@fixture
def sample():
    return read('sample.txt')


WALL = 2


def read(filename: str) -> (np.ndarray, list):
    with open(filename) as f:
        map, path = f.read().split('\n\n')
    # parse map
    map = map.splitlines()
    max_x = max(len(line) for line in map)
    M = np.zeros((len(map), max_x), dtype=int)
    v = {' ': 0, '.': 1, '#': WALL}
    for i, line in enumerate(map):
        for j, c in enumerate(line):
            M[i, j] = v[c]

    # parse path
    path = re.split(r'([RL])', path)
    for i in range(0, len(path), 2):
        path[i] = int(path[i])
    return M, path


def password(row, col, face):
    return 1000 * (row + 1) + 4 * (col + 1) + face


def get_slice(M, row=None, col=None):
    if row is not None:
        row = M[row, :]
        idx, = np.where(row)
        return row[idx], idx[0], idx[-1]
    if col is not None:
        col = M[:, col]
        idx, = np.where(col)
        return col[idx], idx[0], idx[-1]


def find_stop_point(field: np.ndarray, start: int, step: int) -> int:
    n = field.shape[0]
    pos = start
    for i in range(1, step+1):
        pos = (start + i) % n
        if field[pos] == WALL:
            return (pos - 1) % n
    return pos


def move_right(M: np.ndarray, x: int, y: int, step: int) -> int:
    row, start, end = get_slice(M, row=x)
    y = find_stop_point(row, y-start, step) + start
    return y


def move_left(M: np.ndarray, x: int, y: int, step: int) -> int:
    row, start, end = get_slice(M, row=x)
    y = end - find_stop_point(row[::-1], end - y, step)
    return y


def move_down(M: np.ndarray, x: int, y: int, step: int) -> int:
    col, start, end = get_slice(M, col=y)
    x = find_stop_point(col, x-start, step) + start
    return x


def move_up(M: np.ndarray, x: int, y: int, step: int) -> int:
    col, start, end = get_slice(M, col=y)
    x = end - find_stop_point(col[::-1], end - x, step)
    return x


def move(M: np.ndarray, pos: list, step: int) -> list:
    row, col, face = pos
    if face == 0:
        col = move_right(M, row, col, step)
    elif face == 1:
        row = move_down(M, row, col, step)
    elif face == 2:
        col = move_left(M, row, col, step)
    elif face == 3:
        row = move_up(M, row, col, step)
    else:
        raise ValueError()
    return [row, col, face]


def main1(M: np.ndarray, path: list):
    """
    What is the final password?
    """
    faces = '>v<^'
    x, y = np.where(M)
    pos = [x[0], y[0], 0]  # row, col, >
    for step in path:
        if isinstance(step, int):
            pos = move(M, pos, step)
        elif step == 'L':
            pos[-1] = (pos[-1] - 1) % 4
        elif step == 'R':
            pos[-1] = (pos[-1] + 1) % 4
    return password(*pos)


def test_part1(sample):
    assert main1(*sample) == 6032


# part2 main ideas:
# -fold cube
# -trac global position in 3D
# -find relative position and facing from the perspective of the map


class Face:
    def __init__(self, data, x, y):
        self.data = data
        self.x = x
        self.y = y
        self.empty = np.sum(data) == 0
        self.neighbours = {}  # <^>v: Face
        self.basis = np.eye(4)
        self.basis_inv = None

    def __getitem__(self, item):
        return self.data[item]

    def project(self, v):
        x = np.zeros(4)
        x[:-1] = v
        x[-1] = 1
        if self.basis_inv is None:
            self.basis_inv = np.linalg.inv(self.basis)
        res = self.basis_inv @ x
        res = np.round(res).astype(int)
        return res[0], res[1]

    def local_direction(self, v):
        """facing direction >v<^ """
        v = self.project(v)
        f = v[0] + 1 + (v[1] + 1) * 3
        return {5: 'v', 3: '^', 7: '>', 1: '<'}[f]


def _cut(M: np.ndarray):
    S = (M > 0).sum()  # total area
    a = int((S / 6) ** 0.5)

    n, m = M.shape
    n, m = n // a, m // a
    segments = []
    for i in range(n):
        row = [
            Face(M[i * a: (i + 1) * a, j * a: (j + 1) * a], x=i * a, y=j * a)
            for j in range(m)
        ]
        segments.append(row)

    faces = []
    for i, row in enumerate(segments):
        for j, face in enumerate(row):
            if not face.empty:
                face.neighbours = _find_neighbours(segments, i, j)
                faces.append(face)

    return faces, a


def _find_neighbours(segments, i, j):
    # direct neighbours
    res = {}
    # up
    try:
        face = segments[(i - 1) % 4][j]
        if not face.empty:
            res['^'] = face
    except IndexError:
        pass
    # down
    try:
        face = segments[(i + 1) % 4][j]
        if not face.empty:
            res['v'] = face
    except IndexError:
        pass
    # left
    try:
        face = segments[i][(j - 1) % 4]
        if not face.empty:
            res['<'] = face
    except IndexError:
        pass
    # right
    try:
        face = segments[i][(j + 1) % 4]
        if not face.empty:
            res['>'] = face
    except IndexError:
        pass
    return res

#  view from top:
#  z y
#  ⊙->---
# x↓    |
#  |    |
#  ------


rotations = {
    '>': Rotation.from_euler('x', -90, degrees=True),
    '<': Rotation.from_euler('x', 90, degrees=True),
    '^': Rotation.from_euler('y', -90, degrees=True),
    'v': Rotation.from_euler('y', 90, degrees=True),
}


def _cover(faces, transforms) -> dict:
    res = {}
    visited = set()
    basis = np.eye(4)
    basis[-1, :] = 1
    stack = [(faces[0], np.eye(4)), ]
    while stack:
        f, T = stack.pop()
        new_basis = T @ basis
        face_num = Cube.encode(new_basis[:, 2] - new_basis[:, 3])
        if face_num not in visited:
            visited.add(face_num)
            f.basis = new_basis.astype(int)
            res[face_num] = f

            for d, n in f.neighbours.items():
                stack.append(
                    (n, T @ transforms[d])
                )
    return res


class Actor:
    def __init__(self, segment, x, y, vx, vy):
        self.segment = segment
        self.position = np.array([x, y, 0], dtype=int)
        self.velocity = np.array([vx, vy, 0], dtype=int)


class Cube:
    def __init__(self, M: np.ndarray):
        faces, size = _cut(M)
        # init transforms from rotations
        transforms = {}
        for k, r in rotations.items():
            t = np.zeros((4, 4), dtype=int)
            t[:3, :3] = np.round(r.as_matrix()).astype(int)
            t[3, 3] = 1
            transforms[k] = t
        # shifts
        transforms['>'][1, 3] = (size-1)
        transforms['<'][2, 3] = -(size-1)
        transforms['^'][2, 3] = -(size-1)
        transforms['v'][0, 3] = (size-1)

        self.faces = _cover(faces, transforms)
        self.size = size

    @staticmethod
    def encode(b: np.ndarray) -> int:
        v = b + 1
        return int(v[0] + 3 * v[1] + 9 * v[2] + 1e-7)  # 0.1 for rounding

    def step(self, actor: Actor):
        face = self.faces[actor.segment]
        p, v = actor.position, actor.velocity
        p_new = p + v
        x_new, y_new = face.project(p_new)

        # recalc position after go around the corner
        if x_new >= self.size or x_new < 0 or y_new >= self.size or y_new < 0:
            s_new = self.encode(v)
            face_new = self.faces[s_new]
            x_new, y_new = face_new.project(p)
            if face_new[x_new, y_new] == WALL:
                return WALL

            actor.position = p
            actor.segment = s_new
            # turn around the corner
            z = face.basis[:3, 2] - face.basis[:3, 3]
            z_new = face_new.basis[:3, 2] - face_new.basis[:3, 3]
            y = np.cross(z, z_new)
            actor.velocity = np.cross(y, v)
        elif face[x_new, y_new] == WALL:
            return WALL
        else:
            actor.position = p_new

    def turn(self, actor: Actor, side: str):
        face = self.faces[actor.segment]
        v = actor.velocity
        z = face.basis[:3, 2] - face.basis[:3, 3]
        v_new = np.cross(v, z)
        if side == 'L':
            actor.velocity = -v_new
        else:
            actor.velocity = v_new

    def get_pos(self, actor: Actor):
        s, p, v = actor.segment, actor.position, actor.velocity
        face = self.faces[s]
        x, y = face.project(p)
        f = face.local_direction(v)
        return x + face.x, y + face.y, '>v<^'.index(f)


def main2(M: np.ndarray, path: list):
    """
    Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?
    """
    cube = Cube(M)
    me = Actor(22, 0, 0, 0, 1)
    for step in path:
        if isinstance(step, int):
            for _ in range(step):
                if cube.step(me) == WALL:
                    break
        else:
            cube.turn(me, step)
    return password(*cube.get_pos(me))


def test_part2(sample):
    assert main2(*sample) == 5031


if __name__ == "__main__":
    data = read('input22.txt')
    # print(main1(*data))
    print(main2(*data))
