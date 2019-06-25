#!/usr/bin/env python
import pprint
from matplotlib import pyplot as plt
import random
import pickle
import os
from cell import Cell
import sys

destination = 'maze_pickles'
a_destination = 'maze_images'


class Grid:
    """object that contains all the methods that involve the
    creation and manipulation of the grid and subsequent maze
    including how to display each, the class takes  number of
    columns and rows of the maze\grid as instance parameters """
    def __init__(self, columns, rows, origin=1):
        self.rows = rows
        self.columns = columns
        self.grid = self.make_grid()
        self.create_default_maze()
        self.origin = [self.evaluate_origin(origin)]
        self.distances = None

    def evaluate_origin(self, origin):
        column = round(origin/self.columns)
        row = (origin % self.rows) - 1
        return self.grid[column][row]

    def random_cell(self):
        return random.choice(self.all_cells())

    def all_cells(self):
        all_cells = []
        for c in self.grid:
            for r in c:
                all_cells.append(r)
        return all_cells

    # creates the grid as a nested list
    # this is used to create the maze structure later
    def make_grid(self):
        grid = []
        index = 0
        for k in range(self.columns):
            row = []
            for l in range(self.rows):
                row.append(Cell(k, l))
                index += 1
            grid.append(row)
        return grid

    # creates the default structure before the walls of
    # the cells are removed in the process of creating the maze
    # the structure is a dictionary that has the cell's grid number
    # as the key and a list of all 4 walls as the values
    def create_default_maze(self):
        for c in self.grid:
            for r in c:
                directions = ['L', 'R', 'U', 'D']
                if c == self.grid[0]:
                    directions.remove('U')
                if c == self.grid[-1]:
                    directions.remove('D')
                if r == c[0]:
                    directions.remove('L')
                if r == c[-1]:
                    directions.remove('R')
                r.walls = directions
                self.configure_cell(r)
        return

    def configure_cell(self, cell):
        neighbours = self.get_neighbours(cell)
        cell.set_attributes(neighbours)
        return

    # takes a number representing a position within the grid
    # and returns the cell's neighbours within the grid as
    # a list
    def get_neighbours(self, home_cell):
        column, row = home_cell.get_cell_position()
        neighbours = dict()
        up = column - 1, row
        down = column + 1, row
        left = column, row - 1
        right = column, row + 1
        directions = dict(left=left, right=right, up=up, down=down)
        for k, v in directions.items():
            if v[1] >= 0 and v[0] >= 0:
                try:
                    my_column = v[0]
                    my_row = v[1]
                    ans = self.grid[my_column][my_row]
                    neighbours[k] = ans
                except (IndexError, ValueError):
                    continue
        return neighbours

    # calculates the distance of each cell
    # within the maze from the my_origin and returns a dictionary
    def calculate_distances(self) -> dict:
        current_cells = self.origin
        unexplored_cells = self.all_cells()
        distances = dict()
        distances[0] = self.origin
        unexplored_cells.remove(self.origin[0])
        count = 1
        while len(unexplored_cells) > 0:
            last = current_cells
            for c in current_cells:
                s_neighbours = c.get_valid_neighbours()
                neighbours = [n for n in s_neighbours if n in unexplored_cells]
                if neighbours:
                    for n in neighbours:
                        if count not in distances.keys():
                            distances[count] = [n]
                        else:
                            distances[count].append(n)
                        if n in unexplored_cells:
                            unexplored_cells.remove(n)
                        else:
                            pass
                        if current_cells == last:
                            current_cells = []
                            current_cells.extend(neighbours)
                        else:
                            current_cells.extend(neighbours)
                else:
                    continue
            count += 1
        self.distances = distances
        return distances

    def get_distance_to_origin(self, cell):
        if self.distances is None:
            self.calculate_distances()
        for k, v in self.distances.items():
            if cell in v:
                return k
        return None

    def dijkstra_path_find(self, end_point):
        if self.distances is None:
            self.calculate_distances()
        current_cell = end_point
        path = []
        d_to_origin = self.get_distance_to_origin(end_point) - 1
        while d_to_origin > 0:
            neighbours = current_cell.neighbours
            node = [i for i in self.distances[d_to_origin] if i in neighbours][0]
            path.append(node)
            current_cell = node
            d_to_origin -= 1

        return path

    def link_cells(self, iterable):
        while len(iterable) > 1:
            try:
                from_cell = iterable.pop()
                to_cell = iterable[-1]
                from_cell.carve_passage(to_cell)
            except IndexError:
                continue
        return

    def get_dead_ends(self):
        dead_ends = []
        for c in self.all_cells():
            walls = c.walls
            neighbours = c.neighbours
            if len(walls) == 3 or (len(neighbours) == 3 and len(walls) == 2):
                dead_ends.append(c)
        return dead_ends

    # saves a maze dictionary inside a folder called sample_mazes
    # within the current working directory
    def save(self):
        sys.setrecursionlimit(3000)
        cwd = os.getcwd()
        path = os.path.join(cwd, destination)
        try:
            os.mkdir(path)
        except OSError:
            pass
        count = 1
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                count += 1
        my_format = str(self.rows) + 'x' + str(self.columns)
        fpath = os.path.join(path, 'maze-{0}-{1}.pkl'.format(count, my_format))
        with open(fpath, 'wb') as output:
            pickle.dump(self.grid, output)
        print('Maze Saved at {0}'.format(fpath))
        return fpath

    # takes the x_coord and y_coord of the top left point
    # of the cell and uses that to draw the walls of the
    # cell that are required given in the walls parameter
    # of the function. Returns None
    def draw_cell(self, x_coord: int, y_coord: int, walls: str):
        if len(walls) > 0:
            for w in walls:
                if w == 'L':
                    plt.vlines(x_coord, ymin=y_coord - 1, ymax=y_coord)
                elif w == 'R':
                    plt.vlines(x_coord + 1, ymin=y_coord - 1, ymax=y_coord)
                elif w == 'U':
                    plt.hlines(y_coord, xmin=x_coord, xmax=x_coord + 1)
                else:
                    plt.hlines(y_coord - 1, xmin=x_coord, xmax=x_coord + 1)
        else:
            return
        return

    # draws all the cells of the maze and saves the
    # image if user wishes
    def draw(self, save=True):
        x_coord = 1
        y_coord = self.rows + 1
        grid = self.grid
        axis_range = [x_coord, y_coord, x_coord, y_coord]
        plt.axis(axis_range)
        plt.yticks([])
        plt.xticks([])
        for c in grid:
            for r in c:
                wall = r.walls
                self.draw_cell(x_coord, y_coord, wall)
                x_coord += 1
            x_coord = 1
            y_coord -= 1
        if save:
            cwd = os.getcwd()
            path = os.path.join(cwd, a_destination)
            try:
                os.mkdir(path)
            except OSError:
                pass
            count = 1
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path, i)):
                    count += 1
            my_format = str(self.rows) + 'x' + str(self.columns)
            fpath = os.path.join(path, 'maze-{0}-{1}.png'.format(count, my_format))
            plt.savefig(fpath, bbox_inches='tight', pad_inches=0)
        plt.show()


# loads a maze file through directly calling the function
# with the file name as a parameter or by prompting the user
# use the maze setter function in the grid class with appropriate
# to effectively use the Grid class methods after loading
def load_maze(save=None):
    cwd = os.getcwd()
    saves = dict()
    if destination in os.listdir(cwd):
        path = os.path.join(cwd, destination)
    else:
        print('No saves found')
        return
    if save is None:
        while True:
            count = 1
            for i in os.listdir(path):
                saves[count] = i
                count += 1
            pprint.pprint(saves)
            choice = eval(input('Which game would you like to load?\n-->'))
            if type(choice) == int and choice in saves.keys():
                maze_file = saves[choice]
                f_path = os.path.join(path, saves[choice])
                break
            elif str(choice).lower().startswith('q'):
                return
            else:
                print('Invalid Choice')
                continue
    else:
        f_path = os.path.join(path, save)
        maze_file = save
    if os.path.isfile(f_path):
        with open(f_path, 'rb') as save_file:
            maze = pickle.load(save_file)
        print('Loading {0}...'.format(maze_file))
        print('Save Loaded')
        return maze
    else:
        print('File does not exist')
        return
