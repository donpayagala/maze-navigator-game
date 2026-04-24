import tkinter as tk
import time

try:
    import winsound
except ImportError:
    winsound = None

from src.grid import get_level, find_start_and_goal, is_walkable
from src.levels import LEVELS
from src.pathfinding import find_path


CELL = 40
WINDOW_SIZE = "1400x900"
HELP_TEXT = "Use W A S D to move | P for path | Q to quit"

MOVES = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}

THEME = {
    "bg": "#050816",
    "header_bg": "#050816",
    "header_fg": "#39FF14",
    "wall": "#111111",
    "floor": "#B8C1D7",
    "start": "#00E676",
    "goal": "#FF1744",
    "path": "#FFD54F",
    "player": "#00B0FF",
    "roof": "#80D8FF",
    "error": "#FF5252",
}


class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.level = 0
        self.completed = 0
        self.path = []

        # Window setup
        root.title("Maze Navigator")
        root.geometry(WINDOW_SIZE)
        root.configure(bg=THEME["bg"])

        # Header showing level progress
        self.header = tk.Label(
            root,
            font=("Segoe UI", 20, "bold"),
            bg=THEME["header_bg"],
            fg=THEME["header_fg"],
            pady=14,
        )
        self.header.pack(fill="x")

        # Message label for instructions and errors
        self.message = tk.Label(
            root,
            text=HELP_TEXT,
            font=("Segoe UI", 12),
            bg=THEME["bg"],
            fg="white",
        )
        self.message.pack()

        # Frame keeps the maze centered
        self.frame = tk.Frame(root, bg=THEME["bg"])
        self.frame.pack(expand=True)

        self.canvas = tk.Canvas(self.frame, bg=THEME["bg"], highlightthickness=0)
        self.canvas.pack()

        self.load_level()
        root.bind("<Key>", self.on_key)
        self.draw()

    def header_text(self):
        """Return level progress text."""
        marks = "✓" * self.completed + "·" * (len(LEVELS) - self.completed)
        return f"Level {self.level + 1} / {len(LEVELS)}   |   Completed: {marks}"

    def load_level(self):
        """Load the current maze level."""
        self.grid = get_level(self.level)
        self.start, self.goal = find_start_and_goal(self.grid)
        self.player = self.start
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.path.clear()

        self.header.config(text=self.header_text())
        self.canvas.config(width=self.cols * CELL, height=self.rows * CELL)

    def beep(self, freq=600, dur=100):
        """Play a beep sound if supported."""
        if winsound:
            try:
                winsound.Beep(freq, dur)
            except Exception:
                pass

    def show_message(self, text, error=False):
        """Show a temporary message."""
        color = THEME["error"] if error else "white"
        self.message.config(text=text, fg=color)
        self.root.after(2500, lambda: self.message.config(text=HELP_TEXT, fg="white"))

    def draw_cell(self, r, c, color):
        """Draw one maze cell."""
        x = c * CELL
        y = r * CELL

        self.canvas.create_rectangle(
            x,
            y,
            x + CELL,
            y + CELL,
            fill=color,
            outline="#0D1321",
        )

    def draw_path_dot(self, r, c):
        """Draw one shortest-path marker."""
        x = c * CELL
        y = r * CELL

        self.canvas.create_oval(
            x + 14,
            y + 14,
            x + CELL - 14,
            y + CELL - 14,
            fill=THEME["path"],
            outline="",
        )

    def draw_car(self, r, c):
        """Draw the player car."""
        x = c * CELL
        y = r * CELL

        parts = [
            ("oval", x + 8, y + CELL - 12, x + CELL - 8, y + CELL - 4, "#000000"),
            ("rect", x + 7, y + 12, x + CELL - 7, y + CELL - 12, THEME["player"]),
            ("rect", x + 14, y + 16, x + CELL - 14, y + CELL - 16, THEME["roof"]),
        ]

        for shape, x1, y1, x2, y2, color in parts:
            draw = self.canvas.create_oval if shape == "oval" else self.canvas.create_rectangle
            draw(x1, y1, x2, y2, fill=color, outline="", tags="player")

    def draw(self):
        """Redraw the maze, path, and player."""
        self.canvas.delete("all")

        colors = {
            "#": THEME["wall"],
            "S": THEME["start"],
            "G": THEME["goal"],
        }

        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                self.draw_cell(r, c, colors.get(cell, THEME["floor"]))

        # Draw shortest path
        for r, c in self.path:
            if (r, c) not in {self.start, self.goal, self.player}:
                self.draw_path_dot(r, c)

        self.draw_car(*self.player)

    def bump_wall(self, key):
        """Shake the player when movement is blocked."""
        self.beep(300, 80)

        dr, dc = MOVES[key]
        for offset in (4, -4, 4, 0):
            self.canvas.move("player", dc * offset, dr * offset)
            self.root.update()
            time.sleep(0.03)

        self.show_message("Movement blocked: wall or boundary detected.", True)
        self.draw()

    def move(self, key):
        """Move the player if the target cell is walkable."""
        dr, dc = MOVES[key]
        r, c = self.player
        next_pos = (r + dr, c + dc)

        if not is_walkable(self.grid, *next_pos):
            self.bump_wall(key)
            return

        self.player = next_pos
        self.path.clear()
        self.draw()

        if self.player == self.goal:
            self.completed += 1
            self.beep(900, 150)
            self.next_level()

    def show_path(self):
        """Show the shortest path using pathfinding.py."""
        self.path = find_path(self.grid, self.player, self.goal)

        if not self.path:
            self.show_message("No shortest path is available from this position.", True)
            return

        self.show_message("Shortest path displayed successfully.")
        self.draw()

    def next_level(self):
        """Load the next level or end the game."""
        self.level += 1

        if self.level >= len(LEVELS):
            self.header.config(text="🎉 ALL LEVELS COMPLETE 🎉")
            self.show_message("Congratulations. You completed every level.")
            return

        self.load_level()
        self.draw()

    def on_key(self, event):
        """Handle keyboard input."""
        key = event.keysym.lower()

        if key in MOVES:
            self.move(key)
        elif key == "p":
            self.show_path()
        elif key == "q":
            self.root.destroy()
        else:
            self.show_message("Invalid key. Use W, A, S, D, P, or Q.", True)


def main():
    root = tk.Tk()
    MazeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()