import math
import pygame

import global_vars
import warn_popup
from constants import *
from line import Line
from station import Station

middle_held = False

def handle_left_mouse_event(event):
    """Return mouse pos on left click."""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        return event.pos
    return None

def handle_right_mouse_event(event):
    """Return mouse pos on right click."""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        return event.pos
    return None

def handle_line_key_down(event, line_index):
    """Switch to previous/next line in build mode for building."""
    if event.type != pygame.KEYDOWN:
        return line_index

    #last line
    if event.key == pygame.K_LEFT:
        line_index += 1
        if line_index >= len(Line.lines):
            line_index = 0

    #next line
    if event.key == pygame.K_RIGHT:
        line_index -= 1
        if line_index < 0:
            line_index = len(Line.lines) - 1

    return line_index

def handle_build_key_down(event):
    """Toggle build mode if K is pressed."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_b:
            global_vars.camera.x = 14 * TILE_SIZE
            #print("test")
            return True
    return False

def handle_left_click(event):
    """Handle left click in select mode."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            x = math.floor((event.pos[0] + global_vars.camera.x) / TILE_SIZE)
            y = math.floor((event.pos[1] + global_vars.camera.y - UI_HEIGHT) / TILE_SIZE)
            if y < 0:
                return
            y = int(y)
            if Station.station_map[y][x]:
                global_vars.selected_station = Station.station_map[y][x].name

def handle_ui_click(event, sm):
    """Handles click in the UI area."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            x,y = event.pos

            #toggle build mode
            if SCREEN_X - mode_button_offset - mode_button_width < x < SCREEN_X - mode_button_offset:
                if UI_HEIGHT // 2 - mode_button_height < y < UI_HEIGHT // 2 + mode_button_height:
                    if sm.current_state == "BuildMode":
                        sm.change("SelectMode")
                    else:
                        sm.change("BuildMode")

            #check if a line button was clicked
            for i in range(len(Line.lines) + 1):
                rect = pygame.Rect(i * line_width + line_offset + i * line_distance, UI_HEIGHT // 2 - line_height // 2, line_width, line_height)

                if rect.collidepoint(float(x), float(y)):
                    if i < len(Line.lines):
                        Line.line_index = i
                    else:
                        #if the plus button was clicked show the select color popup
                        sm.change("ColorPopupMode")

def handle_mouse_move(events):
    global middle_held

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # middle mouse
                middle_held = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                middle_held = False

        if event.type == pygame.MOUSEMOTION and middle_held:
            dx, dy = event.rel
            global_vars.camera.move((-dx, -dy))


def handle_scroll_wheel(events):
    for event in events:
        #print(event.type, "type")
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.button, "button")
            if event.button == 132:
                global_vars.camera.change_zoom(0.1)
            if event.button == 133:
                global_vars.camera.change_zoom(-0.1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                global_vars.camera.zoom = 1