class Tile:
    """Class for tiles on the bg_map."""
    def __init__(self, number, population, quality_bonus):
        """Initialize tile."""
        self.number = number
        self.population = population
        self.quality_bonus = quality_bonus