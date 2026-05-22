import math
import pygame

import global_vars
import warn_popup
from camera import Camera
from constants import *
from line import Line, delete_line
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
        line_index -= 1
        if line_index < 0:
            line_index = len(Line.lines) - 1

    #next line
    if event.key == pygame.K_RIGHT:
        line_index += 1
        if line_index >= len(Line.lines):
            line_index = 0

    return line_index

def handle_build_key_down(event):
    """Toggle build mode if B is pressed."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_b:
            return True
        if event.key == pygame.K_BACKSPACE:
            global_vars.camera.zoom = 1
            global_vars.camera.x = 0
            global_vars.camera.y = 0
    return False

def handle_left_click(event):
    """Handle left click in select mode."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            #get screen pos and convert to world
            x = math.floor((global_vars.camera.x + event.pos[0] / global_vars.camera.zoom) / TILE_SIZE)
            y = math.floor((global_vars.camera.y + (event.pos[1] - UI_HEIGHT) / global_vars.camera.zoom) / TILE_SIZE)

            if y < 0:
                return
            y = int(y)
            if Station.station_map[y][x]:
                #set selected station to the station at clickd tile pos
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
                        if len(Line.lines) < 10:
                            #if the plus button was clicked show the select color popup
                            sm.change("ColorPopupMode")

        if event.button == 3:
            x,y = event.pos

            # check if a line button was clicked
            for i in range(len(Line.lines) + 1):
                rect = pygame.Rect(i * line_width + line_offset + i * line_distance, UI_HEIGHT // 2 - line_height // 2,
                                   line_width, line_height)

                if rect.collidepoint(float(x), float(y)):
                    if i < len(Line.lines):
                        delete_line(i)

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
            global_vars.camera.move((-dx / global_vars.camera.zoom, -dy / global_vars.camera.zoom))


def handle_scroll_wheel(events):
    for event in events:
        #print(event.type, "type")
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.button, "button")
            if event.button == 132:
                global_vars.camera.change_zoom(0.1)
            if event.button == 133:
                global_vars.camera.change_zoom(-0.1)