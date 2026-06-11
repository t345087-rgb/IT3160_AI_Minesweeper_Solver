from minesweeper.evaluation import evaluate_solver, format_evaluation_result, play_one_game


def test_play_one_game_returns_valid_result():
    won, steps, flags = play_one_game(
        rows=9,
        cols=9,
        mines=10,
        max_steps=200,
        seed=1,
    )

    assert isinstance(won, bool)
    assert isinstance(steps, int)
    assert isinstance(flags, int)
    assert steps >= 0
    assert flags >= 0


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
    assert result.average_runtime_seconds >= 0

def test_evaluate_solver_rejects_non_positive_game_count():
    import pytest

    with pytest.raises(ValueError):
        evaluate_solver(games=0)

def test_format_evaluation_result_includes_runtime():
    result = evaluate_solver(
        games=1,
        rows=9,
        cols=9,
        mines=10,
        max_steps=200,
        seeds=[1],
    )

    output = format_evaluation_result(result)

    assert "Average runtime" in output
    assert "seconds" in output