from typing import Any
import pygame
from text import Text

class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_center, cell_width, cell_value, groups, correct_value=None):
        super().__init__(groups)
        self.cell_width = cell_width
        self.pencil_values = []

        self.initial_value = cell_value
        self.current_value = cell_value

        self.selected = False

        if self.initial_value != 0:
            self.correct_value = cell_value
        else:
            self.correct_value = correct_value

        self.image = pygame.Surface((cell_width, cell_width))
        
        self.rect = self.image.get_rect()
        self.rect.center = pos_center
        
        self.text = pygame.sprite.Group()

        if self.initial_value != 0:
            Text(30, str(cell_value), "Black", (cell_width/2, cell_width/2), [self.text])
        
        self.draw_cell("White")


    def draw_cell(self, color):
        self.image.fill(color)
        pygame.draw.rect(self.image, "Black", self.image.get_rect(), width=2)
        self.text.draw(self.image)

    def set_value(self, value, font_size):
        if self.initial_value != 0:
            return
        
        self.pencil_values.clear()
        
        if self.current_value == value:
            self.current_value = 0
            
            self.text.empty() 

        else:
            self.current_value = value

            self.text.empty() 

            if self.correct_value == self.current_value:
                color = "Blue"
            else:
                color = "Red"

            Text(font_size, str(value), color, (self.cell_width/2, self.cell_width/2), [self.text])

    def pencil(self, input_value, font_size):
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

            Text(font_size, str(value), "Black", (pos_x, pos_y), [self.text])

    def select(self):
        self.selected = True
        self.draw_cell("Grey")

    def deselect(self):
        self.selected = False
        if self.current_value == 0 or self.current_value == self.correct_value:
            self.draw_cell("White")
        else:
            self.draw_cell("#FFCCCB")

    def check_mouse(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.select()
        else:
            self.deselect()
    
    def update(self):
        self.check_mouse()