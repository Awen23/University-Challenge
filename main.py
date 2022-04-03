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
    "COURSEWORK CRUNCH": CourseworkCrunch(),
    "TICKETS THANKS": TicketsThanks(),
    "GAME START": GameStart("Tickets Thanks!", "states/data/bus_stop.png", "states/data/busboi.png", "states/data/tickets_thanks.txt", "TICKETS THANKS"),
    "MEAL DEAL MANIA": MealDealMania(),
    "DUCK DUCK REVOLUTION": DuckDuckRevolution()
}

game = Game(screen, states, "MAIN MENU")
game.run()