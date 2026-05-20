from warn_popup import WarnPopup
from constants import SCREEN_X
import pygame

font = None
selected_station = ""
warn_popup = None

#variables that need global access
def init():
    global font, selected_station, warn_popup

    font = pygame.font.SysFont(None, 36)
    selected_station = ""
    warn_popup = WarnPopup(pygame.Color(255, 205, 69), font, SCREEN_X - 200, 50)