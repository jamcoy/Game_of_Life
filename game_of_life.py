import random
import sys

import pygame

from colours import dark_blue, green, black
from shapes import boat, beacon, blinker, glider

FRAMERATE = 2


def draw_grid():
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, dark_blue, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, dark_blue, (0, y), (width, y))


def draw_cells():
    for (x, y) in cells:
        colour = green if cells[x, y] else black
        rectangle = (x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, colour, rectangle)


def get_neighbours((x, y)):
    positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                 (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    return [cells[r, c] for (r, c) in positions if 0 <= r < rows and 0 <= c < columns]


def evolve():
    for position, alive in cells.items():
        live_neighbours = sum(get_neighbours(position))
        if alive:
            if live_neighbours < 2 or live_neighbours > 3:
                cells[position] = False
        elif live_neighbours == 3:
            cells[position] = True


def get_cells_random(density):
    return {(c, r): random.random() < density for c in range(columns) for r in range(rows)}


def get_cells_pattern(shape):
    new_cells = {(c, r): 0 for c in range(columns) for r in range(rows)}
    start_column = (columns / 2) - 2
    start_row = (rows / 2) - 2
    if shape == "boat":
        pattern_cells = boat.split('\n')
    elif shape == "beacon":
        pattern_cells = beacon.split('\n')
    elif shape == "blinker":
        pattern_cells = blinker.split('\n')
    else:
        pattern_cells = glider.split('\n')
    column_index = 0
    for row in pattern_cells:
        row_index = 0
        for column in row:
            if pattern_cells[column_index][row_index] == "1":
                new_cells[start_column + column_index, start_row + row_index] = True
            row_index += 1
        column_index += 1
    return new_cells


pygame.init()

columns, rows = 80, 80
cells = get_cells_random(0.2)

cell_size = 10
size = width, height = columns * cell_size, rows * cell_size
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

print "= faster"
print "- slower"
print "1 random (medium density)"
print "2 random (low density)"
print "3 boat (still life)"
print "4 beacon (oscillator)"
print "5 blinker (oscillator)"
print "6 glider (spaceship)"

while True:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "=":
                FRAMERATE += 1
            if pygame.key.name(event.key) == "-" and FRAMERATE > 2:
                FRAMERATE -= 1
            if pygame.key.name(event.key) == "1":
                cells = get_cells_random(0.2)
            if pygame.key.name(event.key) == "2":
                cells = get_cells_random(0.08)
            if pygame.key.name(event.key) == "3":
                cells = get_cells_pattern("boat")
            if pygame.key.name(event.key) == "4":
                cells = get_cells_pattern("beacon")
            if pygame.key.name(event.key) == "5":
                cells = get_cells_pattern("blinker")
            if pygame.key.name(event.key) == "6":
                cells = get_cells_pattern("glider")

    draw_cells()
    evolve()
    draw_grid()
    pygame.display.update()
