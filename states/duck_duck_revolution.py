import imp
import pygame
from pygame.locals import *
from enum import Enum
from .base import BaseState
import random
import time

pygame.mixer.init()

# WASD // UP LEFT DOWN RIGHT
bg = pygame.image.load("student_union/student_union_blurred.png")


class Direction(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

UNIT = 15
polygons = {
    Direction.UP:       [(4*UNIT, 6*UNIT), (2*UNIT, 6*UNIT), (2*UNIT, 2*UNIT), (0, 2*UNIT), (3*UNIT, 0), (6*UNIT, 2*UNIT), (4*UNIT, 2*UNIT)],
    Direction.LEFT:     [(6*UNIT, 4*UNIT), (6*UNIT, 2*UNIT), (2*UNIT, 2*UNIT), (2*UNIT, 0), (0, 3*UNIT), (2*UNIT, 6*UNIT), (2*UNIT, 4*UNIT)],
    Direction.DOWN:     [(2*UNIT, 0), (4*UNIT, 0), (4*UNIT, 4*UNIT), (6*UNIT, 4*UNIT), (3*UNIT, 6*UNIT), (0, 4*UNIT), (2*UNIT, 4*UNIT)],
    Direction.RIGHT:    [(0, 2*UNIT), (0, 4*UNIT), (4*UNIT, 4*UNIT), (4*UNIT, 6*UNIT), (6*UNIT, 3*UNIT), (4*UNIT, 0), (4*UNIT, 2*UNIT)],
}
colours = {
    Direction.UP:       (250, 0, 0),
    Direction.LEFT:     (0, 250, 0),
    Direction.DOWN:     (0, 0, 250),
    Direction.RIGHT:    (180, 0, 180),
}
heights = {
    Direction.UP:       610,
    Direction.LEFT:     460,
    Direction.DOWN:     310,
    Direction.RIGHT:    160,
}

class Arrow(pygame.sprite.Sprite):
    def set_rect(self):
        if self.direction == Direction.LEFT or self.direction == Direction.RIGHT:
            self.rect = pygame.Rect(self.centre_x - 3*UNIT, self.centre_x - 2*UNIT, 6*UNIT, 4*UNIT)
        else:
            self.rect = pygame.Rect(self.centre_x - 2*UNIT, self.centre_x - 3*UNIT, 4*UNIT, 6*UNIT)
    def __init__(self, direction, centre_x, centre_y):
        super(Arrow, self).__init__()
        self.direction = direction
        self.base_arrow_polygon = polygons[direction]
        self.checked = False
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.set_rect()
    def update_x(self):
        self.centre_x += 1
        self.set_rect()

class StrikeLine(pygame.sprite.Sprite):
    def __init__(self, strike_line):
        super(StrikeLine, self).__init__()
        self.rect = strike_line

directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]


class DuckDuckRevolution(BaseState):
    def __init__(self):
        super(DuckDuckRevolution, self).__init__()
        self.font = pygame.font.SysFont('serif.ttf', 50)
        self.counter = 0
        self.score = 0
        self.keys_counter = 0
        #self.title = self.font.render(
        #    "Viva la duck duck revolution", True, pygame.Color("white"))
        #self.title_rect = self.title.get_rect(center=(300, 50))
        self.next_state = "OVERWORLD"
        self.up_arrow_currently_down = False
        self.left_arrow_currently_down = False
        self.down_arrow_currently_down = False
        self.right_arrow_currently_down = False
        self.strike_line = StrikeLine(pygame.Rect(self.screen_rect.center[0], 0, 2, 800))
        self.arrow_queue = [Arrow(Direction.LEFT, 0, heights[Direction.LEFT]), Arrow(Direction.RIGHT, 200, heights[Direction.RIGHT])]
        self.my_font = pygame.font.Font("states/data/PixeloidSansBold.ttf", 40)
        self.my_big_font = pygame.font.Font("states/data/PixeloidSansBold.ttf", 40)
        self.receptor_right = pygame.transform.scale(pygame.image.load("./noteskin/receptor_right.png"), (100,100))
        self.receptor_left = pygame.transform.scale(pygame.image.load("./noteskin/receptor_left.png"), (100,100))
        self.receptor_down = pygame.transform.scale(pygame.image.load("./noteskin/receptor_down.png"), (100,100))
        self.receptor_up = pygame.transform.scale(pygame.image.load("./noteskin/receptor_up.png"), (100,100))
        self.arrow_imgs = {
            Direction.UP:       pygame.transform.scale(pygame.image.load("./noteskin/redarrow_up.png"), (100,100)),
            Direction.LEFT:     pygame.transform.scale(pygame.image.load("./noteskin/redarrow_left.png"), (100,100)),
            Direction.DOWN:     pygame.transform.scale(pygame.image.load("./noteskin/redarrow_down.png"), (100,100)),
            Direction.RIGHT:    pygame.transform.scale(pygame.image.load("./noteskin/redarrow_right.png"), (100,100)),
        }
        self.start_time = None

        self.score_final = pygame.Surface((680,420), pygame.SRCALPHA)   # per-pixel alpha
        self.score_final.fill((0,0,0,200))
        #self.score_final = pygame.Rect(300,150,680,420)
        self.button_box = pygame.Rect(535,400,210,90)
        self.next_button = pygame.image.load("states/data/nextbutton.png")
        self.next_button_over = pygame.image.load("states/data/nextbutton_highlighted.png")
        self.ending = False



    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if not self.ending:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__init__()
                    self.done = True
                if event.key == pygame.K_UP:
                    self.up_arrow_currently_down = True
                    self.keys_counter += 1
                elif event.key == pygame.K_LEFT:
                    self.left_arrow_currently_down = True
                    self.keys_counter += 1
                elif event.key == pygame.K_DOWN:
                    self.keys_counter += 1
                    self.down_arrow_currently_down = True
                elif event.key == pygame.K_RIGHT:
                    self.keys_counter += 1
                    self.right_arrow_currently_down = True
            elif event.type == pygame.KEYUP:            
                if event.key == pygame.K_UP:
                    self.keys_counter -= 1
                    self.up_arrow_currently_down = False
                elif event.key == pygame.K_LEFT:
                    self.keys_counter -= 1
                    self.left_arrow_currently_down = False
                elif event.key == pygame.K_DOWN:
                    self.keys_counter -= 1
                    self.down_arrow_currently_down = False
                elif event.key == pygame.K_RIGHT:
                    self.keys_counter -= 1
                    self.right_arrow_currently_down = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_box.collidepoint(event.pos):
                    self.__init__()
                    self.done = True
    
    def draw(self, surface):
        if not self.start_time:
            self.bgm = pygame.mixer.music.load("./student_union/mr_brightside_8bit.mp3")
            self.start_time = time.time()
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        else:
            if (time.time() - self.start_time) > 30:
                pygame.mixer.music.fadeout(1000)
                self.ending = True

        surface.blit(bg, (0, 0))
        #surface.blit(self.title, self.title_rect)
        color = (0, 0, 0)
        pygame.draw.rect(surface, color, self.strike_line)
        # draw receptors
        surface.blit(self.receptor_right, self.receptor_right.get_rect(topleft=(self.screen_rect.center[0]-50, heights[Direction.RIGHT]-44)))
        surface.blit(self.receptor_left, self.receptor_left.get_rect(topleft=(self.screen_rect.center[0]-50, heights[Direction.LEFT]-44)))
        surface.blit(self.receptor_up, self.receptor_up.get_rect(topleft=(self.screen_rect.center[0]-50, heights[Direction.UP]-44)))
        surface.blit(self.receptor_down, self.receptor_down.get_rect(topleft=(self.screen_rect.center[0]-50, heights[Direction.DOWN]-44)))

        surface.blit(self.my_font.render("Score: " + str(self.score), True, pygame.Color("white")), (1000, 50))
        # pygame.draw.polygon(surface, color, list(map(lambda x: (x[0], x[1]+620), polygons[Direction.RIGHT])))
        for arrow in self.arrow_queue:
            arrow_to_draw = self.arrow_imgs[arrow.direction]
            #hello = list(map(lambda x: (x[0] + arrow.centre_x, x[1]+heights[arrow.direction]), polygons[arrow.direction]))
            surface.blit(arrow_to_draw, arrow_to_draw.get_rect(center=(arrow.centre_x, heights[arrow.direction])))
            
            #pygame.draw.polygon(surface, colours[arrow.direction],  list(map(lambda x: (x[0] + arrow.centre_x, x[1]+heights[arrow.direction]), polygons[arrow.direction])))
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
        if pygame.time.get_ticks() % 200 == 0:
            self.arrow_queue.append(
                Arrow(random.choice(directions), 0, 150))
        for x in self.arrow_queue:
            x.update_x()
            x.update_x()
            x.update_x()
            x.update_x()
        self.arrow_queue = list(filter(lambda x: x.centre_x < 1400 and not(x.checked), self.arrow_queue))
        blocks_hit_list = pygame.sprite.spritecollide(self.strike_line, self.arrow_queue, False)
        #print(self.keys_counter)
        if self.keys_counter == 1:
            for arrow in blocks_hit_list:
                if not(arrow.checked):
                    #print(self.score)
                    if arrow.direction == Direction.LEFT and self.left_arrow_currently_down:
                        arrow.checked = True
                        self.score += 1
                    if arrow.direction == Direction.RIGHT and self.right_arrow_currently_down:
                        arrow.checked = True
                        self.score += 1
                    if arrow.direction == Direction.UP and self.up_arrow_currently_down:
                        arrow.checked = True
                        self.score += 1
                    if arrow.direction == Direction.DOWN and self.down_arrow_currently_down:
                        arrow.checked = True
                        self.score += 1
                                
