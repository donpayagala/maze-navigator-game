import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.levels import LEVELS
from src.grid import find_start_and_goal

class TestLevels(unittest.TestCase):
    def test_all_levels_have_start_and_goal(self):
        for level in LEVELS:
            start, goal = find_start_and_goal(level)
            self.assertIsNotNone(start)
            self.assertIsNotNone(goal)

    def test_all_levels_are_rectangular(self):
        for level in LEVELS:
            width = len(level[0])
            for row in level:
                self.assertEqual(len(row), width)

if __name__ == "__main__":
    unittest.main()