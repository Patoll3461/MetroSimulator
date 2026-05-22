import random
from idlelib import rpc

from constants import small_park_max_size, big_park_max_size, middle_park_max_size, max_settlement_size, \
    max_industry_size
from map import bg_map

park_tiles = [0, 1, 5, 6, 18]
street_tiles = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 14]
house_tiles = [2, 7, 13, 15, 30]
skyscraper_bottom_tiles = [3, 11, 16]
skyscraper_top_tiles = [4, 12, 17]
industry_tiles = [8, 9, 10]

street_tiles_left_open = [19, 21, 22, 25, 26, 28, 29]
street_tiles_right_open = [19, 21, 23, 24, 26, 27, 28]
street_tiles_up_open = [20, 21, 22, 23, 26, 27, 29]
street_tiles_down_open = [20, 21, 24, 25, 27, 28, 29]

weights = [30, 1, 1, 1, 2, 2, 2]

def generate_map():
    start = (15, 10)

    bg_map[start[1]][start[0]] = street_tiles[2]

    generate_tile_left((start[0] - 1, start[1]), bg_map[start[1]][start[0]])
    generate_tile_right((start[0] + 1, start[1]), bg_map[start[1]][start[0]])
    generate_tile_up((start[0], start[1] - 1), bg_map[start[1]][start[0]])
    generate_tile_down((start[0], start[1] + 1), bg_map[start[1]][start[0]])

    generate_cluster(small_park_max_size, park_tiles)
    generate_cluster(small_park_max_size, park_tiles)
    generate_cluster(middle_park_max_size, park_tiles)
    generate_cluster(big_park_max_size, park_tiles)

    generate_cluster(max_industry_size, industry_tiles)
    generate_cluster(max_industry_size, industry_tiles)

    for x in range(0, 2):
        for i in range(0, 3):
            generate_skyscraper(i)

    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            if tile == -1:
                build_cluster(col_index, row_index, 0, max_settlement_size, house_tiles)

    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            if tile == -1:
                bg_map[row_index][col_index] = 14

    adjust_orientation()


def generate_tile_left(current, prev):
    x,y = current

    if x < 0 or x > len(bg_map[0]) - 1:
        return

    if bg_map[y][x] != -1:
        return

    placed = False

    if prev in street_tiles_left_open:
        tile = random.choices(street_tiles_right_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    if not placed:
        return

    generate_tile_left((x - 1, y), bg_map[y][x])
    generate_tile_up((x, y - 1), bg_map[y][x])
    generate_tile_down((x, y + 1), bg_map[y][x])

def generate_tile_right(current, prev):
    x,y = current

    if x < 0 or x >= len(bg_map[0]) - 1:
        return

    if bg_map[y][x] != -1:
        return

    placed = False

    if prev in street_tiles_right_open:
        tile = random.choices(street_tiles_left_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    if not placed:
        return

    generate_tile_right((x + 1, y), bg_map[y][x])
    generate_tile_up((x, y - 1), bg_map[y][x])
    generate_tile_down((x, y + 1), bg_map[y][x])

def generate_tile_up(current, prev):
    x,y = current

    if y < 0 or y > len(bg_map) - 2:
        return

    if bg_map[y][x] != -1:
        return

    placed = False

    if prev in street_tiles_up_open:
        tile = random.choices(street_tiles_down_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    if not placed:
        return

    generate_tile_left((x - 1, y), bg_map[y][x])
    generate_tile_right((x + 1, y), bg_map[y][x])
    generate_tile_up((x, y - 1), bg_map[y][x])


def generate_tile_down(current, prev):
    x,y = current

    if y < 0 or y > len(bg_map) - 2:
        return

    if bg_map[y][x] != -1:
        return

    placed = False

    if prev in street_tiles_down_open:
        tile = random.choices(street_tiles_up_open, weights=weights, k=1)[0]
        bg_map[y][x] = tile
        placed = True

    if not placed:
        return

    generate_tile_left((x - 1, y), bg_map[y][x])
    generate_tile_right((x + 1, y), bg_map[y][x])
    generate_tile_down((x, y + 1), bg_map[y][x])


def generate_cluster(max_size, tiles):
    x,y = get_coordinates()

    while bg_map[y][x] != -1:
        x,y = get_coordinates()

    bg_map[y][x] = random.choices(tiles)[0]

    adjacent = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for a in adjacent:
        build_cluster(a[0], a[1], 1, max_size, tiles)

def build_cluster(x, y, size, max_size, tiles):
    if y < 0 or y > len(bg_map) - 2 or x < 0 or x >= len(bg_map[0]) - 1:
        return

    if bg_map[y][x] != -1:
        return

    if size >= max_size:
        return

    bg_map[y][x] = random.choices(tiles)[0]

    adjacent = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for a in adjacent:
        build_cluster(a[0], a[1], size + 1, max_size, tiles)

def generate_skyscraper(skyscraper_tile):
    x,y = get_coordinates()

    while bg_map[y][x] != -1 or bg_map[y - 1][x] != -1 or y <= 0 or x <= 0:
        x,y = get_coordinates()

    bg_map[y][x] = skyscraper_bottom_tiles[skyscraper_tile]

    generate_skyscraper_top(x, y - 1, skyscraper_tile)


def generate_skyscraper_top(x, y, skyscraper):
    bg_map[y][x] = skyscraper_top_tiles[skyscraper]


def adjust_orientation():
    for row_index, row in enumerate(bg_map):
        for col_index, tile in enumerate(row):
            if tile in street_tiles:
                indexes = []

                new = tile

                if 1 <= row_index < len(bg_map) and bg_map[row_index - 1][col_index] in street_tiles_down_open:
                    indexes.append(1)
                if 1 <= col_index < len(row) and bg_map[row_index][col_index - 1] in street_tiles_right_open:
                    indexes.append(0)
                if 0 <= row_index < len(bg_map) - 1 and bg_map[row_index + 1][col_index] in street_tiles_up_open:
                    indexes.append(3)
                if 0 <= col_index < len(row) - 1 and bg_map[row_index][col_index + 1] in street_tiles_left_open:
                    indexes.append(2)

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

                bg_map[row_index][col_index] = new


def get_coordinates():
    x = random.randint(0, 29)
    y = random.randint(0, 17)

    return x,y
