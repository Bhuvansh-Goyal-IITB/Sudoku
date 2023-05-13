import pygame
from sys import exit

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
    
    def game(self):
        pygame.display.set_caption("Game")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and (event.key <= 57 and event.key >= 49):
                    print(event.key - 48)

            pygame.display.update()
            self.clock.tick(self.FPS)

