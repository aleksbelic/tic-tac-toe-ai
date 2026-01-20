import json
from pathlib import Path
from typing import Literal, Optional
import random

class TicTacToeGame:
    _state: list[str]
    _current_player: Literal['X', 'O']
    _data_file_path: Path

    @property
    def state(self) -> list[str]:
        return self._state
    
    @state.setter
    def state(self, new_state: list[str]) -> None:
        self._state = new_state

    @property
    def current_player(self) -> str:
        return self._current_player

    @current_player.setter
    def current_player(self, player: Literal['X', 'O']) -> None:
        self._current_player = player
    
    def __init__(self, data_file_path: Optional[Path] = None) -> None:
        self.state = ["-"] * 9
        self.current_player = "X"
        self.data_file_path: Path = data_file_path or Path(__file__).parent.parent / 'data' / 'q_table.json'

    def print_state(self) -> None:
        print()
        for i in range(0, 9, 3):
            print(f" {self.state[i]} | {self.state[i + 1]} | {self.state[i + 2]} ")
            if i < 6:
                print("---+---+---")
        print()

    def reset(self) -> None:
        self.state = ["-"] * 9
        self.current_player = "X"

    def getWinner(self) -> Optional[str]:
        """Return 'X' or 'O' if there is a winner, else None."""
        winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # columns
            (0, 4, 8), (2, 4, 6)             # diagonals
        )
        for i1, i2, i3 in winning_combinations:
            if self.state[i1] == self.state[i2] == self.state[i3] != "-":
                return self.state[i1]
        return None
    
    def isGameOver(self) -> bool:
        return (self.getWinner() is not None) or ("-" not in self.state) # Check for winner or draw

    def load_q_table(self) -> dict[str, dict[int, float]]:
        if not self.data_file_path.exists():
            return {}
        
        try:
            with open(self.data_file_path, "r") as data_file:
                raw = json.load(data_file)
            return {state: {int(action): value for action, value in actions_values.items()} for state, actions_values in raw.items()}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            return {}

    def get_possible_actions(self) -> list[int]:
        return [i for i, cell in enumerate(self.state) if cell == "-"]
    
    def make_random_action(self) -> None:
        possible_actions = self.get_possible_actions()
        if len(possible_actions) > 0:
            action = random.choice(possible_actions)
            self.state[action] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"

    def get_state_key(self) -> str:
        return f"{''.join(self.state)}|{self.current_player}"

    def save_q_table(self, q_table: dict[str, dict[int, float]]) -> None:
        serializable = {state: {str(action): value for action, value in actions_values.items()} for state, actions_values in q_table.items()}
        self.data_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file_path, "w") as f:
            json.dump(serializable, f, indent=2)

if __name__ == "__main__":
    game = TicTacToeGame()
    game.print_state()
    print(f"Winner: {game.getWinner()}")

    x = game.load_q_table()
    print(x)