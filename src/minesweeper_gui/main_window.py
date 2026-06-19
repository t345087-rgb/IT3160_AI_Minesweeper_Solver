"""Main window for the Minesweeper GUI application."""

from minesweeper.board import Board, Position, CellState
from minesweeper.solver import MinesweeperSolver as Solver

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu, QMessageBox, QStatusBar, QLabel
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence

from minesweeper_gui.board_view import BoardView
from minesweeper_gui.control_panel import ControlPanel
from minesweeper_gui.game_loop import GameLoop


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self._board: Board | None = None
        self._solver: Solver | None = None
        self._game_loop: GameLoop | None = None
        self._solver_delay: float = 0.1
        self.setWindowTitle("AI Minesweeper Solver")
        self._setup_ui()
        self._setup_menu()
        self._setup_solver()
        self._setup_status_bar()
        self._create_new_game()

    def _setup_ui(self) -> None:
        """Set up the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create control panel
        self._control_panel = ControlPanel()
        self._control_panel.start_solver_clicked.connect(self._on_start_solver)
        self._control_panel.stop_solver_clicked.connect(self._on_stop_solver)
        self._control_panel.reset_clicked.connect(self._on_new_game)
        self._control_panel.difficulty_changed.connect(self._on_difficulty_changed)
        self._control_panel.speed_changed.connect(self._on_speed_changed)
        layout.addWidget(self._control_panel)

        # Create and add board view
        self._board_view = BoardView()
        self._board_view.cell_left_clicked.connect(self._on_left_click)
        self._board_view.cell_right_clicked.connect(self._on_right_click)
        layout.addWidget(self._board_view)

    def _setup_solver(self) -> None:
        """Initialize the solver."""
        self._game_loop = GameLoop()
        self._game_loop.move_made.connect(self._on_solver_move)
        self._game_loop.solver_finished.connect(self._on_solver_finished)
        self._game_loop.solver_error.connect(self._on_solver_error)

    def _setup_status_bar(self) -> None:
        """Set up the status bar with game statistics."""
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._mines_label = QLabel("Mines: 0")
        self._flags_label = QLabel("Flags: 0")
        self._revealed_label = QLabel("Revealed: 0")
        self._status_bar.addPermanentWidget(self._mines_label)
        self._status_bar.addPermanentWidget(self._flags_label)
        self._status_bar.addPermanentWidget(self._revealed_label)

    def _setup_menu(self) -> None:
        """Set up the menu bar."""
        menu_bar = self.menuBar()
        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)

        # File menu actions
        new_action = QAction("&New Game", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(lambda checked=False: self._on_new_game())
        file_menu.addAction(new_action)

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _on_left_click(self, pos: Position) -> None:
        """Handle left click to reveal a cell."""
        if self._board is None:
            return

        try:
            self._board.reveal(pos)
            self._board_view.update()
            self._update_stats()

            # Check for mine hit (game over)
            if self._board.has_mine(pos):
                self._show_game_over(False)
            # Check for win condition
            elif self._board.is_won():
                self._show_game_over(True)
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Move", str(e))

    def _on_right_click(self, pos: Position) -> None:
        """Handle right click to toggle flag on a cell."""
        if self._board is None:
            return

        try:
            self._board.toggle_flag(pos)
            self._board_view.update()
            self._update_stats()
            if self._board.is_won():
                self._show_game_over(True)
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Move", str(e))

    def _show_game_over(self, won: bool) -> None:
        """Show game over message."""
        if won:
            QMessageBox.information(self, "Game Over", "Congratulations! You won!")
        else:
            QMessageBox.critical(self, "Game Over", "You hit a mine! Game Over.")

    def _create_new_game(self, rows: int = 9, cols: int = 9, mines: int = 10) -> None:
        """Create a new game with the specified settings."""
        self._stop_solver()
        self._board = Board(rows, cols, mines)
        self._solver = Solver(self._board)
        self._board_view.set_board(self._board)
        self._update_stats()
        self.update()

    def _on_new_game(self) -> None:
        """Create a new game using the currently selected difficulty."""
        rows, cols, mines = self._control_panel.current_board_config()
        self._create_new_game(rows, cols, mines)

    def _on_difficulty_changed(self, rows: int, cols: int, mines: int) -> None:
        """Handle difficulty change."""
        self._create_new_game(rows, cols, mines)

    def _on_speed_changed(self, delay: float) -> None:
        """Handle solver speed change."""
        self._solver_delay = delay

    def _on_start_solver(self) -> None:
        """Start the solver."""
        if self._board is None or self._solver is None or self._game_loop is None:
            return

        # Stop if already running
        if self._game_loop.is_running:
            self._stop_solver()

        # Start the solver loop
        self._game_loop.start(self._board, self._solver, self._solver_delay)

    def _on_stop_solver(self) -> None:
        """Stop the solver."""
        self._stop_solver()

    def _stop_solver(self) -> None:
        """Internal method to stop the solver."""
        if self._game_loop and self._game_loop.is_running:
            self._game_loop.stop()
        self._control_panel.set_solver_running(False)

    def _on_solver_move(self, pos: Position, is_safe: bool) -> None:
        """Handle a move made by the solver."""
        self._board_view.update()
        self._update_stats()

    def _on_solver_finished(self, won: bool) -> None:
        """Handle solver finish."""
        self._control_panel.set_solver_finished(won)
        self._board_view.update()
        self._show_game_over(won)

    def _on_solver_error(self, error: str) -> None:
        """Handle solver error."""
        self._control_panel.set_solver_running(False)
        QMessageBox.warning(self, "Solver Error", error)

    def _update_stats(self) -> None:
        """Update the status bar statistics."""
        if self._board is None:
            return

        # Count mines and flags
        total_mines = self._board.mine_count
        flagged = 0
        revealed = 0

        for row in range(self._board.rows):
            for col in range(self._board.cols):
                pos = Position(row, col)
                state = self._board.state(pos)
                if state == CellState.FLAGGED:
                    flagged += 1
                elif state == CellState.REVEALED:
                    revealed += 1

        self._mines_label.setText(f"Mines: {total_mines}")
        self._flags_label.setText(f"Flags: {flagged}")
        self._revealed_label.setText(f"Revealed: {revealed}")

    def closeEvent(self, event: QCloseEvent) -> None:
        """Stop the solver thread before closing the window."""
        self._stop_solver()
        event.accept()
