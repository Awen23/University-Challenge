import pygame
from .base import BaseState

class Overworld(BaseState):
    def __init__(self):
        super(Overworld, self).__init__()
        self.title = self.font.render("This is the overworld!", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "MEAL DEAL MANIA"
        self.time_active = 0

        self.character_rect = pygame.Rect((0,0), (50,50))
        self.character_rect.center = self.screen_rect.center

    # Runs continuously, it's the loop
    def update(self, dt):
        self.time_active += dt
        
        # if self.time_active >= 5000:
        #     self.done = True

        self.handle_keys(self.character_rect)
        pass

    # Handles arrow keys for moving character
    # TODO: Allow diagonal movement
    def handle_keys(self, mover):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
           self.character_rect.move_ip(-2, 0)
        elif key[pygame.K_RIGHT]:
           self.character_rect.move_ip(2, 0)
        elif key[pygame.K_UP]:
           self.character_rect.move_ip(0, -2)
        elif key[pygame.K_DOWN]:
           self.character_rect.move_ip(0, 2)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.character_rect.move_ip(0, -10)
            
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         self.character_rect.move_ip(0, -10)

    def draw(self, surface):
        surface.fill(pygame.Color("green"))
        surface.blit(self.title, self.title_rect)
        pygame.draw.rect(surface, pygame.Color("blue"), self.character_rect)