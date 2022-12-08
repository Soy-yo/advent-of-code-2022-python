from src.day08.treetop_tree_house import read, solve_part_one, solve_part_two


def test_find_visible_trees():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 21


def test_find_biggest_scenic_score():
    data = read('test-input.txt')
    result = solve_part_two(data)
    assert result == 8
