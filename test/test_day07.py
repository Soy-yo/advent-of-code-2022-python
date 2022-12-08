from src.day07.no_space_left import read, solve_part_one, solve_part_two


def test_get_file_system_sizes():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 95437


def test_get_file_to_delete():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 24933642
