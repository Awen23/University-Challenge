import pygame
from .base import BaseState

class GameStart(BaseState):
    def __init__(self, name, background, avatar, instructions, next_state):
        super(GameStart, self).__init__()
        self.my_font = pygame.font.Font("states/data/PixeloidSans.ttf", 30)
        self.my_big_font = pygame.font.Font("states/data/PixeloidSansBold.ttf", 50)
        self.title = self.my_big_font.render(name, True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=(820, 80))
        self.next_state = next_state

        self.instructions = open(instructions, "r").read()
        self.bg = pygame.image.load(background)
        self.avatar = pygame.image.load(avatar)

        #self.instruction_box = self.Rect(40, 40, 1200, 640)
        self.instruction_box = pygame.Surface((840,640), pygame.SRCALPHA)   # per-pixel alpha
        self.instruction_box.fill((0,0,0,128))  # notice the alpha value in the color

        self.start_button = pygame.image.load("states/data/start_button.png")
        self.start_button_over = pygame.image.load("states/data/start_button_highlighted.png")
        self.button_box = pygame.Rect(715,500,210,90)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_box.collidepoint(event.pos):
                self.done = True
    
    def draw(self, surface):
        surface.blit(self.bg, (0, 0))

        surface.blit(self.instruction_box, (400, 40))
        surface.blit(self.avatar, (40, 320))

        surface.blit(self.title, (self.title_rect.x, self.title_rect.y))

        y_value = 150
        for line in self.instructions.split("\n"):
            text_surface = self.my_font.render(line, True, (255,255,255))
            surface.blit(text_surface, (450,y_value))
            y_value += 40

        b_len_x = 210
        b_len_y = 90
        mos_x, mos_y = pygame.mouse.get_pos()
        if mos_x>self.button_box.x and (mos_x<self.button_box.x+b_len_x):
            x_inside = True
        else: x_inside = False
        if mos_y>self.button_box.y and (mos_y<self.button_box.y+b_len_y):
            y_inside = True
        else: y_inside = False
        if x_inside and y_inside:
            #Mouse is hovering over button
            surface.blit(self.start_button_over, self.start_button_over.get_rect(center = self.button_box.center))
        else:
            surface.blit(self.start_button, self.start_button.get_rect(center = self.button_box.center))