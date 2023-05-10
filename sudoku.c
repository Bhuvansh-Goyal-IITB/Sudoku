#include<stdio.h>

void init_board(int board[][9]);

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

void generate_board(int board[][9]) {

}

int main() {
    int board[9][9] = {
        {1, 2, 0, 4, 0, 6, 7, 8, 0},
        {3, 4, 5, 0, 0, 0, 0, 0, 0},
        {6, 0, 8, 9, 0, 0, 0, 0, 0}
    };
    int pos[2] = {0, 2};
    printf("%d", is_valid(board, pos, 9));
}