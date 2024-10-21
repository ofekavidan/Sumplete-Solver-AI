NORMAL = 'normal'
ENABLED = 'enabled'
DISABLED = 'disabled'


class Cell:
    """
    Cell class represents each cell in the grid.
    """

    def __init__(self, value, solution):
        self.value = value
        self.solution = solution
        self.state = NORMAL

    def reset(self):
        """
        Reset the cell to its initial state which is normal.
        """
        self.state = NORMAL

    def enable(self):
        """
        Enable the cell.
        """
        self.state = ENABLED

    def disable(self):
        """
        Disable the cell.
        """
        self.state = DISABLED

    def is_disabled(self):
        """
        Return True if the cell is disabled. Otherwise, return False.
        """
        return self.state == DISABLED

    def is_enabled(self):
        """
        Return True if the cell is enabled. Otherwise, return False.
        """
        return self.state == ENABLED

    def is_normal(self):
        """
        Return True if the cell is normal. Otherwise, return False.
        """
        return self.state == NORMAL
