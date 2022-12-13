from src.day13.distress_signal import read, solve_part_one, solve_part_two


def test_compare_lists():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 13


def test_sort_lists():
    data = read(f'test-input.txt')
    result = solve_part_two(data)
    assert result == 140
