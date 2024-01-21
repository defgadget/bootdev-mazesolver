from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.wm_title("Some title")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(height=height, width=width)
        self.canvas.pack()
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack()

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 0
        self._y1 = 0
        self._x2 = 0
        self._y2 = 0
        self._win = win

    def get_cell_center(self):
        center_x = (self._x1 + self._x2) / 2
        center_y = (self._y1 + self._y2) / 2
        return (center_x, center_y)

    def draw_move(self, to_cell, undo=False):
        fill_color = "red"
        if undo:
            fill_color = "gray"

        current_center = self.get_cell_center()
        to_cell_center = to_cell.get_cell_center()
        p1 = Point(current_center[0], current_center[1])
        p2 = Point(to_cell_center[0], to_cell_center[1])
        line = Line(p1, p2)

        if self._win:
            self._win.draw_line(line, fill_color)

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        fill_color = "black"

        top_left = Point(0, self._y1)
        bottom_left = Point(0, self._y2)
        left_wall = Line(top_left, bottom_left)
        
        top_right = Point(self._x2, self._y1)
        bottom_right = Point(self._x2, self._y2)
        right_wall = Line(top_right, bottom_right)

        top_left = Point(self._x1, 0)
        top_right = Point(self._x2, 0)
        top_wall = Line(top_left, top_right)

        bottom_left = Point(self._x1, self._y2)
        bottom_right = Point(self._x2, self._y2)
        bottom_wall = Line(bottom_left, bottom_right)
        
        if self.has_left_wall:
            fill_color = "black"
        else:
            fill_color = "white"
        if self._win:
            self._win.draw_line(left_wall, fill_color)

        if self.has_right_wall:
            fill_color = "black"
        else:
            fill_color = "white"
        if self._win:
            self._win.draw_line(right_wall, fill_color)

        if self.has_top_wall:
            fill_color = "black"
        else:
            fill_color = "white"
        if self._win:
            self._win.draw_line(top_wall, fill_color)

        if self.has_bottom_wall:
            fill_color = "black"
        else:
            fill_color = "white"
        if self._win:
            self._win.draw_line(bottom_wall, fill_color)

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
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(entrance, 0, 0)
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell(exit, self._num_cols - 1, self._num_rows - 1)

    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self._num_rows)] for _ in range(self._num_cols)]
        for col in range(len(self._cells)):
            for row in range(len(self._cells[col])):
                cell = self._cells[col][row]
                self._draw_cell(cell, col, row)

    def _draw_cell(self, cell, col, row):
        start_x = self._x1
        start_y = self._y1

        top_left_x = start_x + (col * self._cell_size_x)
        top_left_y = start_y + (row * self._cell_size_y)
        bottom_right_x = start_x + (col * self._cell_size_x) + self._cell_size_x
        bottom_right_y = start_y + (row * self._cell_size_y) + self._cell_size_y

        cell.draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
        time.sleep(.05)

def main():
    win = Window(800, 600)
    Maze(0, 0, 12, 16, 50, 50, win)
    win.wait_for_close()

main()
