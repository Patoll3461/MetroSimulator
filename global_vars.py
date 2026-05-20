from warn_popup import WarnPopup
from constants import SCREEN_X
from camera import Camera

import pygame

font = None
selected_station = ""
warn_popup = None
camera = None

#variables that need global access
def init():
    global font, selected_station, warn_popup, camera

    camera = Camera((0, 0), 0.5, 3)
    font = pygame.font.SysFont(None, 36)
    selected_station = ""
    warn_popup = WarnPopup(pygame.Color(255, 205, 69), font, SCREEN_X - 200, 50)