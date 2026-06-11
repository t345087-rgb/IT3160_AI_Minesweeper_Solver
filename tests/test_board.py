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
