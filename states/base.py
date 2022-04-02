import pygame

class BaseState(object):
    # Constructor that initialises values
    # That are common for all states
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {} # If to pass data between states
        self.font = pygame.font.Font(None, 24)
    
    def startup(self, persistent):
        self.persist = persistent

    # Abstract methods to be implemented by child classes
    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass