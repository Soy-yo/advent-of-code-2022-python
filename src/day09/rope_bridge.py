from __future__ import annotations

import os
import math
from typing import Literal
from itertools import pairwise

from src.utils.io import read_input

MODULE = os.path.split(os.path.split(__file__)[0])[1]


class Vector:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @classmethod
    def horizontal(cls, x: int) -> Vector:
        return cls(x, 0)

    @classmethod
    def vertical(cls, y: int) -> Vector:
        return cls(0, y)

    @classmethod
    def from_direction(cls, direction: Literal["L", "U", 'R', "D"], length: int) -> Vector:
        match direction:
            case 'R':
                return Vector.horizontal(length)
            case 'L':
                return Vector.horizontal(-length)
            case 'U':
                return Vector.vertical(length)
            case 'D':
                return Vector.vertical(-length)
        raise ValueError()

    def is_axis(self) -> bool:
        return self.x == 0 or self.y == 0

    def distance_sq(self, other: Vector) -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def norm(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle(self, other: Vector) -> float:
        return math.acos((self * other) / (self.norm() * other.norm()))

    def __getitem__(self, item: int) -> int:
        return (self._x, self._y)[item]

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int | Vector) -> Vector | int:
        if isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y

    def __floordiv__(self, n: int) -> Vector:
        return Vector(self.x // n, self.y // n)

    def __eq__(self, other: Vector) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


ZERO = Vector(0, 0)
# Actually it should be <= pi / 4, but check < pi / 2 just in case
PI_HALF = math.pi / 2


class Rope:

    def __init__(self, knots: int = 2):
        self._knots = [Vector(0, 0) for _ in range(knots)]

    @property
    def head(self) -> Vector:
        return self._knots[0]

    @property
    def tail(self) -> Vector:
        return self._knots[-1]

    def move(self, direction: Literal["L", "U", 'R', "D"]):
        v = Vector.from_direction(direction, 1)
        ws = [knot - next_knot for knot, next_knot in pairwise(self._knots)]

        self._knots[0] += v

        if len(self._knots) == 1:
            return

        for i, w in enumerate(ws):
            if v == ZERO or w == ZERO:
                break
            elif w.is_axis():
                if abs(v.angle(w)) >= PI_HALF:
                    v = ZERO
            else:
                if v * w == 0:
                    v = (v + w) // 2
                elif abs(v.angle(w)) < PI_HALF:
                    v = w
                else:
                    v = ZERO

            self._knots[i + 1] += v


def get_trajectory(
        rope: Rope,
        moves: list[tuple[Literal["L", "U", 'R', "D"], int]]
) -> list[Vector]:
    trajectory = [rope.head]

    for direction, length in moves:
        for _ in range(length):
            rope.move(direction)
            trajectory.append(rope.tail)

    return trajectory


def read(filename: str) -> list[tuple[Literal["L", "U", 'R', "D"], int]]:
    def transform(line: str) -> tuple[Literal["L", "U", 'R', "D"], int]:
        d, n = line.split()
        return d, int(n)

    path = os.path.join('src', MODULE, 'input', filename)
    return read_input(path, transform=transform)


def solve_part_one(moves: list[tuple[Literal["L", "U", 'R', "D"], int]]) -> int:
    return len(set(get_trajectory(Rope(), moves)))


def solve_part_two(moves: list[tuple[Literal["L", "U", 'R', "D"], int]]) -> int:
    return len(set(get_trajectory(Rope(10), moves)))


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
