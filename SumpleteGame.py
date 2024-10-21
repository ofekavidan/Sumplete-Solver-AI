import tkinter as tk
from tkinter import messagebox
from Board import Board
from Solvers import *
import argparse

WARNING_TITLE = "No Selection"
WARNING_MESSAGE = "Please choose an option before clicking OK."
DEFAULT_GRID_SIZE = 4
DEFAULT_NUM_GAMES = 1
TEXT_FONT = "Arial"
BG_COLOR = '#FAECE8'
TEXT_SIZE = 12
TITLE_SIZE = 14
ROOT_SIZE = "300x300"

OPTIONS = ["Manual", "Hill Climbing", "Backtracking LCV"]
SOLVER_MAP = {
    "hill_climbing": HillClimbingSolver,
    "backtracking_lcv": LCVBacktrackingSolver
}


class SumpleteGame:
    """
    Class to represent the Sumplete game.
    """

    def __init__(self, board, solver_option=None, num_of_games=1):
        self.board = board
        self.solver_option = solver_option
        self.num_games = num_of_games

        if self.solver_option:
            self.run_auto_solver()

    def run_auto_solver(self):
        """
        Run the appropriate auto solver based on user choice.
        """
        selected_option = OPTIONS[self.solver_option].lower().replace(" ", "_") \
            if isinstance(self.solver_option, int) else self.solver_option
        solver_class = SOLVER_MAP.get(selected_option)
        if solver_class:
            for game in range(self.num_games):
                print(f"Solving game {game + 1} of {self.num_games}")
                start_time = time.time()  # start timing
                solver = solver_class(self.board)
                solver.solve()
                end_time = time.time()  # end timing
                elapsed_time = end_time - start_time
                status = self.board.get_game_status()
                print(f"Game {game + 1} status: {status}")
                print(f"Time taken: {elapsed_time:.5f} seconds")
                if game < self.num_games - 1:
                    self.board.reset()
                    self.board.master.update()


def on_ok(selected_grid_size, num_of_games):
    """
    Handle the OK button click event to start the game.
    """
    selected_option = option.get()
    if selected_option != -1:
        root.destroy()
        new_window = tk.Tk()
        new_window.title("Sumplete Game")
        should_auto_run = selected_option != 0

        if selected_option == 0:
            board = Board(new_window, selected_grid_size, should_auto_run)
            SumpleteGame(board, num_of_games=num_of_games)
        else:
            board = Board(new_window, selected_grid_size, should_auto_run)
            SumpleteGame(board, selected_option, num_of_games)
        new_window.mainloop()
    else:
        messagebox.showwarning(WARNING_TITLE, WARNING_MESSAGE)


def on_exit():
    """
    Close the game window.
    """
    root.destroy()


def parse_arguments():
    """
    Parse command line arguments for the game, making all arguments optional.
    """
    parser = argparse.ArgumentParser(description="Sumplete Game")
    parser.add_argument("--grid-size", type=int, default=DEFAULT_GRID_SIZE,
                        help=f"Size of the game grid (default: {DEFAULT_GRID_SIZE})")
    parser.add_argument("--num-games", type=int, default=DEFAULT_NUM_GAMES,
                        help=f"Number of games to solve (default: {DEFAULT_NUM_GAMES})")
    parser.add_argument("--solver", type=str, choices=list(SOLVER_MAP.keys()), default=None,
                        help="Specify the solver to use (optional, bypasses the menu selection if provided)")
    return parser.parse_args()


def initialize_configuration_window():
    """
    Initialize the configuration window to choose the game mode.
    """
    global root, option
    root = tk.Tk()
    root.geometry(ROOT_SIZE)
    root.title("Configure Game")
    root.configure(bg=BG_COLOR)
    tk.Label(root, text=f"Grid Size: {grid_size}x{grid_size}", font=(TEXT_FONT, TITLE_SIZE), bg=BG_COLOR).pack(pady=5)
    tk.Label(root, text=f"Number of Games: {num_games}", font=(TEXT_FONT, TITLE_SIZE), bg=BG_COLOR).pack(pady=5)
    tk.Label(root, text="Please choose an option:", font=(TEXT_FONT, TITLE_SIZE), bg=BG_COLOR).pack(pady=10)
    option = tk.IntVar(value=-1)
    for idx, opt in enumerate(OPTIONS):
        tk.Radiobutton(root, text=opt, variable=option, value=idx, font=(TEXT_FONT, TEXT_SIZE), bg=BG_COLOR,
                       fg='black', selectcolor='white').pack(anchor=tk.W)
    tk.Button(root, text="OK", command=lambda: on_ok(grid_size, num_games), font=(TEXT_FONT, TEXT_SIZE)).pack(
        side=tk.LEFT,
        padx=20, pady=20)
    tk.Button(root, text="Exit", command=on_exit, font=(TEXT_FONT, TEXT_SIZE)).pack(side=tk.RIGHT, padx=20, pady=20)


if __name__ == "__main__":
    args = parse_arguments()
    grid_size = args.grid_size
    num_games = args.num_games

    if args.solver:
        # if a solver is specified run the game directly
        new_window = tk.Tk()
        new_window.title("Sumplete Game")
        board = Board(new_window, grid_size, True)
        SumpleteGame(board, args.solver, num_games)
        new_window.mainloop()
    else:
        # if no solver is specified show the configuration window
        initialize_configuration_window()
        root.mainloop()
