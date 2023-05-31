from typing import Any
import pygame
from text import Text

class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_center, cell_width, cell_value, border, normal_font_size, pencil_font_size, groups):
        super().__init__(groups)
        self.cell_width = cell_width
        self.pencil_values = []

        self.border = border

        self.current_color = "White"

        self.initial_value = cell_value
        self.current_value = cell_value

        self.selected = False

        self.image = pygame.Surface((cell_width, cell_width))
        
        self.rect = self.image.get_rect()
        self.rect.center = pos_center
        
        self.text = pygame.sprite.Group()

        self.normal_font_size = normal_font_size
        self.pencil_font_size = pencil_font_size

        if self.initial_value != 0:
            Text(normal_font_size, str(cell_value), "Black", (cell_width/2, cell_width/2), [self.text])
        
        self.draw_cell()


    def draw_cell(self):
        self.image.fill(self.current_color)
        pygame.draw.rect(self.image, "Black", self.image.get_rect(), width=self.border)
        self.text.draw(self.image)

    def set_value(self, value):
        if self.initial_value != 0:
            return
        
        self.pencil_values.clear()
        self.text.empty() 

        if self.current_value == value:
            self.current_value = 0

        else:
            self.current_value = value
            Text(self.normal_font_size, str(value), "#055C9D", (self.cell_width/2, self.cell_width/2), [self.text])

    def pencil(self, input_value):
        if self.initial_value != 0:
            return

        self.current_value = 0

        if input_value not in self.pencil_values:
            self.pencil_values.append(input_value)
        else:
            self.pencil_values.remove(input_value)

        self.text.empty()

        for value in self.pencil_values:
            row = int((value - 1) / 3)
            col = (value - 1) % 3

            pos_x = (self.cell_width / 6) + (col * (self.cell_width / 3)) 
            pos_y = (self.cell_width / 6) + (row * (self.cell_width / 3))  

            Text(self.pencil_font_size, str(value), "#5d5d5d", (pos_x, pos_y), [self.text])
    
    def clear_cell(self):
        if self.initial_value != 0:
            return

        self.pencil_values.clear()
        self.text.empty() 

        self.current_value = 0

    def update(self):
        self.draw_cell()

        