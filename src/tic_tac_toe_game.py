import json
from pathlib import Path
from typing import Literal, Optional
import random

class TicTacToeGame:
    EMPTY = '-'
    history: list[tuple[list[str], int, str]]   # list of (state, move, player) tuples
    current_player: Literal['X', 'O']           # player to make the next move ('X' always starts 1st)
    current_state: list[str]                    # game's current state
    data_file_path: Path = Path(__file__).parent.parent / 'data' / 'q_table.json'
    train_mode: bool = False                     # whether the game is in training mode or not
    
    def __init__(self, train_mode: bool) -> None:
        self.train_mode = train_mode
        self.history = []
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
        self.history.clear()
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
    
    def make_move(self, move: int) -> None:
        possible_moves = self.get_possible_moves_for_state(self.current_state)

        if move not in possible_moves:
            raise ValueError(f'Invalid move: {move}. Possible moves are: {possible_moves}')

        self.history.append((self.current_state.copy(), move, self.current_player))
        self.current_state[move] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def make_random_move(self) -> None:
        possible_moves = self.get_possible_moves_for_state(self.current_state)
        if len(possible_moves) > 0:
            move = random.choice(possible_moves)
            self.history.append((self.current_state.copy(), move, self.current_player))
            self.current_state[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def make_best_move(self) -> None:
        best_move = self.get_best_move_for_state(self.current_state)

        if best_move is not None:
            self.history.append((self.current_state.copy(), best_move, self.current_player))
            self.current_state[best_move] = self.current_player
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

    def get_best_move_for_state(self, state: list[str]) -> Optional[int]:
        q_table_states = self.load_q_table()
        state_key = ''.join(state)

        if state_key not in q_table_states:
            return None
        
        possible_moves_values = q_table_states[state_key]
        if not possible_moves_values:
            return None
        
        max_value = max(possible_moves_values.values())
        best_moves = [int(move) for move, value in possible_moves_values.items() if value == max_value]
        return random.choice(best_moves)
    
    def train_from_history(self, winner: str) -> None:
        if winner is None:
            return
        
        q_table_states = self.load_q_table()

        for state_before_move, move, player in self.history:
            reward = 0.001 if player == winner else -0.001

            state_key = ''.join(state_before_move)

            if state_key not in q_table_states:
                q_table_states[state_key] = self.generate_possible_moves_values_for_state(state_before_move)

            q_table_states[state_key][move] = round(q_table_states[state_key][move] + reward, 3)

        serializable = {state: {str(move): value for move, value in moves_values.items()} for state, moves_values in q_table_states.items()}

        self.data_file_path.parent.mkdir(parents = True, exist_ok = True)
        with open(self.data_file_path, 'w') as f:
            json.dump(serializable, f, indent = 2)


if __name__ == '__main__':
    game = TicTacToeGame(train_mode = False)

    if game.train_mode:
        print(f'Training mode enabled.\nCurrent Q-table states count: {game.get_q_table_states_count()}')

        for _ in range(10):

            while not game.is_game_over():
                game.print_state()
                game.make_random_move()

            game.print_state()
            winner = game.get_winner()

            if winner is not None:
                game.train_from_history(winner)

            game.reset()

        print(f'Training completed.\nUpdated Q-table states count: {game.get_q_table_states_count()}')

    else:
        while not game.is_game_over():
            game.print_state()

            my_move = input('Play move (0-8): ')
            try:
                game.make_move(int(my_move))
            except ValueError as e:
                print(e)
                continue

            if game.is_game_over():
                break

            game.make_best_move()
    
        game.print_state()

        winner = game.get_winner()
        
        print(f'Winner: {winner if winner else "Draw"}')

