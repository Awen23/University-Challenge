import sys
import pygame
from states.duck_duck_revolution import DuckDuckRevolution
from states.meal_deal_mania import MealDealMania
from states.shelf_search import ShelfSearch

from states.overworld import Overworld
from states.coursework_crunch import CourseworkCrunch
from states.tickets_thanks import TicketsThanks
from states.game_start import GameStart
from states.main_menu import MainMenu
# minigame states here
from game import Game

pygame.init()
screen = pygame.display.set_mode((1280, 720))
states = {
    "MAIN MENU": MainMenu(),
    "OVERWORLD": Overworld(),
    # minigame states here
    # coursework crunch
    "COURSEWORK CRUNCH": CourseworkCrunch(),
    "MEAL DEAL MANIA": MealDealMania(),
    "MEAL DEAL MANIA GAME START": GameStart("Meal Deal Mania!", "states/data/fresh.png", "states/data/busboi.png", "states/data/meal_deal_mania.txt", "MEAL DEAL MANIA"),
    "SHELF SEARCH": ShelfSearch(),
    "DUCK DUCK REVOLUTION": DuckDuckRevolution(),
    "DUCK DUCK REVOLUTION GAME START": GameStart("Duck Duck Revolution!", "student_union/student_union_blurred.png", "states/data/busboi.png", "states/data/duck_duck_revolution.txt", "DUCK DUCK REVOLUTION"),
    "TICKETS THANKS": TicketsThanks(),
    "TICKETS THANKS GAME START": GameStart("Tickets Thanks!", "states/data/bus_stop.png", "states/data/busboi.png", "states/data/tickets_thanks.txt", "TICKETS THANKS")
}

# game = Game(screen, states, "MAIN MENU")
game = Game(screen, states, "DUCK DUCK REVOLUTION")
game.run()