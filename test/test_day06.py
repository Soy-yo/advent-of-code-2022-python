from src.day06.tuning_trouble import read, solve_part_one, solve_part_two


def test_find_start_of_packet():
    for i, n in enumerate((5, 6, 10, 11)):
        data = read(f'test-input-{i}.txt')
        result = solve_part_one(data)
        assert result == n


def test_find_message():
    for i, n in enumerate((23, 23, 29, 26, 19)):
        data = read(f'test-input-{i}.txt')
        result = solve_part_two(data)
        assert result == n
