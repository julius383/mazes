class Cell:
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.neighbours = []
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.walls = None

    # returns the column and row of a cell
    # on the grid
    def get_cell_position(self):
        return self.column, self.row

    # takes a dictionary that has the cells neighbouring this one
    # and sets the corresponding attributes to the cell
    def set_attributes(self, neighbours: dict):
        self.neighbours = list(neighbours.values())
        self.up = neighbours.get('up', None)
        self.down = neighbours.get('down', None)
        self.right = neighbours.get('right', None)
        self.left = neighbours.get('left', None)
        return

    # returns the cell in the direction that is passed as
    # an argument from the given cell
    def get_next_cell(self, direction: str):
        if direction == 'L':
            return self.left
        elif direction == 'R':
            return self.right
        elif direction == 'U':
            return self.up
        elif direction == 'D':
            return self.down
        else:
            return None

    # returns for a cell on the grid
    def get_valid_moves(self, visited: list):
        neighbours = self.neighbours
        return [i for i in neighbours if i not in visited]

    def get_valid_directions(self) -> list:
        neighbours = self.neighbours
        directions = []
        for n in neighbours:
            direction = self.get_direction(n)
            x_walls = self.walls
            n_walls = n.walls
            adj_wall = self.get_adjacent_wall(direction)
            if direction not in x_walls and adj_wall not in n_walls:
                directions.append(direction)
                continue
        return directions

        # returns the direction of one cell from
        # the other
    def get_direction(self, end_cell):
        if end_cell == self.down:
            return 'D'
        elif end_cell == self.up:
            return 'U'
        elif end_cell == self.left:
            return 'L'
        elif end_cell == self.right:
            return 'R'
        else:
            return

    # used to get the wall to remove from the cell
    # that is being moved to
    @staticmethod
    def get_adjacent_wall(wall: str):
        if wall == 'L':
            return 'R'
        elif wall == 'R':
            return 'L'
        elif wall == 'U':
            return 'D'
        elif wall == 'D':
            return 'U'
        else:
            return

    # joins two cells next to each other by
    # removing the appropriate wall from the individual
    # cells
    def carve_passage(self, to_cell):
        wall_1 = self.get_direction(to_cell)
        wall_2 = self.get_adjacent_wall(wall_1)
        try:
            if wall_1 in self.walls:
                self.walls.remove(wall_1)
            if wall_2 in to_cell.walls:
                to_cell.walls.remove(wall_2)
        except (ValueError, TypeError):
            print('Nothing Done')
            return
        return

    # returns a list of legal cells that can be moved to
    # from the given cell within the maze
    def get_valid_neighbours(self) -> list:
        valid_directions = self.get_valid_directions()
        valid_neighbours = []
        for d in valid_directions:
            n = self.get_next_cell(d)
            valid_neighbours.append(n)
        return valid_neighbours
