from minesweeper.board import Board, CellState, Position
from minesweeper.solver import ActionType, Constraint, MinesweeperSolver


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
        if board.in_bounds(position):
            board._states[position.row][position.col] = CellState.REVEALED
            
    for position in flagged or set():
        if board.in_bounds(position):
            board._states[position.row][position.col] = CellState.FLAGGED
            
    return board


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


def test_probability_fallback_uses_remaining_mines_over_hidden_cells(monkeypatch):
    board = Board(5, 5, 8)
    flagged = {Position(0, 0), Position(0, 1)}
    for position in flagged:
        board.flag(position)

    frontier = [position for position in board.positions() if position not in flagged][:21]
    solver = MinesweeperSolver(board)
    monkeypatch.setattr(
        solver,
        "frontier_constraints",
        lambda: [Constraint(frozenset(frontier), 6)],
    )

    probabilities = solver.probability_estimates()

    expected_probability = (board.mine_count - len(flagged)) / (25 - len(flagged))
    assert probabilities == {
        position: expected_probability for position in frontier
    }


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