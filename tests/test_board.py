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
    board = Board(3, 3, 1, seed=1)
    pos = Position(0, 0)

    board.flag(pos)
    assert board.state(pos) == CellState.FLAGGED

    board.flag(pos)
    assert board.state(pos) == CellState.HIDDEN


def test_toggle_flag_alias_matches_flag_toggle():
    board = Board(3, 3, 1, seed=1)
    pos = Position(0, 0)

    board.toggle_flag(pos)
    assert board.state(pos) == CellState.FLAGGED

    board.toggle_flag(pos)
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

    expected_number = str(board.number(pos))
    assert view[2][2] == expected_number


def test_reveal_zero_cell_auto_expands():
    board = Board(rows=3, cols=3, mines=1, seed=42)
    board.reveal(Position(0, 0))

    assert board.state(Position(0, 1)) == CellState.REVEALED
    assert board.state(Position(1, 0)) == CellState.REVEALED
    assert board.state(Position(1, 1)) == CellState.REVEALED


def test_reveal_mine_marks_loss_without_auto_expanding_neighbors():
    board = Board(rows=3, cols=3, mines=1)
    mine = Position(1, 1)
    board._mine_positions = {mine}
    board._compute_numbers()
    board._initialized = True

    board.reveal(mine)

    assert board.is_lost()
    assert board.state(mine) == CellState.REVEALED
    assert board.state(Position(0, 0)) == CellState.HIDDEN


def test_is_won_when_all_safe_cells_are_revealed():
    board = Board(rows=2, cols=2, mines=1)
    mine = Position(0, 0)
    board._mine_positions = {mine}
    board._compute_numbers()
    board._initialized = True

    board.reveal(Position(0, 1))
    board.reveal(Position(1, 0))
    board.reveal(Position(1, 1))

    assert board.is_won()


def test_is_won_when_all_mines_are_flagged():
    board = Board(rows=2, cols=2, mines=1)
    mine = Position(0, 0)
    board._mine_positions = {mine}
    board._compute_numbers()
    board._initialized = True

    board.flag(mine)

    assert board.is_won()
