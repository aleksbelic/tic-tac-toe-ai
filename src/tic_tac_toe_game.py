import json
from pathlib import Path
from typing import Literal, Optional

class TicTacToeGame:
    _state: list[str]
    _current_player: Literal["X", "O"]
    _DATA_FILE = Path("./../data/q_table.json")
    
    def __init__(self) -> None:
        self._state = ["-"] * 9
        self._current_player = "X"

    def get_state(self) -> list[str]:
        return self._state.copy()

    def get_current_player(self) -> str:
        return self._current_player

    def print_state(self) -> None:
        print()
        for i in range(0, 9, 3):
            print(f" {self._state[i]} | {self._state[i + 1]} | {self._state[i + 2]} ")
            if i < 6:
                print("---+---+---")
        print()

    def reset(self) -> None:
        self._state = ["-"] * 9
        self._current_player = "X"

    def getWinner(self) -> Optional[str]:
        winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # columns
            (0, 4, 8), (2, 4, 6)             # diagonals
        )
        for i1, i2, i3 in winning_combinations:
            if self._state[i1] == self._state[i2] == self._state[i3] != "-":
                return self._state[i1]
        return None
    
    def isGameOver(self) -> bool:
        return (self.getWinner() is not None) or ("-" not in self._state) # Check for winner or draw



if __name__ == "__main__":
    game = TicTacToeGame()
    game.print_state()
    print("Winner:", game.getWinner())

