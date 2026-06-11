from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from minesweeper.board import Board
from minesweeper.solver import ActionType, MinesweeperSolver

console = Console()


def render(board: Board) -> None:
    table = Table(show_header=False, box=None)
    for _ in range(board.cols):
        table.add_column(justify="center")
    for row in board.visible_view():
        table.add_row(*row)
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AI Minesweeper Solver demo")
    parser.add_argument("--rows", type=int, default=9)
    parser.add_argument("--cols", type=int, default=9)
    parser.add_argument("--mines", type=int, default=10)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    board = Board(args.rows, args.cols, args.mines, seed=args.seed)
    solver = MinesweeperSolver(board)

    for step in range(args.steps):
        action = solver.choose_next_action()
        if action is None:
            console.print("No more actions.")
            break
        solver.apply_action(action)
        console.print(f"Step {step + 1}: {action.action_type.value} {action.position} | {action.reason} | p={action.probability}")
        render(board)


if __name__ == "__main__":
    main()
