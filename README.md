# Tic-tac-toe AI

A simple Tic-tac-toe implementation with a Q-learning agent. This repository demonstrates how to train and play against an AI that learns via reinforcement learning (Q-learning).

**Highlights**
- Lightweight Python implementation with no external ML libraries required.
- Includes saved Q-tables in `data/` for quick experiments.

**Quick stats**
- Regular states (including empty board): `5478`
- Non-terminal states: `4400`
- Example training used: `50,000` random games

## Repository structure

- `src/`
	- `tic_tac_toe_game.py` — main game and agent implementation
- `data/`
	- `q_table.json` — trained Q-table (example)
	- `q_table_empty.json` — empty Q-table template
- `tests/` — project tests

## Requirements

- Python 3

No external packages are required; the project uses only the Python standard library.

## Usage

Run the game script to start a simple interactive session or to run training/play routines implemented in `src/tic_tac_toe_game.py`:

```bash
python3 src/tic_tac_toe_game.py <OPTIONAL_FLAGS>
```

Depending on the script's CLI or hardcoded behavior, it may: train the agent, load a saved Q-table, or allow human vs AI play.

### Command-line flags

- **--train**: Enable `training mode`. When present, the script runs episodes of self-play and updates the Q-table file.
- **--episodes**: Number of training episodes to run (default: 10). Use `--episodes 1000` to run 1,000 episodes.
- **--data-file**: Path to the Q-table JSON file to read/write (overrides the default `data/q_table.json`).

Example — train for 50,000 episodes and write to a specific file:

```bash
python3 src/tic_tac_toe_game.py --train --episodes 1000 --data-file data/my_q_table.json
```

## Training

The agent uses Q-learning to estimate action values for board states. To train the agent:

- Run the training routine defined in `src/tic_tac_toe_game.py`.
- Training will produce or update a Q-table file under `data/q_table.json`.

Tip: Increase the number of training episodes for a stronger agent; training is fast for Tic-tac-toe.

## Files of interest

- `src/tic_tac_toe_game.py`: core game loop, environment, and Q-learning agent.
- `data/q_table.json`: example trained Q-table you can load for play without retraining.

## Help

Get more info on optional flags via command:

```bash
python3 src/tic_tac_toe_game.py --help
```

