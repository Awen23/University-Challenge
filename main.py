import sys
import pygame
from states.duck_duck_revolution import DuckDuckRevolution
from states.meal_deal_mania import MealDealMania
from states.shelf_search import ShelfSearch

from states.overworld import Overworld
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
    "MEAL DEAL MANIA": MealDealMania(),
    "SHELF SEARCH": ShelfSearch(),
    "DUCK DUCK REVOLUTION": DuckDuckRevolution()
}

game = Game(screen, states, "MAIN MENU")
game.run()