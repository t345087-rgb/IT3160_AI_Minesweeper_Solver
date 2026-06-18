"""Board view widget for rendering the Minesweeper grid."""

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QMouseEvent
from PySide6.QtWidgets import QWidget

from minesweeper.board import Board, CellState, Position


# Cell colors
HIDDEN_COLOR = QColor("#cccccc")
REVEALED_COLOR = QColor("#ffffff")
FLAG_COLOR = QColor("#ff6666")
MINE_COLOR = QColor("#333333")

# Number colors
NUMBER_COLORS = {
    1: QColor("#0000ff"),  # Blue
    2: QColor("#008000"),  # Green
    3: QColor("#ff0000"),  # Red
    4: QColor("#000080"),  # Dark blue
    5: QColor("#800000"),  # Maroon
    6: QColor("#008080"),  # Teal
    7: QColor("#000000"),  # Black
    8: QColor("#808080"),  # Gray
}

CELL_SIZE = 30
GRID_LINE_WIDTH = 1


class BoardView(QWidget):
    """Widget for displaying the Minesweeper board."""

    # Signals for user interactions
    cell_left_clicked = Signal(Position)  # Left click on hidden cell (reveal)
    cell_right_clicked = Signal(Position)  # Right click (toggle flag)

    def __init__(self, board: Board | None = None, parent=None) -> None:
        """Initialize the board view."""
        super().__init__(parent)
        self._board = board
        self.setMinimumSize(300, 300)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

    def set_board(self, board: Board) -> None:
        """Set the board to display."""
        self._board = board
        self.update()

    def minimumSizeHint(self) -> QSize:
        """Return the minimum size hint based on board dimensions."""
        if self._board is None:
            return QSize(300, 300)
        rows = self._board.rows
        cols = self._board.cols
        width = cols * CELL_SIZE + GRID_LINE_WIDTH * 2
        height = rows * CELL_SIZE + GRID_LINE_WIDTH * 2
        return QSize(width, height)

    def paintEvent(self, event) -> None:
        """Paint the board."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._board is None:
            return

        rows = self._board.rows
        cols = self._board.cols

        for row in range(rows):
            for col in range(cols):
                pos = Position(row, col)
                x = col * CELL_SIZE + GRID_LINE_WIDTH
                y = row * CELL_SIZE + GRID_LINE_WIDTH
                cell_rect = QColor(0, 0, 0, 0)
                painter.fillRect(
                    x, y, CELL_SIZE, CELL_SIZE, self._get_cell_color(pos)
                )

                # Draw grid border
                painter.setPen(QPen(Qt.GlobalColor.black, GRID_LINE_WIDTH))
                painter.drawRect(x, y, CELL_SIZE, CELL_SIZE)

                # Draw cell content
                self._draw_cell_content(painter, pos, x, y)

    def _get_cell_color(self, pos: Position) -> QColor:
        """Get the background color for a cell."""
        if self._board is None:
            return HIDDEN_COLOR

        state = self._board.state(pos)
        if state == CellState.REVEALED:
            return REVEALED_COLOR
        elif state == CellState.FLAGGED:
            return FLAG_COLOR
        else:
            return HIDDEN_COLOR

    def _draw_cell_content(self, painter: QPainter, pos: Position, x: int, y: int) -> None:
        """Draw the content of a cell."""
        if self._board is None:
            return

        state = self._board.state(pos)
        if state == CellState.REVEALED:
            if self._board.has_mine(pos):
                # Draw mine
                painter.fillRect(x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10, MINE_COLOR)
            else:
                # Draw number
                number = self._board.number(pos)
                if number > 0:
                    font = QFont("Arial", 14, QFont.Weight.Bold)
                    painter.setFont(font)
                    painter.setPen(NUMBER_COLORS.get(number, Qt.GlobalColor.black))
                    painter.drawText(
                        x, y, CELL_SIZE, CELL_SIZE,
                        Qt.AlignmentFlag.AlignCenter,
                        str(number)
                    )
        elif state == CellState.FLAGGED:
            # Draw flag indicator (simple circle)
            painter.setPen(Qt.GlobalColor.black)
            painter.setBrush(Qt.GlobalColor.red)
            center_x = x + CELL_SIZE // 2
            center_y = y + CELL_SIZE // 2
            painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)

    def _get_position_from_coords(self, x: int, y: int) -> Position | None:
        """Convert pixel coordinates to board position."""
        col = int(x) // CELL_SIZE
        row = int(y) // CELL_SIZE
        if self._board and 0 <= row < self._board.rows and 0 <= col < self._board.cols:
            return Position(row, col)
        return None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events for cell interactions."""
        if self._board is None:
            return

        pos = self._get_position_from_coords(event.position().x(), event.position().y())
        if pos is None:
            return

        # Ignore clicks on revealed cells
        if self._board.state(pos) == CellState.REVEALED:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.cell_left_clicked.emit(pos)
        elif event.button() == Qt.MouseButton.RightButton:
            self.cell_right_clicked.emit(pos)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Handle double-click for chord reveal (reveal neighbors if flag count matches)."""
        pass  # TODO: Implement chord reveal
