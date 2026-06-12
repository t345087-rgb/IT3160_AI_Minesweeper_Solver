from minesweeper.board import Position
from minesweeper.evaluation import (
    evaluate_solver,
    format_evaluation_result,
    is_guess_action,
    play_one_game,
)
from minesweeper.solver import Action, ActionType


def test_play_one_game_returns_valid_result():
    won, steps, flags, guesses = play_one_game(
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
    assert steps >= 0
    assert flags >= 0
    assert guesses >= 0


def test_evaluate_solver_returns_summary_statistics():
    result = evaluate_solver(
        games=3,
        rows=9,
        cols=9,
        mines=10,
        max_steps=200,
        seeds=[1, 2, 3],
    )

    assert result.games == 3
    assert result.wins + result.losses == 3
    assert 0 <= result.win_rate <= 1
    assert result.average_steps >= 0
    assert result.average_flags >= 0
    assert result.total_guesses >= 0
    assert result.average_guesses == result.total_guesses / result.games
    assert result.average_runtime_seconds >= 0


def test_guess_action_is_a_reveal_not_known_to_be_safe():
    position = Position(0, 0)

    assert not is_guess_action(Action(ActionType.REVEAL, position, 0.0, "safe"))
    assert not is_guess_action(Action(ActionType.FLAG, position, 1.0, "mine"))
    assert is_guess_action(Action(ActionType.REVEAL, position, 0.25, "estimated"))
    assert is_guess_action(Action(ActionType.REVEAL, position, None, "no information"))


def test_evaluate_solver_rejects_non_positive_game_count():
    import pytest

    with pytest.raises(ValueError):
        evaluate_solver(games=0)

def test_format_evaluation_result_includes_guesses_and_runtime():
    result = evaluate_solver(
        games=1,
        rows=9,
        cols=9,
        mines=10,
        max_steps=200,
        seeds=[1],
    )

    output = format_evaluation_result(result)

    assert "Average guesses" in output
    assert "Average runtime" in output
    assert "seconds" in output
