import pytest

from minesweeper.board import Board, Position
from minesweeper.solver import (
    ActionType,
    Constraint,
    MAX_ENUMERATION_VARIABLES,
    MinesweeperSolver,
    PROBABILITY_EPSILON,
    _enumerate_component_model_counts,
    _enumerate_component_probabilities,
    frontier_components,
)


def _configured_board(
    rows: int,
    cols: int,
    mines: set[Position],
    *,
    revealed: set[Position],
    flagged: set[Position] | None = None,
) -> Board:
    board = Board(rows, cols, len(mines))
    board._mine_positions = mines
    board._compute_numbers()
    board._initialized = True

    for position in revealed:
        board.reveal(position)
    for position in flagged or set():
        board.flag(position)
    return board


def test_frontier_components_connects_variables_in_same_constraint():
    first = Position(0, 0)
    second = Position(0, 1)

    components = frontier_components(
        [Constraint(frozenset({first, second}), 1)]
    )

    assert components == [[first, second]]


def test_frontier_components_connects_overlapping_constraints_transitively():
    a = Position(0, 0)
    b = Position(0, 1)
    c = Position(0, 2)

    components = frontier_components(
        [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
        ]
    )

    assert components == [[a, b, c]]


def test_frontier_components_separates_independent_constraint_groups():
    first_group = {Position(0, 0), Position(0, 1)}
    second_group = {Position(2, 2), Position(3, 2)}

    components = frontier_components(
        [
            Constraint(frozenset(second_group), 1),
            Constraint(frozenset(first_group), 1),
        ]
    )

    assert components == [
        sorted(first_group, key=lambda p: (p.row, p.col)),
        sorted(second_group, key=lambda p: (p.row, p.col)),
    ]


def test_frontier_components_includes_single_variable_component():
    position = Position(1, 2)

    components = frontier_components(
        [Constraint(frozenset({position}), 0)]
    )

    assert components == [[position]]


def test_frontier_components_has_stable_order():
    positions = [
        Position(2, 1),
        Position(0, 2),
        Position(2, 0),
        Position(0, 1),
    ]

    components = frontier_components(
        [
            Constraint(frozenset({positions[0], positions[2]}), 1),
            Constraint(frozenset({positions[1], positions[3]}), 1),
        ]
    )

    assert components == [
        [Position(0, 1), Position(0, 2)],
        [Position(2, 0), Position(2, 1)],
    ]


def test_frontier_components_returns_empty_list_without_frontier_variables():
    assert frontier_components([]) == []


def test_solver_returns_an_action_on_new_board():
    board = Board(9, 9, 10, seed=2)
    solver = MinesweeperSolver(board)
    action = solver.choose_next_action()
    assert action is not None
    assert action.action_type in {ActionType.REVEAL, ActionType.FLAG}


def test_probability_estimates_after_first_reveal():
    board = Board(9, 9, 10, seed=3)
    board.reveal(Position(4, 4))
    solver = MinesweeperSolver(board)
    probs = solver.probability_estimates()
    assert isinstance(probs, dict)


def test_deterministic_rule_reveals_safe_cells_when_remaining_mines_is_zero():
    mine = Position(0, 0)
    safe_cells = {Position(0, 1), Position(1, 0)}
    board = _configured_board(
        2,
        2,
        {mine},
        revealed={Position(1, 1)},
        flagged={mine},
    )

    actions = MinesweeperSolver(board).deterministic_actions()

    assert {(action.action_type, action.position) for action in actions} == {
        (ActionType.REVEAL, position) for position in safe_cells
    }
    assert all(action.probability == 0.0 for action in actions)


def test_deterministic_rule_flags_cells_when_all_hidden_cells_are_mines():
    mine = Position(0, 0)
    board = _configured_board(
        2,
        2,
        {mine},
        revealed={Position(0, 1), Position(1, 0), Position(1, 1)},
    )

    actions = MinesweeperSolver(board).deterministic_actions()

    assert {(action.action_type, action.position) for action in actions} == {
        (ActionType.FLAG, mine)
    }
    assert actions[0].probability == 1.0


def test_subset_inference_identifies_safe_cell():
    a = Position(0, 0)
    safe = Position(0, 2)
    flagged_mine = Position(1, 2)
    board = _configured_board(
        2,
        3,
        {a, flagged_mine},
        revealed={Position(1, 0), Position(1, 1)},
        flagged={flagged_mine},
    )

    actions = MinesweeperSolver(board).subset_inference_actions()

    assert any(
        action.action_type == ActionType.REVEAL
        and action.position == safe
        and action.probability == 0.0
        for action in actions
    )


def test_probability_estimates_are_between_zero_and_one():
    board = _configured_board(
        2,
        2,
        {Position(0, 0)},
        revealed={Position(1, 1)},
    )

    probabilities = MinesweeperSolver(board).probability_estimates()

    assert probabilities
    assert all(0.0 <= probability <= 1.0 for probability in probabilities.values())


def test_probability_estimates_enumerates_two_independent_small_components(monkeypatch):
    board = Board(2, 3, 1)
    first = {Position(0, 0), Position(0, 1)}
    certain_safe = Position(1, 2)
    unconstrained = {
        Position(0, 2),
        Position(1, 0),
        Position(1, 1),
    }
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset(first), 1),
            Constraint(frozenset({certain_safe}), 0),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {
        Position(0, 0): 0.5,
        Position(0, 1): 0.5,
        certain_safe: 0.0,
        **{position: 0.0 for position in unconstrained},
    }


def test_global_remaining_mines_filters_component_mine_count_combinations(
    monkeypatch,
):
    positions = [Position(0, col) for col in range(6)]
    a, b, c, d, e, f = positions
    solver = MinesweeperSolver(Board(1, 6, 2))
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
            Constraint(frozenset({d, e}), 1),
            Constraint(frozenset({e, f}), 1),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {
        a: 0.0,
        b: 1.0,
        c: 0.0,
        d: 0.0,
        e: 1.0,
        f: 0.0,
    }


def test_global_probabilities_weight_unconstrained_hidden_cells(monkeypatch):
    a, b, c, first_free, second_free = [
        Position(0, col) for col in range(5)
    ]
    solver = MinesweeperSolver(Board(1, 5, 2))
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == pytest.approx(
        {
            a: 1 / 3,
            b: 2 / 3,
            c: 1 / 3,
            first_free: 1 / 3,
            second_free: 1 / 3,
        }
    )


def test_global_probabilities_without_unconstrained_hidden_cells(monkeypatch):
    a, b, c = [Position(0, col) for col in range(3)]
    solver = MinesweeperSolver(Board(1, 3, 1))
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {a: 0.0, b: 1.0, c: 0.0}


def test_global_probabilities_when_remaining_mines_is_zero(monkeypatch):
    a, b, unconstrained = [Position(0, col) for col in range(3)]
    solver = MinesweeperSolver(Board(1, 3, 0))
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [Constraint(frozenset({a, b}), 0)],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {a: 0.0, b: 0.0, unconstrained: 0.0}


def test_no_global_valid_model_uses_component_wise_fallback(monkeypatch):
    a, b, _ = [Position(0, col) for col in range(3)]
    solver = MinesweeperSolver(Board(1, 3, 0))
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [Constraint(frozenset({a, b}), 1)],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {a: 0.5, b: 0.5}


def test_flagged_cells_are_subtracted_from_global_remaining_mines(monkeypatch):
    a, b, c, flagged = [Position(0, col) for col in range(4)]
    board = Board(1, 4, 2)
    board.flag(flagged)
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {a: 0.0, b: 1.0, c: 0.0}
    assert all(
        0.0 <= probability <= 1.0
        for probability in probabilities.values()
    )


def test_component_probabilities_with_overlapping_constraints():
    a, b, c, d, e = [Position(0, col) for col in range(5)]

    probabilities = _enumerate_component_probabilities(
        [a, b, c, d, e],
        [
            Constraint(frozenset({a, b, c}), 1),
            Constraint(frozenset({b, c, d}), 1),
            Constraint(frozenset({c, d, e}), 1),
        ],
    )

    assert probabilities is not None
    assert probabilities == pytest.approx(
        {
            a: 1 / 3,
            b: 1 / 3,
            c: 1 / 3,
            d: 1 / 3,
            e: 1 / 3,
        }
    )


def test_component_model_counts_groups_assignments_by_mine_count():
    a, b, c = [Position(0, col) for col in range(3)]

    model_counts = _enumerate_component_model_counts(
        [a, b, c],
        [Constraint(frozenset({a, b, c}), 1)],
    )

    assert model_counts is not None
    assert model_counts.ways_by_mine_count == {1: 3}
    assert model_counts.mine_hits_by_position_and_mine_count == {
        a: {1: 1},
        b: {1: 1},
        c: {1: 1},
    }


def test_component_model_counts_supports_multiple_total_mine_counts():
    a, b, c = [Position(0, col) for col in range(3)]

    model_counts = _enumerate_component_model_counts(
        [a, b, c],
        [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
        ],
    )

    assert model_counts is not None
    assert model_counts.ways_by_mine_count == {1: 1, 2: 1}
    assert model_counts.mine_hits_by_position_and_mine_count == {
        a: {2: 1},
        b: {1: 1},
        c: {2: 1},
    }


def test_component_model_counts_returns_none_when_unsatisfiable():
    a, b = [Position(0, col) for col in range(2)]
    variables = frozenset({a, b})

    model_counts = _enumerate_component_model_counts(
        [a, b],
        [
            Constraint(variables, 0),
            Constraint(variables, 1),
        ],
    )

    assert model_counts is None


def test_component_probability_wrapper_preserves_marginal_probabilities():
    a, b, c = [Position(0, col) for col in range(3)]

    probabilities = _enumerate_component_probabilities(
        [a, b, c],
        [
            Constraint(frozenset({a, b}), 1),
            Constraint(frozenset({b, c}), 1),
        ],
    )

    assert probabilities == {
        a: 0.5,
        b: 0.5,
        c: 0.5,
    }


def test_tightly_constrained_large_component_has_exact_probabilities():
    variables = [Position(row, col) for row in range(4) for col in range(5)]
    expected = {
        position: float(index % 2)
        for index, position in enumerate(variables)
    }
    constraints = [
        Constraint(frozenset(variables), len(variables) // 2),
        *[
            Constraint(frozenset({position}), int(expected[position]))
            for position in variables
        ],
    ]

    probabilities = _enumerate_component_probabilities(variables, constraints)

    assert probabilities == expected


def test_probability_estimates_enumerates_components_when_total_frontier_exceeds_limit(
    monkeypatch,
):
    board = Board(5, 5, 5)
    frontier = list(board.positions())[:MAX_ENUMERATION_VARIABLES + 1]
    constraints = [
        Constraint(frozenset({position}), index % 2)
        for index, position in enumerate(frontier)
    ]
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(solver, "frontier_constraints", lambda: constraints)

    probabilities = solver.probability_estimates()

    assert probabilities == {
        position: float(index % 2)
        for index, position in enumerate(frontier)
    }


def test_probability_estimates_mixes_enumeration_and_component_fallback(monkeypatch):
    board = Board(5, 5, 8)
    flagged = {Position(0, 0), Position(0, 1)}
    for position in flagged:
        board.flag(position)

    hidden = [position for position in board.positions() if position not in flagged]
    certain_mine = hidden[0]
    large_component = hidden[1:MAX_ENUMERATION_VARIABLES + 2]
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset({certain_mine}), 1),
            Constraint(frozenset(large_component), 6),
        ],
    )

    probabilities = solver.probability_estimates()

    expected_probability = (board.mine_count - len(flagged)) / (25 - len(flagged))
    assert probabilities[certain_mine] == 1.0
    assert all(
        probabilities[position] == expected_probability
        for position in large_component
    )


def test_invalid_component_uses_fallback_without_losing_valid_component(monkeypatch):
    board = Board(2, 2, 1)
    invalid = Position(0, 0)
    certain_mine = Position(1, 1)
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset({invalid}), 0),
            Constraint(frozenset({invalid}), 1),
            Constraint(frozenset({certain_mine}), 1),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities[invalid] == 0.25
    assert probabilities[certain_mine] == 1.0


def test_unsatisfiable_component_uses_probability_estimate_fallback(monkeypatch):
    board = Board(2, 3, 2)
    component = {Position(0, 0), Position(0, 1)}
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [
            Constraint(frozenset(component), 0),
            Constraint(frozenset(component), 1),
        ],
    )

    probabilities = solver.probability_estimates()

    assert probabilities == {
        position: pytest.approx(2 / 6)
        for position in component
    }


def test_probability_estimates_returns_empty_dictionary_without_constraints(monkeypatch):
    solver = MinesweeperSolver(Board(2, 2, 1))
    monkeypatch.setattr(solver, "frontier_constraints", lambda: [])

    assert solver.probability_estimates() == {}


def test_fallback_probabilities_are_clamped_between_zero_and_one(monkeypatch):
    board = Board(5, 5, 1)
    flagged = {Position(0, 0), Position(0, 1)}
    for position in flagged:
        board.flag(position)
    large_component = [
        position for position in board.positions() if position not in flagged
    ][:MAX_ENUMERATION_VARIABLES + 1]
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [Constraint(frozenset(large_component), 1)],
    )

    probabilities = solver.probability_estimates()

    assert probabilities
    assert all(0.0 <= probability <= 1.0 for probability in probabilities.values())
    assert set(probabilities.values()) == {0.0}


def test_choose_next_action_prefers_certain_action_before_guessing(monkeypatch):
    mine = Position(0, 0)
    safe_cells = {Position(0, 1), Position(1, 0)}
    board = _configured_board(
        2,
        2,
        {mine},
        revealed={Position(1, 1)},
        flagged={mine},
    )
    solver = MinesweeperSolver(board)

    def fail_if_guessing_is_attempted():
        raise AssertionError("probability fallback should not run when a certain action exists")

    monkeypatch.setattr(solver, "probability_estimates", fail_if_guessing_is_attempted)

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.REVEAL
    assert action.position in safe_cells
    assert action.probability == 0.0


def _solver_with_probability_estimates(monkeypatch, probabilities):
    solver = MinesweeperSolver(Board(1, 3, 1))
    monkeypatch.setattr(solver, "deterministic_actions", lambda: [])
    monkeypatch.setattr(solver, "subset_inference_actions", lambda: [])
    monkeypatch.setattr(
        solver,
        "probability_estimates",
        lambda: probabilities,
    )
    return solver


def test_choose_next_action_flags_probability_one(monkeypatch):
    mine = Position(0, 0)
    solver = _solver_with_probability_estimates(
        monkeypatch,
        {mine: 1.0, Position(0, 1): 0.4},
    )

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.FLAG
    assert action.position == mine
    assert action.probability == 1.0
    assert "certain mine" in action.reason


def test_choose_next_action_reveals_probability_zero(monkeypatch):
    safe = Position(0, 0)
    solver = _solver_with_probability_estimates(
        monkeypatch,
        {safe: 0.0, Position(0, 1): 0.4},
    )

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.REVEAL
    assert action.position == safe
    assert action.probability == 0.0
    assert "certainly safe" in action.reason


def test_choose_next_action_prefers_certain_flag_over_certain_reveal(
    monkeypatch,
):
    safe = Position(0, 0)
    mine = Position(0, 1)
    solver = _solver_with_probability_estimates(
        monkeypatch,
        {safe: 0.0, mine: 1.0},
    )

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.FLAG
    assert action.position == mine
    assert action.probability == 1.0


def test_choose_next_action_flags_probability_within_epsilon_of_one(
    monkeypatch,
):
    mine = Position(0, 0)
    probability = 1.0 - PROBABILITY_EPSILON / 2
    solver = _solver_with_probability_estimates(
        monkeypatch,
        {mine: probability, Position(0, 1): 0.4},
    )

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.FLAG
    assert action.position == mine
    assert action.probability == probability


def test_choose_next_action_reveals_probability_within_epsilon_of_zero(
    monkeypatch,
):
    safe = Position(0, 0)
    probability = PROBABILITY_EPSILON / 2
    solver = _solver_with_probability_estimates(
        monkeypatch,
        {safe: probability, Position(0, 1): 0.4},
    )

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.REVEAL
    assert action.position == safe
    assert action.probability == probability


def test_choose_next_action_reveals_lowest_risk_when_no_probability_is_certain(
    monkeypatch,
):
    lowest_risk = Position(0, 1)
    solver = _solver_with_probability_estimates(
        monkeypatch,
        {
            Position(0, 0): 0.6,
            lowest_risk: 0.2,
            Position(0, 2): 0.4,
        },
    )

    action = solver.choose_next_action()

    assert action is not None
    assert action.action_type == ActionType.REVEAL
    assert action.position == lowest_risk
    assert action.probability == 0.2
    assert action.reason == "lowest estimated mine probability"
