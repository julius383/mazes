#!/usr/bin/env python3
import time
from Grid import *
import random
from pil_draw import PilGrid
import time


def recursive_backtracker(grid_object):
    start_time = time.time()
    cells = grid_object.all_cells()
    starting_cell = grid_object.random_cell()
    current_cell = starting_cell
    history = []
    visited = []
    while len(visited) != len(cells):
        valid_moves = current_cell.get_valid_moves(visited)
        if valid_moves:
            random.shuffle(valid_moves)
            next_cell = random.choice(valid_moves)
            current_cell.carve_passage(next_cell)
            history.append(current_cell)
            current_cell = next_cell
            visited.append(current_cell)
            continue
        else:
            try:
                current_cell = history.pop()
                continue
            except IndexError:
                break
    stop_time = time.time()
    print('Finished.')
    print('Generation took {0} seconds.'.format(stop_time-start_time))
    return


if __name__ == '__main__':
    my_grid = PilGrid(100, 100)
    recursive_backtracker(my_grid)
    my_grid.color_grid('red')
    print(len(my_grid.get_dead_ends()))
    my_grid.draw_maze()
