import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        self.sprites = []
        self.sprites.append(pygame.image.load("assets/cursor.png").convert_alpha())
        self.sprites.append(pygame.image.load("assets/pencil.png").convert_alpha())

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

    def normal(self):
        self.image = self.sprites[0]

    def pencil(self):
        self.image = self.sprites[1]