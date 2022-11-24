from random import *
from copy import *
from graphics import *
import time

cell_size = 15
columns = 25
grid_width = cell_size * columns

win = GraphWin("Game Of Life", grid_width, grid_width, autoflush=False)
win.setBackground("white")

def draw_cell(x, y, alive):
    cell = Rectangle(Point(x, y), Point(x+cell_size, y+cell_size))
    cell.setOutline(color_rgb(255, 255, 255))
    if alive:
        cell.setFill(color_rgb(0, 0, 0))
    else:
        cell.setFill(color_rgb(255, 255, 255))
    cell.draw(win)

def draw_grid(grid, old_grid):
    for row in range(columns):
        for col in range(columns):
            x = row * cell_size
            y = col * cell_size
            alive = False
            draw = False
            # Only draw if the cell changes state
            if grid[row][col] == 1 and old_grid[row][col] == 0:
                alive = True
                draw = True
            elif grid[row][col] == 0 and old_grid[row][col] == 1:
                draw = True

            if draw == True: 
                draw_cell(x, y, alive) 

def shapes(grid, shape):
    if shape == "SHAPE_1":
        grid[10][15] = 1
        grid[11][14] = 1
        grid[11][15] = 1
        grid[11][16] = 1
        grid[12][15] = 1
    elif shape == "SHAPE_2":
        grid[5][5] = 1
        grid[6][5] = 1
        grid[7][5] = 1
    elif shape == "SHAPE_3":
        grid[5][25] = 1
        grid[6][25] = 1
        grid[7][25] = 1
        grid[7][26] = 1
        grid[6][27] = 1
    elif shape == "SHAPE_4":
        grid[20][15] = 1
        grid[21][15] = 1
        grid[22][15] = 1
        grid[22][16] = 1
        grid[22][17] = 1
        grid[21][17] = 1
        grid[23][17] = 1
    
def main():
    # Create and initialize the matrix containing the cell states
    grid = [[0 for i in range(columns)] for j in range(columns)]
    old_grid = [[0 for i in range(columns)] for j in range(columns)]

    defined_shapes = False
    if defined_shapes != True:
        # Random initialization of the grid
        for row in range(columns):
            for col in range(columns):
                if row != 0 and row != columns-1 and col != 0 and col != columns-1:
                    grid[row][col] = randint(a=0, b=1)
    else:
        shapes(grid, "SHAPE_1")

    # Draw the generation #1
    draw_grid(grid, old_grid)
    update(30)

    # Running Game of life rules
    # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    gen_number = 5000
    for gen in range(gen_number):
        old_grid = deepcopy(grid)
        for row in range(1, columns-1):
            for col in range(1, columns-1):
                alive_neighbours = 0
                # Count the living neighbours around old_grid[row][col]
                for row_eval in range(row-1, row+2):
                    for col_eval in range(col-1, col+2):
                        if old_grid[row_eval][col_eval] == 1:
                            alive_neighbours += 1
                # Don't count the reference cell (e.g. old_grid[row][col]) if living
                if old_grid[row][col] == 1:
                    alive_neighbours -= 1

                # Check game of life rules
                if old_grid[row][col] == 1 and (alive_neighbours < 2 or alive_neighbours > 3):
                    grid[row][col] = 0
                elif old_grid[row][col] == 1 and (alive_neighbours == 2 or alive_neighbours == 3):
                    grid[row][col] = old_grid[row][col]
                elif old_grid[row][col] == 0 and alive_neighbours == 3:
                    grid[row][col] = 1
                else:
                    grid[row][col] = old_grid[row][col]
        
        # Display the new generation
        draw_grid(grid, old_grid)
        update(30)
        # Temporisation
        time.sleep(0.1)

    win.getMouse()
    win.close()

main()