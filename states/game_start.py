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
        self.instruction_box.fill((0,0,0,128))                         # notice the alpha value in the color

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
    
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