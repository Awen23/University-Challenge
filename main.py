import sys
import pygame
from states.meal_deal_mania import MealDealMania
from states.overworld import Overworld
from states.coursework_crunch import CourseworkCrunch
from states.tickets_thanks import TicketsThanks
from states.game_start import GameStart
# minigame states here
from game import Game

pygame.init()
screen = pygame.display.set_mode((1280, 720))
states = {
    "OVERWORLD": Overworld(),
    # minigame states here
    "MEAL DEAL MANIA": MealDealMania(),
    "COURSEWORK CRUNCH": CourseworkCrunch(),
    "TICKETS THANKS": TicketsThanks(),
    "GAME START": GameStart("Tickets Thanks!", "states/data/bus_stop.png", "states/data/busboi.png", "states/data/tickets_thanks.txt", "TICKETS THANKS")
}

game = Game(screen, states, "GAME START")
game.run()