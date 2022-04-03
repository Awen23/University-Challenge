import pygame
from .base import BaseState

class MainMenu(BaseState):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.next_state = "OVERWORLD"

        self.title_img = pygame.image.load("./title.png")
        self.title_rect = self.title_img.get_rect(center=(self.screen_rect.center[0],self.screen_rect.center[1]-150) )

        self.bg_img = pygame.image.load("./menu_bg.png")
        self.bg_rect = self.bg_img.get_rect(topleft=self.screen_rect.topleft)
        self.bg_scroll = (-1, -1)

        self.button_img_unhighlighted = pygame.image.load("./start_button.png")
        self.button_img_highlighted = pygame.image.load("./start_button_highlighted.png")
        self.button_img = self.button_img_unhighlighted
        self.button_rect = self.button_img.get_rect(center=self.screen_rect.center)

    def update(self, dt):
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Start button
            if self.button_rect.collidepoint(mouse_pos):
                self.button_img = self.button_img_highlighted
            else:
                self.button_img = self.button_img_unhighlighted
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_pos):
                self.done = True

    def draw(self, surface):
        surface.blit(self.bg_img, self.bg_rect)
        self.bg_rect.move_ip(self.bg_scroll)
        if self.bg_rect.top == self.screen_rect.top:
            self.bg_scroll = (-1, -1)
        elif self.bg_rect.bottom == self.screen_rect.bottom:
            self.bg_scroll = (1, 1)
            
        surface.blit(self.title_img, self.title_rect)
        surface.blit(self.button_img, self.button_rect)
        #pass