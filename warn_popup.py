import pygame

from constants import SCREEN_X, SCREEN_Y


class WarnPopup:
    """Class for the warn popup."""
    def __init__(self, color, font, width, height):
        """Initialize the popup"""
        self.is_active = False
        self.color = color
        self.font = font
        self.width = width
        self.height = height
        self.text = ""
        self.timer = 0

    def open(self, text):
        """Open the popup."""
        self.is_active = True
        self.text = text
        self.timer = 0

    def close(self):
        """Close the popup."""
        self.is_active = False
        self.text = ""
        self.timer = 0

    def draw(self, screen):
        """Draw the popup."""
        #abort if inactive
        if not self.is_active:
            return

        #draw rect
        pygame.draw.rect(screen, self.color, ((SCREEN_X - self.width) / 2, SCREEN_Y - self.height - 30, self.width, self.height))

        #draw message
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_X / 2, SCREEN_Y - 30 - self.height / 2))

        screen.blit(text, text_rect)

        #increase timer
        self.timer += 1

        #after two seconds close popup
        if self.timer  >= 90:
            self.close()