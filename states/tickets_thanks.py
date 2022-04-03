import pygame
from .base import BaseState
import random
import time

def obscure(pic, color):
    if len(color) != 4:
        raise ValueError("image.obscure needs an rgba, not just an rgb")
    r, g, b, a = color

    overlay = pygame.Surface(pic.get_size())
    overlay.fill((r, g, b))
    overlay.set_alpha(a)

    pic.blit(overlay, (0, 0))
    return pic

class TicketsThanks(BaseState):
    def __init__(self):
        super(TicketsThanks, self).__init__()
        self.title = self.font.render("TicketsThanks", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "OVERWORLD"
        self.start_time = time.time()

        self.words = ["cord", "lord", "tree", "fear", "plea", "cold", "door", "west", "read", "reed", "boot", "soot", "noot", "wear", "tear", 
                        "rear", "free", "feed", "root", "join", "pain", "rats", "wire"]
        self.times = ["14:20", "14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29", "14:30", "14:31", "14:32", 
                        "14:33", "14:34", "14:35", "14:36", "14:37", "14:38", "14:39", "14:40", "14:41", "14:42", "14:43", "14:44"]
        self.time_index = 0
        self.word_index = random.randint(0, len(self.words) - 1)
        self.current_word = self.words[self.word_index]
        self.word_changed = True
        

        self.my_font = pygame.font.Font("states/data/PixeloidSans.ttf", 15)
        self.my_big_font = pygame.font.Font("states/data/PixeloidSansBold.ttf", 40)

        self.bg = pygame.image.load("states/data/bus.png")
        self.ticket_pic = pygame.image.load('states/data/ticket.png')
        self.ticket_x = 508
        self.ticket_y = 120
        self.t_cur_x = 508
        self.t_cur_y = 720
        self.new_ticket = True
        self.remove_ticket = False

        self.score = 0
        self.score_rect = pygame.Rect(460, 7, 50, 30)
        self.time_rect = pygame.Rect(660, 7, 50, 30)

        self.word_box = pygame.Rect(325, 60, 300, 50)
        self.time_box = pygame.Rect(655, 60, 300, 50)

        self.ticket_box = pygame.Rect(self.ticket_x+21, self.ticket_y+290, 220, 61)

        self.yes_pic = pygame.image.load("states/data/tick.png")
        self.no_pic = pygame.image.load("states/data/cross.png")
        self.yes_over = pygame.transform.scale(self.yes_pic.copy(), (50, 50))
        self.no_over = pygame.transform.scale(self.no_pic.copy(), (50,50))
        self.yes_button = pygame.Rect(398.5, 358, 40, 40)
        self.no_button = pygame.Rect(841.5, 358, 40, 40)



    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.yes_button.collidepoint(event.pos):
                if self.words[self.word_index] == self.current_word or self.times[self.time_index] == self.current_word:
                    self.score += 1
                else:
                    self.score -= 1
                self.remove_ticket = True
                self.word_changed = False

            if self.no_button.collidepoint(event.pos):
                if self.words[self.word_index] != self.current_word or self.times[self.time_index] != self.current_word:
                    self.score += 1
                else:
                    self.score -= 1
                self.remove_ticket = True
                self.word_changed = False
    
    def draw(self, surface):
        surface.blit(self.bg, (0, 0))

        text_surface = self.my_font.render("Score: " + str(self.score), True, pygame.Color("white"))
        surface.blit(text_surface, (self.score_rect.x, self.score_rect.y))

        text_surface = self.my_font.render("Time: " + str(30 - round((self.start_time - time.time()))), True, pygame.Color("white"))
        surface.blit(text_surface, (self.time_rect.x, self.score_rect.y))

        pygame.draw.rect(surface, (180,180,0), self.word_box)
        text_surface = self.my_big_font.render("Word: "  + self.words[self.word_index], True, pygame.Color("white"))
        surface.blit(text_surface, (self.word_box.x + 7, self.word_box.y))

        pygame.draw.rect(surface, (180,180,0), self.time_box)
        text_surface = self.my_big_font.render("Time: " + self.times[self.time_index], True, pygame.Color("white"))
        surface.blit(text_surface, (self.time_box.x + 7, self.time_box.y))

        if self.remove_ticket:
            if self.t_cur_y <= 500:
                self.t_cur_y += 7
                surface.blit(self.ticket_pic, (self.ticket_x, self.t_cur_y))
            else:
                surface.blit(self.ticket_pic, (self.ticket_x, self.t_cur_y))
                self.remove_ticket = False
                self.new_ticket = True
        elif self.new_ticket:
            if not self.word_changed:
                self.word_index = random.randint(0, len(self.words) - 1)
                self.time_index = (self.time_index + 1) % len(self.times)
                weights = []
                for i in range(0, len(self.words)):
                    if i != self.word_index:
                        weights.append(0.4/(len(self.words)-1))
                    else:
                        weights.append(0.6)

                t_weights = []
                for i in range(0, len(self.times)):
                    if i != self.time_index:
                        t_weights.append(0.4/(len(self.times)-1))
                    else:
                        t_weights.append(0.6)
                self.current_word = random.choice([random.choices(self.words, weights = weights)[0], random.choices(self.times, weights = t_weights)[0]])
                self.word_changed = True

            if self.t_cur_y >= self.ticket_y:
                self.t_cur_y -= 7
                #self.ticket_box.top -= 1
                surface.blit(self.ticket_pic, (self.ticket_x, self.t_cur_y))
            else:
                surface.blit(self.ticket_pic, (self.ticket_x, self.t_cur_y))
                self.new_ticket = False
        else:
            surface.blit(self.ticket_pic, (self.ticket_x, self.ticket_y))

       # print(self.current_word)
        text_surface = self.my_big_font.render(self.current_word, True, pygame.Color("white"))
        surface.blit(text_surface, (self.t_cur_x+70, self.t_cur_y+300))

        b_len = 40
        mos_x, mos_y = pygame.mouse.get_pos()
        if mos_x>self.yes_button.x and (mos_x<self.yes_button.x+b_len):
            x_inside = True
        else: x_inside = False
        if mos_y>self.yes_button.y and (mos_y<self.yes_button.y+b_len):
            y_inside = True
        else: y_inside = False
        if x_inside and y_inside:
            #Mouse is hovering over button
            surface.blit(self.yes_over, self.yes_over.get_rect(center = self.yes_button.center))
        else:
            surface.blit(self.yes_pic, self.yes_pic.get_rect(center = self.yes_button.center))

        if mos_x>self.no_button.x and (mos_x<self.no_button.x+b_len):
            x_inside = True
        else: x_inside = False
        if mos_y>self.no_button.y and (mos_y<self.no_button.y+b_len):
            y_inside = True
        else: y_inside = False
        if x_inside and y_inside:
            #Mouse is hovering over button
            surface.blit(self.no_over, self.no_over.get_rect(center = self.no_button.center))
        else:
            surface.blit(self.no_pic, self.no_pic.get_rect(center = self.no_button.center))

        
