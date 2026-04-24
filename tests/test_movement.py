import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.grid import get_level
from src.game import move

class TestMovement(unittest.TestCase):
    def test_cannot_walk_into_wall(self):
        grid = get_level(0)
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == "#" and c > 0 and grid[r][c - 1] != "#":
                    player = (r, c - 1)
                    new_pos = move(grid, player, "d")
                    self.assertEqual(new_pos, player)
                    return

    def test_cannot_leave_grid(self):
        grid = get_level(0)
        player = (0, 0)
        new_pos = move(grid, player, "w")
        self.assertEqual(new_pos, player)

if __name__ == "__main__":
    unittest.main()