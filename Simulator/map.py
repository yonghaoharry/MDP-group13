from settings import *
import pygame as pg

class Map:
    # static variables
    height = 20
    width = 15
    config = 0

    non_obstacle_cell_width = 30 # with of the cell
    cell_length = 35  # cell_length - cell_width = the gap between cell gaps, alter here to adjust length
    cell_gap = cell_length - non_obstacle_cell_width
    arena_border_left = 5
    arena_border_up = 5
    arena_border_right = cell_length * 13
    arena_border_down = cell_length * 18

    cells_group = pg.sprite.Group() # the cells sprite group
    map_cells = [] # a 20 * 15  list holding cell objects

    def __init__(self):
        pass

    def generate_map(self, map_config):

        with open(map_config_path + map_config, 'r') as map_config:
            cell_x = 5
            cell_y = 5
            for row in range(1, 21):
                line = map_config.readline()
                cell_row = []
                for col in range (0, 15):
                    if line[col] == '0':
                        cell = cell(cell_x, cell_y)
                    elif line[col] == '1':
                        cell = cell(cell_x, cell_y)
                        cell.is_obstacle = True
                    elif line[col] =='2':
                        cell = cell(cell_x, cell_y)
                        cell.update_color((255, 255, 0))
                        cell.is_start_goal_zone = True
                    cell.row = row-1
                    cell.col = col
                    cell_row.append(cell)
                    cell_x += cell.length + cell.gap
                self.map_cells.append(cell_row)
                cell_x = 5
                cell_y = 5 + (cell.length + cell.gap) *  row

        for cell in self.map_cells:
            self.cells_group.add(cell)

    def map_update(self):
        for cell_row in self.map_cells:
            for cell in cell_row:
                if cell.is_obstacle == False and cell.discovered ==True and cell.is_start_goal_zone == False:
                    self.cells_group.remove(cell)



