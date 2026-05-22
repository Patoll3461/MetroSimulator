import math

import pygame

#constants

#tile size
TILE_SIZE = 64
#width of lines
LINE_WIDTH = math.ceil(TILE_SIZE / 2 * (1 / 3))

#order for line on tile
V_H_INDEX_ORDER = [1, 2, 0, 3, -1]
#screen size
SCREEN_X = 960
SCREEN_Y = 640
#world size
WORLD_X = 1920
WORLD_Y = 1152
#height of ui bar
UI_HEIGHT = 64
#maximum number of lines
MAX_LINES = 10
#size of popup
POPUP_X = 640
POPUP_Y = 320

#available colors for lines
COLORS = [pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255), pygame.Color(255, 255, 0), pygame.Color(0, 255, 255), pygame.Color(255, 0, 255), pygame.Color(166, 255, 192), pygame.Color(255, 145, 0), pygame.Color(250, 186, 255), pygame.Color(60, 46, 128)]

#radius of a station
STATION_RADIUS = 3

#prices
LINE_BASE_PRICE = 30
STATION_BASE_PRICE = 60
START_MONEY = 1000

#UI constants

#mode toggle button
mode_button_offset = 15
mode_button_width = 92
mode_button_height = 32

#money
money_offset = 10
money_width = 192
money_height = 32

#line buttons
line_offset = 10
line_distance = 4
line_width = 32
line_height = 32

#max size for park clusters
big_park_max_size = 25
middle_park_max_size = 15
small_park_max_size = 8

#max size for settlement cluster
max_settlement_size = 20

#max size for industry cluster
max_industry_size = 5