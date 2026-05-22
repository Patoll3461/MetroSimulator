import random

from constants import small_park_max_size, big_park_max_size, middle_park_max_size, max_settlement_size, max_industry_size
from map import bg_map
from tile import Tile

#indexes in the sprite list of different tile types
park_tiles = [0, 1, 5, 6, 18]
street_tiles = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 14]
house_tiles = [2, 7, 13, 15, 30]
skyscraper_tiles = [3, 4, 11, 12, 16, 17]
skyscraper_bottom_tiles = [3, 11, 16]
skyscraper_top_tiles = [4, 12, 17]
industry_tiles = [8, 9, 10]

#which street tiles are open in which direction
street_tiles_left_open = [19, 21, 22, 25, 26, 28, 29]
street_tiles_right_open = [19, 21, 23, 24, 26, 27, 28]
street_tiles_up_open = [20, 21, 22, 23, 26, 27, 29]
street_tiles_down_open = [20, 21, 24, 25, 27, 28, 29]

#population factors
park_population_factor = 20
street_population_factor = 40
settlement_population_factor = 120
industry_population_factor = 230
skyscraper_population_factor = 450

#quality factors
park_quality_factor = 1.02
industry_quality_factor = 0.985
settlement_quality_factor = 0.998
street_quality_factor = 1
skyscraper_quality_factor = 0.996

population_factors = [street_population_factor, park_population_factor, settlement_population_factor, industry_population_factor, skyscraper_population_factor]
quality_factors = [street_quality_factor, park_quality_factor, settlement_quality_factor, industry_quality_factor, skyscraper_quality_factor]
tile_types = [street_tiles, park_tiles, house_tiles, industry_tiles, skyscraper_tiles]

#weights when placing a street, straight street has weight 30, crossings have weight 2, triple intersections and curves have weight 1
weights = [30, 2, 1, 1, 1, 1, 1]

def generate_map():
    """Generate the map."""
    #set the start to center
    start = (15, 10)

    #place a crossing at the start
    bg_map[start[1]][start[0]] = street_tiles[2]

    #generate street mape from there
    generate_tile_left((start[0] - 1, start[1]), bg_map[start[1]][start[0]])
    generate_tile_right((start[0] + 1, start[1]), bg_map[start[1]][start[0]])
    generate_tile_up((start[0], start[1] - 1), bg_map[start[1]][start[0]])
    generate_tile_down((start[0], start[1] + 1), bg_map[start[1]][start[0]])

    #generate parks, 2 small one, one medium and one big
    generate_cluster(small_park_max_size, park_tiles)
    generate_cluster(small_park_max_size, park_tiles)
    generate_cluster(middle_park_max_size, park_tiles)
    generate_cluster(big_park_max_size, park_tiles)


    #generate two industry clusters
    generate_cluster(max_industry_size, industry_tiles)
    generate_cluster(max_industry_size, industry_tiles)

    #generate 6 skyscrapers, 2 of each type
    for x in range(0, 2):
        for i in range(0, 3):
            generate_skyscraper(i)

    #on remaining tiles generate a settlement cluster
    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            if tile == -1:
                build_cluster(col_index, row_index, 0, max_settlement_size, house_tiles)

    #if any tiles remain empty set them to none
    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            if tile == -1:
                bg_map[row_index][col_index] = 14

    #adjust the orientation of all street tiles to fit
    adjust_orientation()

    convert_to_tile_object()


def generate_tile_left(current, prev):
    """Generates a street tile towards the left."""
    x,y = current

    #check if out of bound
    if x < 0 or x > len(bg_map[0]) - 1:
        return

    #check if there is a tile here
    if bg_map[y][x] != -1:
        return

    placed = False

    #check if the previous tile is valid and can connect to the current one
    if prev in street_tiles_left_open:
        #place a connecting tile
        tile = random.choices(street_tiles_right_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    #if nothing was placed dont continue
    if not placed:
        return

    #generate outward
    generate_tile_left((x - 1, y), bg_map[y][x])
    generate_tile_up((x, y - 1), bg_map[y][x])
    generate_tile_down((x, y + 1), bg_map[y][x])

def generate_tile_right(current, prev):
    """Generate a street tile towards the right."""
    x,y = current

    #check if out of bounds
    if x < 0 or x >= len(bg_map[0]) - 1:
        return

    #check if there is already a tile here
    if bg_map[y][x] != -1:
        return

    placed = False

    #check if previous tile is valid to connect to
    if prev in street_tiles_right_open:
        tile = random.choices(street_tiles_left_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    #if nothing was placed, abort
    if not placed:
        return

    #generate further outward
    generate_tile_right((x + 1, y), bg_map[y][x])
    generate_tile_up((x, y - 1), bg_map[y][x])
    generate_tile_down((x, y + 1), bg_map[y][x])

def generate_tile_up(current, prev):
    """Generate a street tile upwards."""
    x,y = current

    #check if out of bound
    if y < 0 or y > len(bg_map) - 2:
        return

    #check if there is a tile here
    if bg_map[y][x] != -1:
        return

    placed = False

    #check if previous is valid to connect to
    if prev in street_tiles_up_open:
        tile = random.choices(street_tiles_down_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    #if nothing was placed abort
    if not placed:
        return

    #generate outwards
    generate_tile_left((x - 1, y), bg_map[y][x])
    generate_tile_right((x + 1, y), bg_map[y][x])
    generate_tile_up((x, y - 1), bg_map[y][x])


def generate_tile_down(current, prev):
    """Generate street tile downwards."""
    x,y = current

    #check if out of bounds
    if y < 0 or y > len(bg_map) - 2:
        return

    #check if there is a tile here
    if bg_map[y][x] != -1:
        return

    placed = False

    #check if previous tile is valid to connect to
    if prev in street_tiles_down_open:
        tile = random.choices(street_tiles_up_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    #if nothing was placed, abort
    if not placed:
        return

    #generate further outward
    generate_tile_left((x - 1, y), bg_map[y][x])
    generate_tile_right((x + 1, y), bg_map[y][x])
    generate_tile_down((x, y + 1), bg_map[y][x])


def generate_cluster(max_size, tiles):
    """Start generating a cluster."""
    #get random coordinates
    x,y = get_coordinates()

    #get new coordinates until current ones are empty
    while bg_map[y][x] != -1:
        x,y = get_coordinates()

    #start with a random tile
    bg_map[y][x] = random.choices(tiles)[0]

    adjacent = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    #for every adjacent continue generating
    for a in adjacent:
        build_cluster(a[0], a[1], 1, max_size, tiles)

def build_cluster(x, y, size, max_size, tiles):
    """Build a cluster."""
    #check if out of bounds
    if y < 0 or y > len(bg_map) - 2 or x < 0 or x >= len(bg_map[0]) - 1:
        return

    #check if is empty
    if bg_map[y][x] != -1:
        return

    #check if max size is reached
    if size >= max_size:
        return

    #set a random tile of give type
    bg_map[y][x] = random.choices(tiles)[0]

    #continue generating on adjacent tiles
    adjacent = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for a in adjacent:
        build_cluster(a[0], a[1], size + 1, max_size, tiles)

def generate_skyscraper(skyscraper_tile):
    """Generate the bottom of a skyscraper."""
    #get random coordinates
    x,y = get_coordinates()

    #get new coordinates until the coordinates and the ones above are free
    while bg_map[y][x] != -1 or bg_map[y - 1][x] != -1 or y <= 0 or x <= 0:
        x,y = get_coordinates()

    #set to the bottom part of the skyscraper with determined type
    bg_map[y][x] = skyscraper_bottom_tiles[skyscraper_tile]

    #generate top part
    generate_skyscraper_top(x, y - 1, skyscraper_tile)


def generate_skyscraper_top(x, y, skyscraper):
    """Generate the top part of a skyscraper."""
    #set the determined sky                    print("hallo???")scraper types top at the given position
    bg_map[y][x] = skyscraper_top_tiles[skyscraper]


def adjust_orientation():
    """Adjust the orientation of all street tiles."""
    #loop through map
    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            #check if is street tile
            if tile in street_tiles:
                indexes = []

                #set the new orientation to current one for fallback
                new = tile

                #get adjacent streets that can connect and add corresponding index
                if 1 <= row_index < len(bg_map) and bg_map[row_index - 1][col_index] in street_tiles_down_open:
                    indexes.append(1)
                if 1 <= col_index < len(row) and bg_map[row_index][col_index - 1] in street_tiles_right_open:
                    indexes.append(0)
                if 0 <= row_index < len(bg_map) - 1 and bg_map[row_index + 1][col_index] in street_tiles_up_open:
                    indexes.append(3)
                if 0 <= col_index < len(row) - 1 and bg_map[row_index][col_index + 1] in street_tiles_left_open:
                    indexes.append(2)

                #set orientation accordingly
                if len(indexes) == 2:
                    if 0 in indexes and 1 in indexes:
                        new = 22
                    if 1 in indexes and 2 in indexes:
                        new = 23
                    if 2 in indexes and 3 in indexes:
                        new = 24
                    if 0 in indexes and 3 in indexes:
                        new = 25
                    if 0 in indexes and 2 in indexes:
                        new = 19
                    if 1 in indexes and 3 in indexes:
                        new = 20

                if len(indexes) == 3:
                    if 0 in indexes and 1 in indexes and 2 in indexes:
                        new = 26
                    if 1 in indexes and 2 in indexes and 3 in indexes:
                        new = 27
                    if 0 in indexes and 2 in indexes and 3 in indexes:
                        new = 28
                    if 0 in indexes and 1 in indexes and 3 in indexes:
                        new = 29

                if len(indexes) == 4:
                    new = 21

                #apply orientation
                bg_map[row_index][col_index] = new


def get_coordinates():
    """Get random coordinates on the map."""
    x = random.randint(0, 29)
    y = random.randint(0, 17)

    return x,y

def convert_to_tile_object():
    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            for index, tile_type in enumerate(tile_types):
                if tile in tile_type:
                    population = random.randint(population_factors[index], 3 * population_factors[index])
                    bg_map[row_index][col_index] = Tile(tile, population, quality_factors[index])

