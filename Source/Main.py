import pygame, Config
from pygame import *
from Data import Main

window = pygame.display.set_mode(Config.SCREEN_SIZE, 0, 32)
pygame.display.set_caption(Config.TITLE + " " + Config.VERSION)
pygame.display.set_icon(pygame.image.load("../Image/Icon.png").convert_alpha())
clock = pygame.time.Clock()
main = Main.Load(window)

while True:
    lastTick = clock.tick(60) / 1000.0
    main.updateMain(str(clock.get_fps())[0:5], window)
