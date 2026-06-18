from __future__ import annotations

import argparse
import builtins

try:
    from rich.console import Console
    from rich.table import Table
except ModuleNotFoundError:
    Table = None

    class Console:  # type: ignore[no-redef]
        """Tiny fallback so the CLI demo still runs without rich installed."""

        def print(self, message: object = "") -> None:
            builtins.print(message)

from minesweeper.board import Board
from minesweeper.evaluation import evaluate_solver, format_evaluation_result
from minesweeper.solver import MinesweeperSolver

console = Console()


DIFFICULTY_PRESETS = {
    "beginner": (9, 9, 10),
    "intermediate": (16, 16, 40),
    "expert": (16, 30, 99),
}


def resolve_board_config(args: argparse.Namespace) -> tuple[int, int, int]:
    """Return rows, cols and mines based on the selected difficulty."""
    if args.difficulty == "custom":
        return args.rows, args.cols, args.mines

    return DIFFICULTY_PRESETS[args.difficulty]


def render(board: Board) -> None:
    if Table is None:
        for row in board.visible_view():
            console.print(" ".join(row))
        return

    table = Table(show_header=False, box=None)
    for _ in range(board.cols):
        table.add_column(justify="center")
    for row in board.visible_view():
        table.add_row(*row)
    console.print(table)


def run_demo(args: argparse.Namespace) -> None:
    rows, cols, mines = resolve_board_config(args)

    board = Board(rows, cols, mines, seed=args.seed)
    solver = MinesweeperSolver(board)

    for step in range(args.steps):
        action = solver.choose_next_action()
        if action is None:
            console.print("No more actions.")
            break

        solver.apply_action(action)
        console.print(
            f"Step {step + 1}: {action.action_type.value} {action.position} "
            f"| {action.reason} | p={action.probability}"
        )
        render(board)


def run_evaluation(args: argparse.Namespace) -> None:
    rows, cols, mines = resolve_board_config(args)

    result = evaluate_solver(
        games=args.games,
        rows=rows,
        cols=cols,
        mines=mines,
        max_steps=args.max_steps,
    )
    console.print(format_evaluation_result(result))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AI Minesweeper Solver demo")
    parser.add_argument("--rows", type=int, default=9)
    parser.add_argument("--cols", type=int, default=9)
    parser.add_argument("--mines", type=int, default=10)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--seed", type=int, default=7)

    parser.add_argument(
        "--difficulty",
        choices=["beginner", "intermediate", "expert", "custom"],
        default="custom",
        help=(
            "Board difficulty preset. Use custom to manually set "
            "--rows, --cols and --mines."
        ),
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run evaluation over multiple games instead of a single demo game.",
    )
    parser.add_argument(
        "--games",
        type=int,
        default=100,
        help="Number of games used in evaluation mode.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=200,
        help="Maximum steps per game in evaluation mode.",
    )

    args = parser.parse_args()

    if args.evaluate:
        run_evaluation(args)
    else:
        run_demo(args)


if __name__ == "__main__":
    main()
