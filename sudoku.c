#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int count_blanks(const int board[][9]);

void print_board(int board[][9]);

int is_valid(int board[][9], int position[], int value);

int next_empty_cell(int board[][9]);

void shuffle(int array[], int size);

int fill_board(int board[][9], int current_pos[], int counter, const int values[], int stop);

void remove_random(int board[][9], int blanks);

void generate_board(int board[][9]);

int solve_board_inner(int board[][9], int current_pos[]);

int solve_board(int board[][9]);

int count_solutions_inner(int board[][9], int current_pos[], int counter, int count_till, int print_solutions);

int count_solutions(int board[][9], int count_till, int print_solutions);

int main() {
    srand(time(NULL));
    
    int board[9][9] = {0};
    generate_board(board);
    print_board(board);
    puts("");
    remove_random(board, 40);
    print_board(board);
    puts("");
    int count = count_solutions(board, -1, 0);
    solve_board(board);
    print_board(board);

    printf("\n%d", count);
}

void generate_board(int board[][9]) {
    int ans = 0;
    int stop = 1 + rand() % 200;

    int temp = next_empty_cell(board);
    int next_empty_pos[2] = {temp / 10, temp % 10};

    int initial[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    shuffle(initial, 9);

    do
    {
        for (size_t i = 0; i < 9; i++) {
            for (size_t j = 0; j < 9; j++) {
                board[i][j] = 0;
            }
        }
        ans = fill_board(board, next_empty_pos, 0, initial, stop);
    } while (ans < stop);
}

void remove_random(int board[][9], int blanks) {
    while (count_blanks(board) < blanks) {
        int random, row, column;
        do
        {
            random = rand() % 81;
            row = random / 9;
            column = random % 9;
        } while (board[row][column] == 0);
        
        int value = board[row][column];
        board[row][column] = 0;

        if (count_solutions(board, 2, 0) > 1) {
            board[row][column] = value;
        }
    }    
}

int solve_board_inner(int board[][9], int current_pos[]) {
    for (size_t i = 1; i <= 9; i++) {
        if (is_valid(board, current_pos, i)) {
            
            board[current_pos[0]][current_pos[1]] = i;

            int temp = next_empty_cell(board);
            int next_empty_pos[2] = {temp / 10, temp % 10};
            if (temp == -1) {
                return 1;
            }

            if (solve_board_inner(board, next_empty_pos) == -1) {
                continue;
            } else {
                return 1;
            }
        }
    }
    
    board[current_pos[0]][current_pos[1]] = 0;
    return -1;
}

int solve_board(int board[][9]) {
    int temp = next_empty_cell(board);
    int next_empty_pos[2] = {temp / 10, temp % 10};
    return solve_board_inner(board, next_empty_pos);
}

int count_solutions_inner(int board[][9], int current_pos[], int counter, int count_till, int print_solutions) {
    for (size_t i = 1; i <= 9; i++) {
        if (is_valid(board, current_pos, i)) {
            board[current_pos[0]][current_pos[1]] = i;

            int temp = next_empty_cell(board);
            int next_empty_pos[2] = {temp / 10, temp % 10};
            if ((temp == -1)) {
                counter += 1;

                if (print_solutions) {
                    print_board(board);
                    puts("");
                }

                board[current_pos[0]][current_pos[1]] = 0;
                return counter;
            }

            counter = count_solutions_inner(board, next_empty_pos, counter, count_till, print_solutions);

            if (counter > (count_till-1)) {
                if (!(count_till == -1)) {
                    board[current_pos[0]][current_pos[1]] = 0;
                    return counter;
                } 
            }
        }
    }
    
    board[current_pos[0]][current_pos[1]] = 0;
    return counter;
}

int count_solutions(int board[][9], int count_till, int print_solutions) {
    int temp = next_empty_cell(board);
    int next_empty_pos[2] = {temp / 10, temp % 10};
    return count_solutions_inner(board, next_empty_pos, 0, count_till, print_solutions);
}

int count_blanks(const int board[][9]) {
    int count = 0;
    for (size_t i = 0; i < 9; i++) {
       for (size_t j = 0; j < 9; j++) {
            if (board[i][j] == 0) count++;
       }    
    }
    return count;
}

void print_board(int board[][9]) {
    for (size_t row = 0; row < 9; row++) {
        for (size_t column = 0; column < 9; column++) {
            printf("%d ", board[row][column]);     
        }
        puts("");
    }
}

int is_valid(int board[][9], int position[], int value) {
    for (size_t row = 0; row < 9; row++) {
        if ((board[row][position[1]] == value) && (row != position[0])) {
            return 0;
        }
    }

    for (size_t column = 0; column < 9; column++) {
        if ((board[position[0]][column] == value) && (column != position[1])) {
            return 0;
        }
    }
    
    for (size_t row = (position[0] / 3) * 3; row < ((position[0] / 3) * 3) + 3; row++) {
        for (size_t column = (position[1] / 3) * 3; column < ((position[1] / 3) * 3) + 3; column++) {
            if ((board[row][column] == value) && !((column == position[1]) && (row == position[0]))) {
                return 0;
            } 
        }
    }
    
    return 1;
}

int next_empty_cell(int board[][9]) {
    for (size_t row = 0; row < 9; row++) {
        for (size_t column = 0; column < 9; column++) {
            if (board[row][column] == 0) {
                return row * 10 + column;
            }       
        }
    }
    return -1;
}

void shuffle(int array[], int size) {
    for (size_t i = 0; i < size; i++) {
        int j;
        do
        {
            j = rand() % size;
        } while (i == j);
        
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    
}

int fill_board(int board[][9], int current_pos[], int counter, const int values[], int stop) {
    for (size_t i = 0; i < 9; i++) {
        if (is_valid(board, current_pos, values[i])) {
            board[current_pos[0]][current_pos[1]] = values[i];

            int temp = next_empty_cell(board);
            int next_empty_pos[2] = {temp / 10, temp % 10};
            if ((temp == -1)) {
                counter += 1;
                if (!(counter > (stop-1))) {
                    board[current_pos[0]][current_pos[1]] = 0;
                }
                return counter;
            }

            int new_vals[9];
            for (size_t i = 0; i < 9; i++) { 
                new_vals[i] = values[i];
            }
            shuffle(new_vals, 9);

            counter = fill_board(board, next_empty_pos, counter, new_vals, stop);

            if (counter > (stop-1)) {
                return counter;
            }
        }
    }
    
    board[current_pos[0]][current_pos[1]] = 0;
    return counter;
}
