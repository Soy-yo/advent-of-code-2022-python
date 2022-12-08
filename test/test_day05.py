from src.day05.supply_stacks import read, solve_part_one, solve_part_two


def test_simulate_stacks():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 'CMZ'


def test_camp_cleanup_overlap():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 'MCD'
