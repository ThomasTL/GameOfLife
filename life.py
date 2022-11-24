from grid import *
from graphics import *
from copy import *

def main():
    columns = 25
    cellSize = 12
    gen_number = 5000

    win = GraphWin("Game Of Life", columns * cellSize, columns * cellSize, autoflush=False)
    win.setBackground("white")

    grid = Grid(win, columns, cellSize)
    grid.initRandGrid()
    grid.drawCells()

    # Running Game of life rules
    # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    for gen in range(gen_number):
        old_cells = deepcopy(grid.cells)
        for row in range(1, columns-1):
            for col in range(1, columns-1):
                alive_neighbours = 0
                # Count the living neighbours around old_cells[row][col]
                for row_eval in range(row-1, row+2):
                    for col_eval in range(col-1, col+2):
                        if old_cells[row_eval][col_eval].isAlive:
                            alive_neighbours += 1
                # Don't count the reference cell (e.g. old_cells[row][col]) if living
                if old_cells[row][col].isAlive:
                    alive_neighbours -= 1

                # Check game of life rules
                if old_cells[row][col].isAlive == True and (alive_neighbours < 2 or alive_neighbours > 3):
                    grid.cells[row][col].isAlive = False
                    grid.cells[row][col].stateHasChanged = True

                elif old_cells[row][col].isAlive == True and (alive_neighbours == 2 or alive_neighbours == 3):
                    grid.cells[row][col].isAlive = old_cells[row][col].isAlive
                    grid.cells[row][col].stateHasChanged = False

                elif old_cells[row][col].isAlive == False and alive_neighbours == 3:
                    grid.cells[row][col].isAlive = True
                    grid.cells[row][col].stateHasChanged = True

                else:
                    grid.cells[row][col].isAlive = old_cells[row][col].isAlive
                    grid.cells[row][col].stateHasChanged = False
        
        # Display the new generation
        grid.drawCells()
        # Temporisation to slow down
        time.sleep(0.1)

    win.getMouse()
    win.close()

main()