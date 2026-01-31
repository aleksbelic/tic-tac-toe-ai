import json
from pathlib import Path
from typing import Literal, Optional
import random

class TicTacToeGame:
    EMPTY = '-'
    states: list[list[str]]           # list of all states encountered during game
    current_player: Literal['X', 'O'] # player to make the next move ('X' always starts 1st)
    current_state: list[str]          # game's current state
    data_file_path: Path = Path(__file__).parent.parent / 'data' / 'q_table.json'
    
    def __init__(self) -> None:
        self.states = []
        self.current_state = [self.EMPTY] * 9
        self.current_player = 'X'

    def print_state(self) -> None:
        print()
        for i in range(0, 9, 3):
            print(f' {self.current_state[i]} | {self.current_state[i + 1]} | {self.current_state[i + 2]} ')
            if i < 6:
                print('---+---+---')
        print()

    def reset(self) -> None:
        self.states.clear()
        self.current_state = [self.EMPTY] * 9
        self.current_player = 'X'

    def get_winner(self) -> Optional[str]:
        """Return 'X' or 'O' if there is a winner, else None."""
        winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # columns
            (0, 4, 8), (2, 4, 6)             # diagonals
        )
        for i1, i2, i3 in winning_combinations:
            if self.current_state[i1] == self.current_state[i2] == self.current_state[i3] != self.EMPTY:
                return self.current_state[i1]
        return None
    
    def is_game_over(self) -> bool:
        return (self.get_winner() is not None) or (self.EMPTY not in self.current_state) # Check for winner or draw

    def load_q_table(self) -> dict[str, dict[int, float]]:
        if not self.data_file_path.exists():
            return {}
        
        try:
            with open(self.data_file_path, 'r') as data_file:
                raw = json.load(data_file)

                if raw is None: return {} # in case q_table file is empty
                
            return {state: {int(move): value for move, value in moves_values.items()} for state, moves_values in raw.items()}
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            return {}
        except Exception as e:
            print(f'Error loading Q-table: {e}')
            return {}
        
    def get_possible_moves_for_state(self, state: list[str]) -> list[int]:
        return [i for i, cell in enumerate(state) if cell == self.EMPTY]
    
    def make_random_move(self) -> None:
        possible_moves = self.get_possible_moves_for_state(self.current_state)
        if len(possible_moves) > 0:
            move = random.choice(possible_moves)
            self.current_state[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def save_current_state_to_q_table(self) -> None:
        q_table_states = self.load_q_table()
        q_table_states[''.join(self.current_state)] = self.generate_possible_moves_values_for_state(self.current_state)

        serializable = {state: {str(move): value for move, value in moves_values.items()} for state, moves_values in q_table_states.items()}

        self.data_file_path.parent.mkdir(parents = True, exist_ok = True)
        with open(self.data_file_path, 'w') as f:
            json.dump(serializable, f, indent = 2)

    def generate_possible_moves_values_for_state(self, state: list[str]):
        new_dict = {}
        for possible_move in self.get_possible_moves_for_state(state):
            new_dict[possible_move] = 0.0
        return new_dict

    def get_q_table_states_count(self) -> int:
        q_table_states = self.load_q_table()
        return len(q_table_states)

    def get_next_player_for_state(self, state: list[str]) -> Optional[Literal['X', 'O']]:
        if self.EMPTY not in state:
            return None
        
        x_count = state.count('X')
        o_count = state.count('O')
        return 'X' if x_count == o_count else 'O'

if __name__ == '__main__':
    for _ in range(100):  # Play 3 sample games
        print(_)
        game = TicTacToeGame()

        while not game.is_game_over():
            game.print_state()
            game.save_current_state_to_q_table()
            game.make_random_move()
        
        game.print_state()
        game.save_current_state_to_q_table()

        winner = game.get_winner()
        print(f'Winner: {winner if winner else "Draw"}')
        game.reset()

    print(game.get_q_table_states_count())
