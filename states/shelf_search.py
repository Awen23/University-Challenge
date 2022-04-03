import random
import pygame
from .base import BaseState
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
        self.font = pygame.font.SysFont('serif.ttf', 50)
        self.title = self.font.render("Shelf search!!!!!!!!!", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=(300, 600))
        self.next_state = "OVERWORLD"
        self.shelves = []
        self.score = 0
        i = 0
        j = 0
        for x in range(50, 1200, 200):
            row = []
            j = 0
            for y in range(50, 500, 100):
                rect = pygame.Rect(x, y + 25, 50, 75)
                row.append(Shelf(i, j, rect))
                j += 1
            self.shelves.append(row)
            i += 1
        self.target = self.generate_target()
        self.target_text = self.font.render('', True, (0, 255, 0))
        self.target_text_rect = self.target_text.get_rect()
        self.target_text_rect.center = (700, 600)

    def generate_target(self):
        x = random.randint(0, len(self.shelves) - 1)
        y = random.randint(0, len(self.shelves[x]) - 1)
        return (x, y)
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.shelves[self.target[0]][self.target[1]].is_clicked():
                self.score += 1
                self.target = self.generate_target()
    def draw(self, surface):
        surface.fill(pygame.Color("darkolivegreen"))
        surface.blit(self.title, self.title_rect)
        color = (181,80,34)
        surface.blit(self.target_text, self.target_text_rect)
        surface.blit(self.font.render(str(human_readable_coordinates(self.target)), True, (255,0,0)), (600, 600))
        surface.blit(self.font.render(str(self.score), True, (0,0,250)), (500, 600))
        for row in self.shelves:
            for cell in row:
                pygame.draw.rect(surface, color,cell.rect)
                
    def update(self, dt):
        return super().update(dt)