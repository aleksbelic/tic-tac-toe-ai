import re
import pytest
from src.tic_tac_toe_game import TicTacToeGame

@pytest.fixture
def game():
    return TicTacToeGame(train_mode = False)

def test_make_random_move_begin_game(game):
    assert game.current_state.count(game.EMPTY) == 9
    assert game.current_state.count('X') == 0
    assert game.current_state.count('O') == 0
    assert game.current_player == 'X'

    game.make_random_move()
    assert game.current_state.count(game.EMPTY) == 8
    assert game.current_state.count('X') == 1
    assert game.current_state.count('O') == 0
    assert game.current_player == 'O'

    game.make_random_move()
    assert game.current_state.count(game.EMPTY) == 7
    assert game.current_state.count('X') == 1
    assert game.current_state.count('O') == 1
    assert game.current_player == 'X'

    assert game.get_winner() == None
    assert game.is_game_over() == False

def test_make_random_move_end_game(game):
    game.current_state = [
        'X', 'X', 'O',
        'O', 'X', 'X',
        '-', 'O', 'O'
    ]
    game.current_player = 'X'

    game.make_random_move()
    assert game.current_state == [
        'X', 'X', 'O',
        'O', 'X', 'X',
        'X', 'O', 'O'
    ]
    assert game.get_winner() == None
    assert game.is_game_over() == True