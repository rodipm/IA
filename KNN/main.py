import numpy as np
import pygame as pg
import sys
import time

""" Global Initializations """

# window parameters
WIDTH, HEIGHT = (800, 800)
SIZE = WIDTH, HEIGHT

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# grid parameters
N_GRIDS = 40
GRID_SIZE = WIDTH//N_GRIDS

grid = np.zeros([N_GRIDS, N_GRIDS], int)

# classes and colors
# 0 = nothing, class 1 = green, class 2 = blue, 3 = undefined point
class_colors = [BLACK, GREEN, BLUE, RED]

""" Our data consists of a 2 dimensional table with 3 columns and N lines
column1 | column2 | column3
---------------------------
    X   |   Y     | Class """

data = np.empty([0, 3], int)


""" Game initialization"""
pg.init()
window = pg.display.set_mode(SIZE)


""" KNN Classifier Implementation"""
def KNN_classifier(data, new_point_atributes):
    raw_data = np.delete(data, -1, 1)

    classified = 0
    distances = np.empty(data.shape[0])

    K = 3

    for i, row in enumerate(raw_data):
        distance = 0
        for j, val in enumerate(row):
            distance += abs(new_point_atributes[j] - val)
        distances[i] = distance
    
    # get minimum distance index list for K
    indexes = []
    for _ in range(K):
        min_index = np.argmin(distances)
        distances[min_index] = max(distances) + 1
        indexes.append(min_index)

    # get class wich has the minumum distance to our point
    votes = {1: 0, 2:0}
    for i in indexes:
        votes[data[i, -1]] += 1

    if votes[1] >= votes[2]:
        classified = 1
    else:
        classified = 2

    return classified


compute = False
drag_draw = False
class_drawing = 0
saved_grid = None
changed_grid = False
while True:
    # event handlers
    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()[0] // GRID_SIZE, pg.mouse.get_pos()[1] // GRID_SIZE
            # mouse 1
            if event.button == 1:
                # class 1
                if grid[y, x] == 1:
                    grid[y, x] = 0
                else:
                    grid[y, x] = 1
                    data = np.append(data, [[x, y, 1]], axis=0)
                    class_drawing = 1

            # middle mouse
            elif event.button == 2:
                # undefined point
                # grid[y, x] = 3
                drag_draw = not drag_draw

            # mouse 2
            elif event.button == 3:
                # class 2
                if grid[y, x] == 2:
                    grid[y, x] = 0
                else:
                    grid[y, x] = 2
                    data = np.append(data, [[x, y, 2]], axis=0)
                    class_drawing = 2
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_SPACE and not changed_grid:
                if data.shape[0] > 0:
                    drag_draw = False
                    compute = True
                    changed_grid = True
            if event.key == pg.K_r:
                if event.mod & pg.KMOD_LSHIFT:
                    grid = np.zeros(grid.shape, int)
                    data = np.empty([0, 3], int)
                    saved_grid = np.copy(grid)
                    changed_grid = False
                else:
                    grid = saved_grid
                    changed_grid = False
            if event.key == pg.K_s:
                print("Saving current grid and data")
                with open('grid.KNN', 'wb') as file:
                    np.save(file, grid)
                with open('data.KNN', 'wb') as file:
                    np.save(file, data)
            if event.key == pg.K_l:
                print("Loading current grid and data")
                with open('grid.KNN', 'rb') as file:
                    grid = np.load(file)
                with open('data.KNN', 'rb') as file:
                    data = np.load(file)

        
    
    if drag_draw:
        x, y = pg.mouse.get_pos(
        )[0] // GRID_SIZE, pg.mouse.get_pos()[1] // GRID_SIZE
        grid[y, x] = class_drawing

    window.fill(WHITE)

    # display_grid
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            color = class_colors[val]
            pg.draw.rect(window, color, (x * GRID_SIZE, y *
                                         GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    # execute KNN classifier
    if compute:
        saved_grid = np.copy(grid)
        print("before: ", saved_grid)
        new_grid = np.copy(grid)
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if grid[x, y] == 0:
                    classified = KNN_classifier(data, (y, x))
                    new_grid[x, y] = classified

        grid = new_grid
        compute = False
        print("after: ", saved_grid)

    pg.display.flip()
