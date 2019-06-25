#!/usr/bin/env python3
from Grid import *
import random
import time
from pil_draw import PilGrid


def wilsons(grid_object):
    start_time = time.time()
    visited = []
    unvisited = grid_object.all_cells()
    first_visited = random.choice(unvisited)
    unvisited.remove(first_visited)
    visited.append(first_visited)
    path = []
    start_cell = random.choice(unvisited)
    current_cell = start_cell
    while unvisited:
        neighbours = current_cell.neighbours
        next_cell = random.choice(neighbours)
        if next_cell in path:
            loop = path.index(next_cell)
            path = [n for n in path if path.index(n) <= loop]
            current_cell = next_cell
        elif next_cell in visited:
            if path:
                visited.extend(path)
                path.append(next_cell)
                grid_object.link_cells(path)
                unvisited = [i for i in unvisited if i not in path]
                if unvisited:
                    current_cell = random.choice(unvisited)
                    path = []
                    continue
                else:
                    break
            else:
                current_cell.carve_passage(next_cell)
                visited.append(current_cell)
                unvisited.remove(current_cell)
                if len(unvisited) > 0:
                    current_cell = random.choice(unvisited)
                continue
        else:
            path.append(next_cell)
            current_cell = next_cell
    stop_time = time.time()
    print('Finished.')
    print('Generation took {0} seconds.'.format(stop_time-start_time))
    return

if __name__ == '__main__':
    my_grid = PilGrid(50, 50)
    wilsons(my_grid)
    my_grid.color_grid('red')
    print(len(my_grid.get_dead_ends()))
    my_grid.draw_maze(True, "wilson-maze-{0}-{1}.png")
