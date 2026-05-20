from line import Line
import global_vars


class Station:
    """Class for station objects."""
    stations = []
    station_map: list[list["Station | None"]] = [[None for _ in range(16)] for _ in range(11)]

    def __init__(self, x, y, name):
        """Initialize station."""
        #check if station or line present
        if Station.station_map[y][x]:
            global_vars.warn_popup.open("Station already existent here!")
            return

        if len(Line.line_map[y][x]) <= 0:
            global_vars.warn_popup.open("Station needs a line to be placed!")
            return

        Station.station_map[y][x] = self
        #get name for station
        self.x = x
        self.y = y
        self.name = name
        Station.stations.append(self)

