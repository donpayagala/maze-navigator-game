# Maze Navigator – Applied Programming Coursework  
Student ID: u2801384  

## Overview  
Maze Navigator is a modular Python application that implements a maze‑navigation game with both a text‑mode interface and a neon‑themed Tkinter GUI.  
The project uses a Breadth‑First Search (BFS) algorithm to compute the shortest path from the player to the goal.  
All core logic (grid handling, pathfinding, and level data) is shared between the text and GUI versions, ensuring clean separation between logic and presentation.

The GUI includes smooth car movement, turning animation, glow effects, and a modern neon visual style.

---

src/
│   ├── __init__.py        # Declares src as a Python package
│   ├── grid.py            # Grid loading, validation, and walkability logic
│   ├── gui.py             # Tkinter-based GUI with animations and visual effects
│   ├── pathfinding.py     # BFS implementation for shortest path calculation
│   ├── levels.py          # Definitions of all maze levels (2D grid format)
│   └── main.py            # Application entry point (GUI or text mode)

tests/
│   ├── conftest.py        # Configures import paths for testing
│   ├── test_grid.py       # Unit tests for grid functionality
│   ├── test_levels.py     # Validation tests for level data
│   └── test_pathfinding.py# Tests for BFS pathfinding correctness

docs/
│   └── README.md          # Project documentation

examples/
│   └── Additional maze layout examples

run_all_tests.py           # Script to execute all test suites