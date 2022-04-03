import imp
import pygame
from pygame.locals import *
from enum import Enum
from .base import BaseState
import random
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
    Direction.UP:       620,
    Direction.LEFT:     500,
    Direction.DOWN:     380,
    Direction.RIGHT:    260,
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
        self.keys_counter = 1
        self.title = self.font.render(
            "Viva la duck duck revolution", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=(300, 50))
        self.next_state = "OVERWORLD"
        self.up_arrow_currently_down = False
        self.left_arrow_currently_down = False
        self.down_arrow_currently_down = False
        self.right_arrow_currently_down = False
        self.strike_line = StrikeLine(pygame.Rect(self.screen_rect.center[0], 0, 2, 800))
        self.arrow_queue = [Arrow(Direction.LEFT, 0, heights[Direction.LEFT]), Arrow(Direction.RIGHT, 200, heights[Direction.RIGHT])]

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
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
    def draw(self, surface):
        surface.blit(bg, (0, 0))
        surface.blit(self.title, self.title_rect)
        color = (0, 0, 0)
        pygame.draw.rect(surface, color, self.strike_line)
        surface.blit(self.font.render(str(self.score), True, (0,0,250)), (500, 100))
        # pygame.draw.polygon(surface, color, list(map(lambda x: (x[0], x[1]+620), polygons[Direction.RIGHT])))
        for arrow in self.arrow_queue:
            pygame.draw.polygon(surface, colours[arrow.direction],  list(map(lambda x: (x[0] + arrow.centre_x, x[1]+heights[arrow.direction]), polygons[arrow.direction])))

    def update(self, dt):
        if pygame.time.get_ticks() % 200 == 0:
            self.arrow_queue.append(
                Arrow(random.choice(directions), 0, 150))
        for x in self.arrow_queue:
            x.update_x()
            x.update_x()
        self.arrow_queue = list(filter(lambda x: x.centre_x < 1400 and not(x.checked), self.arrow_queue))
        blocks_hit_list = pygame.sprite.spritecollide(self.strike_line, self.arrow_queue, False)
        if len(blocks_hit_list) > 0:
            print(blocks_hit_list)
        print(self.keys_counter)
        if self.keys_counter == 1:
            for arrow in blocks_hit_list:
                if not(arrow.checked):
                    print(self.score)
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
                                
