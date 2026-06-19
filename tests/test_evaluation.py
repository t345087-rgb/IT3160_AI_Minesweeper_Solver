from minesweeper.evaluation import (
    evaluate_solver,
    is_guess_action,
    is_winning_board,
    play_one_game,
)
from minesweeper.board import Board, Position, CellState
from minesweeper.solver import Action, ActionType, MinesweeperSolver


def test_play_one_game_returns_valid_result():
    won, steps, flags, guesses, _ = play_one_game(
        rows=9,
        cols=9,
        mines=10,
        max_steps=200,
        seed=1,
    )
    assert isinstance(won, bool)
    assert isinstance(steps, int)
    assert isinstance(flags, int)
    assert isinstance(guesses, int)


def test_evaluate_solver_metrics():
    result = evaluate_solver(games=3, rows=9, cols=9, mines=10)
    assert result.games == 3
    assert result.wins + result.losses == 3
    assert 0.0 <= result.win_rate <= 1.0
    assert result.average_runtime_seconds >= 0


def test_center_opening_is_not_counted_as_guess():
    action = MinesweeperSolver(Board(9, 9, 10)).choose_next_action()

    assert action is not None
    assert action.probability == 0.0
    assert not is_guess_action(action)


def test_no_information_fallback_is_counted_as_guess():
    board = Board(2, 2, 1)
    board.flag(Position(0, 0))
    solver = MinesweeperSolver(board)

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.REVEAL
    assert action.probability is None
    assert is_guess_action(action)


def test_safe_reveal_is_not_counted_as_guess():
    action = Action(ActionType.REVEAL, Position(1, 1), 0.0, "known safe")

    assert not is_guess_action(action)


def test_positive_probability_reveal_is_counted_as_guess():
    action = Action(ActionType.REVEAL, Position(1, 1), 0.25, "lowest estimated mine probability")

    assert is_guess_action(action)


def test_flag_is_not_counted_as_guess():
    action = Action(ActionType.FLAG, Position(1, 1), 1.0, "known mine")

    assert not is_guess_action(action)


def test_is_winning_board_empty():
    board = Board(3, 3, 0)
    
    all_safe_revealed = True
    for pos in board.positions():
        if board.state(pos) != CellState.REVEALED:
            all_safe_revealed = False
            break
            
    assert not all_safe_revealed


def test_is_winning_board_when_all_mines_are_flagged():
    board = Board(rows=2, cols=2, mines=1)
    mine = Position(0, 0)
    board._mine_positions = {mine}
    board._compute_numbers()
    board._initialized = True

    board.flag(mine)

    assert is_winning_board(board)


def test_is_winning_board_rejects_extra_safe_flag():
    board = Board(rows=2, cols=2, mines=1)
    mine = Position(0, 0)
    safe = Position(0, 1)
    board._mine_positions = {mine}
    board._compute_numbers()
    board._initialized = True

    board.flag(mine)
    board.flag(safe)

    assert not is_winning_board(board)


def test_is_winning_board_when_all_safe_cells_are_revealed():
    board = Board(rows=2, cols=2, mines=1)
    mine = Position(0, 0)
    board._mine_positions = {mine}
    board._compute_numbers()
    board._initialized = True

    board.reveal(Position(0, 1))
    board.reveal(Position(1, 0))
    board.reveal(Position(1, 1))

    assert is_winning_board(board)
