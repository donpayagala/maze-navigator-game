# Maze Navigator – Applied Programming Coursework  
Student ID: u2801384  

## Overview  
Maze Navigator is a modular Python application that implements a maze‑navigation game with both a text‑mode interface and a neon‑themed Tkinter GUI.  
The project uses a Breadth‑First Search (BFS) algorithm to compute the shortest path from the player to the goal.  
All core logic (grid handling, pathfinding, and level data) is shared between the text and GUI versions, ensuring clean separation between logic and presentation.

The GUI includes smooth car movement, turning animation, glow effects, and a modern neon visual style.

---

## Project Structure  

src/  
│   ├── __init__.py          # Makes src a Python package  
│   ├── grid.py              # Grid loading, walkability checks, start/goal detection  
│   ├── gui.py               # Neon GUI with car movement, glow effects, animations  
│   ├── pathfinding.py       # BFS shortest‑path algorithm  
│   ├── levels.py            # All 5 maze levels stored as 2D lists  
│   └── main.py              # Entry point (launches GUI or text mode)  

tests/  
│   ├── conftest.py          # Ensures src/ is importable during pytest  
│   ├── test_grid.py         # Tests for grid behaviour  
│   ├── test_levels.py       # Tests for level validity  
│   └── test_pathfinding.py  # Tests for BFS pathfinding  

docs/  
│   └── README.md            # Documentation (this file)  

examples/  
│   └── Additional maze layout examples  

run_all_tests.py             # Helper script to run all tests  

---

## Running the Game  

### GUI Mode (Neon Tkinter Interface)  
From the project root:  
