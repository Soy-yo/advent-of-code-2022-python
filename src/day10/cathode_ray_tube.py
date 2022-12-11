import abc
import os

from src.utils.io import read_input

MODULE = os.path.split(os.path.split(__file__)[0])[1]

COLUMNS = 40


class Instruction(abc.ABC):

    @property
    @abc.abstractmethod
    def cycles(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self, x: int) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def run_with_cycles(self, x: int) -> list[int]:
        raise NotImplementedError()


class Noop(Instruction):

    @property
    def cycles(self) -> int:
        return 1

    def run(self, x: int) -> int:
        return x

    def run_with_cycles(self, x: int) -> list[int]:
        return [x]


class Addx(Instruction):

    def __init__(self, v: int):
        self._v = v

    @property
    def cycles(self) -> int:
        return 2

    def run(self, x: int) -> int:
        return x + self._v

    def run_with_cycles(self, x: int) -> list[int]:
        return [x, self.run(x)]


class CRT:

    def __init__(self, columns: int):
        self._columns = columns
        self._i = 0
        self._j = 0
        self._buffer = []

    def draw(self) -> str:
        return '\n'.join([''.join(row) for row in self._buffer])

    def add_pixel(self, x: int):
        sprite_pixels = (x - 1, x, x + 1)
        pixel = '#' if self._j in sprite_pixels else '.'
        self._add_to_buffer(pixel)

    def _add_to_buffer(self, pixel: str):
        if self._i == len(self._buffer):
            self._buffer.append([])
        self._buffer[self._i].append(pixel)
        self._j += 1
        if self._j == self._columns:
            self._j = 0
            self._i += 1


class CPU:

    def __init__(self, crt: CRT = None):
        self._x = 1
        self._cycle = 0
        self._history = [self._x]
        self._crt = crt

    @property
    def x(self) -> int:
        return self._x

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def history(self) -> list[int]:
        return self._history[:]

    def apply(self, instruction: Instruction):
        cycles = instruction.run_with_cycles(self._x)

        if self._crt is not None:
            for x in (self._x, *cycles[:-1]):
                self._crt.add_pixel(x)

        self._history.extend(cycles)
        self._x = cycles[-1]
        self._cycle += instruction.cycles


def run_instructions(cpu: CPU, instructions: list[Instruction]) -> list[int]:
    for instruction in instructions:
        cpu.apply(instruction)

    return cpu.history


def read(filename: str) -> list[Instruction]:
    def transform(line: str) -> Instruction:
        if line == 'noop':
            return Noop()
        return Addx(int(line.split()[-1]))

    path = os.path.join('src', MODULE, 'input', filename)
    return read_input(path, transform=transform)


def solve_part_one(instructions: list[Instruction]) -> int:
    history = run_instructions(CPU(), instructions)
    cycles = (20, 60, 100, 140, 180, 220)
    return sum(c * history[c - 1] for c in cycles)


def solve_part_two(instructions: list[Instruction]) -> str:
    crt = CRT(COLUMNS)
    run_instructions(CPU(crt), instructions)
    return crt.draw()


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
