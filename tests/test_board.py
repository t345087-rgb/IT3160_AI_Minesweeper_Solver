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


def test_cannot_reveal_flagged_cell():
    import pytest

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

    assert view[2][2] != "#"