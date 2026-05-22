import math
from time import sleep

import pygame

from constants import UI_HEIGHT, TILE_SIZE
from input import handle_left_mouse_event, handle_right_mouse_event, handle_line_key_down, handle_left_click, \
    handle_build_key_down, handle_ui_click
from line import Line
from popup import Popup, StationPopup
from map import metro_map
import global_vars
from station import get_total_revenue

class StateMachine:
    """Class fpr state machine."""
    def __init__(self):
        """Initialize state machine."""
        self.states = {}
        self.current_state = None

    def add(self, name, state):
        """Add a new state."""
        self.states[name] = state

    def change(self, name, **kwargs):
        """Change current state."""
        if self.current_state:
            self.states[self.current_state].exit()
        self.current_state = name
        self.states[self.current_state].enter(**kwargs)

    def update(self):
        """Call the states update function."""
        self.states[self.current_state].update()

    def draw(self, screen: pygame.Surface):
        self.states[self.current_state].draw(screen)

    def handle_events(self, events, sm):
        """Call the states handle_events function."""
        self.states[self.current_state].handle_events(events, sm)

    def handle_ui_events(self, events, sm):
        """Call the states handle_ui_events function."""
        self.states[self.current_state].handle_ui_events(events, sm)

    def enter(self):
        self.states[self.current_state].enter()

class BaseState:
    """Interface for a base state"""
    def __init__(self, sm):
        """Initialize state."""
        self.sm = sm

    def enter(self, **kwargs): pass
    def exit(self): pass
    def update(self): pass
    def draw(self, screen: pygame.Surface): pass
    def handle_events(self, events, sm): pass
    def handle_ui_events(self, events, sm): pass

class NonPopupState(BaseState):
    def handle_ui_events(self, events, sm):
        for event in events:
            handle_ui_click(event, sm)

    def draw(self, screen: pygame.Surface):
        pos = pygame.mouse.get_pos()
        x = math.floor((pos[0] // global_vars.camera.zoom + global_vars.camera.x) / TILE_SIZE)
        y = math.floor(((pos[1] - UI_HEIGHT) // global_vars.camera.zoom + global_vars.camera.y) / TILE_SIZE)

        for column, tile_row in enumerate(metro_map):
            for row, tile in enumerate(tile_row):
                if tile == 2:
                    metro_map[column][row] = 0

        if pos[1] < UI_HEIGHT:
            return

        metro_map[y][x] = 2

        #if one second has passed get revenue
        if global_vars.frame >= 60:
            revenue = round(get_total_revenue())
            global_vars.money += revenue
            global_vars.mps = revenue
            global_vars.frame = 0

class BuildMode(NonPopupState):
    """Class for the build mode state"""
    def handle_events(self, events, sm):
        """Handle input."""
        for event in events:
            #check if left pressed
            pos = handle_left_mouse_event(event)
            if pos:
                #build new line at pos
                mx, my = pos

                if my < UI_HEIGHT:
                    return

                x = math.floor((mx // global_vars.camera.zoom + global_vars.camera.x) / TILE_SIZE)
                y = math.floor(((my - UI_HEIGHT) // global_vars.camera.zoom + global_vars.camera.y) / TILE_SIZE)
                if y < 0:
                    return
                y = int(y)

                if Line.line_index < len(Line.lines):
                    Line.lines[Line.line_index].add_tile(x, y)

            Line.line_index = handle_line_key_down(event, Line.line_index)

            #check if right key pressed
            pos = handle_right_mouse_event(event)
            if pos:
                #build station at pos
                mx, my = pos

                if my < UI_HEIGHT:
                    return

                world_x = mx / global_vars.camera.zoom + global_vars.camera.x
                world_y = (my - UI_HEIGHT) / global_vars.camera.zoom + global_vars.camera.y

                x = int(world_x // TILE_SIZE)
                y = int(world_y // TILE_SIZE)
                if y < 0:
                    return

                self.sm.change("StationPopupMode", x=x, y=y)

            #check if K pressed
            if handle_build_key_down(event):
                self.sm.change("SelectMode")

class SelectMode(NonPopupState):
    """Class for select mode state."""
    def handle_events(self, events, sm):
        """Handle input."""
        for event in events:
            #check if left key clicked
            handle_left_click(event)
            #check if state needs to change
            if handle_build_key_down(event):
                self.sm.change("BuildMode")

class PopupMode(BaseState):
    """Class for popup state."""
    def __init__(self, sm, popup: Popup):
        #get a popup object parsed in additionally
        super().__init__(sm)
        self.popup: Popup = popup
        self.x = 0
        self.y = 0

    def enter(self, **kwargs):
        """Parse the x and y position in case of station placement."""
        if "x" in kwargs:
            self.x = kwargs["x"]

        if "y" in kwargs:
            self.y = kwargs["y"]

        if type(self.popup) == StationPopup:
            self.popup.set_position(self.x, self.y)

        self.popup.open()

    def exit(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, screen: pygame.Surface):
        """Draw the popup."""
        if self.popup:
            self.popup.draw(screen)

    def handle_ui_events(self, events, sm):
        """Handle UI Input."""
        #check if a button on popup was clicked
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = event.pos
                    if self.popup:
                        self.popup.is_clicked(x, y, sm)

    def handle_events(self, events, sm):
        """Handle input for the Text Input"""
        self.popup.capture_input(events, sm)

class NewLineState(BaseState):
    """State when placing a new line."""
    def __init__(self, sm):
        """Initialize a color variable additionally"""
        super().__init__(sm)
        self.color = None

    def set_color(self, color):
        """Set the color variable."""
        self.color = color

    def handle_events(self, events, sm):
        """Handle input"""
        for event in events:
            #get mouse pos
            pos = handle_left_mouse_event(event)
            if pos:
                mx, my = pos

                x = math.floor((mx // global_vars.camera.zoom + global_vars.camera.x) / TILE_SIZE)
                y = math.floor(((my - UI_HEIGHT) // global_vars.camera.zoom + global_vars.camera.y) / TILE_SIZE)
                #get the old length of lines
                old_len = len(Line.lines)
                #check if ui area was clicked
                if mx // TILE_SIZE < 0 or my // TILE_SIZE - UI_HEIGHT // TILE_SIZE < 0:
                    return

                #try to add a line
                Line(x, y, self.color)
                #if line adding was successfully
                if len(Line.lines) > old_len:
                    #change back to build mode
                    Line.line_index = len(Line.lines) - 1
                    self.sm.change("BuildMode")

    def draw(self, screen: pygame.Surface):
        pos = pygame.mouse.get_pos()
        x = math.floor((pos[0] // global_vars.camera.zoom + global_vars.camera.x) / TILE_SIZE)
        y = math.floor(((pos[1] - UI_HEIGHT) // global_vars.camera.zoom + global_vars.camera.y) / TILE_SIZE)

        for column, tile_row in enumerate(metro_map):
            for row, tile in enumerate(tile_row):
                if tile == 2:
                    metro_map[column][row] = 0

        if pos[1] < UI_HEIGHT:
            return

        metro_map[y][x] = 2

        #if one second has passed get revenue
        if global_vars.frame >= 60:
            revenue = round(get_total_revenue())
            global_vars.money += revenue
            global_vars.mps = revenue
            global_vars.frame = 0