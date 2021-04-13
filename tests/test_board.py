from game.game_of_life import Board
import pytest


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def rows(board):
    return board.BOARD_SIZE[0]


@pytest.fixture
def cols(board):
    return board.BOARD_SIZE[1]


@pytest.fixture
def test_cell(board):
    return board.board[0][0]


def test_board_init(board, rows, cols):
    assert (
        board.level == 0
        and len(board.board) == rows
        and len(board.board[0]) == cols
    )


def test_initialize(board, rows, cols):
    board.initialize()
    assert (
        len(board.board) == rows
        and len(board.board[0]) == cols
        and str(board.board[rows - 1][cols - 1].mode) == "0"  # Check that random objects on the list are defined  as dead.
        and str(board.board[0][cols - 1].mode) == "0"         # Check that random objects on the list are defined  as dead.
        and str(board.board[rows - 1][0].mode) == "0"         # Check that random objects on the list are defined  as dead.
        and str(board.board[0][0].mode) == "0"                # Check that random objects on the list are defined  as dead.
    )


def test_valid_row(board, rows, cols):
    invalid_row = rows + 5
    valid_col = cols - 1
    assert board.is_valid_square(invalid_row, valid_col) is False


def test_valid_col(board, rows, cols):
    valid_row = rows - 1
    invalid_col = cols + 7
    assert board.is_valid_square(valid_row, invalid_col) is False


def test_get_square_returns_correct_cell(board, test_cell):
    assert test_cell == board.get_square(0, 0)


def test_get_square_returns_none_when_needed(board, rows, cols):
    invalid_row = rows + 5
    invalid_col = cols + 5
    assert board.get_square(invalid_row, invalid_col) is None


def test_changing_prev_cell_from_alive_to_dead(board, test_cell):
    test_cell.mode.kill()
    test_cell.previous_mode.revive()
    board.set_current_mode_as_prev(0, 0)
    assert str(test_cell.previous_mode) == "0"


def test_changing_prev_cell_from_dead_to_alive(board, test_cell):
    test_cell.mode.revive()
    test_cell.previous_mode.kill()
    board.set_current_mode_as_prev(0, 0)
    assert str(test_cell.previous_mode) == "1"


def test_change_of_game_level_related_to_cell(board, test_cell):
    test_cell.previous_mode.set_level(5)
    test_cell.mode.set_level(10)
    board.level = 15
    board.set_current_mode_as_prev(0, 0)
    assert test_cell.previous_mode.game_level == 10 and test_cell.mode.game_level == 15


def test_set_square_alive(board, test_cell):
    test_cell.mode.kill()
    board.set_square(0, 0, 'alive')
    assert str(test_cell.mode) == "1"


def test_set_square_dead(board, test_cell):
    test_cell.mode.revive()
    board.set_square(0, 0, 'dead')
    assert str(test_cell.mode) == "0"


def test_set_square_undefined_makes_no_change(board, test_cell):
    test_cell.mode.revive()
    board.set_square(0, 0, 'undefined_state')
    assert str(test_cell.mode) == "1"


def test_set_beginning(board, test_cell):
    test_cell.mode.kill()
    board.set_beginning([(0, 0)])
    assert str(test_cell.mode) == "1"


def test_set_beginning_fails(board, rows, cols, test_cell):
    test_cell.mode.kill()
    board.set_beginning([(rows + 1, cols + 1)])
    assert str(test_cell.mode) == "0"


def test_neighbors(board, test_cell):
    neighbor1 = board.board[0][1]
    neighbor2 = board.board[1][0]
    neighbor3 = board.board[1][1]
    random_level = 5
    board.level = random_level
    neighbor1.mode.set_level(random_level)
    neighbor1.previous_mode.kill()
    neighbor2.mode.set_level(random_level - 1)
    neighbor2.mode.revive()
    neighbor3.mode.set_level(random_level - 1)
    neighbor3.mode.revive()
    neighbors_list = board.get_neighbors(0, 0)
    neighbors_alive_num = board.get_alive_neighbors_num(0, 0)
    assert len(neighbors_list) == 3, neighbors_alive_num == 2


def test_game_run_changes_level(board):
    random_number = 5
    board.level = random_number
    board.game_round(3, (2, 3))
    assert board.level == random_number + 1


def test_game_born(board):
    board.initialize()
    board.set_square(0, 1, 'alive')
    board.set_square(1, 0, 'alive')
    board.set_square(1, 1, 'alive')
    board.game_round(3, (2, 3))
    assert str(board.board[0][0].mode) == "1"


def test_game_survive(board):
    board.initialize()
    board.set_square(0, 0, 'alive')
    board.set_square(0, 1, 'alive')
    board.set_square(1, 0, 'alive')
    board.game_round(3, (2, 3))
    assert str(board.board[0][0].mode) == "1"


def test_game_lonley(board):
    board.initialize()
    board.set_square(0, 0, 'alive')
    board.game_round(3, (2, 3))
    assert str(board.board[0][0].mode) == "0"


def test_game_crowded(board):
    board.initialize()
    board.set_square(0, 0, 'alive')
    board.set_square(0, 1, 'alive')
    board.set_square(0, 2, 'alive')
    board.set_square(1, 0, 'alive')
    board.set_square(1, 1, 'alive')
    board.set_square(1, 2, 'alive')
    board.game_round(3, (2, 3))
    assert str(board.board[0][1].mode) == "0"


def test_all_cells_dead(board):
    board.initialize()
    assert board.check_if_all_dead()


def test_all_cells_dead_fails(board):
    board.initialize()
    board.board[0][0].mode.revive()
    assert board.check_if_all_dead() is False


def test_nothing_changes(board):
    board.initialize()
    assert board.check_if_nothing_changes()


def test_nothing_changes_fails(board):
    board.board[0][0].previous_mode.revive()
    board.board[0][0].mode.kill()
    assert board.check_if_nothing_changes() is False


def test_board_str(board):
    assert str(board) is not None
