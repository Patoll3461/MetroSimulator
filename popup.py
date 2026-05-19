import pygame

from constants import SCREEN_X, POPUP_X, SCREEN_Y, POPUP_Y, line_width, line_height, COLORS
from line import Line
from station import Station


class Popup:
    """Interface for popup objects."""
    def __init__(self, color, font):
        """Initialize the popup"""
        self.color = color
        self.font = font
    def draw(self, screen: pygame.Surface): pass
    def capture_input(self, events): pass
    def is_clicked(self, x, y, sm, **kwargs): pass
    def close(self, sm): pass


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

        #render close button
        close_text = self.font.render("X", True, (0, 0, 0))
        close_rect = close_text.get_rect(center=(SCREEN_X - (SCREEN_X - POPUP_X) / 2 - 30, SCREEN_Y - (SCREEN_Y - POPUP_Y) / 2 - POPUP_Y + 30))
        bg_rect = close_rect.inflate(10, 10)

        pygame.draw.rect(screen, (143, 143, 143), bg_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)

        screen.blit(close_text, close_rect)

    def is_clicked(self, x, y, sm, **kwargs):
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

        #get rect for close button
        close_text = self.font.render("X", True, (0, 0, 0))
        close_rect = close_text.get_rect(center=(SCREEN_X - (SCREEN_X - POPUP_X) / 2 - 30, SCREEN_Y - (SCREEN_Y - POPUP_Y) / 2 - POPUP_Y + 30))
        bg_rect = close_rect.inflate(10, 10)

        #check if close button clicked
        if bg_rect.collidepoint(x, y):
            #close popup
            self.close(sm)

    def close(self, sm):
        """Function to close popup."""
        sm.change("BuildMode")


class StationPopup(Popup):
    """Class for the Station Name Input Popup."""
    def __init__(self, color, font):
        """Add the input field as attribute."""
        super().__init__(color, font)

        popup_x = (SCREEN_X - POPUP_X) // 2
        popup_y = (SCREEN_Y - POPUP_Y) // 2

        self.name_input = InputField(pygame.Color(87, 157, 201), font, popup_x + (POPUP_X - 400) / 2, popup_y + 120)


    def draw(self, screen: pygame.Surface):
        """Draw the popup."""
        self.name_input.is_hovering()
        # calculate coordinates for heading
        rect = pygame.Rect((SCREEN_X - POPUP_X) // 2, (SCREEN_Y - POPUP_Y) // 2, POPUP_X, POPUP_Y)

        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        header = self.font.render("Enter a name for Station", True, (0, 0, 0))

        popup_x = (SCREEN_X - POPUP_X) // 2
        popup_y = (SCREEN_Y - POPUP_Y) // 2

        # render heading
        header_rect = header.get_rect(center=(SCREEN_X / 2, popup_y + 40))
        screen.blit(header, header_rect)

        self.name_input.draw(screen)

        # render submit button
        button_text = self.font.render("Submit", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=(SCREEN_X // 2, popup_y + POPUP_Y - 80))
        bg_rect = button_rect.inflate(20, 10)

        pygame.draw.rect(screen, (255, 171, 61), bg_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)

        screen.blit(button_text, button_rect)

        #render close button
        close_text = self.font.render("X", True, (0, 0, 0))
        close_rect = close_text.get_rect(center=(SCREEN_X - (SCREEN_X - POPUP_X) / 2 - 30, SCREEN_Y - (SCREEN_Y - POPUP_Y) / 2 - POPUP_Y + 30))
        bg_rect = close_rect.inflate(10, 10)

        pygame.draw.rect(screen, (143, 143, 143), bg_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)

        screen.blit(close_text, close_rect)

    def is_clicked(self, x, y, sm, **kwargs):
        #check if input box is clicked
        self.name_input.is_clicked(x, y)

        popup_y = (SCREEN_Y - POPUP_Y) // 2

        #get submit button rect
        button_text = self.font.render("Submit", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=(SCREEN_X // 2, popup_y + POPUP_Y - 80))
        bg_rect = button_rect.inflate(20, 10)

        #check if submit button pressed
        if bg_rect.collidepoint(x, y):
            name = self.name_input.text

            #check if name entered and name not yet used
            if len(name) > 0 and name not in [s.name for s in Station.stations]:
                if not kwargs.get("station_x") and not kwargs.get("station_y"):
                    return

                #get old amount of stations
                old_length = len(Station.stations)
                #add station
                Station(kwargs["station_x"], kwargs["station_y"], name)

                #check if station creation was successfully
                if old_length < len(Station.stations):
                    #reset input and close popup
                    self.name_input.text = ""
                    self.name_input.focused = False
                    self.name_input.color = pygame.Color(87, 157, 201)
                    sm.change("BuildMode")

        #get close button rect
        close_text = self.font.render("X", True, (0, 0, 0))
        close_rect = close_text.get_rect(center=(SCREEN_X - (SCREEN_X - POPUP_X) / 2 - 30, SCREEN_Y - (SCREEN_Y - POPUP_Y) / 2 - POPUP_Y + 30))
        bg_rect = close_rect.inflate(10, 10)

        #check if close button pressed
        if bg_rect.collidepoint(x, y):
            #close popup
            self.close(sm)

    def capture_input(self, events):
        """Get Input for the Input Field."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.name_input.add_letter(event)

    def close(self, sm):
        """Close the Popup."""
        sm.change("BuildMode")


class InputField:
    """Class for the input field."""
    def __init__(self, color, font, x, y):
        """Initialize the Input field."""
        self.focused = False
        self.text = ""
        self.color = color
        self.font = font
        self.x = x
        self.y = y
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, 400, 50)

    def draw(self, screen):
        """Draw the input field"""
        #draw main bg
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        render_text = self.font.render(self.text, True, (0, 0, 0))

        padding_x = 10

        #get rect for text
        text_rect = render_text.get_rect()
        text_rect.left = self.rect.left + padding_x
        text_rect.center = self.rect.center

        #handle overflow
        clip_rect = self.rect.copy()
        clip_rect.inflate_ip(-10, -10)

        screen.set_clip(clip_rect)
        screen.blit(render_text, text_rect)
        screen.set_clip(None)

    def is_hovering(self):
        """Check if cursor needs to change because of hovering."""
        x,y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def is_clicked(self, x, y):
        """Check if the text field is clicked."""
        if self.rect.collidepoint(x, y):
            self.focused = True
            self.color = pygame.Color(58, 107, 138)

    def add_letter(self, event):
        """Add a letter to the input."""
        if not self.focused:
            return

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return

        if not event.unicode:
            return

        self.text += event.unicode
