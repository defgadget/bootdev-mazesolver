import unittest

from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        print("Testing maxe create cells")
        num_cols = [1, 3, 12]
        num_rows = [1, 5, 10]
        
        for i in range(len(num_cols)):
            for j in range(len(num_rows)):
                m1 = Maze(0,0, num_rows[j], num_cols[i], 10, 10)
                self.assertEqual(
                    len(m1._cells),
                    num_cols[i]
                )
                self.assertEqual(
                    len(m1._cells[0]),
                    num_rows[j],
                )
                break

    def test_maze_break_entrance_and_exit(self):
        print("testing break entrance and exit")
        num_cols = 2
        num_rows = 2

        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m._cells[0][0].has_top_wall)
        self.assertFalse(m._cells[1][1].has_bottom_wall)

    def test_maze_reset_cells_visited(self):
        tests = [(4, 4), (5, 5)]
        print("testing reset cells")

        for test in tests:
            cols = test[0]
            rows = test[1]

            m = Maze(0, 0, rows, cols, 1, 1)
            for col in range(cols):
                for row in range(rows):
                    self.assertFalse(m._cells[col][row].visited)
        

if __name__ == "__main__":
    unittest.main()
