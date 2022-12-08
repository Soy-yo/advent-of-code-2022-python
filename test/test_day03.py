from src.day03.rucksack_reorganization import read, solve_part_one, solve_part_two


def test_rucksack_reorganization():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 157


def test_rucksack_reorganization_badges():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 70
