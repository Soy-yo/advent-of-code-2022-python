from src.day10.cathode_ray_tube import read, solve_part_one, solve_part_two


def test_signal_strength():
    data = read('test-input.txt')
    result = solve_part_one(data)
    assert result == 13140


def test_draw():
    data = read(f'test-input.txt')
    result = solve_part_two(data)
    assert result == ('##..##..##..##..##..##..##..##..##..##..\n'
                      '###...###...###...###...###...###...###.\n'
                      '####....####....####....####....####....\n'
                      '#####.....#####.....#####.....#####.....\n'
                      '######......######......######......####\n'
                      '#######.......#######.......#######.....')
