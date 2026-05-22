import math
from itertools import product

from constants import STATION_RADIUS, STATION_BASE_PRICE
from line import Line
import global_vars
from map import bg_map


class Station:
    """Class for station objects."""
    stations = []
    station_map: list[list["Station | None"]] = [[None for _ in range(31)] for _ in range(20)]

    def __init__(self, x, y, name):
        """Initialize station."""
        #check if station or line present
        if Station.station_map[y][x]:
            global_vars.warn_popup.open("Station already existent here!")
            return

        if len(Line.line_map[y][x]) <= 0:
            global_vars.warn_popup.open("Station needs a line to be placed!")
            return

        payed, price = global_vars.check_money(STATION_BASE_PRICE, global_vars.station_min_price)
        if not payed:
            global_vars.warn_popup.open(f"Insufficient money! Need {price}!")
            return
        global_vars.station_min_price = price

        Station.station_map[y][x] = self
        #get name for station
        self.x = x
        self.y = y
        self.name = name
        self.population = self.get_population_in_radius()
        self.quality_factor = self.get_quality_factor()

        #check if money is present

        Station.stations.append(self)

    def get_population_in_radius(self):
        tile_radius = []
        for x in range(-STATION_RADIUS, STATION_RADIUS + 1):
            for y in range(-STATION_RADIUS, STATION_RADIUS + 1):
                if 0 <= self.y - y < len(bg_map) and 0 <= self.x - x < len(bg_map[0]):
                    tile_radius.append(bg_map[self.y - y][self.x - x])

        tile_populations = [t.population for t in tile_radius]

        return sum(tile_populations)

    def get_quality_factor(self):
        tile_radius = []
        for x in range(-STATION_RADIUS, STATION_RADIUS + 1):
            for y in range(-STATION_RADIUS, STATION_RADIUS + 1):
                if 0 <= self.y - y < len(bg_map) and 0 <= self.x - x < len(bg_map[0]):
                    tile_radius.append(bg_map[self.y - y][self.x - x])

        tile_qualities = [t.quality_bonus for t in tile_radius]

        return math.prod(tile_qualities)


    def get_lines(self):
        lines = []
        for line_state in Line.line_map[self.y][self.x]:
            lines.append(line_state.line)

        return lines

    def get_revenue(self):
        revenue = 0

        for line in self.get_lines():
            revenue += self.population * 0.0003 * self.quality_factor * math.sqrt(len(get_stations_on_line(line)))

        return revenue

def get_stations_on_line(given_line):
    stations = []

    for station in Station.stations:
        for line in station.get_lines():
            if line.color == given_line.color:
                stations.append(station)

    return stations

def get_total_revenue():
    revenue = 0

    for station in Station.stations:
        revenue += station.get_revenue()

    return revenue


