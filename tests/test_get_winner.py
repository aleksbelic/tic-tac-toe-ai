import pytest
from src.tic_tac_toe_game import TicTacToeGame


@pytest.fixture
def game():
    return TicTacToeGame(train_mode = False)


def test_row_win_x(game):
    game.current_state = [
        'X', 'X', 'X',
        '-', '-', '-',
        '-', '-', '-',
    ]
    assert game.get_winner() == 'X'

    game.current_state = [
        '-', '-', '-',
        'X', 'X', 'X',
        '-', '-', '-',
    ]
    assert game.get_winner() == 'X'

    game.current_state = [
        '-', '-', '-',
        '-', '-', '-',
        'X', 'X', 'X',
    ]
    assert game.get_winner() == 'X'


def test_row_win_o(game):
    game.current_state = [
        'O', 'O', 'O',
        '-', '-', '-',
        '-', '-', '-',
    ]
    assert game.get_winner() == 'O'

    game.current_state = [
        '-', '-', '-',
        'O', 'O', 'O',
        '-', '-', '-',
    ]
    assert game.get_winner() == 'O'

    game.current_state = [
        '-', '-', '-',
        '-', '-', '-',
        'O', 'O', 'O',
    ]
    assert game.get_winner() == 'O'


def test_column_win_x(game):
    game.current_state = [
        'X', '-', '-',
        'X', '-', '-',
        'X', '-', '-',
    ]
    assert game.get_winner() == 'X'

    game.current_state = [
        '-', 'X', '-',
        '-', 'X', '-',
        '-', 'X', '-',
    ]
    assert game.get_winner() == 'X'

    game.current_state = [
        '-', '-', 'X',
        '-', '-', 'X',
        '-', '-', 'X',
    ]
    assert game.get_winner() == 'X'


def test_column_win_o(game):
    game.current_state = [
        'O', '-', '-',
        'O', '-', '-',
        'O', '-', '-',
    ]
    assert game.get_winner() == 'O'


    game.current_state = [
        '-', 'O', '-',
        '-', 'O', '-',
        '-', 'O', '-',
    ]
    assert game.get_winner() == 'O'

    game.current_state = [
        '-', '-', 'O',
        '-', '-', 'O',
        '-', '-', 'O',
    ]
    assert game.get_winner() == 'O'


def test_diagonal_win_x(game):
    game.current_state = [
        'X', '-', '-',
        '-', 'X', '-',
        '-', '-', 'X',
    ]
    assert game.get_winner() == 'X'

    game.current_state = [
        '-', '-', 'X',
        '-', 'X', '-',
        'X', '-', '-',
    ]
    assert game.get_winner() == 'X'


def test_diagonal_win_o(game):
    game.current_state = [
        'O', '-', '-',
        '-', 'O', '-',
        '-', '-', 'O',
    ]
    assert game.get_winner() == 'O'
    game.current_state = [
        '-', '-', 'O',
        '-', 'O', '-',
        'O', '-', '-',
    ]
    assert game.get_winner() == 'O'


def test_empty_board(game):
    game.current_state = [
        '-', '-', '-',
        '-', '-', '-',
        '-', '-', '-',
    ]
    assert game.get_winner() is None


def test_no_winner_in_progress(game):
    game.current_state = [
        'X', 'O', 'X',
        '-', 'O', '-',
        '-', '-', 'X',
    ]
    assert game.get_winner() is None


def test_draw(game):
    game.current_state = [
        'X', 'O', 'X',
        'X', 'O', 'O',
        'O', 'X', 'X',
    ]
    assert game.get_winner() is None
