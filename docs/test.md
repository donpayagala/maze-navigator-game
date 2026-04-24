# Tests

This folder contains automated tests for the Maze Navigator project.

## What is tested?

### 1. Grid Functions
- Levels load correctly
- Start and goal positions exist
- Walkability rules work

### 2. Pathfinding (BFS)
- A path exists when it should
- Path is continuous (adjacent steps)
- Path starts at S and ends at G

### 3. Movement Rules
- Player cannot walk into walls
- Player cannot leave the grid

### 4. Level Validity
- All levels contain exactly one S and one G
- All levels are rectangular

These tests ensure the core logic works independently of the GUI.
