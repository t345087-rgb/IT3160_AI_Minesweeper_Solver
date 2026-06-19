"""Game loop for running the solver in a background thread."""

import time
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot, QThread

from minesweeper.board import Board, Position
from minesweeper.solver import ActionType

if TYPE_CHECKING:
    from minesweeper.solver import MinesweeperSolver


class SolverWorker(QObject):
    """Worker object that runs the solver in a background thread."""

    # Signals to communicate with main thread
    move_made = Signal(Position, bool)  # (position, is_safe)
    solver_finished = Signal(bool)  # won/lost
    solver_error = Signal(str)  # error message
    solver_stopped = Signal()

    def __init__(
        self,
        board: Board,
        solver: "MinesweeperSolver",
        delay: float = 0.1,
    ) -> None:
        """Initialize the solver worker."""
        super().__init__()
        self._board = board
        self._solver = solver
        self._delay = delay
        self._running = False
        self._stopped = False

    def run(self) -> None:
        """Run the solver loop."""
        self._running = True
        self._stopped = False

        while self._running and not self._stopped:
            try:
                # Check if game is already over
                if self._board.is_won():
                    self.solver_finished.emit(True)
                    break
                if self._board.is_lost():
                    self.solver_finished.emit(False)
                    break

                action = self._solver.choose_next_action()
                if action is None:
                    # No safe move found
                    self.solver_error.emit("No safe move found")
                    break

                self._solver.apply_action(action)
                self.move_made.emit(
                    action.position,
                    action.action_type == ActionType.REVEAL
                    and not self._board.is_lost(),
                )

                # Check game state after move
                if self._board.is_lost():
                    self.solver_finished.emit(False)
                    break
                if self._board.is_won():
                    self.solver_finished.emit(True)
                    break

                # Apply delay for visualization
                time.sleep(self._delay)

            except Exception as e:
                self.solver_error.emit(str(e))
                break

        self._running = False

    def stop(self) -> None:
        """Stop the solver loop."""
        self._stopped = True
        self._running = False


class GameLoop(QObject):
    """Manages the game loop for running the solver."""

    move_made = Signal(Position, bool)  # Forwarded from worker
    solver_finished = Signal(bool)  # Forwarded from worker
    solver_error = Signal(str)  # Forwarded from worker

    def __init__(self) -> None:
        """Initialize the game loop."""
        super().__init__()
        self._worker: SolverWorker | None = None
        self._thread: QThread | None = None

    def start(
        self,
        board: Board,
        solver: "MinesweeperSolver",
        delay: float = 0.1,
    ) -> None:
        """Start the game loop with a new thread."""
        self.stop()  # Stop any existing loop

        # Create worker and thread
        self._worker = SolverWorker(board, solver, delay)
        self._thread = QThread()

        # Move worker to thread
        self._worker.moveToThread(self._thread)

        # Connect signals
        self._worker.move_made.connect(self.move_made)
        self._worker.solver_finished.connect(self.solver_finished)
        self._worker.solver_finished.connect(self._on_finished)
        self._worker.solver_error.connect(self.solver_error)
        self._worker.solver_error.connect(self._on_error)

        # Start thread
        self._thread.started.connect(self._worker.run)
        self._thread.start()

    def stop(self) -> None:
        """Stop the game loop."""
        if self._worker:
            self._worker.stop()

        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        self._worker = None

    @Slot(bool)
    def _on_finished(self, won: bool) -> None:
        """Clean up when solver finishes."""
        self._cleanup_thread()

    @Slot(str)
    def _on_error(self, error: str) -> None:
        """Clean up when solver stops because of an error."""
        self._cleanup_thread()

    def _cleanup_thread(self) -> None:
        """Release worker thread resources after the solver loop exits."""
        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None
        self._worker = None

    @property
    def is_running(self) -> bool:
        """Check if the solver is currently running."""
        return self._thread is not None and self._thread.isRunning()
