import os
from functools import reduce

from src.utils.io import read_lines

MODULE = os.path.split(os.path.split(__file__)[0])[1]


def get_priority(c: str) -> int:
    if c.islower():
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27


def get_compartments(rucksack: str) -> tuple[set[str], set[str]]:
    half = len(rucksack) // 2
    return set(rucksack[:half]), set(rucksack[half:])


def sum_wrong_priorities(rucksacks: list[str]) -> int:
    compartments = [get_compartments(rucksack) for rucksack in rucksacks]
    wrong_items = [list(left & right)[0] for left, right in compartments]
    priorities = [get_priority(item) for item in wrong_items]
    return sum(priorities)


def sum_group_badges(rucksacks: list[str], n: int) -> int:
    result = 0
    for i in range(0, len(rucksacks), n):
        badge = list(reduce(set.intersection, (set(rucksacks[i + j]) for j in range(n))))[0]
        result += get_priority(badge)

    return result


def read(filename: str) -> list[str]:
    path = os.path.join('src', MODULE, 'input', filename)
    return read_lines(path)


def solve_part_one(rucksacks: list[str]) -> int:
    return sum_wrong_priorities(rucksacks)


def solve_part_two(rucksacks: list[str]) -> int:
    return sum_group_badges(rucksacks, n=3)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
