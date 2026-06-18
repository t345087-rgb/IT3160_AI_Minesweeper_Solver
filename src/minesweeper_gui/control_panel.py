"""Control panel widget for solver controls."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel,
    QSpinBox, QComboBox, QGroupBox
)


class ControlPanel(QWidget):
    """Widget containing solver controls."""

    # Signals
    start_solver_clicked = Signal()
    stop_solver_clicked = Signal()
    reset_clicked = Signal()
    difficulty_changed = Signal(int, int, int)  # rows, cols, mines
    speed_changed = Signal(float)  # delay in seconds

    def __init__(self, parent=None) -> None:
        """Initialize the control panel."""
        super().__init__(parent)
        self._solver_running = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QHBoxLayout(self)

        # Difficulty selection
        difficulty_group = QGroupBox("Difficulty")
        diff_layout = QHBoxLayout(difficulty_group)

        self._difficulty_combo = QComboBox()
        self._difficulty_combo.addItem("Easy (9x9, 10 mines)", {"rows": 9, "cols": 9, "mines": 10})
        self._difficulty_combo.addItem("Medium (16x16, 40 mines)", {"rows": 16, "cols": 16, "mines": 40})
        self._difficulty_combo.addItem("Hard (16x30, 99 mines)", {"rows": 16, "cols": 30, "mines": 99})
        self._difficulty_combo.currentIndexChanged.connect(self._on_difficulty_changed)
        diff_layout.addWidget(self._difficulty_combo)

        # Speed control
        speed_group = QGroupBox("Solver Speed")
        speed_layout = QHBoxLayout(speed_group)

        self._speed_spin = QSpinBox()
        self._speed_spin.setRange(1, 1000)
        self._speed_spin.setValue(100)
        self._speed_spin.setSuffix(" ms")
        self._speed_spin.valueChanged.connect(self._on_speed_changed)
        speed_layout.addWidget(QLabel("Delay:"))
        speed_layout.addWidget(self._speed_spin)

        # Action buttons
        button_layout = QHBoxLayout()

        self._new_game_btn = QPushButton("New Game")
        self._new_game_btn.clicked.connect(self._on_new_game)

        self._start_btn = QPushButton("Start Solver")
        self._start_btn.clicked.connect(self._on_start_clicked)

        self._stop_btn = QPushButton("Stop Solver")
        self._stop_btn.clicked.connect(self._on_stop_clicked)
        self._stop_btn.setEnabled(False)

        button_layout.addWidget(self._new_game_btn)
        button_layout.addWidget(self._start_btn)
        button_layout.addWidget(self._stop_btn)

        # Status
        self._status_label = QLabel("Status: Ready")

        # Add all to main layout
        layout.addWidget(difficulty_group)
        layout.addWidget(speed_group)
        layout.addLayout(button_layout)
        layout.addWidget(self._status_label)
        layout.addStretch()

    def _on_difficulty_changed(self, index: int) -> None:
        """Handle difficulty selection change."""
        data = self._difficulty_combo.currentData()
        if data:
            self.difficulty_changed.emit(data["rows"], data["cols"], data["mines"])

    def _on_speed_changed(self, value: int) -> None:
        """Handle speed change."""
        self.speed_changed.emit(value / 1000.0)

    def _on_new_game(self) -> None:
        """Handle new game button click."""
        self.reset_clicked.emit()

    def current_board_config(self) -> tuple[int, int, int]:
        """Return the board configuration selected in the difficulty combo."""
        data = self._difficulty_combo.currentData()
        if not data:
            return 9, 9, 10
        return data["rows"], data["cols"], data["mines"]

    def _on_start_clicked(self) -> None:
        """Handle start solver button click."""
        self._solver_running = True
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)
        self._new_game_btn.setEnabled(False)
        self._difficulty_combo.setEnabled(False)
        self._status_label.setText("Status: Solver running...")
        self.start_solver_clicked.emit()

    def _on_stop_clicked(self) -> None:
        """Handle stop solver button click."""
        self._solver_running = False
        self._start_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._new_game_btn.setEnabled(True)
        self._difficulty_combo.setEnabled(True)
        self._status_label.setText("Status: Stopped")
        self.stop_solver_clicked.emit()

    def set_solver_finished(self, won: bool) -> None:
        """Update UI when solver finishes."""
        self._solver_running = False
        self._start_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._new_game_btn.setEnabled(True)
        self._difficulty_combo.setEnabled(True)
        if won:
            self._status_label.setText("Status: Solved! (Won)")
        else:
            self._status_label.setText("Status: Solved! (Hit mine)")

    def set_solver_running(self, running: bool) -> None:
        """Update UI when solver state changes."""
        if running:
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
            self._new_game_btn.setEnabled(False)
            self._difficulty_combo.setEnabled(False)
            self._status_label.setText("Status: Solver running...")
        else:
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)
            self._new_game_btn.setEnabled(True)
            self._difficulty_combo.setEnabled(True)
            self._status_label.setText("Status: Ready")
