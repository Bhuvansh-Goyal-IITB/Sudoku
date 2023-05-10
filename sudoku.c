#include<stdio.h>

void init_board(int board[][9]);

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

int main() {

}