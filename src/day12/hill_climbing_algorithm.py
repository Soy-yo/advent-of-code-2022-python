import os
from typing import Iterable, Callable, Literal

import numpy as np

from src.utils.io import read_lines

MODULE = os.path.split(os.path.split(__file__)[0])[1]

START = 'S'
END = 'E'
LOWEST = 'a'
HIGHEST = 'z'


class Hill:

    def __init__(
            self,
            heights: list[list[int]],
            start: tuple[int, int],
            end: tuple[int, int]
    ):
        self._heights = np.array(heights, dtype=np.int32)
        self._start = start
        self._end = end

    @property
    def start(self) -> tuple[int, int]:
        return self._start

    @property
    def end(self) -> tuple[int, int]:
        return self._end

    def adjacent_positions(self, position: tuple[int, int]) -> Iterable[tuple[int, int]]:
        rows, cols = self._heights.shape
        i, j = position

        if j > 0:
            yield i, j - 1

        if i > 0:
            yield i - 1, j

        if j < cols - 1:
            yield i, j + 1

        if i < rows - 1:
            yield i + 1, j

    def __getitem__(self, item: tuple[int, int]) -> int:
        return self._heights[item]


def climb(
        hill: Hill,
        start: tuple[int, int] = None,
        end: tuple[int, int] | Callable[[tuple[int, int]], bool] = None,
        direction: Literal["forward", "backwards"] = 'forward'
) -> list[tuple[int, int]]:
    if start is None:
        start = hill.start if direction == 'forward' else hill.end
    if end is None:
        end = hill.end if direction == 'forward' else hill.start

    def _end(x: tuple[int, int]) -> bool:
        if callable(end):
            return end(x)
        return x == end

    def is_valid(a: tuple[int, int], b: tuple[int, int]) -> bool:
        if direction == 'forward':
            return hill[a] + 1 >= hill[b]
        return hill[b] + 1 >= hill[a]

    queue = [start]
    paths = {start: None}

    def get_path(x: tuple[int, int]) -> list[tuple[int, int]]:
        path = []
        while x is not None:
            path.append(x)
            x = paths[x]
        return list(reversed(path))

    while queue:
        p = queue.pop(0)

        if _end(p):
            return get_path(p)

        for q in hill.adjacent_positions(p):
            if q in paths:
                continue

            if is_valid(p, q):
                paths[q] = p
                queue.append(q)

    raise ValueError()


def read(filename: str) -> Hill:
    start = None
    end = None

    path = os.path.join('src', MODULE, 'input', filename)
    lines = read_lines(path)
    heights = []

    for i, line in enumerate(lines):
        if START in line:
            start = i, line.index(START)
            line = line.replace(START, LOWEST)
        if END in line:
            end = i, line.index(END)
            line = line.replace(END, HIGHEST)

        heights.append([ord(c) - ord('a') for c in line])

    assert start is not None
    assert end is not None

    return Hill(heights, start, end)


def solve_part_one(hill: Hill) -> int:
    return len(climb(hill)) - 1


def solve_part_two(hill: Hill) -> int:
    return len(climb(hill, end=lambda p: hill[p] == 0, direction='backwards')) - 1


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
