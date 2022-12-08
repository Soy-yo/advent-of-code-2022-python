import os

from src.utils.io import read_multi_input

MODULE = os.path.split(os.path.split(__file__)[0])[1]


def get_top_n_max_calories(calories: list[list[int]], n: int = 1) -> int:
    calories_per_elf = (sum(elf_calories) for elf_calories in calories)
    if n == 1:
        return max(calories_per_elf)
    return sum(sorted(calories_per_elf, reverse=True)[:n])


def read(filename: str) -> list[list[int]]:
    path = os.path.join('src', MODULE, 'input', filename)
    return read_multi_input(path, transform=int)


def solve_part_one(calories: list[list[int]]) -> int:
    return get_top_n_max_calories(calories)


def solve_part_two(calories: list[list[int]]) -> int:
    return get_top_n_max_calories(calories, n=3)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
