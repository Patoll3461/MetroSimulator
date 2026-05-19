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
#height of ui bar
UI_HEIGHT = 64
#maximum number of lines
MAX_LINES = 10
#size of popup
POPUP_X = 640
POPUP_Y = 320

#available colors for lines
COLORS = [pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255), pygame.Color(255, 255, 0), pygame.Color(0, 255, 255), pygame.Color(255, 0, 255), pygame.Color(166, 255, 192), pygame.Color(255, 145, 0), pygame.Color(250, 186, 255), pygame.Color(60, 46, 128)]

#UI constants

#mode toggle button
mode_button_offset = 30
mode_button_width = 256
mode_button_height = 32

#line buttons
line_offset = 10
line_distance = 8
line_width = 32
line_height = 32