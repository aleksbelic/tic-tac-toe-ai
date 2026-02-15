# Tic-tac-toe AI

A simple Tic-tac-toe implementation with a Q-learning agent. This repository demonstrates how to train and play against an AI that learns via reinforcement learning (Q-learning).

**Highlights**
- Lightweight Python implementation with no external ML libraries required.
- Includes saved Q-tables in `data/` for quick experiments.

**Quick stats**
- Regular states (including empty board): `5478`
- Non-terminal states: `4400`
- Example training used: `120,000` random games

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

### Play interactive mode

Run without flags to play human vs AI:

```bash
python3 src/tic_tac_toe_game.py
```

The AI will use the Q-table from `data/q_table.json` (if available) to play optimally.

### Train the agent

Run with `--train` to train the agent via self-play. Training displays progress with percentages:

```bash
python3 src/tic_tac_toe_game.py --train --episodes 20000
```

Sample training output:

```
Training mode enabled - running self-play episodes...
 * 2000/20000 (10.0%) completed
 * 4000/20000 (20.0%) completed
 * 6000/20000 (30.0%) completed
 ...
Training completed!
Q-table states count: 4400
```

### Command-line flags

- **--train**: Enable training mode. Runs self-play episodes and updates the Q-table file. Without this flag, the script launches interactive play mode.
- **--episodes**: Number of training episodes (default: 10, but 20,000+ recommended for a strong agent).
- **--data-file**: Path to the Q-table JSON file to read/write (overrides default `data/q_table.json`).

Example — train for 20,000 episodes and save to a custom file:

```bash
python3 src/tic_tac_toe_game.py --train --episodes 20000 --data-file data/my_q_table.json
```

## Training

The agent uses Q-learning to estimate action values for board states. To train the agent:

- Run with `--train --episodes N` where N is the number of episodes.
- Training will produce or update the Q-table file (`data/q_table.json` by default).
- Progress is displayed as percentage completion every 10% of episodes.

## Files of interest

- `src/tic_tac_toe_game.py`: core game loop, environment, and Q-learning agent.
- `data/q_table.json`: example trained Q-table you can load for play without retraining.

## Getting help

For details on all available flags:

```bash
python3 src/tic_tac_toe_game.py --help
```

## DEV & Unit tests

Create a virtual environment:
```bash
python3 -m venv .venv
```

Activate virtual environment:
```bash
source .venv/bin/activate
```

Install DEV dependencies (`pytest` and `pytest-cov`):
```bash
(.venv): pip install -r requirements-dev.txt
```

Run unit tests:
```bash
(.venv): pytest
```

Run unit tests & check test-coverage:
```bash
(.venv): pytest --cov=src tests/
```

