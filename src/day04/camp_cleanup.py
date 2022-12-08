import os

from src.utils.io import read_input

MODULE = os.path.split(os.path.split(__file__)[0])[1]


class Interval:

    def __init__(self, start: int, end: int):
        assert start <= end

        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    def is_subset(self, other: "Interval") -> bool:
        return other.start <= self.start and self.end <= other.end

    def intersects(self, other: "Interval") -> bool:
        return self.start <= other.end <= self.end or other.start <= self.end <= other.end


def count_complete_overlapping(ranges: list[tuple[Interval, Interval]]) -> int:
    return sum(1 for one, other in ranges if one.is_subset(other) or other.is_subset(one))


def count_overlaps(ranges: list[tuple[Interval, Interval]]) -> int:
    return sum(1 for one, other in ranges if one.intersects(other))


def read(filename: str) -> list[tuple[Interval, Interval]]:
    def transform(line: str) -> tuple[Interval, Interval]:
        elf1, elf2 = line.split(',')
        start1, end1 = elf1.split('-')
        start2, end2 = elf2.split('-')
        return Interval(int(start1), int(end1)), Interval(int(start2), int(end2))

    path = os.path.join('src', MODULE, 'input', filename)
    return read_input(path, transform=transform)


def solve_part_one(ranges: list[tuple[Interval, Interval]]) -> int:
    return count_complete_overlapping(ranges)


def solve_part_two(ranges: list[tuple[Interval, Interval]]) -> int:
    return count_overlaps(ranges)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
