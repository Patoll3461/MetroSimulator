from line import Line


class Station:
    """Class for station objects."""
    stations = []
    station_map: list[list["Station | None"]] = [[None for _ in range(16)] for _ in range(11)]

    def __init__(self, x, y):
        """Initialize station."""
        #check if station or line present
        if Station.station_map[y][x] or len(Line.line_map[y][x]) <= 0:
            print("Station already here or no line present")
            return
        else:
            Station.station_map[y][x] = self
        #get name for station
        self.name = input("Enter name for station: ")
        self.x = x
        self.y = y
        Station.stations.append(self)

