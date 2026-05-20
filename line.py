import pygame

import global_vars
from constants import V_H_INDEX_ORDER, MAX_LINES


class Line:
    """This class defines individual lines"""
    line_index = 0
    lines = []
    line_map = [[[] for _ in range(31)] for _ in range(21)]

    def __init__(self, start_x, start_y, color: pygame.Color):
        """Initialize line object."""
        #check if limit reached
        if len(Line.lines) >= MAX_LINES:
            return

        self.color = color
        self.tiles = []
        self.add_tile(start_x, start_y, True, True)

        #check if adding tile was successfully
        if len(self.tiles) <= 0:
            return

        Line.lines.append(self)

    def __str__(self):
        if self.color == pygame.Color(255, 0, 0):
            return "Red Line"
        elif self.color == pygame.Color(0, 255, 0):
            return "Green Line"
        elif self.color == pygame.Color(0, 0, 255):
            return "Blue Line"
        else:
            return "Misc Line"

    def add_tile(self, x, y, is_first: bool = False, debug: bool = False):
        """Add the line to a new tile."""
        v_index = 1
        h_index = 1
        orientation = 0

        if self.check_if_tile_exists(x, y):
            global_vars.warn_popup.open("Line already exists here!")
            return

        #if it is not the first tile of the line check what index the connecting piece is on
        if not is_first:
            adjacent_tiles = [Line.line_map[y][x - 1], Line.line_map[y - 1][x], Line.line_map[y][x + 1], Line.line_map[y + 1][x]]
            for index, tile in enumerate(adjacent_tiles):
                for line_state in tile:
                    if line_state.line.color == self.color:
                        h_index = line_state.h_index
                        v_index = line_state.v_index
                        break

        #check if the connecting index is free on this tile
        free_h_indexes, free_v_indexes = get_free_indexes(x, y)
        orientation = self.check_orientation(x, y)

        if is_first:
            orientation = 0

        if orientation == 10:
            global_vars.warn_popup.open("Line needs connecting tile!")
            return

        #if the connecting index is not free try to adjust the index of all tiles in the line
        if h_index not in free_h_indexes:
            h_index = self.adjust_h_indexes(x, y)
            if h_index == 10:
                global_vars.warn_popup.open("No space here!")
                return
        if v_index not in free_v_indexes:
            v_index = self.adjust_v_indexes(x, y)
            if v_index == 10:
                global_vars.warn_popup.open("No space here!")
                return

        if self.check_if_triple(x, y):
            global_vars.warn_popup.open("Can not build triple intersections!")
            return

        if self.check_if_loop(x, y):
            global_vars.warn_popup.open("Can not build loops!")
            return

        #add the tile to map and check if orientation of adjacent tiles needs to change
        Line.line_map[y][x].append(LineState(self, orientation, h_index, v_index, x, y))
        self.tiles.append((x, y))
        if is_first:
            return
        self.adjust_orientation()

    def check_orientation(self, x, y):
        """Checks what orientation a tile at given position should be."""
        orientation = 0
        adjacent_tiles = [Line.line_map[y][x - 1], Line.line_map[y - 1][x], Line.line_map[y][x + 1], Line.line_map[y + 1][x]]
        indexes = []
        for index, tile in enumerate(adjacent_tiles):
            for line_state in tile:
                if line_state.line.color == self.color:
                    indexes.append(index)
        if len(indexes) == 1:
            i = indexes[0]
            if i == 0 or i == 2:
                orientation = 0
            elif i == 1 or i == 3:
                orientation = 1
        elif len(indexes) == 2:
            if 0 in indexes and 1 in indexes:
                orientation = 2
            elif 1 in indexes and 2 in indexes:
                orientation = 3
            elif 2 in indexes and 3 in indexes:
                orientation = 4
            elif 3 in indexes and 0 in indexes:
                orientation = 5
            elif 1 in indexes and 3 in indexes:
                orientation = 1
            elif 0 in indexes and 2 in indexes:
                orientation = 0
        else:
            return 10

        return orientation

    def adjust_orientation(self):
        """Adjust the orientation of all tiles."""
        for tile in self.tiles:
            orientation = self.check_orientation(tile[0], tile[1])
            for line_state in Line.line_map[tile[1]][tile[0]]:
                if line_state.line.color == self.color:
                    line_state.orientation = orientation

    def adjust_h_indexes(self, x, y):
        """Adjust the h index of all tiles in a row."""
        #get tiles
        adjacent = self.get_h_adjacent(x, y)
        adjacent.extend(line_state for line_state in Line.line_map[y][x] if line_state.line.color == self.color)
        #get free indexes
        free_h_indexes = [get_free_indexes(tile.x, tile.y)[0] for tile in adjacent]
        free_h_indexes.append(get_free_indexes(x, y)[0])
        #get indexes that are free on all tiles
        common = set(free_h_indexes[0]).intersection(*free_h_indexes[1:])
        ordered = [h for h in V_H_INDEX_ORDER if h in common]

        if len(ordered) <= 0:
            return 10

        h_index = ordered[0]

        #set the index
        for tile in adjacent:
            tile.h_index = h_index

        return h_index

    def get_h_adjacent(self, x, y):
        """Get all tiles that are in a horizontal row."""
        index = 1
        result_left = []
        #get left adjacent
        while index - len(result_left) <= 1:
            for line_state in Line.line_map[y][x - index]:
                if line_state.line.color == self.color:
                    result_left.append(line_state)
            index += 1

        index = 1
        result_right = []
        #get right adjacent
        while index - len(result_right) <= 1:
            for line_state in Line.line_map[y][x + index]:
                if line_state.line.color == self.color:
                    result_right.append(line_state)
            index += 1

        result = result_left + result_right
        return result

    def adjust_v_indexes(self, x, y):
        """Adjust the v index of all tiles in a column."""
        #get tiles
        adjacent = self.get_v_adjacent(x, y)
        adjacent.extend(line_state for line_state in Line.line_map[y][x] if line_state.line.color == self.color)
        #get free indexes
        free_v_indexes = [get_free_indexes(tile.x, tile.y)[1] for tile in adjacent]
        free_v_indexes.append(get_free_indexes(x, y)[1])
        #get indexes that are free on all tiles
        common = set(free_v_indexes[0]).intersection(*free_v_indexes[1:])
        #order indexes
        ordered = [v for v in V_H_INDEX_ORDER if v in common]

        if len(ordered) <= 0:
            return 10

        v_index = ordered[0]

        #set indexes
        for tile in adjacent:
            tile.v_index = v_index

        return v_index

    def get_v_adjacent(self, x, y):
        """Get all tiles that are in a vertical column."""
        index = 1
        result_top = []
        #get top adjacent
        while index - len(result_top) <= 1:
            for line_state in Line.line_map[y - index][x]:
                if line_state.line.color == self.color:
                    result_top.append(line_state)
            index += 1

        index = 1
        result_bottom = []
        #get bottom adjacent
        while index - len(result_bottom) <= 1:
            for line_state in Line.line_map[y + index][x]:
                if line_state.line.color == self.color:
                    result_bottom.append(line_state)
            index += 1

        result = result_top + result_bottom
        return result

    def check_if_tile_exists(self, x, y):
        """Checks if the line is already present at given coordinate."""
        exists = False
        for line_state in Line.line_map[y][x]:
            if line_state.line.color == self.color:
                exists = True
                break

        return exists

    def check_if_triple(self, x, y):
        """Checks if there are any triple intersections when a new tile at x;y is placed."""
        result = False
        for tile in self.tiles:
            #check for intersection
            orientation = self.check_for_intersections(tile[0], tile[1], x, y)
            if orientation == 10:
                return True

        return result

    def check_for_intersections(self, x, y, new_x, new_y):
        """Checks if there is a triple intersection at given x and y if new_x and new_y form a new tile for the line."""
        orientation = 0
        #get adjacent tiles and their coordinates
        adjacent_tiles = [Line.line_map[y][x - 1], Line.line_map[y - 1][x], Line.line_map[y][x + 1], Line.line_map[y + 1][x]]
        adjacent_coordinates = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
        indexes = []
        #get amount of bordering tiles
        for index, tile in enumerate(adjacent_tiles):
            for line_state in tile:
                if line_state.line.color == self.color:
                    indexes.append(index)

        #if 3 or more bordering tiles exist, there is a triple intersection
        if len(indexes) > 2:
            return 10
        #no triple intersection, as there is only one or no adjacent
        elif len(indexes) < 2:
            return 0
        else:
            #when there are two adjacent tiles check if the new tile is adjacent as well, in which case building it would result in a triple intersection
            if (new_x, new_y) in adjacent_coordinates:
                return 10

        return orientation

    def check_if_loop(self, x, y):
        """Checks what orientation a tile at given position should be."""
        orientation = 0
        adjacent_tiles = [Line.line_map[y][x - 1], Line.line_map[y - 1][x], Line.line_map[y][x + 1], Line.line_map[y + 1][x]]
        indexes = []
        for index, tile in enumerate(adjacent_tiles):
            for line_state in tile:
                if line_state.line.color == self.color:
                    indexes.append(index)

        if len(indexes) >= 2:
            return 10

        return orientation

def get_free_indexes(x, y):
    """Gets free indexes at given position"""
    lines: list = Line.line_map[y][x]

    #get occupied indexes at pos
    occupied_h_indexes = [line.h_index for line in lines]
    occupied_v_indexes = [line.v_index for line in lines]

    free_h_indexes = [h for h in V_H_INDEX_ORDER if h not in occupied_h_indexes]
    free_v_indexes = [v for v in V_H_INDEX_ORDER if v not in occupied_v_indexes]

    return free_h_indexes, free_v_indexes


class LineState:
    """Class for LineState objects, used on the map object, holds line object and orientation"""
    def __init__(self, line, orientation, h_index, v_index, x, y):
        self.line = line
        self.orientation = orientation
        self.h_index = h_index
        self.v_index = v_index
        self.x = x
        self.y = y