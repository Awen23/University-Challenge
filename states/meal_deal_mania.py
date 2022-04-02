import pygame
from .base import BaseState
import random

class MealDealMania(BaseState):
    def __init__(self):
        super(MealDealMania, self).__init__()
        self.title = self.font.render("Meal deal maniaaaa", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "OVERWORLD"
        self.score = 0

        # Background image
        self.background = pygame.image.load("./fresh/shelves.png").convert_alpha()
        #self.background.set_alpha(5)

        # The products on the shelves
        self.products = [ [None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None] ]
        self.load_products()

    
    def load_products(self):
        sandwich = Product(pygame.image.load("./fresh/sandwich-small.png"), True)
        crisps = Product(pygame.image.load("./fresh/crisps-small.png"), True)
        drink = Product(pygame.image.load("./fresh/drink-small.png"), True)

        product_selection = [sandwich, crisps, drink]
        for shelf in self.products:
            # why don't for each work here? who knows
            for i in range(0, len(shelf)):
                shelf[i] = product_selection[random.randint(0, len(product_selection)-1)]


    def update(self, dt):
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw_products(self, surface):
        first_x = 60
        first_y = 126

        for i in range(len(self.products)):
            for j in range(len(self.products[i])):
                if (i%2 == 0):
                    surface.blit(self.products[i][j].img, (first_x+(j*300),first_y+(i*124)))
                else:
                    surface.blit(self.products[i][j].img, (first_x+170+(j*300),first_y+(i*124)))
    
    def draw(self, surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.title, self.title_rect)
        self.draw_products(surface)


class Product():
    def __init__(self, img, is_in_meal_deal):
        self.img = img
        self.is_in_meal_deal = is_in_meal_deal