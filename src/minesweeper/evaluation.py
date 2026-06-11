"""Utilities for evaluating the Minesweeper solver over multiple games."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from minesweeper.board import Board, CellState
from minesweeper.solver import ActionType, MinesweeperSolver


@dataclass
class EvaluationResult:
    """Summary statistics for a batch of Minesweeper games."""

    games: int
    wins: int
    losses: int
    win_rate: float
    average_steps: float
    average_flags: float


def is_winning_board(board: Board) -> bool:
    """Return True if every non-mine cell has been revealed."""

    for pos in board.positions():
        if not board.has_mine(pos) and board.state(pos) != CellState.REVEALED:
            return False

    return True


def count_flags(board: Board) -> int:
    """Return the number of currently flagged cells."""

    return sum(1 for pos in board.positions() if board.state(pos) == CellState.FLAGGED)


def play_one_game(
    rows: int = 9,
    cols: int = 9,
    mines: int = 10,
    max_steps: int = 200,
    seed: int | None = None,
) -> tuple[bool, int, int]:
    """Play one complete game using the solver."""

    board = Board(rows=rows, cols=cols, mines=mines, seed=seed)
    solver = MinesweeperSolver(board)

    steps = 0

    for _ in range(max_steps):
        if is_winning_board(board):
            return True, steps, count_flags(board)

        action = solver.choose_next_action()

        if action is None:
            return is_winning_board(board), steps, count_flags(board)

        if action.action_type == ActionType.REVEAL:
            if board.has_mine(action.position):
                return False, steps + 1, count_flags(board)

            board.reveal(action.position)

        elif action.action_type == ActionType.FLAG:
            board.flag(action.position)

        steps += 1

    return is_winning_board(board), steps, count_flags(board)


def evaluate_solver(
    games: int = 100,
    rows: int = 9,
    cols: int = 9,
    mines: int = 10,
    max_steps: int = 200,
    seeds: Iterable[int] | None = None,
) -> EvaluationResult:
    """Evaluate the solver on many randomly generated boards."""

    if games <= 0:
        raise ValueError("games must be positive")

    seed_list = list(seeds) if seeds is not None else list(range(games))

    if len(seed_list) < games:
        raise ValueError("not enough seeds for the requested number of games")

    wins = 0
    total_steps = 0
    total_flags = 0

    for i in range(games):
        won, steps, flags = play_one_game(
            rows=rows,
            cols=cols,
            mines=mines,
            max_steps=max_steps,
            seed=seed_list[i],
        )

        if won:
            wins += 1

        total_steps += steps
        total_flags += flags

    losses = games - wins

    return EvaluationResult(
        games=games,
        wins=wins,
        losses=losses,
        win_rate=wins / games,
        average_steps=total_steps / games,
        average_flags=total_flags / games,
    )


def format_evaluation_result(result: EvaluationResult) -> str:
    """Format evaluation result for terminal output."""

    return (
        "Evaluation result\n"
        f"- Games: {result.games}\n"
        f"- Wins: {result.wins}\n"
        f"- Losses: {result.losses}\n"
        f"- Win rate: {result.win_rate:.2%}\n"
        f"- Average steps: {result.average_steps:.2f}\n"
        f"- Average flags: {result.average_flags:.2f}"
    )