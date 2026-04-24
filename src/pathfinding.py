from collections import deque
from src.grid import Grid, Pos, is_walkable


def neighbours(grid: Grid, r: int, c: int):
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [(r + dr, c + dc) for dr, dc in steps if is_walkable(grid, r + dr, c + dc)]


def find_path(grid: Grid, start: Pos, goal: Pos):
    queue = deque([start])
    came = {start: None}

    while queue:
        cur = queue.popleft()
        if cur == goal:
            break
        for nxt in neighbours(grid, *cur):
            if nxt not in came:
                came[nxt] = cur
                queue.append(nxt)

    if goal not in came:
        return []

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came[cur]
    return path[::-1]