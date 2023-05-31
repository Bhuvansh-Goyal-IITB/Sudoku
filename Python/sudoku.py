import random

def index_1d(row, col):
    return row * 9 + col


def count_empty(board):
    count = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                count += 1
    return count


def print_board(board):
    top = "╔═╤╦╗"
    mid_1 = "╟─┼╫╢"
    num = "║ │║║"
    mid_2 = "╠═╪╬╣"
    bottom = "╚═╧╩╝"

    for row in range(19):
        for col in range(37):
            current = None
            if row == 0:
                current = top
            elif row == 18:
                current = bottom
            elif row % 2 == 1:
                current = num
            elif row == 6 or row == 12:
                current = mid_2
            else:
                current = mid_1

            if col == 0:
                print(current[0], end="")
            elif col % 4 == 0 and col != 12 and col != 24 and col != 36:
                print(current[2], end="")
            elif col == 12 or col == 24:
                print(current[3], end="")
            elif col == 36:
                print(current[4])
            else:
                if current == num and col % 4 == 2:
                    row_index = int((row - 1) / 2)
                    col_index = int(((col / 2) - 1) / 2)
                    if not board[row_index][col_index]:
                        print(" ", end="")
                    else:
                        print(board[row_index][col_index], end="")
                else:
                    print(current[1], end="")


def eliminate_entropy(current_entropy, position, value):
    for row in range(9):
        index = index_1d(row, position[1])
        if value in current_entropy[index] and row != position[0]:
            current_entropy[index].remove(value)

    for col in range(9):
        index = index_1d(position[0], col)
        if value in current_entropy[index] and col != position[1]:
            current_entropy[index].remove(value)

    row_start = (position[0] // 3) * 3
    col_start = (position[1] // 3) * 3
    for row in range(3):
        for col in range(3):
            index = index_1d(row_start + row, col_start + col)
            if value in current_entropy[index] and (row_start + row, col_start + col) != position:
                current_entropy[index].remove(value)


def initialize_entropy(board, entropy):
    for row in range(9):
        for col in range(9):
            if board[row][col]:
                entropy.append({board[row][col]})
            else:
                entropy.append({_ for _ in range(1, 10)})

    for row in range(9):
        for col in range(9):
            if board[row][col] > 0:
                eliminate_entropy(entropy, (row, col), board[row][col])


def least_entropy_cell_pos(board, entropy):
    best_entropy = -1
    best_pos = None

    for row in range(9):
        for col in range(9):
            if not board[row][col]:
                index = index_1d(row, col)
                if best_entropy == -1 or best_entropy > len(entropy[index]):
                    best_entropy = len(entropy[index])
                    best_pos = (row, col)

    return best_pos


def sofa_box(board, entropy, best_entropy, row_index, col_index):
    frequency = [0 for _ in range(9)]
    missing = {_ for _ in range(1, 10)}

    best_count = best_entropy
    best_value = None

    for row in range(3):
        for col in range(3):
            pos = ((row_index * 3) + row, (col_index * 3) + col)
            index = index_1d(pos[0], pos[1])
            if not board[pos[0]][pos[1]]:
                for value in entropy[index]:
                    frequency[value - 1] += 1
            else:
                if board[pos[0]][pos[1]] not in missing:
                    print("Error")
                    print_board(board)
                missing.remove(board[pos[0]][pos[1]])

    for index, count in enumerate(frequency):
        if not count and ((index + 1) in missing):
            return -1
        if count < best_count and count:
            best_count = count
            best_value = index + 1

    return best_value, best_count


def sofa_row(board, entropy, best_entropy, row_index):
    frequency = [0 for _ in range(9)]
    missing = {_ for _ in range(1, 10)}

    best_count = best_entropy
    best_value = None

    for col in range(9):
        index = index_1d(row_index, col)
        if not board[row_index][col]:
            for value in entropy[index]:
                frequency[value - 1] += 1
        else:
            missing.remove(board[row_index][col])

    for index, count in enumerate(frequency):
        if not count and ((index + 1) in missing):
            return -1
        if count < best_count and count:
            best_count = count
            best_value = index + 1

    return best_value, best_count


def sofa_col(board, entropy, best_entropy, col_index):
    frequency = [0 for _ in range(9)]
    missing = {i for i in range(1, 10)}

    best_count = best_entropy
    best_value = None

    for row in range(9):
        index = index_1d(row, col_index)
        if not board[row][col_index]:
            for value in entropy[index]:
                frequency[value - 1] += 1
        else:
            missing.remove(board[row][col_index])

    for index, count in enumerate(frequency):
        if not count and ((index + 1) in missing):
            return -1
        if count < best_count and count:
            best_count = count
            best_value = index + 1

    return best_value, best_count


def solve_recursive(board, solutions, entropy, solve_random, branch_difficulty, count):
    best_pos = least_entropy_cell_pos(board, entropy)
    best_value = None
    best_set = None

    if best_pos is None:
        count += 1
        if solutions is not None:
            solutions.append([[val for val in row] for row in board])
        return count

    best_count = len(entropy[index_1d(best_pos[0], best_pos[1])])

    for i in range(3):
        for j in range(3):
            # print(count)
            best_box = sofa_box(board, entropy, best_count, i, j)
            if best_box == -1:
                return count
            elif best_box[0] is not None:
                best_count = best_box[1]
                best_value = best_box[0]
                best_set = (i, j)

    for i in range(9):
        best_row = sofa_row(board, entropy, best_count, i)
        if best_row == -1:
            return count
        elif best_row[0] is not None:
            best_count = best_row[1]
            best_value = best_row[0]
            best_set = (i, -1)

    for i in range(9):
        best_col = sofa_col(board, entropy, best_count, i)
        if best_col == -1:
            return count
        elif best_col[0] is not None:
            best_count = best_col[1]
            best_value = best_col[0]
            best_set = (-1, i)

    if best_count != 0:
        branch_difficulty[0] += pow(best_count - 1, 2) * 100

    if best_value is not None:
        if best_set[0] == -1:
            last_index = None

            for i in range(9):
                entropy_index = index_1d(i, best_set[1])
                if last_index is not None:
                    board[last_index][best_set[1]] = 0
                if best_value in entropy[entropy_index] and not board[i][best_set[1]]:
                    last_index = i
                    board[i][best_set[1]] = best_value
                    # print("Column")
                    # print_board(board)
                    new_entropy = [{value for value in entropy} for entropy in entropy]
                    eliminate_entropy(new_entropy, (i, best_set[1]), best_value)

                    count = solve_recursive(board, solutions, new_entropy, solve_random, branch_difficulty, count)
                    if count > 1:
                        board[last_index][best_set[1]] = 0
                        return count
            if last_index is not None:
                board[last_index][best_set[1]] = 0
            return count
        elif best_set[1] == -1:
            last_index = None
            for i in range(9):
                entropy_index = index_1d(best_set[0], i)
                if last_index is not None:
                    board[best_set[0]][last_index] = 0
                if best_value in entropy[entropy_index] and not board[best_set[0]][i]:
                    last_index = i
                    board[best_set[0]][i] = best_value
                    # print("Row")
                    # print_board(board)
                    new_entropy = [{value for value in entropy} for entropy in entropy]
                    eliminate_entropy(new_entropy, (best_set[0], i), best_value)
                    count = solve_recursive(board, solutions, new_entropy, solve_random, branch_difficulty, count)
                    if count > 1:
                        board[best_set[0]][last_index] = 0
                        return count
            if last_index is not None:
                board[best_set[0]][last_index] = 0
            return count
        else:
            last_pos = None
            for i in range(3):
                for j in range(3):
                    if last_pos is not None:
                        board[last_pos[0]][last_pos[1]] = 0
                    entropy_index = index_1d(best_set[0] * 3 + i, best_set[1] * 3 + j)
                    if best_value in entropy[entropy_index] and not board[best_set[0] * 3 + i][best_set[1] * 3 + j]:
                        last_pos = (best_set[0] * 3 + i, best_set[1] * 3 + j)
                        board[last_pos[0]][last_pos[1]] = best_value
                        # print("Box")
                        # print_board(board)
                        new_entropy = [{value for value in entropy} for entropy in entropy]
                        eliminate_entropy(new_entropy, last_pos, best_value)
                        count = solve_recursive(board, solutions, new_entropy, solve_random, branch_difficulty, count)
                        if count > 1:
                            board[last_pos[0]][last_pos[1]] = 0
                            return count
            if last_pos is not None:
                board[last_pos[0]][last_pos[1]] = 0
            return count
    else:
        # if board[best_pos[0]][best_pos[1]] != 0:
        #     return count
        value_list = [val for val in entropy[index_1d(best_pos[0], best_pos[1])]]
        if solve_random:
            random.shuffle(value_list)
        for value in value_list:
            board[best_pos[0]][best_pos[1]] = value
            # print("Best pos")
            # print(count)
            # print_board(board)
            new_entropy = [{value for value in entropy} for entropy in entropy]
            eliminate_entropy(new_entropy, best_pos, value)
            # print(new_entropy)
            count = solve_recursive(board, solutions, new_entropy, solve_random, branch_difficulty, count)
            if count > 1:
                board[best_pos[0]][best_pos[1]] = 0
                return count

        board[best_pos[0]][best_pos[1]] = 0
        return count


def solve(board, solutions, print_result, solve_random):
    initial_entropy = []
    initialize_entropy(board, initial_entropy)

    branch_difficulty = [0]
    empty = count_empty(board)

    num_solutions = solve_recursive(board, solutions, initial_entropy, solve_random, branch_difficulty, 0)

    if print_result:
        if num_solutions > 1:
            print("More than one solutions")
            print("Solution 1:")
            print_board(solutions[0])
        elif num_solutions == 0:
            print("No solutions found")
        else:
            print(f"Difficulty: {branch_difficulty[0] + empty}\n")
            print("Solution:")
            print_board(solutions[0])

    return branch_difficulty[0] + empty, num_solutions

def string_to_board(string):
    board = [[0 for _ in range(9)] for _ in range(9)]
    for index, char in enumerate(string):
        if char == ".":
            board[index // 9][index % 9] = 0
        else:
            if char not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return False
            board[index // 9][index % 9] = int(char)

    return solve(board, None, False, False)[1] == 1