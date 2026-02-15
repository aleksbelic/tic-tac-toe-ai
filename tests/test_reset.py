import pytest
from src.tic_tac_toe_game import TicTacToeGame

@pytest.fixture
def game():
    return TicTacToeGame(train_mode = False)


def test_reset(game):
    game.make_random_move()
    game.make_random_move()
    game.make_random_move()

    game.reset()
    assert game.history == []
    assert game.current_state == [game.EMPTY] * 9
    assert game.current_player == 'X'
    assert game.train_mode == False
