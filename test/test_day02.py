from src.day02.rock_paper_scissors import read, solve_part_one, solve_part_two


def test_rock_paper_scissors_simulator():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 15


def test_rock_paper_scissors_correct_simulator():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 12
