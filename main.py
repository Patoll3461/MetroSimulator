import pygame
import sys
import math

from camera import Camera
from constants import *
import global_vars
from input import handle_mouse_move
from line import Line, LineState
from map import metro_map
from popup import ColorPopup, StationPopup
from state_machine import StateMachine, BuildMode, SelectMode, PopupMode, NewLineState
from station import Station

build_mode = False
hover = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

def start():
    """Start the game and run the game loop."""
    global build_mode
    pygame.init()

    global_vars.init()

    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption("Metro Simulator")

    #init game
    running = True
    clock = pygame.time.Clock()
    #define font
    font = pygame.font.SysFont(None, 36)

    #define popups
    color_popup = ColorPopup(pygame.Color(184, 184, 184), font)
    station_popup = StationPopup(pygame.Color(184, 184, 184), font)

    #initialize game state
    sm = StateMachine()
    sm.add("BuildMode", BuildMode(sm))
    sm.add("SelectMode", SelectMode(sm))
    sm.add("ColorPopupMode", PopupMode(sm, color_popup))
    sm.add("StationPopupMode", PopupMode(sm, station_popup))
    sm.add("NewLineMode", NewLineState(sm))
    sm.change("SelectMode")

    while running:
        #get events
        events = pygame.event.get()

        #check for game stop
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #handle input based on state
        sm.handle_events(events)
        sm.handle_ui_events(events, sm)
        sm.update()

        handle_mouse_move(events)
        #fill screen white
        screen.fill((255, 255, 255))
        #draw lines, stations and UI
        draw_screen(screen, global_vars.camera)
        draw_ui(screen, font, sm.current_state)
        sm.draw(screen)
        global_vars.warn_popup.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    #quit game
    pygame.quit()
    sys.exit()


def draw_screen(screen: pygame.Surface, camera: Camera):
    """Render the screen elements."""
    global hover

    x_bounds = len(metro_map[0])
    y_bounds = len(metro_map)

    viewport = (camera.x, camera.y)

    pygame.draw.rect(screen, pygame.Color(0, 0, 0), (0, UI_HEIGHT - 5, x_bounds * TILE_SIZE, 5))

    for row_index in range(viewport[1] // TILE_SIZE, y_bounds):
        row = metro_map[row_index]

        for col_index in range(viewport[0] // TILE_SIZE, x_bounds):
            tile = metro_map[row_index][col_index]

            x = col_index * TILE_SIZE - camera.x
            y = row_index * TILE_SIZE - camera.y

            #draw hover if map value is two
            if tile == 2 and y > UI_HEIGHT - TILE_SIZE:
                hover.fill((0, 0, 0, 128))
                screen.blit(hover, (x, y))

            #render lines in case of line
            if len(Line.line_map[row_index][col_index]) > 0:
                lines: list[LineState] = Line.line_map[row_index][col_index]
                line_amount = count_lines(lines)

                for index, line in enumerate(lines):
                    #horizontal line
                    if line.orientation == 0:
                        draw_lines_horizontal(screen, lines[index].line.color, x, y + UI_HEIGHT, line_amount, lines[index].h_index)
                        #vertical line
                    elif line.orientation == 1:
                        draw_line_vertical(screen, lines[index].line.color, x, y + UI_HEIGHT, line_amount, lines[index].v_index)
                    elif 2 <= line.orientation <= 5:
                        draw_edge(screen, lines[index].line.color, x, y + UI_HEIGHT, line_amount, lines[index].h_index, lines[index].v_index, line.orientation - 2)

            if Station.station_map[row_index][col_index]:
                draw_circle(screen, pygame.Color(71, 186, 250), x, y + UI_HEIGHT)

def count_lines(lines: list[LineState]) -> tuple[int, int]:
    """Count the horizontal/vertical lines on a tile."""
    h = 0
    v = 0

    for line in lines:
        if line.orientation == 0:
            h += 1
        elif line.orientation == 1:
            v += 1
        else:
            v += 1
            h += 1

    return h, v

def draw_lines_horizontal(screen: pygame.Surface, color: pygame.Color, x: int, y: int, line_amount: tuple[int, int], index: int):
    """Draw a horizontal line all the way through."""
    pygame.draw.rect(screen, color,(x, y + 0.25 * TILE_SIZE + index * (TILE_SIZE / 2 * (1 / 3)), TILE_SIZE, LINE_WIDTH))

def draw_line_vertical(screen: pygame.Surface, color: pygame.Color, x: int, y: int, line_amount: tuple[int, int], index: int):
    """Draw a vertical line all the way through."""
    pygame.draw.rect(screen, color, (x + 0.25 * TILE_SIZE + index * (TILE_SIZE / 2 * (1 / 3)), y, LINE_WIDTH, TILE_SIZE))

def draw_edge(screen, color, x, y, line_amount, h_index, v_index, orientation):
    """Draw an edge consisting of two different parts, horizontal and vertical."""
    #Good luck debugging this only god knows how it works
    if orientation == 0:
        draw_vertical_edge_part(screen, color, x, y, line_amount, v_index, 0, (0.25 * TILE_SIZE + h_index * (TILE_SIZE / 2 * (1 / 3))) + LINE_WIDTH)
        draw_horizontal_edge_part(screen, color, x, y, line_amount, h_index, 0, (0.25 * TILE_SIZE + v_index * (TILE_SIZE / 2 * (1 / 3))) + LINE_WIDTH)
    elif orientation == 1:
        draw_vertical_edge_part(screen, color, x, y, line_amount, v_index, 0, (0.25 * TILE_SIZE + h_index * (TILE_SIZE / 2 * (1 / 3))) + LINE_WIDTH)
        draw_horizontal_edge_part(screen, color, x, y, line_amount, h_index, 0.25 * TILE_SIZE + v_index * (TILE_SIZE / 2 * (1 / 3)), math.ceil(TILE_SIZE - (0.25 * TILE_SIZE + v_index * (TILE_SIZE / 2 * (1 / 3)))))
    elif orientation == 2:
        draw_vertical_edge_part(screen, color, x, y, line_amount, v_index, 0.25 * TILE_SIZE + h_index * (TILE_SIZE / 2 * (1 / 3)), math.ceil(TILE_SIZE - (0.25 * TILE_SIZE + h_index * (TILE_SIZE / 2 * (1 / 3)))))
        draw_horizontal_edge_part(screen, color, x, y, line_amount, h_index,  0.25 * TILE_SIZE + v_index * (TILE_SIZE / 2 * (1 / 3)), math.ceil(TILE_SIZE - (0.25 * TILE_SIZE + v_index * (TILE_SIZE / 2 * (1 / 3)))))
    elif orientation == 3:
        draw_vertical_edge_part(screen, color, x, y, line_amount, v_index, 0.25 * TILE_SIZE + h_index * (TILE_SIZE / 2 * (1 / 3)), math.ceil(TILE_SIZE - (0.25 * TILE_SIZE + h_index * (TILE_SIZE / 2 * (1 / 3)))))
        draw_horizontal_edge_part(screen, color, x, y, line_amount, h_index, 0, (0.25 * TILE_SIZE + v_index * (TILE_SIZE / 2 * (1 / 3))) + LINE_WIDTH)

def draw_horizontal_edge_part(screen, color, x, y, line_amount, index, offset, width):
    """Draw the horizontal part of the edge."""
    pygame.draw.rect(screen, color,(x + offset, y + 0.25 * TILE_SIZE + index * (TILE_SIZE / 2 * (1 / 3)), width, LINE_WIDTH))

def draw_vertical_edge_part(screen, color, x, y, line_amount, index, offset, height):
    """Draw the vertical part of the edge."""
    pygame.draw.rect(screen, color, (x + 0.25 * TILE_SIZE + index * (TILE_SIZE / 2 * (1 / 3)), y + offset, LINE_WIDTH, height))

def draw_circle(screen, color, x, y):
    """Draw two circles for a station object."""
    size = 0.33

    if len(Line.line_map[y // TILE_SIZE - UI_HEIGHT // TILE_SIZE][x // TILE_SIZE]) >= 4:
        size = 0.5

    pygame.draw.circle(screen, color, (x + TILE_SIZE / 2, y + TILE_SIZE / 2), math.ceil(TILE_SIZE * size))
    pygame.draw.circle(screen, pygame.Color(0, 0, 0), (x + TILE_SIZE / 2, y + TILE_SIZE / 2), math.ceil(TILE_SIZE * size), 5)


def draw_ui(screen, font, game_state):
    """Draw the top bar UI"""
    #draw over lines and hovers falsely renders in ui space
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), (0, 0, SCREEN_X, UI_HEIGHT - 3))
    #draw the line ui
    for i in range(0, len(Line.lines) + 1):
        if i < len(Line.lines):
            line = Line.lines[i]
            rect = pygame.draw.rect(screen, line.color, (i * line_width + line_offset + i * line_distance, UI_HEIGHT / 2 - line_height / 2, line_width, line_height))
            #draw an outline on selected line
            if i == Line.line_index:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                #draw the number text
            number = font.render(str(i + 1), True, (0, 0, 0))
            text_rect = number.get_rect(center=rect.center)
            screen.blit(number, text_rect)
        else:
            #draw the add line button
            rect = pygame.Rect(i * line_width + line_offset + i * line_distance, UI_HEIGHT // 2 - line_height // 2, line_width, line_height)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            number = font.render("+", True, (0, 0, 0))
            text_rect = number.get_rect(center=rect.center)
            screen.blit(number, text_rect)

    #draw the build mode toggle button
    rect = pygame.draw.rect(screen, pygame.Color(39, 171, 166), (SCREEN_X - mode_button_offset - mode_button_width, UI_HEIGHT // 2 - mode_button_height // 2, mode_button_width, mode_button_height))
    text = font.render("Select Mode" if game_state == "SelectMode" else "Build Mode", True, (0, 0, 0))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

    #draw the current station text
    station_text = font.render(global_vars.selected_station, True, (0, 0, 0))
    station_text_rect = station_text.get_rect(midleft=(len(Line.lines) * line_width + line_offset + len(Line.lines) * line_distance + 50, UI_HEIGHT // 2))
    screen.blit(station_text, station_text_rect)

if __name__ == "__main__":
    start()