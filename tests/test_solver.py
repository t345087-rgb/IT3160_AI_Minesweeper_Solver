from minesweeper.board import Board, Position
from minesweeper.solver import (
    ActionType,
    Constraint,
    MAX_ENUMERATION_VARIABLES,
    MinesweeperSolver,
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
    }


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
