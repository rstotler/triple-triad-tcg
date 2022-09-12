import pygame, os
from pygame import *
pygame.init()

TITLE = "Triple Triad TCG Adventure"
VERSION = "v0.047"
SCREEN_SIZE = [800, 600]
BORDER_INDENT = 6
PLAYER_COLOR = [[60, 60, 100], [100, 40, 40], [140, 20, 140]]
CARD_COUNT = 13

# Fonts #
FONT_ROMAN_16 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/CodeNewRomanB.otf", 16)
FONT_ROMAN_42 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/CodeNewRomanB.otf", 42)
FONT_ROMAN_116 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/CodeNewRomanB.otf", 116)
FONT_FF_32 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/FinalFantasy.ttf", 32)
FONT_FF_54 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/FinalFantasy.ttf", 54)
