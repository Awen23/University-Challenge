import pygame
from .base import BaseState

class Overworld(BaseState):
    def __init__(self):
        super(Overworld, self).__init__()
        self.time_active = 0
        # Background
        self.bg_img = pygame.image.load("./overworld.png")

        # Title
        self.my_font = pygame.font.Font("states/data/PixeloidSansBold.ttf", 40)
        self.title = self.font.render("Overworld", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=(self.screen_rect.center[0]-90, 20))

        # Character
        self.character_img_down = pygame.transform.scale(pygame.image.load("./duck/duck_down.png"), (35, 50))
        self.character_img_left = pygame.transform.scale(pygame.image.load("./duck/duck_left.png"), (50, 35))
        self.character_img_right = pygame.transform.scale(pygame.image.load("./duck/duck_right.png"), (50, 35))
        self.character_img_up = pygame.transform.scale(pygame.image.load("./duck/duck_up.png"), (35, 50))
        self.character_img = self.character_img_down
        self.character_rect = self.character_img.get_rect(center=(640,130))
        # Location icons
        self.locations = {}
        self.initialise_locations()
    
    def startup(self, persistent):
        self.character_rect = self.character_img.get_rect(center=(640,130))

    
    def initialise_locations(self):
        # Make this better..
        cc = pygame.transform.scale(pygame.image.load("./1w_facade.png"), (200, 100))
        self.locations["COURSEWORK CRUNCH GAME START"] = (cc, cc.get_rect(center=(320, 240)))

        mdm = pygame.transform.scale(pygame.image.load("./fresh_facade.png"), (120, 120))
        self.locations["MEAL DEAL MANIA GAME START"] = (mdm, mdm.get_rect(center=(260,500)))

        ss =  pygame.transform.scale(pygame.image.load("states/data/library.png"), (120, 120))
        self.locations["SHELF SEARCH GAME START"] = (ss, ss.get_rect(center=(940, 320)))

        ddr = pygame.transform.scale(pygame.image.load("./su_facade.png"), (120, 120))
        self.locations["DUCK DUCK REVOLUTION GAME START"] = (ddr, ddr.get_rect(center=(1060, 440)))

        tt = pygame.transform.scale(pygame.image.load("./bus_facade.png"), (120, 120))
        self.locations["TICKETS THANKS GAME START"] = (tt, tt.get_rect(center=(640, 640)))


    # Runs continuously, it's the loop
    def update(self, dt):
        self.time_active += dt
        # if self.time_active >= 5000:
        #     self.done = True

        # Move character
        self.handle_keys(self.character_rect)
        # Maybe use pygame.Rect.collidedict instead...
        intersect_index = self.character_rect.collidelist([loc[1] for loc in self.locations.values()])
        # If != -1, we have intersected
        if intersect_index != -1:
            # Need to change next state here
            self.next_state = list(self.locations.keys())[intersect_index]
            self.done = True

    # Handles arrow keys for moving character
    # TODO: Allow diagonal movement
    def handle_keys(self, mover):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.character_img = self.character_img_left
            self.character_rect.move_ip(-4, 0)
        elif key[pygame.K_RIGHT]:
            self.character_img = self.character_img_right
            self.character_rect.move_ip(4, 0)
        elif key[pygame.K_UP]:
            self.character_img = self.character_img_up
            self.character_rect.move_ip(0, -4)
        elif key[pygame.K_DOWN]:
            self.character_img = self.character_img_down
            self.character_rect.move_ip(0, 4)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        surface.blit(self.bg_img, self.bg_img.get_rect())
        # Text
        surface.blit(self.my_font.render("Overworld", True, pygame.Color("white")), self.title_rect)
        # Draw character rect
        surface.blit(self.character_img, self.character_rect)
        # Draw locations rects
        for loc in self.locations.values():
            surface.blit(loc[0], loc[1])
            #pygame.draw.rect(surface, pygame.Color("red"), loc_rect)