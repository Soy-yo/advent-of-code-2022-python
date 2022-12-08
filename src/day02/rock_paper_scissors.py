import os
from enum import Enum

from src.utils.io import read_input

MODULE = os.path.split(os.path.split(__file__)[0])[1]


class Action(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_char(cls, c: str) -> "Action":
        match c:
            case 'A' | 'X':
                return Action.ROCK
            case 'B' | 'Y':
                return Action.PAPER
            case 'C' | 'Z':
                return Action.SCISSORS
        raise ValueError(f'Invalid char {c}')


class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def from_char(cls, c: str) -> "Outcome":
        match c:
            case 'X':
                return Outcome.LOSE
            case 'Y':
                return Outcome.DRAW
            case 'Z':
                return Outcome.WIN
        raise ValueError(f'Invalid char {c}')


GAME_OUTCOME = {
    (Action.ROCK, Action.ROCK): Outcome.DRAW,
    (Action.ROCK, Action.PAPER): Outcome.LOSE,
    (Action.ROCK, Action.SCISSORS): Outcome.WIN,

    (Action.PAPER, Action.ROCK): Outcome.WIN,
    (Action.PAPER, Action.PAPER): Outcome.DRAW,
    (Action.PAPER, Action.SCISSORS): Outcome.LOSE,

    (Action.SCISSORS, Action.ROCK): Outcome.LOSE,
    (Action.SCISSORS, Action.PAPER): Outcome.WIN,
    (Action.SCISSORS, Action.SCISSORS): Outcome.DRAW,
}


def reverse_outcome():
    return {(rival, outcome): mine for (mine, rival), outcome in GAME_OUTCOME.items()}


def simulate(strategy: list[tuple[str, str]]) -> int:
    strategy = [
        (Action.from_char(rival), Action.from_char(mine))
        for rival, mine in strategy
    ]
    return sum(mine.value + GAME_OUTCOME[mine, rival].value for rival, mine in strategy)


def simulate_correctly(strategy: list[tuple[str, str]]) -> int:
    strategy = [
        (Action.from_char(rival), Outcome.from_char(outcome))
        for rival, outcome in strategy
    ]
    expected_shape = reverse_outcome()
    return sum(
        expected_shape[rival, outcome].value + outcome.value
        for rival, outcome in strategy
    )


def read(filename: str) -> list[tuple[str, str]]:
    # Make type hinting work
    def transform(line: str) -> tuple[str, str]:
        a, b = line.split(' ')
        return a, b

    path = os.path.join('src', MODULE, 'input', filename)
    return read_input(path, transform=transform)


def solve_part_one(strategy: list[tuple[str, str]]) -> int:
    return simulate(strategy)


def solve_part_two(strategy: list[tuple[str, str]]) -> int:
    return simulate_correctly(strategy)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
