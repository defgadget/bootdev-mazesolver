from maze import Maze
from graphics import Window


def main():
    win = Window(800, 600)
    m = Maze(0, 0, 12, 16, 50, 50, win, 12)
    m.solve()
    win.wait_for_close()

main()


