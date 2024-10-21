# Sumplete Game

## Running the Code
![image](https://github.com/user-attachments/assets/c29f9aec-740b-4c11-af9f-8bb9ff21b13a)

### Basic Command
To run the game with default parameters (one 4x4 game):

### Game Modes
1. **Regular Game (Manual Mode)**
   - Select "Manual" in the configuration window
   - Click "OK"
   - Play the game:
     - First click on a square: Mark with X (not selected)
     - Second click: Mark with O (selected)
     - Third click: Return to unmarked state

2. **Automatic Solver**
   - Select an algorithm from the list in the configuration window
   - Click "OK" to watch the algorithm solve the puzzle

To exit without choosing an option, click "Exit".

### Running with Parameters
You can customize the game run using the following flags:

- `--grid-size`: Change the board size
- `--num-games`: Run multiple games automatically (results printed to terminal)
- `--solver`: Choose a specific solving algorithm

Example command with parameters:
```python SumpleteGame.py --grid-size 6 --num-games 2 --solver hill_climbing```

### Available Solving Algorithms
- `hill_climbing`
- `backtracking_lcv`
