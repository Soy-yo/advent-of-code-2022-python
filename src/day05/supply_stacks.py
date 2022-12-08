import os
import re
import copy
from dataclasses import dataclass, field
from typing import Iterable

from src.utils.io import read_lines

MODULE = os.path.split(os.path.split(__file__)[0])[1]


@dataclass(frozen=True)
class Move:
    count: int = field()
    from_stack: int = field()
    to_stack: int = field()


def simulate(
        stacks: dict[int, list[str]],
        moves: list[Move],
        reverse: bool = True
) -> dict[int, list[str]]:
    def pick(elements: list[str]) -> Iterable[str]:
        if reverse:
            return reversed(elements)
        return elements

    stacks = copy.deepcopy(stacks)
    for move in moves:
        from_stack = stacks[move.from_stack]
        to_stack = stacks[move.to_stack]
        taken = pick(from_stack[-move.count:])
        to_stack.extend(taken)
        del from_stack[-move.count:]
    return stacks


def read(filename: str) -> tuple[dict[int, list[str]], list[Move]]:
    def read_stacks(it: Iterable[str]) -> dict[int, list[str]]:
        crate_re = re.compile(r'\[\w]')
        crates = []
        index_re = re.compile(r'\d')
        indices = []
        for line in it:
            if line == '':
                break
            if index_re.search(line):
                matches = index_re.finditer(line)
                indices.extend([(int(m.group()), m.start()) for m in matches])
            else:
                matches = crate_re.finditer(line)
                crates.append([(m.group()[1], m.start() + 1) for m in matches])

        stacks = {index: [] for index, _ in indices}
        starts = {start: index for index, start in indices}

        for crate_list in reversed(crates):
            for crate, start in crate_list:
                index = starts[start]
                stacks[index].append(crate)

        return stacks

    def read_moves(it: Iterable[str]) -> list[Move]:
        move_re = re.compile(r'^move (\d+) from (\d+) to (\d+)$')
        moves = []
        for line in it:
            count, frm, to = move_re.search(line).groups()
            moves.append(Move(int(count), int(frm), int(to)))
        return moves

    path = os.path.join('src', MODULE, 'input', filename)
    data = read_lines(path)
    iterable = iter(data)
    return read_stacks(iterable), read_moves(iterable)


def solve_part_one(stack_moves: tuple[dict[int, list[str]], list[Move]]) -> str:
    stacks = simulate(*stack_moves)
    return ''.join(stack[-1] if stacks else '' for _, stack in sorted(stacks.items()))


def solve_part_two(stack_moves: tuple[dict[int, list[str]], list[Move]]) -> str:
    stacks = simulate(*stack_moves, reverse=False)
    return ''.join(stack[-1] if stacks else '' for _, stack in sorted(stacks.items()))


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
