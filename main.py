import sys
import pygame
from states.meal_deal_mania import MealDealMania
from states.overworld import Overworld
# minigame states here
from game import Game

pygame.init()
screen = pygame.display.set_mode((1280, 720))
states = {
    "OVERWORLD": Overworld(),
    # minigame states here
    "MEAL DEAL MANIA": MealDealMania()
}

game = Game(screen, states, "OVERWORLD")
game.run()