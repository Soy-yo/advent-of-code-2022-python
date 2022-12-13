from __future__ import annotations

import os
import json
from functools import cmp_to_key

from src.utils.io import read_multi_input
from src.utils.list_helpers import flatten

MODULE = os.path.split(os.path.split(__file__)[0])[1]

LT = -1
EQ = 0
GT = 1

list_or_int = list["list_or_int"] | int


def compare(left: list[list_or_int], right: list[list_or_int]) -> int:
    for a, b in zip(left, right):
        if isinstance(a, int) and not isinstance(b, int):
            a = [a]
        elif not isinstance(a, int) and isinstance(b, int):
            b = [b]

        if isinstance(a, int):
            if a < b:
                return -1
            if b < a:
                return GT
        else:
            r = compare(a, b)
            if r == EQ:
                continue
            return r

    if len(left) < len(right):
        return LT

    if len(right) < len(left):
        return GT

    return EQ


def read(filename: str) -> list[list[list[list_or_int]]]:
    path = os.path.join('src', MODULE, 'input', filename)
    return read_multi_input(path, transform=json.loads)


def solve_part_one(lists: list[list[list[list_or_int]]]) -> int:
    result = 0
    for i, (left, right) in enumerate(lists):
        if compare(left, right) == LT:
            result += i + 1

    return result


def solve_part_two(lists: list[list[list[list_or_int]]]) -> int:
    lists = flatten(lists)
    divider1 = [[2]]
    divider2 = [[6]]
    lists = [*lists, divider1, divider2]
    lists = sorted(lists, key=cmp_to_key(compare))
    return (lists.index(divider1) + 1) * (lists.index(divider2) + 1)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
