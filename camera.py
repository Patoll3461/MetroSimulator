from constants import SCREEN_X, WORLD_X, SCREEN_Y, WORLD_Y


class Camera:
    def __init__(self, viewport: tuple[int, int], zoom: int, max_zoom):
        self.x, self.y = viewport
        self.zoom = zoom
        self.max_zoom = max_zoom

    def zoom(self, zoom_factor):
        self.zoom += zoom_factor
        if self.zoom >= self.max_zoom:
            self.zoom = self.max_zoom

    def move(self, vector: tuple[int, int]):
        self.x += vector[0]
        self.y += vector[1]

        if self.x >= WORLD_X - SCREEN_X:
            self.x = WORLD_X - SCREEN_X
        if self.x <= 0:
            self.x = 0
        if self.y >= WORLD_Y - SCREEN_Y:
            self.y = WORLD_Y - SCREEN_Y
        if self.y <= 0:
            self.y = 0