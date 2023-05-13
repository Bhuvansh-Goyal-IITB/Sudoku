import pygame
from sys import exit
from button import Button
from text import Text
from board import Board

class Game:
    def __init__(self):
        pygame.init()
        
        WIDTH = 600
        HEIGHT = 800
        self.FPS = 60

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def quit(self):
        pygame.quit()
        exit()

    def main_menu(self):
        menu_buttons = pygame.sprite.Group()
        visible = pygame.sprite.Group()

        sudoku_title = Text(30, "SUDOKU", "Black", (300, 200), [visible])
        
        play_button = Button((300, 400), (100, 50), "Play", 24, self.game, [menu_buttons, visible])
        quit_button = Button((300, 500), (100, 50), "Quit", 24, self.quit, [menu_buttons, visible])
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    self.game()

            self.screen.fill("White")

            menu_buttons.update()
            visible.draw(self.screen)
           
            pygame.display.update()
            self.clock.tick(self.FPS)
    
    def game(self):
        pygame.display.set_caption("Game")

        pencil_mode = False

        board = Board((300, 400), 60, 55) 

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.cell_group.update()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pencil_mode = not pencil_mode
                if event.type == pygame.KEYDOWN and (event.key >= 49 and event.key <= 57):
                    board.set_value(event.key - 48, pencil_mode)
                    board.test()

            board.highlight_wrong()
            board.select_check()
    
            board.cell_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.main_menu()