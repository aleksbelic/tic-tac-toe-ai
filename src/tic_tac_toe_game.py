import json
from pathlib import Path
from typing import Literal, Optional

class TicTacToeGame:
    _state: list[str]
    _current_player: Literal["X", "O"]
    _data_file_path: Path
    
    def __init__(self, data_file_path: Optional[Path] = None) -> None:
        self._state = ["-"] * 9
        self._current_player = "X"
        self._data_file_path: Path = data_file_path or Path(__file__).parent.parent / "data" / "q_table.json"

    @property
    def get_state(self) -> list[str]:
        return self._state.copy()

    @property
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
        """Return 'X' or 'O' if there is a winner, else None."""
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

    def load_q_table(self) -> dict[str, dict[int, float]]:
        if not self._data_file_path.exists():
            return {}
        
        try:
            with open(self._data_file_path, "r") as data_file:
                raw = json.load(data_file)
            return {state: {int(a): v for a, v in data["actions"].items()} for state, data in raw.items()}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            return {}


if __name__ == "__main__":
    game = TicTacToeGame()
    game.print_state()
    print(f"Winner: {game.getWinner()}")

    x = game.load_q_table()
    print(x)