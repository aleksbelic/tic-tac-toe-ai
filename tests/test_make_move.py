import re
import pytest
from src.tic_tac_toe_game import TicTacToeGame

@pytest.fixture
def game():
    return TicTacToeGame(train_mode = False)

def test_make_move(game):
    assert game.current_state == [game.EMPTY] * 9
    assert game.current_player == 'X'

    game.make_move(4)
    assert game.current_state[4] == 'X'
    assert game.current_state == [
        '-', '-', '-',
        '-', 'X', '-',
        '-', '-', '-'
    ]
    assert game.current_player == 'O'

    with pytest.raises(ValueError, match = re.escape('Invalid move: 4. Possible moves are: [0, 1, 2, 3, 5, 6, 7, 8]')):
        game.make_move(4)

    game.make_move(0)
    assert game.current_state[0] == 'O'
    assert game.current_state == [
        'O', '-', '-',
        '-', 'X', '-',
        '-', '-', '-'
    ]
    assert game.current_player == 'X'

    with pytest.raises(ValueError, match = re.escape('Invalid move: 0. Possible moves are: [1, 2, 3, 5, 6, 7, 8]')):
        game.make_move(0)