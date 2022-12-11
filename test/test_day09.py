from src.day09.rope_bridge import read, solve_part_one, solve_part_two


def test_get_distinct_positions():
    data = read('test-input-0.txt')
    result = solve_part_one(data)
    assert result == 13


def test_get_distinct_positions_with_bigger_rope():
    for i, n in enumerate((1, 36)):
        data = read(f'test-input-{i}.txt')
        result = solve_part_two(data)
        assert result == n
