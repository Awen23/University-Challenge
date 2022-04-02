import pygame
from .base import BaseState

class Overworld(BaseState):
    def __init__(self):
        super(Overworld, self).__init__()
        self.title = self.font.render("This is the overworld!", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=(640, 260))
        self.time_active = 0
        # Character
        self.character_rect = pygame.Rect((0,0), (50,50))
        self.character_rect.center = self.screen_rect.center
        # Location icons
        self.location_rects = {}
        self.initialise_locations()
    
    def initialise_locations(self):
        # Make this better..
        self.location_rects["MEAL DEAL MANIA"] = pygame.Rect((0,0), (50,50))
        self.location_rects["MEAL DEAL MANIA"].center = (740, 360)

        self.location_rects["COURSEWORK CRUNCH"] = pygame.Rect((0,0), (50,50))
        self.location_rects["COURSEWORK CRUNCH"].center = (540, 360)

        self.location_rects["SHELF SEARCH"] = pygame.Rect((0,0), (50,50))
        self.location_rects["SHELF SEARCH"].center = (640, 460)


    # Runs continuously, it's the loop
    def update(self, dt):
        self.time_active += dt
        # if self.time_active >= 5000:
        #     self.done = True

        # Move character
        self.handle_keys(self.character_rect)
        # Maybe use pygame.Rect.collidedict instead...
        intersect_index = self.character_rect.collidelist(list(self.location_rects.values()))
        # If != -1, we have intersected
        if intersect_index != -1:
            # Need to change next state here
            self.next_state = list(self.location_rects.keys())[intersect_index]
            self.done = True

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

    def draw(self, surface):
        surface.fill(pygame.Color("green"))
        surface.blit(self.title, self.title_rect)
        # Draw character rect
        pygame.draw.rect(surface, pygame.Color("blue"), self.character_rect)
        # Draw locations rects
        for loc_rect in self.location_rects.values():
            pygame.draw.rect(surface, pygame.Color("red"), loc_rect)