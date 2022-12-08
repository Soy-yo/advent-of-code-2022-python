from src.day01.calorie_counting import read, solve_part_one, solve_part_two


def test_calorie_counter():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 24000


def test_top_n_calorie_counter():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 45000
