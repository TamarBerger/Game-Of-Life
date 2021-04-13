class Mode:
    """Describe the game pieces' color"""
    DEAD = 0
    ALIVE = 1

    def __init__(self):
        self.mode = self.DEAD
        self.game_level = 0

    def kill(self):
        """Set the mode as dead, equivalent to 0"""
        self.mode = self.DEAD

    def revive(self):
        """Set the mode as alive, equivalent to 1"""
        self.mode = self.ALIVE

    def set_level(self, level):
        self.game_level = level
    
    def __str__(self):
        if self.mode == 0:
            return "0"
        else:
            return "1"


class Board:
    """Create and maintain the game board."""

    BOARD_SIZE = (50, 50)

    def __init__(self):
        self.board = []
        self.level = 0
        self.initialize()

    def initialize(self):
        """Set board, all cells initial mode is dead."""
        self.board = []
        for _ in range(self.BOARD_SIZE[0]):
            self.board.append(
            [Cell() for column in range(self.BOARD_SIZE[1])]
            )

    def is_valid_square(self, row, column):
        """Return True if square in board bounds, False otherwise."""
        row_exists = row in range(self.BOARD_SIZE[0])
        column_exists = column in range(self.BOARD_SIZE[1])
        return row_exists and column_exists

    def get_square(self, row, col):
        """Return the game mode by its position on board."""
        if self.is_valid_square(row, col):
            return self.board[row][col]
        else:
            return None

    def set_current_mode_as_prev(self, row, col):
        """Set the previous mode of cell to the current one."""
        current_cell = self.get_square(row, col)
        current_cell_level = current_cell.mode.game_level
        if str(current_cell.mode) == "1":
            current_cell.previous_mode.revive()
        else:
            current_cell.previous_mode.kill()
        current_cell.previous_mode.set_level(current_cell_level)
        current_cell.mode.set_level(self.level)

    def set_square(self, row, col, state):
        """Set the mode of piece on the board."""
        self.set_current_mode_as_prev(row, col)
        if state == 'alive':
            self.board[row][col].mode.revive()
        elif state == 'dead':
            self.board[row][col].mode.kill()
        else:
            print("Accepts only 'alive' or 'dead'.")

    def set_beginning(self, list_of_cells):
        """Allow user to choose cells that will live at the beginning of the game."""
        for cell in list_of_cells:
            row = cell[0]
            col = cell[1]
            if self.is_valid_square(row, col):
                self.set_square(row, col, 'alive')
            else:
                print("Your choice is not whithin the boards boundaries")

    def get_neighbors(self, row, col):
        """Return the value of all existing neighbors."""
        if self.is_valid_square(row, col):
            options = [
                (row - 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row, col - 1),
                (row, col + 1),
                (row + 1, col - 1),
                (row + 1, col),
                (row + 1, col + 1)
            ]
            neighbors_list = []
            for opt in options:
                square_result = self.get_square(opt[0], opt[1])
                if square_result is not None:
                    if square_result.mode.game_level == self.level:
                        neighbors_list.append(str(square_result.previous_mode))
                    elif square_result.mode.game_level == self.level - 1:
                        neighbors_list.append(str(square_result.mode))
                    else:
                        print("Problem with cell level!!!!")
            return neighbors_list

    def get_alive_neighbors_num(self, row, col):
        """Return the number of all live neighbors - based on the previous round."""
        pals = self.get_neighbors(row, col)
        num = pals.count('1')
        return num

    def game_round(self, born, survive):
        self.level = self.level + 1
        for row in range(self.BOARD_SIZE[0]):
            for col in range(self.BOARD_SIZE[1]):
                live_pals = self.get_alive_neighbors_num(row, col)
                if live_pals == born:
                    self.set_square(row, col, 'alive')
                elif survive[0] <= live_pals <= survive[1]:
                    self.set_current_mode_as_prev(row, col)
                else:
                    self.set_square(row, col, 'dead')
    
    def check_if_all_dead(self):
        for row in range(self.BOARD_SIZE[0]):
            for col in range(self.BOARD_SIZE[1]):
                if str(self.get_square(row, col).mode) == '1':
                    return False
        return True

    def check_if_nothing_changes(self):
        for row in range(self.BOARD_SIZE[0]):
            for col in range(self.BOARD_SIZE[1]):
                if str(self.get_square(row, col).mode) != str(self.get_square(row, col).previous_mode):
                    return False
        return True

    def __str__(self):
        """Return current state of the board for display purposes."""
        printable = ""
        for row in self.board:
            for col in row:
                printable = printable + f" {col.mode} "
            printable = printable + '\n'
        return printable


class Cell():
    """Represent a general cell on the board."""

    def __init__(self):
        self.mode = Mode()
        self.previous_mode = Mode()
    
    def __str__(self):
        return (
            f"Current mode: {self.mode}\n"
            + f"Previous mode: {self.previous_mode}\n"
            + f"Current game level: {self.mode.game_level}\n"
        )


def game_of_life(initial_live_cells_list, B=3, S=(2, 3)):
    current_game = Board()
    Board.set_beginning(current_game, initial_live_cells_list)
    # print("Initial setting of the board: ")
    # print(current_game)
    Board.game_round(current_game, B, S)
    # print(f"Level : {current_game.level}")
    # print(current_game)
    while Board.check_if_all_dead(current_game) is False and Board.check_if_nothing_changes(current_game) is False:
        Board.game_round(current_game, B, S)
        # print(f"Level : {current_game.level}")
        # print(current_game)
    return current_game

