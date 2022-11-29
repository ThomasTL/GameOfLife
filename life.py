from grid import *
from graphics import *
from copy import *
from datetime import datetime
import os

columns = 40
cellSize = 12
gen_number = 5000
colors = [[0, 0, 0]]
# colors = [[0, 0, 255], [0, 255, 0]]
# colors = [[0, 0, 255], [0, 255, 0], [255, 0, 0]]
# colors = [[0, 0, 255], [0, 255, 0], [255, 0, 0], [128, 128, 128]]

win = GraphWin("Conway's Game of Life", columns * cellSize, columns * cellSize, autoflush=False)
grid = Grid(win, columns, cellSize)

confFilePath = "./config/"
if not os.path.exists(confFilePath):
    os.makedirs(confFilePath)

now = datetime.now()
fileName = "./config/" + now.strftime("%Y%m%d-%H%M%S") + " - GOL Config.txt"
confFile = open(fileName, "w")

def nextGeneration():
    # Running Game of life rules
    # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    old_cells = deepcopy(grid.cells)
    for row in range(1, columns-1):
        for col in range(1, columns-1):
            living_neighbours = 0
            living_neighbours_dna = [0 for i in range(len(colors))]
            # Count the living neighbours around old_cells[row][col]
            for row_eval in range(row-1, row+2):
                for col_eval in range(col-1, col+2):
                    # Do not evaluate the reference cell
                    if not(row == row_eval and col == col_eval):
                        if old_cells[row_eval][col_eval].isAlive and old_cells[row][col].isAlive == True:
                            if old_cells[row][col].dna == old_cells[row_eval][col_eval].dna:
                                living_neighbours += 1
                        elif old_cells[row_eval][col_eval].isAlive and old_cells[row][col].isAlive == False:
                            living_neighbours_dna[old_cells[row_eval][col_eval].dna] += 1

            # Search if dead cell has exactly 3 neighbours with the same dna and take the first one we find in the list
            dnaId = 0
            foundThreeLivingNeighbours = False
            for i in living_neighbours_dna:
                if i == 3:
                    dnaId = living_neighbours_dna.index(i)
                    foundThreeLivingNeighbours = True
                    break

            # Check game of life rules
            if old_cells[row][col].isAlive == True and (living_neighbours < 2 or living_neighbours > 3):
                grid.cells[row][col].isAlive = False
                grid.cells[row][col].stateHasChanged = True

            elif old_cells[row][col].isAlive == True and (living_neighbours == 2 or living_neighbours == 3):
                grid.cells[row][col].isAlive = old_cells[row][col].isAlive
                grid.cells[row][col].stateHasChanged = False

            elif old_cells[row][col].isAlive == False and foundThreeLivingNeighbours == True:
                grid.cells[row][col].isAlive = True
                grid.cells[row][col].stateHasChanged = True
                grid.cells[row][col].dna = dnaId
                grid.cells[row][col].color = colors[dnaId]

            else:
                grid.cells[row][col].isAlive = old_cells[row][col].isAlive
                grid.cells[row][col].stateHasChanged = False

def main():
    win.setBackground("white")

    # Initialize the grid with the starting state
    cellPopulation = grid.initRandGrid()    
    grid.setCellColor(colors, "rand")
    grid.drawCells()

    gridSizeStr = "Grid size: " + str(columns) + " x " + str(columns)
    populationStr = "Maximum population: " + str(columns * columns) + " cells"
    cellPopulationStr = "Total cell population: " + str(cellPopulation) + " cells"
    percentOccupancyStr = "Percentage occupancy: " + str(int((cellPopulation / (columns * columns)) * 100)) + "%"

    # Write the configuration in file
    confFile.write(gridSizeStr + "\n")
    confFile.write(populationStr + "\n")
    confFile.write(cellPopulationStr + "\n")
    confFile.write(percentOccupancyStr + "\n")
    # Output the configuration on the console
    print(gridSizeStr)
    print(populationStr)
    print(cellPopulationStr)
    print(percentOccupancyStr)
    # Print and write the starting state in a file for later if needed
    # grid.printCellsToConsole()
    grid.writeCellsToFile(confFile)
    confFile.close()

    # Run the game of life for as much generation as in gen_number
    for gen in range(gen_number):
        # Compute next cell generation
        nextGeneration()
        
        # Draw the new generation
        grid.drawCells()
        # Temporisation to slow down the display
        time.sleep(0.1)

    win.getMouse()
    win.close()

main()