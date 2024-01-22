import random
import time
from cell import Cell

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win
        if seed:
            random.seed(seed)
        else:
            random.seed(0)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(0, 0)
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, col, row):
        current_col, current_row = col, row
        current_cell = self._cells[current_col][current_row]
        current_cell.visited = True
        while True:
            to_visit = []

            self._get_unvisited_cells(to_visit, col, row)

            if len(to_visit) == 0:
                self._draw_cell(col, row)
                return

            next_col, next_row = random.choice(to_visit)
            next_cell = self._cells[next_col][next_row]

            top = next_row == current_row - 1
            bottom = next_row == current_row + 1
            left = next_col == current_col - 1
            right = next_col == current_col + 1

            if top:
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            if bottom:
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            if left:
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            if right:
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False

            self._break_walls_r(next_col, next_row)
            

    def _get_unvisited_cells(self, to_visit, col, row):
        if col > 0 and not self._cells[col - 1][row].visited:
            to_visit.append((col - 1, row))
        if col < self._num_cols - 1 and not self._cells[col + 1][row].visited:
            to_visit.append((col + 1, row))
        if row > 0 and not self._cells[col][row - 1].visited:
            to_visit.append((col, row - 1))
        if row < self._num_rows - 1 and not self._cells[col][row + 1].visited:
            to_visit.append((col, row + 1))

    def _reset_cells_visited(self):
        for col in range(len(self._cells)):
            for row in range(len(self._cells[0])):
                self._cells[col][row].visited = False

    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self._num_rows)] for _ in range(self._num_cols)]
        for col in range(len(self._cells)):
            for row in range(len(self._cells[col])):
                self._draw_cell(col, row)

    def _draw_cell(self, col, row):
        start_x = self._x1
        start_y = self._y1

        top_left_x = start_x + (col * self._cell_size_x)
        top_left_y = start_y + (row * self._cell_size_y)
        bottom_right_x = start_x + (col * self._cell_size_x) + self._cell_size_x
        bottom_right_y = start_y + (row * self._cell_size_y) + self._cell_size_y

        current_cell = self._cells[col][row]
        current_cell.draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self._animate()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, col, row):
        self._animate()
        current_cell = self._cells[col][row]
        current_cell.visited = True
        if col == self._num_cols - 1 and row == self._num_rows - 1:
            return True

        if (
            col > 0
            and not current_cell.has_left_wall
            and not self._cells[col - 1][row].visited
        ):
            current_cell.draw_move(self._cells[col - 1][row])
            if self._solve_r(col - 1, row):
                return True
            else:
                current_cell.draw_move(self._cells[col - 1][row], True)
        if (
            col < self._num_cols - 1
            and not current_cell.has_right_wall
            and not self._cells[col + 1][row].visited
        ):
            current_cell.draw_move(self._cells[col + 1][row])
            if self._solve_r(col + 1, row):
                return True
            else:
                current_cell.draw_move(self._cells[col + 1][row], True)
        if (
            row > 0
            and not current_cell.has_top_wall
            and not self._cells[col][row - 1].visited
        ):
            current_cell.draw_move(self._cells[col][row - 1])
            if self._solve_r(col, row - 1):
                return True
            else:
                current_cell.draw_move(self._cells[col][row - 1], True)
        if (
            row < self._num_rows - 1
            and not current_cell.has_bottom_wall
            and not self._cells[col][row + 1].visited
        ):
            current_cell.draw_move(self._cells[col][row + 1])
            if self._solve_r(col, row + 1):
                return True
            else:
                current_cell.draw_move(self._cells[col][row + 1], True)
        return False

    def _animate(self):
        if self._win:
            self._win.redraw()
        time.sleep(.04)
