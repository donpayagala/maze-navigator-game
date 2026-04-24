from typing import List, Tuple
from src.levels import LEVELS

Pos = Tuple[int, int]
Grid = List[List[str]]


def get_level(i: int) -> Grid:
    return [row[:] for row in LEVELS[i]]


def find_start_and_goal(grid: Grid):
    start = goal = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            elif cell == "G":
                goal = (r, c)
    return start, goal


def is_walkable(grid: Grid, r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != "#"