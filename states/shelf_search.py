import random
import pygame
from .base import BaseState
import time

pygame.mixer.init()

def human_readable_coordinates(tup):
    return (tup[0] + 1, tup[1] + 1)
class Shelf(pygame.sprite.Sprite):
    def __init__(self, x, y, rect):
        super(Shelf, self).__init__()
        self.x = x, 
        self.y = y
        self.rect = rect
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
class ShelfSearch(BaseState):
    def __init__(self):
        super(ShelfSearch, self).__init__()
        self.bg = pygame.image.load("library/shelves_blurred_cropped.png")
        self.start_time = False

        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.my_font = pygame.font.Font("states/data/PixeloidSans.ttf", 20)
        self.my_big_font = pygame.font.Font("states/data/PixeloidSansBold.ttf", 40)

        self.instruction_box = pygame.Surface((1200,640), pygame.SRCALPHA)   # per-pixel alpha
        self.instruction_box.fill((0,0,0,128))

        self.title = self.font.render("Shelf Search", True, pygame.Color("orange"))
        #self.title_rect = self.title.get_rect(center=(300, 600))
        self.next_state = "OVERWORLD"
        self.shelves = []
        self.score = 0
        self.score_rect = pygame.Rect(460, 7, 50, 30)
        self.time_rect = pygame.Rect(660, 7, 50, 30)
        i = 0
        j = 0
        for x in range(90, 1200, 200):
            row = []
            j = 0
            for y in range(50, 500, 100):
                rect = pygame.Rect(x+25, y + 25, 50, 75)
                row.append(Shelf(i, j, rect))
                j += 1
            self.shelves.append(row)
            i += 1
        self.target = self.generate_target()
        self.target_text = self.my_font.render('', True, (0, 255, 0))
        self.target_text_rect = self.target_text.get_rect()
        self.target_text_rect.center = (700, 600)

        self.score_final = pygame.Surface((680,420), pygame.SRCALPHA)   # per-pixel alpha
        self.score_final.fill((0,0,0,200))
        #self.score_final = pygame.Rect(300,150,680,420)
        self.button_box = pygame.Rect(535,400,210,90)
        self.next_button = pygame.image.load("states/data/nextbutton.png")
        self.next_button_over = pygame.image.load("states/data/nextbutton_highlighted.png")
        self.ending = False

    def startup(self, persistent):
        self.ending = False

    def generate_target(self):
        x = random.randint(0, len(self.shelves) - 1)
        y = random.randint(0, len(self.shelves[x]) - 1)
        return (x, y)
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if not self.ending:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__init__()
                    self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.shelves[self.target[0]][self.target[1]].is_clicked():
                    self.score += 1
                    self.target = self.generate_target()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_box.collidepoint(event.pos):
                    print("DONE")
                    self.__init__()
                    self.done = True
    def draw(self, surface):
        if not self.start_time:
            self.start_time = time.time()
            self.ambience = pygame.mixer.music.load("states/data/library_ambient.mp3")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        else:
            if (time.time() - self.start_time) > 30:
                self.ending = True

        surface.blit(self.bg, (0, 0))
        surface.blit(self.instruction_box, (40, 40))
        #surface.blit(self.title, self.title_rect)
        color = (181,80,34)
        black_box = pygame.Surface((1280,720))  # the size of your rect
        black_box.set_alpha(128)                # alpha level
        black_box.fill((255,255,255))           # this fills the entire surface
        surface.blit(black_box, (0,0))
        surface.blit(self.target_text, self.target_text_rect)
        surface.blit(self.my_big_font.render(str(human_readable_coordinates(self.target)), True, (255,0,0)), (600, 600))
        surface.blit(self.my_big_font.render(str(self.score), True, (0,0,250)), (500, 600))
        for row in self.shelves:
            for cell in row:
                pygame.draw.rect(surface, color,cell.rect)

        text_surface = self.my_font.render("Score: " + str(self.score), True, pygame.Color("black"))
        surface.blit(text_surface, (self.score_rect.x, self.score_rect.y))

        text_surface = self.my_font.render("Time: " + str(30 - round(time.time() - self.start_time)), True, pygame.Color("black"))
        surface.blit(text_surface, (self.time_rect.x, self.time_rect.y))

        if self.ending:
            #pygame.draw.rect(surface, (0,0,0), self.score_final)
            surface.blit(self.score_final, (300, 150))
            text_surface = self.my_big_font.render("Score: " + str(self.score), True, (255,255,255))
            size = self.my_big_font.size("Score: " + str(self.score))
            surface.blit(text_surface, (640-round(size[0]/2), 250))

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
                surface.blit(self.next_button_over, self.next_button_over.get_rect(center = self.button_box.center))
            else:
                surface.blit(self.next_button, self.next_button.get_rect(center = self.button_box.center))
            
                
    def update(self, dt):
        return super().update(dt)