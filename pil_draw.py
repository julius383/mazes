from Grid import Grid
from PIL import Image, ImageDraw
import os

a_destination = 'maze_images'

class PilGrid(Grid):
    def __init__(self, columns, rows, origin=1):
        super().__init__(columns, rows, origin)
        self.width = 800
        self.height = 800
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.inset = 50
        self.cell_width = self.calculate_cell_width()
        self.rect_width = self.rows * self.cell_width
        self.rect_height = self.columns * self.cell_width
        self.draw = ImageDraw.Draw(self.image)
        self.pixel_ranges = self.get_pixel_ranges()
        self.default_end = self.rows * self.columns

    def calculate_cell_width(self):
        return (self.width - self.inset)//self.rows

    def draw_cell(self, x_coord: int, y_coord: int, walls: str):
        if len(walls) > 0:
            for wall in walls:
                if wall == 'L':
                    start = (x_coord, y_coord)
                    stop = (x_coord, y_coord + self.cell_width)
                    self.draw.line((start, stop), width=1, fill="black")
                elif wall == 'R':
                    start = (x_coord + self.cell_width, y_coord)
                    stop = (x_coord + self.cell_width, y_coord + self.cell_width)
                    self.draw.line((start, stop), width=1, fill="black")
                elif wall == 'U':
                    start = (x_coord, y_coord)
                    stop = (x_coord + self.cell_width, y_coord)
                    self.draw.line((start, stop), width=1, fill="black")
                else:
                    start = (x_coord, y_coord + self.cell_width)
                    stop = (x_coord + self.cell_width, y_coord + self.cell_width)
                    self.draw.line((start, stop), width=1, fill="black")
        return

    def draw_maze(self, save=True, fstring="maze-{0}-{1}.png"):
        displacement = self.inset//2
        x_coord, y_coord = displacement, displacement
        grid = self.grid
        for c in grid:
            for r in c:
                wall = r.walls
                self.draw_cell(x_coord, y_coord, wall)
                x_coord += self.cell_width
            x_coord = displacement
            y_coord += self.cell_width
        self.draw.rectangle(
                [(displacement, displacement),
                    (self.rect_width+displacement, self.rect_height+displacement)],
                            outline="black")
        self.image.show()
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
            fpath = os.path.join(path, fstring.format(count, my_format))
            self.image.save(fpath)
        return

    def get_pixel_ranges(self) -> dict:
        pixel_ranges = dict()
        displacement = self.inset // 2
        starting_x = displacement
        starting_y = displacement
        for c in self.grid:
            for r in c:
                lower_x = starting_x
                upper_x = (starting_x + self.cell_width)
                lower_y = starting_y
                upper_y = (starting_y + self.cell_width)
                pixel_ranges[r] = [(lower_x, upper_x), (lower_y, upper_y)]
                starting_x += self.cell_width
            starting_x = displacement
            starting_y += self.cell_width
        return pixel_ranges

    def color_cell(self, cell, base_color=(150, 0, 0)):
        pix_obj = self.image.load()
        x_range = self.pixel_ranges[cell][0]
        y_range = self.pixel_ranges[cell][1]
        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                pix_obj[x, y] = base_color
        del pix_obj
        return

    def set_color_intensity(self, cell, base_color='red'):
        distance = self.get_distance_to_origin(cell)
        maximum = max(self.distances.keys())
        intensity = (maximum - distance) / maximum
        dark = int(round(255 * intensity, 4))
        bright = int(round(128 + (127 * intensity), 3))
        if base_color.lower() == 'green':
            my_color = (dark, bright, dark)
        elif base_color.lower() == 'red':
            my_color = (bright, dark, dark)
        elif base_color.lower() == 'blue':
            my_color = (dark, dark, bright)
        else:
            my_color = (bright, dark, bright)
        return my_color

    def color_grid(self, base_color='red'):
        for cell in self.all_cells():
            current_color = self.set_color_intensity(cell, base_color)
            self.color_cell(cell, current_color)
        return

    def show_shortest_path(self, end=None):
        if end is None:
            end = self.default_end
        path = self.dijkstra_path_find(end)
        for cell in path:
            self.color_cell(cell,)
        return
