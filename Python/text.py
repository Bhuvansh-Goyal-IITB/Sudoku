import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, size, text, color, pos, groups, AA=1):
        super().__init__(groups)
        self.font = pygame.font.Font("assets/FiraCode-Regular.ttf", size)
        self.image = self.font.render(text, AA, color)
        self.rect = self.image.get_rect(center=pos)
