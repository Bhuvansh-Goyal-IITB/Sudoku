import pygame
from text import Text

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_center, size, text, font_size, on_click, _groups):
        super().__init__(_groups)
        self.on_click = on_click

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = pos_center

        self.image.fill("White")

        pygame.draw.rect(self.image, "Black", self.image.get_rect(), width=4)

        self.text = pygame.sprite.Group()
        Text(font_size, text, "Black", (size[0]/2, size[1]/2), [self.text])

        self.text.draw(self.image)

    def check_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                if self.on_click:
                    self.on_click()
            else:
                self.image.fill("Grey")
                pygame.draw.rect(self.image, "Black", self.image.get_rect(), width=4)
                self.text.draw(self.image)
        else:
            self.image.fill("White")
            pygame.draw.rect(self.image, "Black", self.image.get_rect(), width=4)
            self.text.draw(self.image)
        
    def update(self):
        self.check_mouse()
