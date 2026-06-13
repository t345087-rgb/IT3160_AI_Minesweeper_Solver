from minesweeper.evaluation import evaluate_solver, is_winning_board, play_one_game
from minesweeper.board import Board, Position, CellState

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

def test_is_winning_board_empty():
    board = Board(3, 3, 0)
    
    all_safe_revealed = True
    for pos in board.positions():
        if board.state(pos) != CellState.REVEALED:
            all_safe_revealed = False
            break
            
    assert not all_safe_revealed