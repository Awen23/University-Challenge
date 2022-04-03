from turtle import screensize
import pygame
from .base import BaseState
import random
from operator import attrgetter
import copy

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

        # Potential products
        self.sandwich = ("sandwich", pygame.image.load("./fresh/sandwich-small.png"), True)
        self.crisps = ("crisps", pygame.image.load("./fresh/crisps-small.png"), True)
        self.drink = ("drink", pygame.image.load("./fresh/drink-small.png"), True)

        self.wrap = ("wrap", pygame.image.load("./fresh/wrap-small.png"), False)
        self.chocolate = ("chocolate", pygame.image.load("./fresh/chocolate-small.png"), False)

        self.product_selection = [self.sandwich, self.crisps, self.drink, self.wrap, self.chocolate]
        self.meal_deal_selection = [self.sandwich, self.crisps, self.drink]

        # The products on the shelves
        self.products = []
        self.load_products()
        self.last_moused_prod = self.products[0][0]

        # Silhouettes
        self.silhouette = pygame.image.load("./fresh/silhouette.png")
        self.silhouette_rects = []
        self.silhouette_rects.append(self.silhouette.get_rect(topleft=(-500, 400)))
        self.silhouette_rects.append(self.silhouette.get_rect(topleft=(2000, 200)))

        # Three items to make the meal deal
        self.inventory = []
        # Player score
        self.score = 0
        self.score_text = self.font.render("Score: " + str(self.score), True, pygame.Color("white"))
        self.score_rect = self.score_text.get_rect(topleft = (1000, 0))

        self.round = 0

    
    def has_duplicates(self, seq):
        seen = []
        unique_list = [x for x in seq if x not in seen and not seen.append(x)]
        return len(seq) != len(unique_list)
    
    def load_products(self):
        # Instantiate empty products with their positions.
        first_x = 60
        first_y = 126
        for i in range(4):
            self.products.append([])
            for j in range(4):
                # Change numbers beside first_x and first_y to fiddle with placements
                if (i%2 == 0):
                    pos = (first_x+(j*300),first_y+(i*124))
                else:
                    pos = (first_x+170+(j*300),first_y+(i*124))
                self.products[i].append(Product(pos))
        
        for shelf in self.products:
            # why don't for each work here? who knows
            for i in range(0, len(shelf)):
                rand_prod = self.product_selection[random.randint(0, len(self.product_selection)-1)]
                shelf[i].name = rand_prod[0]
                shelf[i].img = copy.copy(rand_prod[1])
                shelf[i].rect = rand_prod[1].get_rect(topleft=shelf[i].pos)
                shelf[i].is_in_meal_deal = rand_prod[2]
        self.ensure_meal_deal()
    
    def replenish_product(self, old_prod):
        flat_list = [item for sublist in self.products for item in sublist]
        seen = []
        unique_list = [x for x in flat_list if x not in seen and not seen.append(x)]
        
        num_in_meal_deal = 0
        for prod in unique_list:
            if prod.is_in_meal_deal:
                num_in_meal_deal += 1

        rand_prod = self.product_selection[random.randint(0, len(self.product_selection)-1)]
        old_prod.name = rand_prod[0]
        old_prod.img = copy.copy(rand_prod[1])
        old_prod.is_in_meal_deal = rand_prod[2]
        

        # Need to check if there is meal-dealable items and add specific ones if so
    
    def ensure_meal_deal(self):
        # Remove duplicates
        flat_list = [item for sublist in self.products for item in sublist]
        seen = []
        unique_list = [x for x in flat_list if x not in seen and not seen.append(x)]
        
        num_in_meal_deal = 0
        for prod in unique_list:
            if prod.is_in_meal_deal == True:
                num_in_meal_deal += 1
        
        #print("num_in_meal_deal:" + str(num_in_meal_deal))
        if num_in_meal_deal >= 3:
            return
        else:
            for i in range(0, 3):
                self.products[0][i].name = self.product_selection[i][0]
                self.products[0][i].img = self.product_selection[i][1]
                self.products[0][i].is_in_meal_deal = self.product_selection[i][2]

    def update(self, dt):
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            moused_prods = [p for s in self.products for p in s if p.rect.collidepoint(mouse_pos)]
            if (len(moused_prods) != 0):
                self.last_moused_prod = moused_prods[0]
                self.last_moused_prod.img = pygame.transform.scale(self.last_moused_prod.img, (100,100))
            else:
                self.last_moused_prod.img = pygame.transform.scale(self.last_moused_prod.img, (90,90))
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            clicked_prods = [p for s in self.products for p in s if p.rect.collidepoint(mouse_pos)]
            if (len(clicked_prods) == 0):
                return
            prod = clicked_prods[0]
            # Make product disappear
            #prod.img = pygame.Surface(prod.size, pygame.SRCALPHA, 32).convert_alpha()
            clicked_prods[0].img.set_alpha(0)
            # Replenish product
            #self.replenish_product(clicked_prods[0])
            # Add to inventory
            if len(self.inventory) < 3:
                # Display inventory in top right pls
                self.inventory.append(prod)
            if len(self.inventory) == 3:
                # Test for win state
                # Are all items different?
                if self.has_duplicates(self.inventory):
                    print("NOT ALL ITEMS ARE DIFFERENT")
                else:
                    # Are all three items in inventory in meal deal?
                    if all(p.is_in_meal_deal for p in self.inventory):
                        print("MEAL DEAL SUCCESS")
                        self.score += 100
                
                self.inventory = []
                self.products = []
                self.load_products()
                self.round += 1


    def draw_products(self, surface):
        first_x = 60
        first_y = 126
        for shelf in self.products:
            for prod in shelf:
                surface.blit(prod.img, prod.pos)

    def draw_silhouettes(self, surface):
        for sil in self.silhouette_rects:
            surface.blit(self.silhouette, sil)
            if sil.right < 0:
                print("hi")
                sil.move_ip(5, 0)
            elif sil.left > 1280:
                sil.move_ip(-5, 0)
        
    
    def draw(self, surface):
        surface.blit(self.background, (0,0))
        self.draw_products(surface)
        # draw silhouette(s)
        self.draw_silhouettes(surface)
        # surface.blit(self.silhouette, self.silhouette1_rect)
        # surface.blit(self.silhouette, self.silhouette2_rect)
        # self.silhouette1_rect.move_ip(5, 0)
        # self.silhouette2_rect.move_ip(-5, 0)

        surface.blit(self.font.render("Score: " + str(self.score), True, pygame.Color("white")), self.score_rect) # score


class Product():
    def __init__(self, pos):
        self.name = None
        self.img = None
        self.rect = None
        self.pos = pos
        self.size = (90, 90)
        self.is_in_meal_deal = None

    def __eq__(self, val):
        attrs = ('name', 'size')
        return attrgetter(*attrs)(self) == attrgetter(*attrs)(val)
    
    def __ne__(self, val):
        attrs = ('name', 'size')
        return attrgetter(*attrs)(self) != attrgetter(*attrs)(val)
