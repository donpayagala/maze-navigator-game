import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.grid import get_level, find_start_and_goal
from src.pathfinding import find_path

class TestPathfinding(unittest.TestCase):
    def test_path_exists_level1(self):
        grid = get_level(0)
        start, goal = find_start_and_goal(grid)
        path = find_path(grid, start, goal)
        self.assertGreater(len(path), 0)

    def test_path_is_continuous(self):
        grid = get_level(0)
        start, goal = find_start_and_goal(grid)
        path = find_path(grid, start, goal)
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1)

    def test_path_starts_and_ends_correctly(self):
        grid = get_level(0)
        start, goal = find_start_and_goal(grid)
        path = find_path(grid, start, goal)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)

if __name__ == "__main__":
    unittest.main()