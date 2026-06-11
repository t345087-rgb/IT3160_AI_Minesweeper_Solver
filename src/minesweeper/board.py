from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from random import sample
from typing import Iterable


class CellState(str, Enum):
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"


@dataclass(frozen=True)
class Position:
    row: int
    col: int


class Board:
    """Minesweeper board used for simulation and testing the AI solver."""

    def __init__(self, rows: int, cols: int, mines: int, seed: int | None = None):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        if mines < 0 or mines >= rows * cols:
            raise ValueError("mines must be between 0 and rows*cols - 1")

        self.rows = rows
        self.cols = cols
        self.mine_count = mines
        self._mine_positions: set[Position] = set()
        self._states = [[CellState.HIDDEN for _ in range(cols)] for _ in range(rows)]
        self._numbers = [[0 for _ in range(cols)] for _ in range(rows)]
        self._seed = seed
        self._initialized = False

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def positions(self) -> Iterable[Position]:
        for r in range(self.rows):
            for c in range(self.cols):
                yield Position(r, c)

    def neighbors(self, pos: Position) -> list[Position]:
        result: list[Position] = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nxt = Position(pos.row + dr, pos.col + dc)
                if self.in_bounds(nxt):
                    result.append(nxt)
        return result

    def initialize(self, first_click: Position | None = None) -> None:
        """Place mines. The optional first click is guaranteed safe."""
        import random

        rng = random.Random(self._seed)
        candidates = list(self.positions())
        if first_click is not None:
            safe = {first_click, *self.neighbors(first_click)}
            candidates = [p for p in candidates if p not in safe]
        self._mine_positions = set(rng.sample(candidates, self.mine_count))
        self._compute_numbers()
        self._initialized = True

    def _compute_numbers(self) -> None:
        for pos in self.positions():
            self._numbers[pos.row][pos.col] = sum(n in self._mine_positions for n in self.neighbors(pos))

    def reveal(self, pos: Position) -> int:
        if not self.in_bounds(pos):
            raise ValueError("position out of bounds")
        if not self._initialized:
            self.initialize(first_click=pos)
        if self._states[pos.row][pos.col] == CellState.FLAGGED:
            raise ValueError("cannot reveal a flagged cell")
        self._states[pos.row][pos.col] = CellState.REVEALED
        return self._numbers[pos.row][pos.col]

    def flag(self, pos: Position) -> None:
        if not self.in_bounds(pos):
            raise ValueError("position out of bounds")
        if self._states[pos.row][pos.col] == CellState.REVEALED:
            raise ValueError("cannot flag a revealed cell")
        self._states[pos.row][pos.col] = CellState.FLAGGED

    def state(self, pos: Position) -> CellState:
        return self._states[pos.row][pos.col]

    def number(self, pos: Position) -> int:
        return self._numbers[pos.row][pos.col]

    def has_mine(self, pos: Position) -> bool:
        return pos in self._mine_positions

    def visible_view(self) -> list[list[str]]:
        view: list[list[str]] = []
        for pos in self.positions():
            pass
        for r in range(self.rows):
            row: list[str] = []
            for c in range(self.cols):
                pos = Position(r, c)
                st = self.state(pos)
                if st == CellState.HIDDEN:
                    row.append("#")
                elif st == CellState.FLAGGED:
                    row.append("F")
                else:
                    row.append(str(self.number(pos)))
            view.append(row)
        return view
