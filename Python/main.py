import pygame
from sys import exit
from button import Button
from text import Text

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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu()
            
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.main_menu()