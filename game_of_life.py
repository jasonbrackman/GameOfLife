"""
- Need a 2d array defining the horizontal / vertical of the board
--> User should be able to decide how large the board is.

- Each square can be "alive" or "dead"

- Rules:
    A live cell with fewer than 2 live neighbors dies.
    A live cell with more than 3 live neighbors dies.
    A live cell with 2 or 3 live neighbors lives on to the next generation.
    A dead cell with exactly 3 neighbors becomes a live cell.

"""
import copy
import random

random.seed(12000)


class Cell(object):
    alive = 'o'
    dead = '.'
    infected = 'x'
    food = '#'


    def __init__(self):
        self.state = self.get_random_state()
        self.time_to_live = 5

    @staticmethod
    def get_random_state():
        result = random.choice([Cell.alive] * 3 +
                               [Cell.food] * 1 +
                               [Cell.dead] * 10)
        return result

    @property
    def is_alive(self):
        if self.state == self.alive:
            return True
        return False

    @property
    def is_dead(self):
        if self.state == self.dead:
            return True
        return False


class Gameboard(object):
    def __init__(self, rows, coloumns):
        self.rows = rows
        self.coloumns = coloumns
        self.board = dict()
        self.setup_board()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for key in self.board.keys():
                if self.board[key].state != other.board[key].state:
                    return False
        return True

    def setup_board(self):
        for row in range(self.rows):
            for coloumn in range(self.coloumns):
                self.board[(row, coloumn)] = Cell()

    def print_life(self):

        lines = list()

        for row in range(self.rows):
            cells_for_row = list()
            for coloumn in range(self.coloumns):
                cells_for_row.append(self.board[(row, coloumn)].state)
            lines.append(cells_for_row)

        for line in lines:
            print(' '.join(line))
        print("\n")

    def _update_lifespan(self, v, counter):
        packed_values = {"state": v.state, "time_to_live": v.time_to_live}
        if v.is_alive:
            if v.time_to_live <= 0:
                packed_values["state"] = v.dead

            elif counter < 2 or counter > 3:
                # overcrowding causes less life
                packed_values["time_to_live"] -= 2

            else:
                # normal aging
                packed_values["time_to_live"] -= 1

        elif v.is_dead and counter == 3:
            # new birth
            packed_values["state"] = v.alive
            packed_values["time_to_live"] = 3

        return packed_values

    def play_life(self):
        new_board = self.board
        for k, v in self.board.items():
            counter = 0
            _row, _coloumn = k

            # get current state of the cell
            for row in range(_row - 1, _row + 2):
                for coloumn in range(_coloumn - 1, _coloumn + 2):
                    if not (row, coloumn) == k:
                        if (row, coloumn) in self.board.keys():
                            if self.board[(row, coloumn)].is_alive:
                                counter += 1

            # TODO: Have the cell travel for food
            # applying all changes to a new_board since all state changes happen together
            # Don't want to change the state of a cell without all cells knowing what to do at the same time.
            values = self._update_lifespan(v, counter)
            new_board[k].state = values["state"]
            new_board[k].time_to_live = values["time_to_live"]

        self.board = new_board


if __name__ == "__main__":
    num = 0
    go = Gameboard(10, 12)
    go.print_life()
    temp_go = copy.deepcopy(go)
    while True:
        go.play_life()
        num += 1
        if go == temp_go:
            if num >= 10:
                print(num)
                break
        else:
            temp_go = copy.deepcopy(go)
            go.print_life()