import tkinter as tk
import time

try:
    import winsound
except ImportError:
    winsound = None

from src.grid import get_level, find_start_and_goal, is_walkable
from src.pathfinding import find_path
from src.levels import LEVELS

CELL = 40  # big, arcade-style tiles

THEME = {
    "dark": "#000000",
    "bg": "#050816",
    "header_bg": "#050816",
    "header_fg": "#39FF14",
    "wall_base": "#0F0F0F",
    "wall_glow": "#17181B",
    "floor": "#B8C1D7",
    "start": "#00E676",
    "goal": "#FF1744",
    "path": "#2C2323",
    "player": "#00B0FF",
    "player_roof": "#80d8ff",
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def mix_color(c1, c2, alpha):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * alpha)
    g = int(g1 + (g2 - g1) * alpha)
    b = int(b1 + (b2 - b1) * alpha)
    return rgb_to_hex(r, g, b)


class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.level = 0
        self.completed = 0
        self.direction = "d"
        self.wall_phase = 0.0
        self.load_level()

        self.root.geometry("1400x900")
        self.root.configure(bg=THEME["bg"])
        self.root.title("Maze Navigator")

        self.header = tk.Label(
            root,
            text=self.header_text(),
            font=("Segoe UI", 20, "bold"),
            bg=THEME["header_bg"],
            fg=THEME["header_fg"],
            pady=14
        )
        self.header.pack(fill="x")

        self.canvas = tk.Canvas(
            root,
            width=self.cols * CELL,
            height=self.rows * CELL,
            bg=THEME["bg"],
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        root.bind("<Key>", self.on_key)
        self.draw()
        self.animate_walls()

    def header_text(self):
        marks = "✓" * self.completed + "·" * (len(LEVELS) - self.completed)
        return f"Level {self.level + 1} / {len(LEVELS)}   |   Completed: {marks}"

    def load_level(self):
        self.grid = get_level(self.level)
        self.start, self.goal = find_start_and_goal(self.grid)
        self.player = self.start
        self.path = []
        self.rows, self.cols = len(self.grid), len(self.grid[0])

    def play_beep(self, freq=700, dur=120):
        if winsound:
            try:
                winsound.Beep(freq, dur)
            except Exception:
                pass

    def draw_car(self, r, c, body, roof, facing):
        x = c * CELL
        y = r * CELL

        self.canvas.create_oval(
            x + 8, y + CELL - 14,
            x + CELL - 8, y + CELL - 4,
            fill=THEME['dark'], outline=""
        )

        if facing == "w":
            self.canvas.create_rectangle(x + 12, y + 6, x + CELL - 12, y + CELL - 6, fill=body, outline="")
            self.canvas.create_polygon(x + 16, y + 10, x + CELL - 16, y + 10, x + CELL - 22, y + CELL // 2, x + 22, y + CELL // 2, fill=roof, outline="")
        elif facing == "s":
            self.canvas.create_rectangle(x + 12, y + 6, x + CELL - 12, y + CELL - 6, fill=body, outline="")
            self.canvas.create_polygon(x + 16, y + CELL - 10, x + CELL - 16, y + CELL - 10, x + CELL - 22, y + CELL // 2, x + 22, y + CELL // 2, fill=roof, outline="")
        elif facing == "a":
            self.canvas.create_rectangle(x + 6, y + 12, x + CELL - 6, y + CELL - 12, fill=body, outline="")
            self.canvas.create_polygon(x + 10, y + 16, x + 10, y + CELL - 16, x + CELL // 2, y + CELL - 22, x + CELL // 2, y + 22, fill=roof, outline="")
        else:
            self.canvas.create_rectangle(x + 6, y + 12, x + CELL - 6, y + CELL - 12, fill=body, outline="")
            self.canvas.create_polygon(x + CELL - 10, y + 16, x + CELL - 10, y + CELL - 16, x + CELL // 2, y + CELL - 22, x + CELL // 2, y + 22, fill=roof, outline="")

    def draw(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]

                if cell == "#":
                    color = mix_color(THEME["wall_base"], THEME["wall_glow"], self.wall_phase)
                elif cell == "S":
                    color = THEME["start"]
                elif cell == "G":
                    self.draw_car(r, c, THEME["goal"], "#ff8a80", "d")
                    continue
                else:
                    color = THEME["floor"]

                x1, y1 = c * CELL, r * CELL
                x2, y2 = x1 + CELL, y1 + CELL

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#0D1321", width=1)
                self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 - 3, y2 - 3, outline="#1f4068", width=1)

        for r, c in self.path:
            if (r, c) not in (self.start, self.goal):
                self.canvas.create_oval(
                    c * CELL + 14, r * CELL + 14,
                    c * CELL + CELL - 14, r * CELL + CELL - 14,
                    fill=THEME["path"],
                    outline=""
                )

        pr, pc = self.player
        self.draw_car(int(pr), int(pc), THEME["player"], THEME["player_roof"], self.direction)

    def animate_move(self, old, new):
        steps = 4
        (r1, c1), (r2, c2) = old, new

        for i in range(1, steps + 1):
            t = i / steps
            r = r1 + (r2 - r1) * t
            c = c1 + (c2 - c1) * t
            self.player = (r, c)
            self.draw()
            self.root.update()
            time.sleep(0.005)

        self.player = new

    def level_complete_flash(self):
        self.play_beep(900, 150)
        for _ in range(3):
            self.canvas.configure(bg="#FFFFFF")
            self.root.update()
            time.sleep(0.05)
            self.canvas.configure(bg=THEME["bg"])
            self.root.update()
            time.sleep(0.05)

    def animate_walls(self):
        self.wall_phase += 0.08
        if self.wall_phase > 1.0:
            self.wall_phase = 0.0
        self.draw()
        self.root.after(120, self.animate_walls)

    def on_key(self, event):
        key = event.keysym.lower()
        if key in "wasd":
            self.direction = key
            self.move(key)
        if key == "p":
            self.show_path()

    def move(self, key):
        dr = {"w": -1, "s": 1}.get(key, 0)
        dc = {"a": -1, "d": 1}.get(key, 0)
        nr, nc = int(self.player[0] + dr), int(self.player[1] + dc)

        if is_walkable(self.grid, nr, nc):
            old = (int(self.player[0]), int(self.player[1]))
            new = (nr, nc)
            self.animate_move(old, new)
            self.path = []
            self.draw()

            if new == self.goal:
                self.completed += 1
                self.level_complete_flash()
                self.next_level()

    def next_level(self):
        self.level += 1

        if self.level >= len(LEVELS):
            self.header.config(text="🎉 ALL LEVELS COMPLETE 🎉")
            return

        self.load_level()
        self.header.config(text=self.header_text())
        self.canvas.config(width=self.cols * CELL, height=self.rows * CELL)
        self.draw()

    def show_path(self):
        start = (int(self.player[0]), int(self.player[1]))
        self.path = find_path(self.grid, start, self.goal)
        self.draw()


def main():
    root = tk.Tk()
    MazeGUI(root)
    root.mainloop()