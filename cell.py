from graphics import Point, Line
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
        self.visited = False

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
