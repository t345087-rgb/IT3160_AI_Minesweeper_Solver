import pytest
from minesweeper.board import Board, CellState, Position


def test_board_initializes_without_mine_on_first_click():
    board = Board(9, 9, 10, seed=1)
    first = Position(4, 4)
    board.reveal(first)
    assert not board.has_mine(first)
    assert board.state(first) == CellState.REVEALED


def test_neighbors_center_has_eight_neighbors():
    board = Board(3, 3, 1, seed=1)
    assert len(board.neighbors(Position(1, 1))) == 8


def test_neighbors_corner_has_three_neighbors():
    board = Board(3, 3, 1, seed=1)
    assert len(board.neighbors(Position(0, 0))) == 3


def test_neighbors_edge_has_five_neighbors():
    """BỔ SUNG: Kiểm tra ô nằm ở cạnh biên (không phải góc) phải có đúng 5 ô lân cận."""
    board = Board(3, 3, 1, seed=1)
    assert len(board.neighbors(Position(0, 1))) == 5


def test_first_click_also_protects_neighbors():
    board = Board(9, 9, 10, seed=1)
    first = Position(4, 4)

    board.reveal(first)

    safe_positions = [first] + board.neighbors(first)
    for pos in safe_positions:
        assert not board.has_mine(pos)


def test_flag_changes_hidden_cell_to_flagged():
    board = Board(3, 3, 1, seed=1)
    pos = Position(0, 0)

    board.flag(pos)
    assert board.state(pos) == CellState.FLAGGED


def test_flag_and_unflag_toggle():
    """BỔ SUNG: Kiểm tra tính năng gỡ cờ (Unflag) khi gọi hàm flag lần thứ 2."""
    board = Board(3, 3, 1, seed=1)
    pos = Position(0, 0)

    board.flag(pos)
    assert board.state(pos) == CellState.FLAGGED

    board.flag(pos)  # Click lần 2 để gỡ cờ
    assert board.state(pos) == CellState.HIDDEN


def test_cannot_reveal_flagged_cell():
    board = Board(3, 3, 1, seed=1)
    pos = Position(0, 0)

    board.flag(pos)

    with pytest.raises(ValueError):
        board.reveal(pos)


def test_visible_view_hides_unrevealed_cells():
    board = Board(3, 3, 1, seed=1)
    view = board.visible_view()

    assert view == [
        ["#", "#", "#"],
        ["#", "#", "#"],
        ["#", "#", "#"],
    ]


def test_visible_view_shows_revealed_number():
    board = Board(5, 5, 1, seed=1)
    pos = Position(2, 2)

    board.reveal(pos)
    view = board.visible_view()

    # TỐI ƯU: Kiểm tra chính xác xem ô lật ra có hiển thị đúng chuỗi ký tự số mìn hay không
    expected_number = str(board.number(pos))
    assert view[2][2] == expected_number


def test_reveal_zero_cell_auto_expands():
    """BỔ SUNG: Kiểm tra xem thuật toán loang tự động (Flood Fill) có mở các ô xung quanh không."""
    # Tạo board 3x3, đặt mìn ở góc (2, 2). Ô (0, 0) chắc chắn là ô số 0
    board = Board(rows=3, cols=3, mines=1, seed=42)
    board.reveal(Position(0, 0))

    # Khối ô số 0 loang ra, các ô an toàn lân cận phải chuyển sang trạng thái REVEALED
    assert board.state(Position(0, 1)) == CellState.REVEALED
    assert board.state(Position(1, 0)) == CellState.REVEALED
    assert board.state(Position(1, 1)) == CellState.REVEALED