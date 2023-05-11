#include<stdio.h>
#include<stdlib.h>
#include<time.h>

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
    for (size_t i = 1; i <= 9; i++) {
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

int solve_board(int board[][9], int current_pos[]) {
    for (size_t i = 1; i <= 9; i++) {
        if (is_valid(board, current_pos, i)) {
            
            board[current_pos[0]][current_pos[1]] = i;

            int temp = next_empty_cell(board);
            int next_empty_pos[2] = {temp / 10, temp % 10};
            if (temp == -1) {
                return 1;
            }

            if (solve_board(board, next_empty_pos) == -1) {
                continue;
            } else {
                return 1;
            }
        }
    }
    
    board[current_pos[0]][current_pos[1]] = 0;
    return -1;
}

int count_solutions(int board[][9], int current_pos[], int counter, int count_till, int print_solutions) {
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

            counter = count_solutions(board, next_empty_pos, counter, count_till, print_solutions);

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

int main() {
    srand(time(NULL));

    int board[9][9] = {2, 9, 5, 7, 4, 3, 8, 6, 1, 4, 3, 1, 8, 6, 5, 9, 0, 0, 8, 7, 6, 1, 9, 2, 5, 4, 3, 3, 8, 7, 4, 5, 9, 2, 1, 6, 6, 1, 2, 3, 8, 7, 4, 9, 5, 5, 4, 9, 2, 1, 6, 7, 3, 8, 7, 6, 3, 5, 3, 4, 1, 8, 9, 9, 2, 8, 6, 7, 1, 3, 5, 4, 1, 5, 4, 9, 3, 8, 6, 0, 0};
    int zeros[9][9] = {0};
    generate_board(zeros);
    print_board(zeros);
}