import pygame
from .base import BaseState
import random
import time
import re

pygame.font.init()

class CourseworkCrunch(BaseState):
    def __init__(self):
        super(CourseworkCrunch, self).__init__()
        self.start_time = time.time()
        self.title = self.font.render("Coursework Crunch", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "OVERWORLD"
        self.ended = False
        self.bg = pygame.image.load("states/data/computer.png")
        self.run_pic = pygame.image.load('states/data/run.png')
        self.run_over = self.run_pic.copy()
        # this works on images with per pixel alpha too
        alpha = 128
        self.run_over.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        self.questions = open("states/data/stack_overflow.txt", "r").read().split("\n")
        self.snippets = open("states/data/text.txt", "r").read().split("\n") #CHANGE TO CODE AND @@
        #print(pygame.font.get_fonts())
        self.random_index = random.randint(0, len(self.questions) - 1)
        self.current_question = self.questions[self.random_index]
        self.current_snippet = self.snippets[self.random_index]
        self.my_font = pygame.font.Font("states/data/PixeloidSans.ttf", 12)
        self.input_rect = pygame.Rect(701, 115, 475, 333)
        self.user_text = ''
        self.pressed_c = False
        self.pressed_v = False
        self.errored = False
        self.done_lines = -1
        self.run_button = pygame.Rect(905, 375, 42, 37)
        self.title_rect = pygame.Rect(216, 147, 354, 28)
        self.error_rect = pygame.Rect(721, 530, 467, 50)
        self.heapunderflow_rect = pygame.Rect(721, 500, 467, 50)
        self.ctrlc_rect = pygame.Rect(764, 587, 50, 30)
        self.ctrlv_rect = pygame.Rect(1002, 587, 50, 30)
        self.score_rect = pygame.Rect(460, 7, 50, 30)
        self.time_rect = pygame.Rect(660, 7, 50, 30)
        self.score = 0
        self.last_question = False


    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.run_button.collidepoint(event.pos):
                self.errored = True
                self.last_question = self.current_question
                self.random_index = random.randint(0, len(self.questions))
                self.current_question = self.questions[self.random_index]
                user_list = list(filter(None, re.split("[ \[\]\(\)|']", self.user_text)))
                code_list = list(filter(None, re.split("[ \[\]\(\)|']", self.current_snippet)))
                print("USER LIST:")
                print(user_list)
                print("CODE LIST:")
                print(code_list)
                for inp, aim in zip(user_list, code_list):
                    if inp.lower() == aim.lower():
                        self.score += 1
                    else:
                        print("DIFF " + inp.lower() + " " + aim.lower())
            

        if event.type == pygame.KEYDOWN:
            if self.errored:
                keys = pygame.key.get_pressed()

                if (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and keys[pygame.K_c]:
                    self.pressed_c = True

                if (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and keys[pygame.K_v] and self.pressed_c:
                    self.pressed_c = False
                    self.errored = False
                    self.current_snippet = self.snippets[self.random_index]
                    self.user_text = ''
            else:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.user_text += "\n"
                elif event.key == pygame.K_TAB:
                    self.user_text += "   "
                else:
                    self.user_text += event.unicode
    
    def draw(self, surface):
        if (time.time() - self.start_time) > 6000:
            print("here")
            self.ended = True
        surface.blit(self.bg, (0, 0))
        text_surface = self.my_font.render("Score: " + str(self.score), True, pygame.Color("white"))
        surface.blit(text_surface, (self.score_rect.x, self.score_rect.y))

        text_surface = self.my_font.render("Time: " + str(60 - round((time.time() - self.start_time))), True, pygame.Color("white"))
        surface.blit(text_surface, (self.time_rect.x, self.score_rect.y))

        y_value = 294
        for line in self.current_snippet.split("\n"):
            text_surface = self.my_font.render(line, True, (0,0,0))
            surface.blit(text_surface, (253,y_value))
            y_value += 20

        #pygame.draw.rect(surface, (53, 46, 35), self.input_rect)
        y_value = 5
        for line in self.user_text.split("\n"):
            text_surface = self.my_font.render(line, True, pygame.Color("white"))
            surface.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+y_value))
            y_value += 20

        pygame.draw.rect(surface, pygame.Color("lightgrey"), self.run_button)

        if not self.errored:
            text_surface = self.my_font.render(self.current_question, True, pygame.Color("black"))
            surface.blit(text_surface, (self.title_rect.x, self.title_rect.y))
        else:
            text_surface = self.my_font.render(self.last_question, True, pygame.Color("black"))
            surface.blit(text_surface, (self.title_rect.x, self.title_rect.y))

        if self.errored:
            text_surface = self.my_font.render("Ask HeapUnderflow:", True, pygame.Color("white"))
            surface.blit(text_surface, (self.heapunderflow_rect.x, self.heapunderflow_rect.y))

            text_surface = self.my_font.render(self.current_question + "??????", True, pygame.Color("white"))
            surface.blit(text_surface, (self.error_rect.x, self.error_rect.y))
            if self.pressed_c:
                text_surface = self.my_font.render("CTRL+C", True, pygame.Color("green"))
            else:
                text_surface = self.my_font.render("CTRL+C", True, pygame.Color("white"))
            surface.blit(text_surface, (self.ctrlc_rect.x, self.ctrlc_rect.y))

            if self.pressed_v:
                text_surface = self.my_font.render("CTRL+V", True, pygame.Color("green"))
                self.current_question = self.questions[self.random_index]
                surface.blit(text_surface, (self.ctrlv_rect.x, self.ctrlv_rect.y))
                pygame.time.wait(5)
                self.errored = False
            else:
                text_surface = self.my_font.render("CTRL+V", True, pygame.Color("white"))
            surface.blit(text_surface, (self.ctrlv_rect.x, self.ctrlv_rect.y))

        x_len = 42
        y_len = 37
        mos_x, mos_y = pygame.mouse.get_pos()
        if mos_x>self.run_button.x and (mos_x<self.run_button.x+x_len):
            x_inside = True
        else: x_inside = False
        if mos_y>self.run_button.y and (mos_y<self.run_button.y+y_len):
            y_inside = True
        else: y_inside = False
        if x_inside and y_inside:
            #Mouse is hovering over button
            surface.blit(self.run_over, self.run_pic.get_rect(center = self.run_button.center))
        else:
            surface.blit(self.run_pic, self.run_pic.get_rect(center = self.run_button.center))
        

