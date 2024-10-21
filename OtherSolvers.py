########################################################################################
###########                  OTHER SOLVERS WE TESTED                         ###########
########################################################################################
from Solvers import BaseSolver
import math
import random
import time

class BacktrackingSolver(BaseSolver):
    """
    Backtracking solver implementation with corrected MRV heuristic and row/column sum checks.
    """

    def __init__(self, board, heuristic='none'):
        super().__init__(board)
        self.heuristic = heuristic.lower()

    def solve(self):
        """
        Solve the puzzle using the Backtracking algorithm.
        """
        return self._backtrack(0, 0)

    def _backtrack(self, row, col):
        """
        Recursive backtracking function to solve the puzzle.
        """
        self.num_moves += 1
        self.board.master.update()
        # time.sleep(0.1)

        if row == self.board.grid_size:
            return self.board.check_win_condition()

        if col == self.board.grid_size:
            return self._backtrack(row + 1, 0)

        for state in [True, False]:
            if state:
                self._enable_cell(row, col)
            else:
                self._disable_cell(row, col)

            if self._is_valid_state(row, col):
                if col == self.board.grid_size - 1:
                    if self._calculate_row_sum(row) != self.board.targets_row[row]:
                        continue

                if row == self.board.grid_size - 1:
                    if self._calculate_col_sum(col) != self.board.targets_col[col]:
                        continue

                if self._backtrack(row, col + 1):
                    return True

            self._reset_cell(row, col)
        self._reset_cell(row, col)
        return False

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


class MRVDegreeBacktrackingSolver(BaseSolver):
    """
    Backtracking solver implementation using the Minimum Remaining Values (MRV) heuristic
    with Degree heuristic as a tie-breaker.
    """

    def __init__(self, board):
        super().__init__(board)

    def solve(self):
        """
        Solve the puzzle using the Backtracking algorithm with MRV and Degree heuristics.
        """
        return self._backtrack()

    def _backtrack(self):
        """
        Recursive backtracking function to solve the puzzle.
        """
        self.num_moves += 1
        self.board.master.update()
        # time.sleep(0.01)

        # Find the next cell to assign using MRV and Degree heuristics
        cell = self._select_unassigned_variable()
        if not cell:
            return self.board.check_win_condition()

        row, col = cell

        for value in [True, False]:
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

    def _select_unassigned_variable(self):
        """
        Select the next unassigned variable using MRV heuristic with Degree heuristic as tie-breaker.
        """
        min_remaining_values = float('inf')
        max_degree = -1
        selected_cell = None

        for row in range(self.board.grid_size):
            for col in range(self.board.grid_size):
                if self.board.grid[row][col].is_normal():
                    remaining_values = self._count_legal_values(row, col)
                    if remaining_values < min_remaining_values:
                        min_remaining_values = remaining_values
                        max_degree = self._calculate_degree(row, col)
                        selected_cell = (row, col)
                    elif remaining_values == min_remaining_values:
                        degree = self._calculate_degree(row, col)
                        if degree > max_degree:
                            max_degree = degree
                            selected_cell = (row, col)

        return selected_cell

    def _count_legal_values(self, row, col):
        """
        Count the number of legal values for a cell.
        """
        count = 0
        for value in [True, False]:
            if value:
                self._enable_cell(row, col)
            else:
                self._disable_cell(row, col)

            if self._is_valid_state(row, col):
                count += 1

            self._reset_cell(row, col)

        return count

    def _calculate_degree(self, row, col):
        """
        Calculate the degree of a cell (number of constraints on other variables).
        """
        degree = 0
        for r in range(self.board.grid_size):
            if r != row and self.board.grid[r][col].is_normal():
                degree += 1
        for c in range(self.board.grid_size):
            if c != col and self.board.grid[row][c].is_normal():
                degree += 1
        return degree

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


class StochasticHillClimbingSolver(BaseSolver):
    """
    Stochastic Hill Climbing solver for the Sumplete game.
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

    def solve(self):
        """
        Solve the Sumplete game using the Stochastic Hill Climbing algorithm.
        """
        current_violations = self.calculate_violated_constraints()
        best_violations = current_violations

        for _ in range(1000 * self.board.grid_size):
            # Randomly select a cell and apply a move
            i = random.randint(0, self.board.grid_size - 1)
            j = random.randint(0, self.board.grid_size - 1)
            self.apply_move(i, j)

            violations = self.calculate_violated_constraints()
            if violations < best_violations:
                best_violations = violations
                self.update_board_visual()

                if best_violations == 0:
                    break

        return self.board.check_win_condition()


class FirstChoiceHillClimbingSolver(BaseSolver):
    """
    First-Choice Hill Climbing solver for the Sumplete game.
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

    def solve(self):
        """
        Solve the Sumplete game using the First-Choice Hill Climbing algorithm.
        """
        current_violations = self.calculate_violated_constraints()
        best_violations = current_violations

        for _ in range(1000 * self.board.grid_size):
            improved = False
            for i in range(self.board.grid_size):
                for j in range(self.board.grid_size):
                    # Apply move
                    self.apply_move(i, j)
                    violations = self.calculate_violated_constraints()

                    if violations < best_violations:
                        best_violations = violations
                        improved = True
                        self.update_board_visual()
                        break  # Break the loop after the first improvement
                if improved:
                    break  # Exit outer loop if improvement was found

            if best_violations == 0:
                break

        return self.board.check_win_condition()


class SimulatedAnnealingSolver(BaseSolver):
    """
    Simulated Annealing solver for the Sumplete game.
    """

    def __init__(self, board, initial_temperature=100.0, cooling_rate=0.99, max_iterations=1000):
        super().__init__(board)
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations

    def _calculate_error(self):
        """
        Calculate the error in the current state.
        """
        error = 0
        for i in range(self.board.grid_size):
            error += abs(self.calculate_sum(i, True) - self.board.targets_row[i])
            error += abs(self.calculate_sum(i, False) - self.board.targets_col[i])
        return error

    def _get_random_cell(self):
        """
        Get a random cell.
        """
        return random.randint(0, self.board.grid_size - 1), random.randint(0, self.board.grid_size - 1)

    def _accept_new_state(self, current_error, new_error):
        """
        Accept the new state based on the error and temperature.
        """
        if new_error < current_error:
            return True
        return random.random() < math.exp((current_error - new_error) / self.temperature)

    def solve(self):
        """
        Solve the Sumplete game using the Simulated Annealing algorithm.
        """
        current_error = self._calculate_error()

        for _ in range(self.max_iterations):
            row, col = self._get_random_cell()
            self.apply_move(row, col)
            new_error = self._calculate_error()

            if self._accept_new_state(current_error, new_error):
                current_error = new_error
            else:
                self.apply_move(row, col)  # Revert the move

            self.update_board_visual()
            self.temperature *= self.cooling_rate

            if current_error == 0:
                break

        return self.board.check_win_condition()


class GeneticAlgorithmSolver(BaseSolver):
    """
    Genetic Algorithm solver for the Sumplete game.
    """

    def __init__(self, board, population_size=50, generations=100, elite_size=10, tournament_size=25):
        super().__init__(board)
        self.population_size = population_size
        self.generations = generations
        self.elite_size = elite_size
        self.tournament_size = tournament_size

    def _create_individual(self):
        """
        Create a random individual.
        """
        return [[random.choice([True, False]) for _ in range(self.board.grid_size)]
                for _ in range(self.board.grid_size)]

    def _calculate_fitness(self, individual):
        """
        Calculate the fitness of an individual.
        """
        error = 0
        for i in range(self.board.grid_size):
            row_sum = sum(self.board.grid[i][j].value for j in range(self.board.grid_size) if individual[i][j])
            col_sum = sum(self.board.grid[j][i].value for j in range(self.board.grid_size) if individual[j][i])
            error += abs(row_sum - self.board.targets_row[i]) + abs(col_sum - self.board.targets_col[i])
        return error

    def _crossover(self, parent1, parent2):
        """
        Perform crossover between two parents.
        """
        return [[random.choice([parent1[i][j], parent2[i][j]])
                 for j in range(self.board.grid_size)]
                for i in range(self.board.grid_size)]

    def _get_random_cell(self):
        """
        Get a random cell.
        """
        return random.randint(0, self.board.grid_size - 1), random.randint(0, self.board.grid_size - 1)

    def _mutate(self, individual):
        """
        Mutate an individual.
        """
        i, j = self._get_random_cell()
        individual[i][j] = not individual[i][j]
        return individual

    def _select_parent(self, population):
        """
        Select a parent using tournament selection.
        """
        tournament = random.sample(population, self.tournament_size)
        return min(tournament, key=self._calculate_fitness)

    def _update_board(self, solution):
        """
        Update the board based on the solution.
        """
        for i in range(self.board.grid_size):
            for j in range(self.board.grid_size):
                if solution[i][j]:
                    self.board.remove_x_and_show_circle(i, j)
                else:
                    self.board.show_x(i, j)
                self.update_board_visual()

    def solve(self):
        """
        Solve the Sumplete game using the Genetic Algorithm.
        """
        population = [self._create_individual() for _ in range(self.population_size)]

        for _ in range(self.generations):
            population.sort(key=self._calculate_fitness)

            if self._calculate_fitness(population[0]) == 0:
                self._update_board(population[0])
                break

            new_population = population[:self.elite_size]

            while len(new_population) < self.population_size:
                parent1 = self._select_parent(population)
                parent2 = self._select_parent(population)
                child = self._mutate(self._crossover(parent1, parent2))
                new_population.append(child)

            population = new_population

        return self.board.check_win_condition()
