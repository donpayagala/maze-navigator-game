import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.grid import get_level, find_start_and_goal, is_walkable

class TestGrid(unittest.TestCase):
    def test_level_loads(self):
        grid = get_level(0)
        self.assertIsInstance(grid, list)
        self.assertGreater(len(grid), 0)

    def test_start_and_goal_exist(self):
        grid = get_level(0)
        start, goal = find_start_and_goal(grid)
        self.assertIsNotNone(start)
        self.assertIsNotNone(goal)

    def test_walkable_floor_cell(self):
        grid = get_level(0)
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == ".":
                    self.assertTrue(is_walkable(grid, r, c))
                    return

if __name__ == "__main__":
    unittest.main()