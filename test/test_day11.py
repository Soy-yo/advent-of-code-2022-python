from src.day11.monkey_in_the_middle import read, solve_part_one, solve_part_two


def test_monkey_business():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 10605


def test_huge_monkey_business():
    data = read(f'test-input.txt')
    result = solve_part_two(data)
    assert result == 2713310158
