from src.day12.hill_climbing_algorithm import read, solve_part_one, solve_part_two


def test_climb():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 31


def test_climb_from_any():
    data = read(f'test-input.txt')
    result = solve_part_two(data)
    assert result == 29
