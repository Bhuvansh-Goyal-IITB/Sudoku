from sudoku import string_to_board
from cursor import Cursor
from button import Button
from board import Board
from text import Text
from sys import exit
import pyperclip
import random
import ctypes
import pygame
import json

ctypes.windll.shcore.SetProcessDpiAwareness(2)

class Game:
    def __init__(self):
        pygame.init()
        
        WIDTH = 1000
        HEIGHT = 1000
        self.FPS = 60

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.cursor_group = pygame.sprite.Group()
        self.cursor = Cursor([self.cursor_group])
        pygame.mouse.set_visible(False)

        icon_image = pygame.image.load("assets/sudoku_icon.ico") 
        pygame.display.set_icon(icon_image)

        pygame.display.set_caption("Sudoku")

        self.clock = pygame.time.Clock()

    def quit(self):
        pygame.quit()
        exit()

    def main_menu(self):
        menu_buttons = pygame.sprite.Group()
        visible = pygame.sprite.Group()

        sudoku_title = Text(140, "SUDOKU", "Black", (500, 200), [visible])
        
        play_button = Button((500, 400), (170, 70), "Play", 34, self.difficulty, [menu_buttons, visible])
        quit_button = Button((500, 490), (170, 70), "Quit", 34, self.quit, [menu_buttons, visible])
        info_button = Button((500, 580), (170, 70), "Info", 34, self.info, [menu_buttons, visible])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.fill("White")

            menu_buttons.update()
            visible.draw(self.screen)   

            self.cursor_group.update()
            self.cursor_group.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(self.FPS)
    
    def difficulty(self):
        is_mouse_pressed = pygame.mouse.get_pressed()[0]

        diff_buttons = pygame.sprite.Group()
        visible = pygame.sprite.Group()
        
        def easy():
            self.play("easy")
        
        def medium():
            self.play("medium")
            
        def hard():
            self.play("hard")
            
        def expert():
            self.play("expert")     

        easy_button = Button((500, 350), (200, 80), "Easy", 40, easy, [diff_buttons, visible])
        medium_button = Button((500, 450), (200, 80), "Medium", 40, medium, [diff_buttons, visible])
        hard_button = Button((500, 550), (200, 80), "Hard", 40, hard, [diff_buttons, visible])
        expert_button = Button((500, 650), (200, 80), "Expert", 40, expert, [diff_buttons, visible])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    is_mouse_pressed = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    if string_to_board(pyperclip.paste()):
                        self.play()

            self.screen.fill("White")

            if not is_mouse_pressed:
                diff_buttons.update()
            visible.draw(self.screen)
           
            self.cursor_group.update()
            self.cursor_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)

    def info(self):
        buttons = pygame.sprite.Group()
        visible = pygame.sprite.Group()

        Text(58, "Controls:", "Black", (180, 80), [visible])
        Text()
        
        
        
        controls_lines = "-> P to toggle pencil mode,-> U for undo,-> M for main menu".split(",")

        line_spacing = 50

        for index, line in enumerate(controls_lines):
            text = Text(38, line, "Black", (500, 150 + (index * line_spacing)), [visible])
            text.rect.left = 30

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu()

            self.screen.fill("White")

            # buttons.update()
            visible.draw(self.screen)   

            self.cursor_group.update()
            self.cursor_group.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(self.FPS)

    def play(self, difficulty=None):
        if difficulty is None:
            board_str = pyperclip.paste()
        else:
            with open("puzzles/puzzles.json") as file:
                data = json.load(file)
                random_board = random.choice(data[difficulty])
                board_str = random_board["puzzle"]

        board = Board((500, 500), 105, board_str, 60, 26, 3)
        drag = False

        pencil_mode = False

        while True:
            board.reset_color()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.select_cell()
                if event.type == pygame.KEYDOWN and (event.key >= 49 and event.key <= 57):
                    board.set_value(event.key - 48, pencil_mode)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pencil_mode = not pencil_mode
                    if pencil_mode:
                        self.cursor.pencil()
                    else:
                        self.cursor.normal()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    board.undo()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu()

            self.screen.fill("White")

            board.handle_highlighting()
            board.update_cells()
            board.draw_cells(self.screen)

            self.cursor_group.update()
            self.cursor_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = Game()
    game.main_menu()