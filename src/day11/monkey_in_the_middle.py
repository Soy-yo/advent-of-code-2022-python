import os
import re
import math
import operator
from dataclasses import dataclass, field
from typing import Callable, Any
from functools import reduce

from src.utils.io import read_multi_input

MODULE = os.path.split(os.path.split(__file__)[0])[1]


@dataclass(frozen=True)
class MonkeyData:
    items: list[int] = field()
    operation: Callable[[int], int] = field()


@dataclass(frozen=True)
class MonkeyTest:
    divisor: int = field()
    true_id: int = field()
    false_id: int = field()


class Monkey:

    def __init__(self, items: list[int], operation: Callable[[int], int]):
        self._items = items[:]
        self._item_inspection_count = 0
        self._operation = operation
        self._callback = None

    @property
    def item_inspection_count(self) -> int:
        return self._item_inspection_count

    @property
    def callback(self) -> Callable[[int], Any]:
        return self._callback

    @callback.setter
    def callback(self, callback: Callable[[int], Any]):
        self._callback = callback

    def add_item(self, item: int):
        self._items.append(item)

    def do_monkey_stuff(self):
        while self._items:
            self._do_monkey_stuff()
            self._item_inspection_count += 1

    def _do_monkey_stuff(self):
        item = self._items.pop(0)
        new_item = self._operation(item)
        if self._callback is not None:
            self._callback(new_item)


def get_monkey_business(monkeys: list[Monkey], rounds: int, n: int) -> int:
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.do_monkey_stuff()

    most_active = sorted(map(lambda m: m.item_inspection_count, monkeys), reverse=True)[:n]
    return reduce(operator.mul, most_active)


def read(filename: str) -> tuple[list[MonkeyData], list[MonkeyTest]]:
    def extract_operation(op_str: str) -> Callable[[int], int]:
        op = op_str.split('= ')[-1]
        lhs, o, rhs = op.split(' ')

        operator_fun = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul
        }[o]

        def f(x: int) -> int:
            lhs_ = x if lhs == 'old' else int(lhs)
            rhs_ = x if rhs == 'old' else int(rhs)
            return operator_fun(lhs_, rhs_)

        return f

    path = os.path.join('src', MODULE, 'input', filename)
    monkey_info = read_multi_input(path)

    number_re = re.compile(r'(\d+)')

    monkeys = []
    tests = []

    for _, items, operation, test, if_true, if_false in monkey_info:
        items = [int(item) for item in number_re.findall(items)]
        operation = extract_operation(operation)

        test_number = int(number_re.search(test).group())
        if_true_monkey = int(number_re.search(if_true).group())
        if_false_monkey = int(number_re.search(if_false).group())

        monkeys.append(MonkeyData(items, operation))
        tests.append(MonkeyTest(test_number, if_true_monkey, if_false_monkey))

    return monkeys, tests


def solve_part_one(data: tuple[list[MonkeyData], list[MonkeyTest]]) -> int:
    monkey_data, tests = data
    monkeys = [Monkey(m.items, m.operation) for m in monkey_data]

    def after_operation(number: int, true: int, false: int):
        def f(x: int):
            x //= 3
            to_monkey = monkeys[true] if x % number == 0 else monkeys[false]
            to_monkey.add_item(x)

        return f

    for monkey, test in zip(monkeys, tests):
        monkey.callback = after_operation(test.divisor, test.true_id, test.false_id)

    return get_monkey_business(monkeys, rounds=20, n=2)


def solve_part_two(data: tuple[list[MonkeyData], list[MonkeyTest]]) -> int:
    monkey_data, tests = data
    monkeys = [Monkey(m.items, m.operation) for m in monkey_data]
    modulo = math.lcm(*[test.divisor for test in tests])

    def after_operation(number: int, true: int, false: int):
        def f(x: int):
            # Trick to avoid getting stupidly enormous numbers
            # As we don't care about the actual number
            x %= modulo
            to_monkey = monkeys[true] if x % number == 0 else monkeys[false]
            to_monkey.add_item(x)

        return f

    for monkey, test in zip(monkeys, tests):
        monkey.callback = after_operation(test.divisor, test.true_id, test.false_id)

    return get_monkey_business(monkeys, rounds=10_000, n=2)


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
