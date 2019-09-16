from Grid import *
import time
import random
from pil_draw import PilGrid


def hunt_and_kill(grid_object: Grid):
    start_time = time.time()
    visited_cells = []
    unvisited_cells = grid_object.all_cells()
    random.shuffle(unvisited_cells)
    starting_cell = random.choice(unvisited_cells)
    current_cell = starting_cell
    while unvisited_cells:
        neighbours = current_cell.get_valid_moves(visited_cells)
        if neighbours:
            next_cell = random.choice(neighbours)
            current_cell.carve_passage(next_cell)
            visited_cells.append(next_cell)
            unvisited_cells.remove(next_cell)
            current_cell = next_cell
        else:
            for cell in unvisited_cells:
                valid_neighbours = cell.get_valid_moves(unvisited_cells)
                if cell not in visited_cells and valid_neighbours:
                    valid_link = random.choice(valid_neighbours)
                    cell.carve_passage(valid_link)
                    next_cell = cell
                    current_cell.carve_passage(next_cell)
                    visited_cells.append(next_cell)
                    unvisited_cells.remove(next_cell)
                    current_cell = next_cell
                    break
            else:
                break
    stop_time = time.time()
    print('Finished.')
    print('Generation took {0} seconds'.format(stop_time-start_time))
    return


if __name__ == '__main__':
    my_grid = PilGrid(50, 50)
    hunt_and_kill(my_grid)
    my_grid.color_grid('green')
    print(len(my_grid.get_dead_ends()))
    my_grid.draw_maze()
