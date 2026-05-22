from station import get_total_revenue
from warn_popup import WarnPopup
from constants import SCREEN_X, LINE_BASE_PRICE, STATION_BASE_PRICE, START_MONEY
from camera import Camera

import pygame
import math
import argparse

font = None
selected_station = ""
warn_popup = None
camera = None
money = 0
mps = 0
line_min_price = 0
station_min_price = 0
frame = 0

#variables that need global access
def init():
    """Initialize global vars"""
    global font, selected_station, warn_popup, camera, money, mps, line_min_price, station_min_price, frame

    #main camera
    camera = Camera((0, 0), 0.5, 3)
    #font used for ui
    font = pygame.font.SysFont(None, 36)
    #the currently selected station to be displayed at top
    selected_station = ""
    #the warn popup that can popup at the bottom
    warn_popup = WarnPopup(pygame.Color(255, 205, 69), font, SCREEN_X - 200, 50)
    #current money amount
    money = START_MONEY
    #money per second
    mps = 0
    #line price min
    line_min_price = LINE_BASE_PRICE
    #station price min
    station_price_min = STATION_BASE_PRICE
    #current frame
    frame = 0

def check_money(base_price, minimum):
    """Check if money is present"""
    global money

    #calculate prise based of base price, current money per second and minimum
    price = max(minimum, round(base_price * (1 + 0.1 * math.log2(1 + mps))))

    #return the price
    if money < price:
        return False, price
    else:
        money -= price
        return True, price