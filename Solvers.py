import math
import random
import time


class BaseSolver:
    """
    Base class for all solvers.
    """

    def __init__(self, board, num_moves=0):
        self.board = board
        self.cur_board = [[cell.is_enabled() for cell in row] for row in self.board.grid]
        self.num_moves = num_moves

    def apply_move(self, i: int, j: int):
        """
        Apply a move to the board by flipping the state of cell (i, j).
        """
        if self.cur_board[i][j]:
            self.board.show_x(i, j)
            self.cur_board[i][j] = False
        else:
            self.board.remove_x_and_show_circle(i, j)
            self.cur_board[i][j] = True
        self.num_moves += 1

    def calculate_sum(self, index, is_row):
        """
        Calculate the sum of enabled cells in a row or column.
        """
        if is_row:
            return sum(self.board.grid[index][j].value for j in range(self.board.grid_size) if self.cur_board[index][j])
        return sum(self.board.grid[i][index].value for i in range(self.board.grid_size) if self.cur_board[i][index])

    def update_board_visual(self):
        """
        Update the board visualization.
        """
        self.board.master.update()
        # time.sleep(0.1)


########################################################################################
###########                     THE TWO CHOSEN SOLVERS                       ###########
########################################################################################

class HillClimbingSolver(BaseSolver):
    """
    Hill Climbing solver for the Sumplete game. Using Random-Restart.
    """

    def calculate_violated_constraints(self):
        """
        Calculate the number of violated constraints.
        """
        violations = 0
        for i in range(self.board.grid_size):
            if self.calculate_sum(i, True) != self.board.targets_row[i]:
                violations += 1
            if self.calculate_sum(i, False) != self.board.targets_col[i]:
                violations += 1
        return violations

    def random_restart(self):
        """
        Randomly restart the board.
        """
        for i in range(self.board.grid_size):
            for j in range(self.board.grid_size):
                if random.random() < 0.3:
                    self.apply_move(i, j)
        self.update_board_visual()

    def solve(self):
        """
        Solve the Sumplete game using the Hill Climbing algorithm.
        """
        current_violations = self.calculate_violated_constraints()
        best_violations = current_violations

        for _ in range(1000 * self.board.grid_size):
            improved = False
            for i in range(self.board.grid_size):
                for j in range(self.board.grid_size):
                    self.apply_move(i, j)
                    violations = self.calculate_violated_constraints()
                    if violations < best_violations:
                        best_violations = violations
                        improved = True
                    else:
                        self.apply_move(i, j)

                    self.update_board_visual()

            if best_violations == 0:
                break

            if not improved:
                self.random_restart()
                best_violations = self.calculate_violated_constraints()

        return self.board.check_win_condition()


class LCVBacktrackingSolver(BaseSolver):
    """
    Backtracking solver implementation using the Least Constraining Value heuristic.
    """

    def __init__(self, board):
        super().__init__(board)

    def solve(self):
        """
        Solve the puzzle using the Backtracking algorithm with LCV heuristic.
        """
        return self._backtrack()

    def _backtrack(self, row=None, col=None):
        """
        Recursive backtracking function to solve the puzzle.
        """
        self.num_moves += 1
        self.board.master.update()

        # Find the next empty cell
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return self.board.check_win_condition()

        row, col = empty_cell

        # Get the possible values (True/False) ordered by least constraining value
        for value in self._least_constraining_values(row, col):
            if value:
                self._enable_cell(row, col)
            else:
                self._disable_cell(row, col)

            if self._is_valid_state(row, col):
                if all(not cell.is_normal() for cell in self.board.grid[row]):
                    if self._calculate_row_sum(row) != self.board.targets_row[row]:
                        self._reset_cell(row, col)
                        continue

                if all(not row[col].is_normal() for row in self.board.grid):
                    if self._calculate_col_sum(col) != self.board.targets_col[col]:
                        self._reset_cell(row, col)
                        continue

                if self._backtrack():
                    return True

            self._reset_cell(row, col)

        return False

    def _find_empty_cell(self):
        """
        Find the next empty normal cell in the grid.
        """
        for row in range(self.board.grid_size):
            for col in range(self.board.grid_size):
                if self.board.grid[row][col].is_normal():
                    return row, col
        return None

    def _least_constraining_values(self, row, col):
        """
        Determine the order of values to try based on the Least Constraining Value heuristic.
        """
        constraints = []
        for value in [True, False]:
            if value:
                self._enable_cell(row, col)
            else:
                self._disable_cell(row, col)

            constraint_count = self._count_constraints(row, col)
            constraints.append((value, constraint_count))

            self._reset_cell(row, col)

        return [value for value, _ in sorted(constraints, key=lambda x: x[1])]

    def _count_constraints(self, row, col):
        """
        Count the number of constraints imposed by the current cell state on its row and column.
        """
        violations = 0
        for i in range(self.board.grid_size):
            if self.calculate_sum(i, True) > self.board.targets_row[i]:
                violations += 1
            if self.calculate_sum(i, False) > self.board.targets_col[i]:
                violations += 1
        return violations

    def _enable_cell(self, row, col):
        """Enable the cell and update the board."""
        self.board.remove_x_and_show_circle(row, col)
        self.board.grid[row][col].enable()

    def _disable_cell(self, row, col):
        """Disable the cell and update the board."""
        self.board.show_x(row, col)
        self.board.grid[row][col].disable()

    def _reset_cell(self, row, col):
        """Reset the cell visually and logically."""
        self.board.reset_button(row, col)

    def _is_valid_state(self, row, col):
        """Check if the current state is valid."""
        row_sum = self._calculate_row_sum(row)
        col_sum = self._calculate_col_sum(col)
        return (row_sum <= self.board.targets_row[row] and
                col_sum <= self.board.targets_col[col])

    def _calculate_row_sum(self, row):
        """Calculate the sum of enabled cells in a row."""
        return sum(cell.value for cell in self.board.grid[row] if cell.is_enabled())

    def _calculate_col_sum(self, col):
        """Calculate the sum of enabled cells in a column."""
        return sum(self.board.grid[row][col].value
                   for row in range(self.board.grid_size)
                   if self.board.grid[row][col].is_enabled())
