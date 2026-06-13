from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Iterable

from minesweeper.board import Board, CellState, Position


MAX_ENUMERATION_VARIABLES = 20


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


def _constraints_for_component(
    component: list[Position],
    constraints: Iterable[Constraint],
) -> list[Constraint]:
    component_variables = set(component)
    related = [
        constraint
        for constraint in constraints
        if constraint.variables & component_variables
    ]
    for constraint in related:
        if not constraint.variables.issubset(component_variables):
            raise RuntimeError(
                "frontier constraint spans multiple connected components"
            )
    return related


def _enumerate_component_probabilities(
    variables: list[Position],
    constraints: Iterable[Constraint],
) -> dict[Position, float] | None:
    component_constraints = list(constraints)
    variable_set = set(variables)
    constraint_variables = [
        constraint.variables & variable_set
        for constraint in component_constraints
    ]
    constraints_by_variable: dict[Position, list[int]] = {
        position: [] for position in variables
    }
    for constraint_index, positions in enumerate(constraint_variables):
        for position in positions:
            constraints_by_variable[position].append(constraint_index)

    ordered_variables = sorted(
        variables,
        key=lambda position: (
            -len(constraints_by_variable[position]),
            position.row,
            position.col,
        ),
    )
    assigned_mines = [0] * len(component_constraints)
    unassigned_variables = [
        len(positions) for positions in constraint_variables
    ]
    valid_count = 0
    mine_hits = {position: 0 for position in variables}
    assignment: set[Position] = set()

    def backtrack(variable_index: int) -> None:
        nonlocal valid_count

        if variable_index == len(ordered_variables):
            if all(
                assigned_mines[index] == constraint.mine_count
                for index, constraint in enumerate(component_constraints)
            ):
                valid_count += 1
                for position in assignment:
                    mine_hits[position] += 1
            return

        position = ordered_variables[variable_index]
        related_constraints = constraints_by_variable[position]
        for is_mine in (0, 1):
            branch_is_valid = True
            for constraint_index in related_constraints:
                assigned_mines[constraint_index] += is_mine
                unassigned_variables[constraint_index] -= 1
                mine_count = component_constraints[constraint_index].mine_count
                if (
                    assigned_mines[constraint_index] > mine_count
                    or assigned_mines[constraint_index]
                    + unassigned_variables[constraint_index]
                    < mine_count
                ):
                    branch_is_valid = False

            if branch_is_valid:
                if is_mine:
                    assignment.add(position)
                backtrack(variable_index + 1)
                if is_mine:
                    assignment.remove(position)

            for constraint_index in related_constraints:
                assigned_mines[constraint_index] -= is_mine
                unassigned_variables[constraint_index] += 1

    backtrack(0)

    if valid_count == 0:
        return None
    return {
        position: mine_hits[position] / valid_count
        for position in variables
    }


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
        """Estimate frontier mine probabilities component by component."""
        constraints = self.frontier_constraints()
        components = frontier_components(constraints)
        if not components:
            return {}

        fallback_probability = self._fallback_probability()
        probabilities: dict[Position, float] = {}
        for component in components:
            component_constraints = _constraints_for_component(
                component,
                constraints,
            )
            component_probabilities = None
            if len(component) <= MAX_ENUMERATION_VARIABLES:
                component_probabilities = _enumerate_component_probabilities(
                    component,
                    component_constraints,
                )

            if component_probabilities is None:
                component_probabilities = {
                    position: fallback_probability for position in component
                }
            probabilities.update(component_probabilities)

        return probabilities

    def _fallback_probability(self) -> float:
        flagged_cells = sum(
            self.board.state(position) == CellState.FLAGGED
            for position in self.board.positions()
        )
        hidden_unflagged_cells = sum(
            self.board.state(position) == CellState.HIDDEN
            for position in self.board.positions()
        )
        remaining_mines = self.board.mine_count - flagged_cells
        probability = (
            remaining_mines / hidden_unflagged_cells
            if hidden_unflagged_cells > 0
            else 0.0
        )
        return max(0.0, min(1.0, probability))

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
