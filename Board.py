import random
import tkinter as tk
from Cell import Cell
from tkinter import Canvas, messagebox

BG_COLOR = '#FAECE8'
TEXT_FONT = "Arial"


class Board:
    """
    Class to represent the game board.
    """

    def __init__(self, master, grid_size=3, should_auto_run=False):
        self.master = master
        self.grid_size = grid_size
        self.grid = []
        self.targets_row = []
        self.targets_col = []
        self.buttons = []
        self.click_count = {}
        self.should_auto_run = should_auto_run

        self.create_game()

    def create_game(self):
        """
        Create the game grid and UI.
        """
        self.create_game_grid()
        self.create_ui()

    def create_game_grid(self):
        """
        Create the game grid with random values and solutions.
        """
        self.grid = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                rand_value = random.randint(1, 9)
                rand_solution = random.random() < 0.6
                cell = Cell(rand_value, rand_solution)
                row.append(cell)
            self.grid.append(row)

        self.targets_row = [sum(cell.value for cell in row if cell.solution) for row in self.grid]
        self.targets_col = [sum(self.grid[i][j].value for i in range(self.grid_size)
                                if self.grid[i][j].solution) for j in range(self.grid_size)]

    def create_ui(self):
        """
        Create the game UI with buttons and labels.
        """
        self.master.configure(bg=BG_COLOR)

        for i in range(self.grid_size):
            row_buttons = []
            for j in range(self.grid_size):
                btn_id = f"{i},{j}"
                canvas = Canvas(self.master, width=60, height=60, bg="white", highlightthickness=1,
                                highlightbackground="black")
                canvas.grid(row=i, column=j, padx=1, pady=1)
                number = self.grid[i][j].value
                canvas.create_text(30, 30, text=str(number), font=(TEXT_FONT, 18))
                canvas.bind("<Button-1>", lambda event, row=i, col=j: self.handle_click(row, col))
                row_buttons.append(canvas)
                self.click_count[btn_id] = 0
            self.buttons.append(row_buttons)

        for i in range(self.grid_size):
            tk.Label(self.master, text=f" {self.targets_row[i]}", font=(TEXT_FONT, 14), bg=BG_COLOR).grid(
                row=i, column=self.grid_size, padx=5)

        for j in range(self.grid_size):
            tk.Label(self.master, text=f" {self.targets_col[j]}", font=(TEXT_FONT, 14), bg=BG_COLOR).grid(
                row=self.grid_size, column=j, pady=5)

    def handle_click(self, i, j):
        """
        Handle the button click event.
        """
        btn_id = f"{i},{j}"
        self.click_count[btn_id] += 1
        if self.click_count[btn_id] == 1:
            self.show_x(i, j)
        elif self.click_count[btn_id] == 2:
            self.remove_x_and_show_circle(i, j)
        elif self.click_count[btn_id] == 3:
            self.reset_button(i, j)

        self.check_win_condition()

    def show_x(self, i, j):
        """
        Show an X on the cell to indicate it is disabled.
        """
        canvas = self.buttons[i][j]
        canvas.delete("circle")
        canvas.delete("x")
        canvas.create_line(10, 10, 50, 50, fill="red", width=4, tags="x", stipple="gray50")
        canvas.create_line(10, 50, 50, 10, fill="red", width=4, tags="x", stipple="gray50")
        self.grid[i][j].disable()

    def remove_x_and_show_circle(self, i, j):
        """
        Remove the X and show a circle to indicate the cell is enabled.
        """
        canvas = self.buttons[i][j]
        canvas.delete("x")
        canvas.delete("circle")
        canvas.create_oval(10, 10, 50, 50, outline="green", width=4, tags="circle")
        self.grid[i][j].enable()

    def reset_button(self, i, j):
        """
        Reset the button to its original state.
        """
        canvas = self.buttons[i][j]
        canvas.delete("circle")
        canvas.delete("x")
        self.grid[i][j].reset()
        self.click_count[f"{i},{j}"] = 0

    def check_win_condition(self):
        """
        Check if the win condition is met.
        """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j].is_normal():
                    return False

        for i in range(self.grid_size):
            if sum(self.grid[i][j].value for j in range(self.grid_size) if self.grid[i][j].is_enabled()) != \
                    self.targets_row[i]:
                return False

        for j in range(self.grid_size):
            if sum(self.grid[i][j].value for i in range(self.grid_size) if self.grid[i][j].is_enabled()) != \
                    self.targets_col[j]:
                return False
        if not self.should_auto_run:
            messagebox.showinfo("Sumplete", "Congratulations! You won the game!")
        return True

    def get_game_status(self):
        """
        Get the current game status.
        """
        return "solved" if self.check_win_condition() else "not solved"

    def reset(self):
        """
        Reset the game board for a new game.
        """
        # Clear existing grid and UI
        for row in self.buttons:
            for canvas in row:
                canvas.destroy()
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Reset instance variables
        self.grid = []
        self.targets_row = []
        self.targets_col = []
        self.buttons = []
        self.click_count = {}

        # Create a new game
        self.create_game()

        # Update the UI
        self.master.update()
