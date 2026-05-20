from constants import SCREEN_X, WORLD_X, SCREEN_Y, WORLD_Y


class Camera:
    def __init__(self, viewport: tuple[int, int], min_zoom: float, max_zoom):
        self.x, self.y = viewport
        self.zoom = 1
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def change_zoom(self, zoom_factor):
        self.zoom += zoom_factor
        if self.zoom >= self.max_zoom:
            self.zoom = self.max_zoom
        if self.zoom <= self.min_zoom:
            self.zoom = self.min_zoom

    def move(self, vector: tuple[int, int]):
        self.x += vector[0]
        self.y += vector[1]

        if self.x >= WORLD_X - (SCREEN_X / self.zoom):
            self.x = WORLD_X - (SCREEN_X / self.zoom)
        if self.x <= 0:
            self.x = 0
        if self.y >= WORLD_Y - (SCREEN_Y / self.zoom):
            self.y = WORLD_Y - (SCREEN_Y / self.zoom)
        if self.y <= 0:
            self.y = 0