from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Iterable

from minesweeper.board import Board, CellState, Position


class ActionType(str, Enum):
    REVEAL = "reveal"
    FLAG = "flag"


@dataclass(frozen=True)
class Action:
    action_type: ActionType
    position: Position
    probability: float | None = None
    reason: str = ""


@dataclass(frozen=True)
class Constraint:
    variables: frozenset[Position]
    mine_count: int


def frontier_components(constraints: Iterable[Constraint]) -> list[list[Position]]:
    """Return connected frontier-variable components in stable position order."""
    adjacency: dict[Position, set[Position]] = {}
    for constraint in constraints:
        variables = sorted(constraint.variables, key=lambda p: (p.row, p.col))
        for position in variables:
            adjacency.setdefault(position, set())
        for first, second in combinations(variables, 2):
            adjacency[first].add(second)
            adjacency[second].add(first)

    components: list[list[Position]] = []
    visited: set[Position] = set()
    for start in sorted(adjacency, key=lambda p: (p.row, p.col)):
        if start in visited:
            continue

        component: list[Position] = []
        stack = [start]
        visited.add(start)
        while stack:
            position = stack.pop()
            component.append(position)
            for neighbor in adjacency[position]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

        component.sort(key=lambda p: (p.row, p.col))
        components.append(component)

    components.sort(key=lambda component: (component[0].row, component[0].col))
    return components


class MinesweeperSolver:
    """Solver combining deterministic logic and probability fallback."""

    def __init__(self, board: Board):
        self.board = board

    def frontier_constraints(self) -> list[Constraint]:
        constraints: list[Constraint] = []
        for pos in self.board.positions():
            if self.board.state(pos) != CellState.REVEALED:
                continue
            hidden: set[Position] = set()
            flagged = 0
            for n in self.board.neighbors(pos):
                if self.board.state(n) == CellState.FLAGGED:
                    flagged += 1
                elif self.board.state(n) == CellState.HIDDEN:
                    hidden.add(n)
            remaining = self.board.number(pos) - flagged
            if hidden:
                constraints.append(Constraint(frozenset(hidden), remaining))
        return constraints

    def deterministic_actions(self) -> list[Action]:
        """Basic Minesweeper rules.

        Rule 1: if remaining mines = 0, every hidden neighbor is safe.
        Rule 2: if remaining mines = number of hidden neighbors, every hidden neighbor is a mine.
        """
        actions: dict[Position, Action] = {}
        for con in self.frontier_constraints():
            if con.mine_count == 0:
                for p in con.variables:
                    actions[p] = Action(ActionType.REVEAL, p, 0.0, "all remaining neighbors are safe")
            elif con.mine_count == len(con.variables):
                for p in con.variables:
                    actions[p] = Action(ActionType.FLAG, p, 1.0, "all remaining neighbors are mines")
        return list(actions.values())

    def subset_inference_actions(self) -> list[Action]:
        """Infer new constraints using subset rule: A⊆B => B-A has count count(B)-count(A)."""
        base = self.frontier_constraints()
        inferred: list[Constraint] = []
        for a in base:
            for b in base:
                if a == b:
                    continue
                if a.variables.issubset(b.variables):
                    diff = b.variables - a.variables
                    count = b.mine_count - a.mine_count
                    if diff:
                        inferred.append(Constraint(frozenset(diff), count))

        actions: dict[Position, Action] = {}
        for con in inferred:
            if con.mine_count == 0:
                for p in con.variables:
                    actions[p] = Action(ActionType.REVEAL, p, 0.0, "subset inference: safe")
            elif con.mine_count == len(con.variables):
                for p in con.variables:
                    actions[p] = Action(ActionType.FLAG, p, 1.0, "subset inference: mine")
        return list(actions.values())

    def probability_estimates(self) -> dict[Position, float]:
        """Estimate mine probability on frontier by enumerating valid assignments.

        This is intentionally simple and suitable for beginner/intermediate boards.
        Large frontier components can be optimized later by splitting into components
        or using Gaussian elimination / CSP search.
        """
        constraints = self.frontier_constraints()
        variables = sorted({p for con in constraints for p in con.variables}, key=lambda p: (p.row, p.col))
        if not variables:
            return {}
        if len(variables) > 20:
            flagged_cells = sum(
                self.board.state(p) == CellState.FLAGGED for p in self.board.positions()
            )
            hidden_cells = sum(
                self.board.state(p) == CellState.HIDDEN for p in self.board.positions()
            )
            remaining_mines = self.board.mine_count - flagged_cells
            base_probability = remaining_mines / hidden_cells if hidden_cells > 0 else 0.0
            base_probability = max(0.0, min(1.0, base_probability))
            return {p: base_probability for p in variables}

        valid_count = 0
        mine_hits = {p: 0 for p in variables}
        index = {p: i for i, p in enumerate(variables)}

        for mask in range(1 << len(variables)):
            assignment = {p for i, p in enumerate(variables) if (mask >> i) & 1}
            ok = True
            for con in constraints:
                if sum(p in assignment for p in con.variables) != con.mine_count:
                    ok = False
                    break
            if not ok:
                continue
            valid_count += 1
            for p in assignment:
                mine_hits[p] += 1

        if valid_count == 0:
            return {p: 0.5 for p in variables}
        return {p: mine_hits[p] / valid_count for p in variables}

    def choose_next_action(self) -> Action | None:
        for strategy in (self.deterministic_actions, self.subset_inference_actions):
            actions = strategy()
            if actions:
                flags = [a for a in actions if a.action_type == ActionType.FLAG]
                return flags[0] if flags else actions[0]

        probs = self.probability_estimates()
        if probs:
            safest = min(probs.items(), key=lambda item: item[1])
            return Action(ActionType.REVEAL, safest[0], safest[1], "lowest estimated mine probability")

        hidden = [p for p in self.board.positions() if self.board.state(p) == CellState.HIDDEN]
        if hidden:
            return Action(ActionType.REVEAL, hidden[0], None, "no information; first hidden cell fallback")
        return None

    def apply_action(self, action: Action) -> None:
        if action.action_type == ActionType.FLAG:
            self.board.flag(action.position)
        else:
            self.board.reveal(action.position)
