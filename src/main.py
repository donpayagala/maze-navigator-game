# Entry point for Maze Navigator.
# Lets user choose GUI or text version.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.game import run_text_game
from src.gui import main as run_gui

if __name__ == "__main__":
    run_gui() if input("Type 1 for GUI, else text: ") == "1" else run_text_game()