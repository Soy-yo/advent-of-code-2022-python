import os

import numpy as np

MODULE = os.path.split(os.path.split(__file__)[0])[1]


def visible_trees(grid: np.ndarray[np.int32]) -> list[tuple[int, int]]:
    visible = set()

    rows, cols = grid.shape

    # Make sure we allow zeroes in the edge
    highest_down = np.full(cols, -1)
    highest_right = np.full(rows, -1)
    highest_up = np.full(cols, -1)
    highest_left = np.full(rows, -1)

    for i in range(rows):
        indices, = np.where(grid[i] > highest_down)
        visible.update((i, j) for j in indices)
        highest_down = np.maximum(highest_down, grid[i])

    for j in range(cols):
        indices, = np.where(grid[:, j] > highest_right)
        visible.update((i, j) for i in indices)
        highest_right = np.maximum(highest_right, grid[:, j])

    for i in range(rows - 1, 0, -1):
        indices, = np.where(grid[i] > highest_up)
        visible.update((i, j) for j in indices)
        highest_up = np.maximum(highest_up, grid[i])

    for j in range(cols - 1, 0, -1):
        indices, = np.where(grid[:, j] > highest_left)
        visible.update((i, j) for i in indices)
        highest_left = np.maximum(highest_left, grid[:, j])

    return list(visible)


def scenic_score(grid: np.ndarray[np.int32]) -> np.ndarray[np.int32]:
    rows, cols = grid.shape

    up = np.zeros_like(grid, dtype=np.int32)
    left = np.zeros_like(grid, dtype=np.int32)
    down = np.zeros_like(grid, dtype=np.int32)
    right = np.zeros_like(grid, dtype=np.int32)

    # Index matrices to compute distances
    ii, jj = np.mgrid[:rows, :cols]

    for i in range(1, rows):
        indices = np.where(grid[i] <= grid[:i], ii[:i], 0)
        up[i] = np.min(i - indices, axis=0)

    for j in range(1, cols):
        # Ensure correct shape with newaxis
        indices = np.where(grid[:, j, np.newaxis] <= grid[:, :j], jj[:, :j], 0)
        left[:, j] = np.min(j - indices, axis=1)

    for i in range(rows - 2, -1, -1):
        indices = np.where(grid[i] <= grid[i+1:], ii[i+1:], rows - 1)
        down[i] = np.min(indices - i, axis=0)

    for j in range(cols - 2, -1, -1):
        # Ensure correct shape with newaxis
        indices = np.where(grid[:, j, np.newaxis] <= grid[:, j+1:], jj[:, j+1:], cols - 1)
        right[:, j] = np.min(indices - j, axis=1)

    return up * left * down * right


def read(filename: str) -> np.ndarray[np.int32]:
    path = os.path.join('src', MODULE, 'input', filename)
    return np.genfromtxt(path, dtype=np.int32, delimiter=1)


def solve_part_one(grid: np.ndarray[np.int32]) -> int:
    return len(visible_trees(grid))


def solve_part_two(grid: np.ndarray[np.int32]) -> int:
    return np.max(scenic_score(grid))


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
