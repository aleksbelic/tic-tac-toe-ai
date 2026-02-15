import pytest
from src.tic_tac_toe_game import TicTacToeGame

@pytest.fixture
def game():
    return TicTacToeGame(train_mode = False)


def test_is_game_over_no_winner(game):
    game.current_state = [
        'X', 'O', 'X',
        'X', 'O', 'O',
        'O', 'X', 'X',
    ]
    assert game.is_game_over() == True


def test_is_game_over_winner(game):
    game.current_state = [
        'X', 'X', 'X',
        'O', 'O', '-',
        '-', '-', '-',
    ]
    assert game.is_game_over() == True


def test_is_game_over_not_over(game):
    game.current_state = [
        'X', 'O', 'X',
        'X', 'O', '-',
        '-', '-', '-',
    ]
    assert game.is_game_over() == False 


def test_is_game_over_winner_and_full(game):
    game.current_state = [
        'X', 'X', 'X',
        'O', 'O', 'X',
        'X', 'O', 'O',
    ]
    assert game.is_game_over() == True


def test_is_game_over_empty_board(game):
    game.current_state = [
        '-', '-', '-',
        '-', '-', '-',
        '-', '-', '-',
    ]
    assert game.is_game_over() == False


def test_is_game_over_one_move_left(game):
    game.current_state = [
        'X', 'O', 'X',
        'X', 'O', 'O',
        'O', 'X', '-',
    ]
    assert game.is_game_over() == False 
