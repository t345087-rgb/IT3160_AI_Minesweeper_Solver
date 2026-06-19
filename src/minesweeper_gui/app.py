"""Main entry point for the Minesweeper GUI application."""

import sys
from PySide6.QtWidgets import QApplication

from minesweeper_gui.main_window import MainWindow


def main() -> int:
    """Run the Minesweeper GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("AI Minesweeper Solver")

    # Create and show main window
    window = MainWindow()
    window.resize(800, 600)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())