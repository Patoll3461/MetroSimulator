import math

import pygame

#constants
TILE_SIZE = 64
LINE_WIDTH = math.ceil(TILE_SIZE / 2 * (1 / 3))
V_H_INDEX_ORDER = [1, 2, 0, 3, -1]
SCREEN_X = 960
SCREEN_Y = 640
UI_HEIGHT = 64
MAX_LINES = 10
POPUP_X = 640
POPUP_Y = 320

COLORS = [pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255), pygame.Color(255, 255, 0), pygame.Color(0, 255, 255), pygame.Color(255, 0, 255), pygame.Color(166, 255, 192), pygame.Color(255, 145, 0), pygame.Color(250, 186, 255), pygame.Color(60, 46, 128)]

#UI constants
mode_button_offset = 30
mode_button_width = 256
mode_button_height = 32

line_offset = 10
line_distance = 8
line_width = 32
line_height = 32