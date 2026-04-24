from src.grid import get_level, find_start_and_goal, is_walkable
from src.pathfinding import find_path
from src.levels import LEVELS

def show(grid, player):
    for r, row in enumerate(grid):
        print("".join("P" if (r, c) == player else cell for c, cell in enumerate(row)))
    print()


def move(grid, player, key):
    dr = {"w": -1, "s": 1}.get(key, 0)
    dc = {"a": -1, "d": 1}.get(key, 0)
    nr, nc = player[0] + dr, player[1] + dc
    return (nr, nc) if is_walkable(grid, nr, nc) else player


def run_text_game():

    for i in range(len(LEVELS)):
        grid = get_level(i)
        start, goal = find_start_and_goal(grid)
        player = start

        print(f"\n=== Level {i + 1} ===")
        while True:
            show(grid, player)
            if player == goal:
                print("Level complete!")
                break

            cmd = input("Move (w/a/s/d), p=path, q=quit: ").lower()
            if cmd == "q":
                return
            if cmd == "p":
                for r, c in find_path(grid, player, goal):
                    if grid[r][c] == ".":
                        grid[r][c] = "o"
                show(grid, player)
                continue

            player = move(grid, player, cmd)