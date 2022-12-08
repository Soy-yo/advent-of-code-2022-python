import os
from collections import Counter

from src.utils.io import read_all

MODULE = os.path.split(os.path.split(__file__)[0])[1]


class NoZeroCounter(Counter):

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self[key] == 0:
            del self[key]


def find_marker(buffer: str, marker_size: int) -> int:
    counter = NoZeroCounter(buffer[:marker_size])
    if len(counter) == marker_size:
        return marker_size

    for i in range(marker_size, len(buffer)):
        subs = i - marker_size
        counter[buffer[subs]] -= 1
        counter[buffer[i]] += 1

        if len(counter) == marker_size:
            return i + 1

    raise ValueError


def read(filename: str) -> str:
    path = os.path.join('src', MODULE, 'input', filename)
    return read_all(path)


def solve_part_one(buffer: str) -> int:
    return find_marker(buffer, 4)


def solve_part_two(buffer: str) -> int:
    return find_marker(buffer, 14)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
