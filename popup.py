import pygame

from constants import SCREEN_X, POPUP_X, SCREEN_Y, POPUP_Y, line_width, line_height, COLORS
from line import Line


class Popup:
    """Interface for popup objects."""
    def __init__(self, color, font):
        """Initialize the popup"""
        self.color = color
        self.font = font
    def draw(self, screen: pygame.Surface): pass
    def show(self): pass
    def is_clicked(self, x, y, sm): pass

class ColorPopup(Popup):
    """Class for color picker popup."""
    def __init__(self, color, font):
        """Initialize the selected color index as well."""
        super().__init__(color, font)
        self.selected = None

    def draw(self, screen: pygame.Surface):
        """Draw the popup."""
        #calculate coordinates for heading
        rect = pygame.Rect((SCREEN_X - POPUP_X) // 2, (SCREEN_Y - POPUP_Y) // 2, POPUP_X, POPUP_Y)

        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        header = self.font.render("Select a color", True, (0, 0, 0))

        popup_x = (SCREEN_X - POPUP_X) // 2
        popup_y = (SCREEN_Y - POPUP_Y) // 2

        #render heading
        header_rect = header.get_rect(center=(SCREEN_X / 2, popup_y + 40))
        screen.blit(header, header_rect)

        #calculate sizes for the color picker grid
        cols = 5
        rows = 2

        spacing = 10

        grid_width = cols * line_width + (cols - 1) * spacing
        grid_height = rows * line_height + (rows - 1) * spacing

        popup_x = (SCREEN_X - POPUP_X) // 2
        popup_y = (SCREEN_Y - POPUP_Y) // 2

        start_x = popup_x + (POPUP_X - grid_width) // 2
        start_y = popup_y + 100

        i = 0

        for row_index in range(rows):
            for col_index in range(cols):
                #calculate individual object size
                rect = pygame.Rect(start_x + col_index * (line_width + spacing), start_y + row_index * (line_height + spacing), line_width, line_height)
                color = COLORS[i]

                #if color is already used show it as grey
                if COLORS[i] in [l.color for l in Line.lines]:
                    color = pygame.Color(143, 143, 143)

                pygame.draw.rect(screen, color, rect)

                #outline the selected color
                if self.selected is not None:
                    if COLORS[self.selected] == COLORS[i] and color != pygame.Color(143, 143, 143):
                        pygame.draw.rect(screen, (0, 0, 0), rect, 3)


                i += 1

        #render submit button
        button_text = self.font.render("Submit", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=(SCREEN_X // 2, popup_y + POPUP_Y - 80))
        bg_rect = button_rect.inflate(20, 10)

        pygame.draw.rect(screen, (255, 171, 61), bg_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)

        screen.blit(button_text, button_rect)

    def is_clicked(self, x, y, sm):
        """Check if a popup button was clicked."""
        #calculate the color picker grid for collision detection
        popup_x = (SCREEN_X - POPUP_X) // 2
        popup_y = (SCREEN_Y - POPUP_Y) // 2

        cols = 5
        rows = 2

        spacing = 10

        grid_width = cols * line_width + (cols - 1) * spacing
        grid_height = rows * line_height + (rows - 1) * spacing

        popup_x = (SCREEN_X - POPUP_X) // 2
        popup_y = (SCREEN_Y - POPUP_Y) // 2

        start_x = popup_x + (POPUP_X - grid_width) // 2
        start_y = popup_y + 100

        i = 0

        for row_index in range(rows):
            for col_index in range(cols):
                #get individual object rect
                rect = pygame.Rect(start_x + col_index * (line_width + spacing), start_y + row_index * (line_height + spacing), line_width, line_height)
                #check if the rect was clicked
                if rect.collidepoint(x, y):
                    #set selected to clicked index
                    self.selected = i

                i += 1

        #get the submit button rect
        button_text = self.font.render("Submit", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=(SCREEN_X // 2, popup_y + POPUP_Y - 80))
        bg_rect = button_rect.inflate(20, 10)

        #check if button is clicked
        if bg_rect.collidepoint(x, y):
            #if the color is already in use abort
            if COLORS[self.selected] in [l.color for l in Line.lines]:
                return

            #close the popup by changing to new line mode
            sm.change("NewLineMode")
            #set the color of new line
            sm.states[sm.current_state].set_color(COLORS[self.selected])
            self.selected = None


