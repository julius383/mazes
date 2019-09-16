#!/usr/bin/env python
from Grid import *
import time
import random
from pil_draw import PilGrid


def aldous_broder(grid_object: Grid):
    start_time = time.time()
    start_cell = grid_object.random_cell()
    current_cell = start_cell
    unvisited_cells = grid_object.all_cells()
    while unvisited_cells:
        neighbours = current_cell.neighbours
        random.shuffle(neighbours)
        next_cell = random.choice(neighbours)
        if next_cell in unvisited_cells:
            current_cell.carve_passage(next_cell)
        try:
            unvisited_cells.remove(current_cell)
        except ValueError:
            pass
        current_cell = next_cell
    stop_time = time.time()
    print('Finished.')
    print('Generation took {0} seconds.'.format(stop_time-start_time))
    return


if __name__ == '__main__':
    my_grid = PilGrid(50, 50)
    aldous_broder(my_grid)
    my_grid.color_grid('blue')
    my_grid.draw_maze()
