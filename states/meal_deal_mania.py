import pygame
from .base import BaseState

class MealDealMania(BaseState):
    def __init__(self):
        super(MealDealMania, self).__init__()
        self.title = self.font.render("Meal deal maniaaaa", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "OVERWORLD"

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
    
    def draw(self, surface):
        surface.fill(pygame.Color("blue"))
        surface.blit(self.title, self.title_rect)