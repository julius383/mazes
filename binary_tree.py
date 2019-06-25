#!/usr/bin/env python3
from Grid import *
import random
import time
from pil_draw import PilGrid


# implementation of binary tree algorithm
# bias argument specifies the options available
# when picking moves randomly during operation of algorithm
def binary_tree(grid_object: Grid, bias='NW'):
    start_time = time.time()
    cells = list(grid_object.all_cells())
    if bias == 'NW':
        choices = ['U', 'L']
    elif bias == 'NE':
        choices = ['U', 'R']
    elif bias == 'SW':
        choices = ['D', 'L']
    elif bias == 'SE':
        choices = ['D', 'R']
    else:
        return
    for c in cells:
        neighbours = c.neighbours
        candidates = []
        for n in neighbours:
            if c.get_direction(n) in choices:
                candidates.append(n)
        if candidates:
            random.shuffle(candidates)
            move = random.choice(candidates)
            c.carve_passage(move)
        else:
            continue
    stop_time = time.time()
    print('Finished.')
    print('Generation took {0} seconds.'.format(stop_time-start_time))
    return

if __name__ == '__main__':
    my_grid = PilGrid(50, 50)
    binary_tree(my_grid, 'SE')
    my_grid.color_grid('green')
    my_grid.draw_maze(True, "binary-tree-maze-{0}-{1}.png")
