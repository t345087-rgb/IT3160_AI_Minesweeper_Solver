from minesweeper.board import Board, Position
from minesweeper.solver import ActionType, MinesweeperSolver


def test_solver_returns_an_action_on_new_board():
    board = Board(9, 9, 10, seed=2)
    solver = MinesweeperSolver(board)
    action = solver.choose_next_action()
    assert action is not None
    assert action.action_type in {ActionType.REVEAL, ActionType.FLAG}


def test_probability_estimates_after_first_reveal():
    board = Board(9, 9, 10, seed=3)
    board.reveal(Position(4, 4))
    solver = MinesweeperSolver(board)
    probs = solver.probability_estimates()
    assert isinstance(probs, dict)
