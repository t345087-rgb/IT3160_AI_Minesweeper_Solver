"""Utilities for evaluating the Minesweeper solver over multiple games."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable

from minesweeper.board import Board, CellState
from minesweeper.solver import Action, ActionType, MinesweeperSolver


@dataclass
class EvaluationResult:
    """Summary statistics for a batch of Minesweeper games."""
    games: int
    wins: int
    losses: int
    win_rate: float
    average_steps: float
    average_flags: float
    total_guesses: int
    average_guesses: float
    average_runtime_seconds: float


def is_winning_board(board: Board) -> bool:
    """Return True if all non-mine cells are revealed OR all mines are correctly flagged."""
    if not board._initialized:
        return False

    all_safe_revealed = True
    all_mines_flagged = True
    
    for pos in board.positions():
        if board.has_mine(pos):
            if board.state(pos) != CellState.FLAGGED:
                all_mines_flagged = False
        else:
            if board.state(pos) != CellState.REVEALED:
                all_safe_revealed = False
                
    return all_safe_revealed or all_mines_flagged


def count_flags(board: Board) -> int:
    """Return the number of currently flagged cells."""
    return sum(1 for pos in board.positions() if board.state(pos) == CellState.FLAGGED)


def is_guess_action(action: Action) -> bool:
    """Return True when a reveal is not known to be safe."""
    return action.action_type == ActionType.REVEAL and action.probability != 0.0


def play_one_game(
    rows: int = 9,
    cols: int = 9,
    mines: int = 10,
    max_steps: int = 200,
    seed: int | None = None,
) -> tuple[bool, int, int, int, float]:
    """Play one complete game using the solver. Returns (won, steps, flags, guesses, inference_time)."""
    board = Board(rows=rows, cols=cols, mines=mines, seed=seed)
    solver = MinesweeperSolver(board)
    steps = 0
    guesses = 0
    pure_inference_time = 0.0

    for _ in range(max_steps):
        if is_winning_board(board):
            return True, steps, count_flags(board), guesses, pure_inference_time

        t0 = time.perf_counter()
        action = solver.choose_next_action()
        pure_inference_time += time.perf_counter() - t0

        if action is None:
            return is_winning_board(board), steps, count_flags(board), guesses, pure_inference_time

        steps += 1

        if is_guess_action(action):
            guesses += 1

        if action.action_type == ActionType.REVEAL:
            if board.has_mine(action.position):
                try:
                    board.reveal(action.position)
                except ValueError:
                    pass
                return False, steps, count_flags(board), guesses, pure_inference_time
            board.reveal(action.position)
        elif action.action_type == ActionType.FLAG:
            board.flag(action.position)

    return is_winning_board(board), steps, count_flags(board), guesses, pure_inference_time


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
    total_guesses = 0
    total_runtime_seconds = 0.0

    for i in range(games):
        won, steps, flags, guesses, inference_time = play_one_game(
            rows=rows,
            cols=cols,
            mines=mines,
            max_steps=max_steps,
            seed=seed_list[i],
        )

        total_runtime_seconds += inference_time

        if won:
            wins += 1
        total_steps += steps
        total_flags += flags
        total_guesses += guesses

    losses = games - wins
    return EvaluationResult(
        games=games,
        wins=wins,
        losses=losses,
        win_rate=wins / games,
        average_steps=total_steps / games,
        average_flags=total_flags / games,
        total_guesses=total_guesses,
        average_guesses=total_guesses / games,
        average_runtime_seconds=total_runtime_seconds / games,
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
        f"- Average flags: {result.average_flags:.2f}\n"
        f"- Average guesses: {result.average_guesses:.2f}\n"
        f"- Average runtime: {result.average_runtime_seconds:.6f} seconds"
    )