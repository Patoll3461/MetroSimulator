from constants import SCREEN_X, WORLD_X, SCREEN_Y, WORLD_Y, UI_HEIGHT

import pygame

class Camera:
    def __init__(self, viewport: tuple[int, int], min_zoom: float, max_zoom):
        """Initialize camera."""
        self.x, self.y = viewport
        self.zoom = 1
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def change_zoom(self, zoom_factor):
        """Zoom in or out."""
        #get mouse pos
        mx, my = pygame.mouse.get_pos()

        #convert to world pos
        world_x = self.x + mx / self.zoom
        world_y = self.y + (my - UI_HEIGHT) / self.zoom

        #zoom and clamp
        self.zoom += zoom_factor
        if self.zoom >= self.max_zoom:
            self.zoom = self.max_zoom
        if self.zoom <= self.min_zoom:
            self.zoom = self.min_zoom

        #reset position to world pos from before so the cam zooms onto mouse cursor
        self.x = world_x - mx / self.zoom
        self.y = world_y - (my - UI_HEIGHT) / self.zoom

        #clamp position
        visible_width = SCREEN_X / self.zoom
        visible_height = (SCREEN_Y - UI_HEIGHT) / self.zoom

        if self.x >= WORLD_X - visible_width:
            self.x = WORLD_X - visible_width
        if self.x <= 0:
            self.x = 0

        if self.y >= WORLD_Y - visible_height:
            self.y = WORLD_Y - visible_height
        if self.y <= 0:
            self.y = 0

        #scale(self.zoom)

    def move(self, vector: tuple[int, int]):
        """Move the camera."""
        #adjust pos
        self.x += vector[0]
        self.y += vector[1]

        #clamp pos
        visible_width = SCREEN_X / self.zoom
        visible_height = (SCREEN_Y - UI_HEIGHT) / self.zoom

        if self.x >= WORLD_X - visible_width:
            self.x = WORLD_X - visible_width
        if self.x <= 0:
            self.x = 0

        if self.y >= WORLD_Y - visible_height:
            self.y = WORLD_Y - visible_height
        if self.y <= 0:
            self.y = 0