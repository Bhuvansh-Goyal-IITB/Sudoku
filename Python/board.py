import pygame
from sudoku import *
from cell import Cell
from typing import List

class Board:
    def __init__(self, pos_center, cell_width, board_str, normal_font_size, pencil_font_size, border):
        def extract(string, index):
            if string[index] == ".":
                return 0
            else:
                return int(string[index])

        self.board = [[extract(board_str, row * 9 + col) for col in range(9)] for row in range(9)]
        self.cell_group = pygame.sprite.Group()

        self.cells: List[List[Cell]] = [[0 for i in range(9)] for j in range(9)] 

        initial_pos = [(pos_center[0] - ((4 * cell_width) - 3 * border)), (pos_center[1] - ((4 * cell_width) - 3 * border))]
        current_pos = [initial_pos[0], initial_pos[1]] 

        self.current_selected_cell = None

        self.moves = []

        for row in range(9):
            if row == 0:
                current_pos[1] = initial_pos[1]
            elif row == 3 or row == 6:
                current_pos[1] += cell_width
            else:
                current_pos[1] += cell_width - border

            for col in range(9):
                if col == 0:
                    current_pos[0] = initial_pos[0]
                elif col == 3 or col == 6:
                    current_pos[0] += cell_width
                else:
                    current_pos[0] += cell_width - border

                self.cells[row][col] = Cell(current_pos, cell_width, self.board[row][col], border, normal_font_size, pencil_font_size, [self.cell_group])
         
    def set_value(self, value, pencil):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].initial_value:
                    continue
                if self.cells[row][col].selected:
                    if pencil:
                        self.board[row][col] = 0
                        self.cells[row][col].pencil(value)

                    else:
                        pencil_values = [i for i in self.cells[row][col].pencil_values]

                        neighbour_pencil_values = []

                        for i in range(9):
                            if i != row:
                                neighbour_pencil_values.append([(i, col), [_ for _ in self.cells[i][col].pencil_values]])

                        for j in range(9):
                            if j != col:
                                neighbour_pencil_values.append([(row, j), [_ for _ in self.cells[row][j].pencil_values]])

                        row_start = int(row / 3) * 3
                        col_start = int(col / 3) * 3
                        for i in range(row_start, row_start + 3):
                            for j in range(col_start, col_start + 3):
                                if row != i and col != j:
                                    neighbour_pencil_values.append([(i, j), [_ for _ in self.cells[i][j].pencil_values]])

                        self.moves.append([(row, col), self.board[row][col], pencil_values, neighbour_pencil_values])
                        if self.board[row][col] == value:
                            self.board[row][col] = 0
                        else:
                            self.board[row][col] = value
                            self.check_pencil_values((row, col), value)

                        self.cells[row][col].set_value(value)

    def undo(self):
        if not len(self.moves):
            return

        row, col = self.moves[-1][0]
        value = self.moves[-1][1]
        pencil_values = self.moves[-1][2]
        neighbours = self.moves[-1][3]

        self.moves.pop()

        self.cells[row][col].clear_cell()
        
        if value == 0:
            for pencil_value in pencil_values:
                self.cells[row][col].pencil(pencil_value)

            for neighbour in neighbours:
                _row, _col = neighbour[0]
                values = neighbour[1]

                if self.board[row][col] in values:
                    self.cells[_row][_col].pencil(self.board[row][col])
        else:
            self.cells[row][col].set_value(value) 

        self.board[row][col] = self.cells[row][col].current_value

    def check_pencil_values(self, pos, value):
        row, col = pos
        for i in range(9):
            if value in self.cells[i][col].pencil_values and (i != row):
                self.cells[i][col].pencil(value)

        for j in range(9):
            if value in self.cells[row][j].pencil_values and (j != col):
                self.cells[row][j].pencil(value)

        row_start = int(row / 3) * 3
        col_start = int(col / 3) * 3
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if value in self.cells[i][j].pencil_values and ((row, col) != (i, j)):
                    self.cells[i][j].pencil(value)

    def reset_color(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].current_color = "White"

    def select_cell(self):
        cell_selected = False
        for row in range(9):
            for col in range(9):
                if not cell_selected and self.cells[row][col].rect.collidepoint(pygame.mouse.get_pos()):
                    self.cells[row][col].selected = True
                    self.current_selected_cell = self.cells[row][col]
                    cell_selected = True
                else:
                    self.cells[row][col].selected = False
        if not cell_selected:
            self.current_selected_cell = None
    
    def handle_highlighting(self):
        if self.current_selected_cell is not None:
            selected_value = self.current_selected_cell.current_value

            if selected_value != 0:
                for row in range(9):
                    for col in range(9):
                        for i in range(9):
                            if (self.board[i][col] == selected_value) and (i != row):
                                self.cells[i][col].current_color = "#d3d3d3"
                            
                        for j in range(9):
                            if (self.board[row][j] == selected_value) and (j != col):
                                self.cells[row][j].current_color = "#d3d3d3"
                            
                        row_start = int(row / 3) * 3
                        col_start = int(col / 3) * 3
                        for i in range(row_start, row_start + 3):
                            for j in range(col_start, col_start + 3):
                                if (self.board[i][j] == selected_value) and ((row, col) != (i, j)):
                                    self.cells[i][j].current_color = "#d3d3d3"
            
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if value:
                    for i in range(9):
                        if (self.board[i][col] == value) and (i != row):
                            self.cells[i][col].current_color = "#FF7276"
                        
                    for j in range(9):
                        if (self.board[row][j] == value) and (j != col):
                            self.cells[row][j].current_color = "#FF7276"
                        
                    row_start = int(row / 3) * 3
                    col_start = int(col / 3) * 3
                    for i in range(row_start, row_start + 3):
                        for j in range(col_start, col_start + 3):
                            if (self.board[i][j] == value) and ((row, col) != (i, j)):
                                self.cells[i][j].current_color = "#FF7276"

        if self.current_selected_cell is not None:
            self.current_selected_cell.current_color = "#b6b6b6"
    
    def update_cells(self):
        self.cell_group.update()
    
    def draw_cells(self, surface):
        self.cell_group.draw(surface)
