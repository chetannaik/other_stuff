from matplotlib import pyplot as plt
from matplotlib import rc
from scipy.stats import itemfreq

import copy
import numpy as np
import seaborn

# configure plot parameters
rc("figure", facecolor="white")
rc("axes", facecolor="white")
rc("axes", edgecolor="grey")
rc("grid", alpha=0.9)
rc("grid", linewidth=0.2)
rc("grid", linestyle=":")
colors = seaborn.color_palette()


# Peg Solitaire board model
FILLED_PEG = 1
EMPTY_PEG = 0
BLANK = -1
BOARD_SIZE = 7
COL_MOVE = "|"
ROW_MOVE = "--"


class Board:
    """Board class that models Peg Solitaire game.

    This class has setters, getters, methods that get all possible moves,
    check validity of a move, make a move, plot the board state and
    other useful utilities.

    Attributes:
        board: A python list indicating initial state of the board.
    """
    __init_state = [-1, -1, 1, 1, 1, -1, -1,
                    -1, -1, 1, 1, 1, -1, -1,
                    1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1,
                    -1, -1, 1, 1, 1, -1, -1,
                    -1, -1, 1, 1, 1, -1, -1]

    def __init__(self, board=__init_state):
        """Initializes Board with __init_state."""
        self.board = board

    def __eq__(self, other):
        """Checks of two instance of a board are equal."""
        if other is None:
            return False
        return self.board == other.board

    def __hash__(self):
        """Gets hash of a board state."""
        __board_state = self.get_string_state()
        return hash(''.join(__board_state))

    def copy(self):
        """Returns a deepcopy of board instance."""
        return copy.deepcopy(self)

    def get_board_state(self):
        """Returns a board state as a list."""
        return self.board

    def set_board_state(self, state):
        """Sets the board state using a input list."""
        self.board = state

    def move(self, init_pos, final_pos):
        """Moves a peg from init_pos to final_pos."""
        if self.is_valid(init_pos, final_pos):
            middle_peg, _ = self.get_middle_peg(init_pos, final_pos)
            self.board[final_pos - 1] = FILLED_PEG
            self.board[init_pos - 1] = EMPTY_PEG
            self.board[middle_peg - 1] = EMPTY_PEG

    @staticmethod
    def get_middle_peg(init_pos, final_pos):
        """Returns middle_peg using init_pos to final_pos.

        Args:
            init_pos: A number indicating initial position of the move.
            final_pos: A number indicating final position of the move.
        """
        if abs(final_pos - init_pos) > BOARD_SIZE:
            if final_pos < init_pos:
                # move_up
                middle_peg = final_pos + 7
                return middle_peg, COL_MOVE
            else:
                # move_down
                middle_peg = init_pos + 7
                return middle_peg, COL_MOVE
        else:
            middle_peg = (init_pos + final_pos) / 2
            return middle_peg, ROW_MOVE

    def is_valid(self, init_pos, final_pos):
        """Checks if a move fromi nit_pos to final_pos is valid.

        - Has checks to ensure that init_pos and middle_peg has pegs while
        final_pos is empty.
        - Has checks to ensure that we are moving
        in the movable board area and not the 2x2 blank squares on the corners
        of the board.
        - Has checks to ensure that a board move involves a peg move 2 position
        either horizontally(ROW_MOVE) or vertically(COL_MOVE).

        Args:
            init_pos: A number indicating initial position of the move.
            final_pos: A number indicating final position of the move.
        """
        middle_peg, move_type = self.get_middle_peg(init_pos, final_pos)
        if self.board[final_pos - 1] == FILLED_PEG:
            return False
        if self.board[init_pos - 1] == EMPTY_PEG:
            return False
        if self.board[middle_peg - 1] == EMPTY_PEG:
            return False
        if ((self.board[init_pos - 1] == BLANK) or
                (self.board[middle_peg - 1] == BLANK) or
                (self.board[final_pos - 1] == BLANK)):
            return False
        if move_type == COL_MOVE:
            if not (init_pos % 7 and middle_peg % 7 and final_pos % 7):
                return False
            if abs(final_pos - init_pos) != BOARD_SIZE * 2:
                return False
        else:
            if abs(final_pos - init_pos) != 2:
                return False
            _, init_row = get_peg_coordinates_from_number(init_pos)
            _, final_row = get_peg_coordinates_from_number(final_pos)
            if init_row != final_row:
                return False
        return True

    def plot_board(self, text=True, name=None):
        """ Plots the current state of the board as a grid.

        Args:
            text: A boolean which indicates whether to overlay the plot with
                numbers.
        """
        n_rows, n_cols = BOARD_SIZE, BOARD_SIZE
        x = np.arange(n_rows + 1)
        y = np.arange(n_cols + 1)
        x, y = np.meshgrid(x, y)
        board = np.array(self.board)
        z = board.reshape((n_rows, n_cols))

        fig = plt.figure(figsize=(3, 3))
        ax = fig.add_subplot(111, aspect='equal')
        ax.invert_yaxis()

        ax.pcolormesh(x, y, z,
                      edgecolor='1',
                      linewidth=1.5)
        ax.axis('off')

        width = 1
        if text:
            for r in range(1, n_rows + 1):
                for c in range(1, n_cols + 1):
                    plt.text((c - 1) + width / 2.,
                             (r - 1) + width / 2.,
                             str(((r - 1) * n_cols) + c),
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=9,
                             color="white")

        plt.xticks([])
        plt.yticks([])
        if name:
            plt.savefig(name + '.png', bbox_inches='tight')
        # else:
        #     plt.show()

    def get_board_stats(self):
        """Returns board statistics which include number of pegs, holes and
        empty spaces.
        """
        return dict(itemfreq(self.board))

    def get_string_state(self):
        """Returns board state in 0X- string format.
        "0" = 0
        "X" = 1
        "-" = -1
        """
        str_list = []
        row = ""
        for num, ae in enumerate(self.board):
            if num % BOARD_SIZE == BOARD_SIZE - 1:
                if ae == -1:
                    row += "-"
                if ae == 1:
                    row += "X"
                if ae == 0:
                    row += "0"
                str_list.append(row)
                row = ""
            else:
                if ae == -1:
                    row += "-"
                if ae == 1:
                    row += "X"
                if ae == 0:
                    row += "0"
        return str_list

    def get_possible_transitions(self):
        """Returns all possible moves possible from the current state of the
        board."""
        __transitions = []
        for box in range(1, 50):
            (x, y) = get_peg_coordinates_from_number(box)
            # go right
            if 7 >= x + 2 >= 1:
                init = get_number_from_peg_coordinates((x, y))
                final = get_number_from_peg_coordinates((x+2, y))
                if self.is_valid(init, final):
                    __transitions.append((init, final))
            # go left
            if 7 >= x - 2 >= 1:
                init = get_number_from_peg_coordinates((x, y))
                final = get_number_from_peg_coordinates((x-2, y))
                if self.is_valid(init, final):
                    __transitions.append((init, final))
            # go up
            if 7 >= y - 2 >= 1:
                init = get_number_from_peg_coordinates((x, y))
                final = get_number_from_peg_coordinates((x, y-2))
                if self.is_valid(init, final):
                    __transitions.append((init, final))
            # go down
            if 7 >= y + 2 >= 1:
                init = get_number_from_peg_coordinates((x, y))
                final = get_number_from_peg_coordinates((x, y+2))
                if self.is_valid(init, final):
                    __transitions.append((init, final))
        return __transitions


# Utilities
def translate_input_to_array(inp_list):
    """Converts input string in 0X- format to array of numbers as required
    by the Board class.

    Args:
        inp_list: A list of strings of 0's, X's and -'s representing the
            state of the board.
            eg: ['--000--',
                 '--0X0--',
                 '00XXX00',
                 '000X000',
                 '000X000',
                 '--000--',
                 '--000--']
    """
    state = []
    for e in inp_list:
        ml = []
        for s in e:
            if s == "-":
                ml.append(-1)
            if s == "0":
                ml.append(0)
            if s == "X":
                ml.append(1)
        state.extend(ml)
    return state


def get_peg_coordinates_from_number(number):
    """Return peg x and y co-ordinates from its number."""
    row = number % 7 if (number % 7 != 0) else 7
    col = 0
    for col in range(7):
        if number - (7 * col) == row:
            break
    return row, col + 1


def get_number_from_peg_coordinates(peg_coordinates):
    """Return peg number from its x and y co-ordinates."""
    x, y = peg_coordinates
    number = (y - 1) * 7 + x
    return number


def plot_answer(start, moves):
    """Plots step by step moves made on board.

    Args:
        board: An instance of Board class.
        moves: A list of tuples representing moves.
    """
    board = Board(start)
    board.plot_board(name="move 0")
    for m_num, move in enumerate(moves):
        board.move(*move)
        name = "move %d" % (m_num + 1)
        board.plot_board(name=name)


def get_rotated_states(inp_state):
    """Returns 4 rotated and 4 flipped and rotated versions of
    Board state inp_state.
    """
    state = np.array(inp_state).reshape(7, 7)
    rotations = list()
    # rotated states
    rotations.append(np.rot90(state, k=0).ravel().tolist())
    rotations.append(np.rot90(state, k=3).ravel().tolist())
    rotations.append(np.rot90(state, k=2).ravel().tolist())
    rotations.append(np.rot90(state, k=1).ravel().tolist())
    # mirrored and rotated states
    rotations.append(np.fliplr(np.rot90(state, k=0)).ravel().tolist())
    rotations.append(np.fliplr(np.rot90(state, k=1)).ravel().tolist())
    rotations.append(np.fliplr(np.rot90(state, k=2)).ravel().tolist())
    rotations.append(np.fliplr(np.rot90(state, k=3)).ravel().tolist())
    return rotations


def is_explored(state, explored):
    """Checks if input state is explored or of the rotations of input state is
    explored."""
    if state in explored:
        return True
    return False
