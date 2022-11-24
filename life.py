from random import *
from copy import *
from graphics import *
import time

cell_size = 20
population = 15
grid_width = cell_size * population

win = GraphWin("Game Of Life", grid_width, grid_width)

def print_matrix(matrix, matrix_size):
    for row in range(matrix_size):
        line = ""
        for col in range(matrix_size):
            cell = " "
            if matrix[row][col] == 1:
                cell = "@"
            line += cell + " "
        print(line)
    print()

def draw_cell(x, y, alive):
    cell = Rectangle(Point(x, y), Point(x+cell_size, y+cell_size))
    cell.setOutline(color_rgb(255, 255, 255))
    if alive:
        cell.setFill(color_rgb(0, 0, 0))
    else:
        cell.setFill(color_rgb(255, 255, 255))
    cell.draw(win)

def draw_grid(grid):
    for row in range(population):
        for col in range(population):
            x = row * cell_size
            y = col * cell_size
            alive = False
            if grid[row][col] == 1:
                alive = True
            draw_cell(x, y, alive)   

def main():
    # Population => number of cells in the matrix
    # population = 20

    # Create and initialize the matrix containing the cell states
    grid = [[2 for i in range(population)] for j in range(population)]
    for row in range(population):
        for col in range(population):
            grid[row][col] = randint(a=0, b=1)

    # Display the generation #1
    # print_matrix(grid, population)
    draw_grid(grid)

    # Game of life rules
    # 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # 2. Any live cell with two or three live neighbours lives on to the next generation.
    # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

    gen_number = 5000
    for gen in range(gen_number):
        old_grid = deepcopy(grid)
        for row in range(1, population-1):
            for col in range(1, population-1):
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
        # print_matrix(grid, population)
        draw_grid(grid)
        # Slow down the process
        # time.sleep(0.1)

    win.getMouse()
    win.close()

main()