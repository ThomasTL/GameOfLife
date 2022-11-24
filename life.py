from grid import *
from graphics import *
from copy import *

def main():
    columns = 20
    cellSize = 15
    gen_number = 5000

    win = GraphWin("Game Of Life", columns * cellSize, columns * cellSize, autoflush=False)
    win.setBackground("white")

    grid = Grid(win, columns, cellSize)
    grid.initRandGrid()
    grid.drawGrid()

    # Running Game of life rules
    # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    for gen in range(gen_number):
        old_grid = deepcopy(grid.grid)
        for row in range(1, columns-1):
            for col in range(1, columns-1):
                alive_neighbours = 0
                # Count the living neighbours around old_grid[row][col]
                for row_eval in range(row-1, row+2):
                    for col_eval in range(col-1, col+2):
                        if old_grid[row_eval][col_eval].isAlive:
                            alive_neighbours += 1
                # Don't count the reference cell (e.g. old_grid[row][col]) if living
                if old_grid[row][col].isAlive:
                    alive_neighbours -= 1

                # Check game of life rules
                if old_grid[row][col].isAlive == True and (alive_neighbours < 2 or alive_neighbours > 3):
                    grid.grid[row][col].isAlive = False
                    grid.grid[row][col].stateHasChanged = True

                elif old_grid[row][col].isAlive == True and (alive_neighbours == 2 or alive_neighbours == 3):
                    grid.grid[row][col].isAlive = old_grid[row][col].isAlive
                    grid.grid[row][col].stateHasChanged = False

                elif old_grid[row][col].isAlive == False and alive_neighbours == 3:
                    grid.grid[row][col].isAlive = True
                    grid.grid[row][col].stateHasChanged = True

                else:
                    grid.grid[row][col].isAlive = old_grid[row][col].isAlive
                    grid.grid[row][col].stateHasChanged = False
        
        # Display the new generation
        grid.drawGrid()
        # Temporisation
        time.sleep(0.1)

    win.getMouse()
    win.close()

main()