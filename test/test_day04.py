from src.day04.camp_cleanup import read, solve_part_one, solve_part_two


def test_camp_cleanup_complete_overlap():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 2


def test_camp_cleanup_overlap():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 4
