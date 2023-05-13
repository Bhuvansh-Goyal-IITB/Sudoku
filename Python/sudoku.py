import random

class Sudoku:
    def __init__(self, blanks):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        self.generate_board(blanks)
        self.unsolved_board = [[self.board[i][j] for i in range(9)] for j in range(9)]

        self.solve_board()
        self.solved_board = [[self.board[i][j] for i in range(9)] for j in range(9)]

    def new_board(self, blanks):
        self.__init__(blanks)

    def solve_board(self):
        def inner(current_pos):
            for i in range(1, 10):
                if (self.is_valid(current_pos, i)):
                    self.board[current_pos[0]][current_pos[1]] = i 

                    next_empty_pos = self.next_empty_cell()
                    if next_empty_pos is None:
                        return True

                    if inner(next_empty_pos) == False:
                        continue
                    else:
                        return True
            
            self.board[current_pos[0]][current_pos[1]] = 0
            return False

        first_empty = self.next_empty_cell()
        inner(first_empty)

    def generate_board(self, blanks):
        stop = random.randint(1, 5000)
        
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        iteration = self.fill_board(stop)
        while (iteration < stop):
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            iteration = self.fill_board(stop)
        
        if not self.remove_random(blanks):
            self.generate_board(blanks)

    def print_board(self, board):
        for row in range(9):
            for col in range(9):
                print(f"{board[row][col]} ", end="")
            print("") 

    def count_blanks(self):
        count = 0
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0: 
                    count += 1
        return count

    def remove_random(self, blanks):
        iteration = 0
        filled_pos = []
        while self.count_blanks() < blanks:
            filled_pos.clear()
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] != 0:
                        filled_pos.append((i, j))
            random_pos = random.choice(filled_pos)

            current_value = self.board[random_pos[0]][random_pos[1]]
            self.board[random_pos[0]][random_pos[1]] = 0

            if not self.unique_solution():
                self.board[random_pos[0]][random_pos[1]] = current_value

            iteration += 1
            print(f"iteration: {iteration}")
            if iteration > 70:
                return False
        return True

    def is_valid(self, pos, value):
        for row in range(9):
            if (self.board[row][pos[1]] == value) and (row != pos[0]):
                return False
        
        for col in range(9):
            if (self.board[pos[0]][col] == value) and (col != pos[1]):
                return False

        row_start = int(pos[0] / 3) * 3
        col_start = int(pos[1] / 3) * 3
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if (self.board[row][col] == value) and ((row, col) != pos):
                    return False
                
        return True
    
    def next_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        
        return None
    
    def fill_board(self, stop):
        def inner(current_pos, counter, values):
            for i in range(9):
                if (self.is_valid(current_pos, values[i])):
                    self.board[current_pos[0]][current_pos[1]] = values[i]

                    next_empty_pos = self.next_empty_cell()
                    if next_empty_pos is None:
                        counter += 1
                        if not (counter > stop - 1):
                            self.board[current_pos[0]][current_pos[1]] = 0
                        return counter

                    random.shuffle(values)

                    counter = inner(next_empty_pos, counter, values)

                    if counter > stop - 1:
                        return counter
            
            self.board[current_pos[0]][current_pos[1]] = 0
            return counter

        first_empty = self.next_empty_cell()
        initial_values = [i for i in range(1, 10)]
        random.shuffle(initial_values)

        return inner(first_empty, 0, initial_values)

    def unique_solution(self):
        def inner(current_pos, counter):
            for i in range(1, 10):
                if (self.is_valid(current_pos, i)):
                    self.board[current_pos[0]][current_pos[1]] = i 

                    next_empty_pos = self.next_empty_cell()
                    if next_empty_pos is None:
                        counter += 1
                        self.board[current_pos[0]][current_pos[1]] = 0
                        return counter

                    counter = inner(next_empty_pos, counter)

                    if counter > 1:
                        self.board[current_pos[0]][current_pos[1]] = 0
                        return counter
            
            self.board[current_pos[0]][current_pos[1]] = 0
            return counter

        first_empty = self.next_empty_cell()
        return inner(first_empty, 0) == 1
