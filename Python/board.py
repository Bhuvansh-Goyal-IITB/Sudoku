import pygame
from sudoku import Sudoku
from cell import Cell

class Board:
    def __init__(self, pos_center, cell_width, blanks):
        self.sudoku = Sudoku(blanks)
        self.cell_group = pygame.sprite.Group()

        self.cells = [[0 for i in range(9)] for j in range(9)] 

        initial_pos = [(pos_center[0] - ((4 * cell_width) - 6)), (pos_center[1] - ((4 * cell_width) - 6))]
        current_pos = [initial_pos[0], initial_pos[1]] 
        for row in range(9):
            if row == 0:
                current_pos[1] = initial_pos[1]
            elif row == 3 or row == 6:
                current_pos[1] += cell_width
            else:
                current_pos[1] += cell_width - 2

            for col in range(9):
                if col == 0:
                    current_pos[0] = initial_pos[0]
                elif col == 3 or col == 6:
                    current_pos[0] += cell_width
                else:
                    current_pos[0] += cell_width - 2

                self.cells[row][col] = Cell(current_pos, cell_width, self.sudoku.unsolved_board[row][col], [self.cell_group], self.sudoku.solved_board[row][col])
         
    def set_value(self, value, pencil):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].selected:
                    if pencil:
                        self.cells[row][col].pencil(value, 24)
                    else:
                        self.cells[row][col].set_value(value, 30)
                    self.cells[row][col].select()
    
    def test(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].selected:
                    self.cells[row][col].select()
                else:
                    self.cells[row][col].deselect()
    def select_check(self):
        count = 0
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].selected:
                    count += 1
                if count > 1:
                    self.cells[row][col].deselect()
                    return
    
    def highlight_wrong(self):
        for i in range(9):
            for j in range(9):
                if (self.cells[i][j].current_value == 0):
                    continue
                

                pos = (i, j)
                value = self.cells[i][j].current_value

                for row in range(9):
                    if (self.cells[row][pos[1]].current_value == value) and (row != pos[0]):
                        self.cells[row][pos[1]].draw_cell("#FFCCCB")
                        # print(f"{row}, {pos[1]}")
                
                for col in range(9):
                    if (self.cells[pos[0]][col].current_value == value) and (col != pos[1]):
                        self.cells[pos[0]][col].draw_cell("#FFCCCB")
                        # print(f"{pos[0]}, {pos[1]}")

                row_start = int(pos[0] / 3) * 3
                col_start = int(pos[1] / 3) * 3
                for row in range(row_start, row_start + 3):
                    for col in range(col_start, col_start + 3):
                        if (self.cells[row][col].current_value == value) and ((row, col) != pos):
                            self.cells[row][col].draw_cell("#FFCCCB")
                            # print(f"{row}, {col}")