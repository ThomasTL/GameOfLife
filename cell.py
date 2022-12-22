from random import *
from copy import *

populations = [["#000000"], ["#0000FF", "#00FF00"], ["#0000FF", "#00FF00", "#FF0000"]]

# TODO: Need to add some meaningful comments

# TODO: To use @dataclass decorator for Cell class
class Cell():
    def __init__(self):
        self.isAlive = False
        self.stateHasChanged = False
        self.color = "#000000"
        self.dna = 0

    def addDna(self, dna: int) -> None:
        self.dna.append(dna)

    def hasDna(self, dna: int) -> bool:
        hasdna = False
        for sDna in self.dna:
            if sDna == dna:
                hasdna = True
        return hasdna

class CellGrid():
    def __init__(self, columns, population) -> None:
        self.reInit(columns, population)
        # self.columns = columns
        # self.setPopulation(population)
        # self.cells = [[Cell() for i in range(self.columns)] for j in range(self.columns)]
        # self.cellPopulation = self.initRandGrid()
        # self.setCellColor("rand")
    
    def reInit(self, columns, population):
        self.columns = columns
        self.setPopulation(population)
        self.cells = [[Cell() for i in range(self.columns)] for j in range(self.columns)]
        self.cellPopulation = self.initRandGrid()
        self.setCellColor("rand")

    def initRandGrid(self) -> int:
        cellPopulation = 0
        # Random initialization of all the cells
        for row in range(self.columns):
            for col in range(self.columns):
                if row != 0 and row != self.columns - 1 and col != 0 and col != self.columns - 1:
                    if randint(a=0, b=1) == 1:
                        self.cells[row][col].isAlive = True
                        self.cells[row][col].stateHasChanged = True
                        cellPopulation += 1
                    else:
                        self.cells[row][col].isAlive = False
                        self.cells[row][col].stateHasChanged = True
        return cellPopulation    

    def setCellColor(self, distMode: str) -> None:
        for row in range(self.columns):
            for col in range(self.columns):
                if row != 0 and row != self.columns - 1 and col != 0 and col != self.columns - 1:
                    if distMode == "rand":
                        if self.cells[row][col].isAlive:
                            colorId = randint(a=0, b=len(self.colors) - 1)
                            self.cells[row][col].color = self.colors[colorId]
                            self.cells[row][col].dna = colorId
                    elif distMode == "equal":
                        pass

    def getCell(self, col: int, row: int) -> Cell:
        return self.cells[row][col]

    def getCellPopulation(self) -> int:
        return self.cellPopulation

    def setPopulation(self, population) -> None:
        self.colors = populations[population]

    def dumpd(self) -> dict:
        grid = dict()
        grid["grid-config"] = {
            "columns":self.columns,
            "population":len(self.colors)
        }
        grid["cell-grid"] = {
            "grid":self.dumpGrid()
        }
        return grid

    def loadd(self, grid: dict) -> None:
        self.setPopulation(int(grid["grid-config"]["population"]) - 1)
        self.columns = int(grid["grid-config"]["columns"])
        self.cells = [[Cell() for i in range(self.columns)] for j in range(self.columns)]        
        self.loadGrid(grid["cell-grid"])
        
    def dumpGrid(self) -> list:
        grid = []
        for row in range(self.columns):
            line = ""
            for col in range(self.columns):
                cell = "."
                if self.cells[row][col].isAlive:
                    cell = str(self.cells[row][col].dna)
                line += cell  
            grid.append(line)
        return grid

    def loadGrid(self, grid) -> None:
        for row in range(self.columns):
            for col in range(self.columns):
                line = grid["grid"][row]
                if line[col] == ".":
                    self.cells[row][col].isAlive = False
                    self.cells[row][col].stateHasChanged = True
                else:
                    self.cells[row][col].isAlive = True
                    self.cells[row][col].dna = int(line[col])
                    self.cells[row][col].color = self.colors[int(line[col])]
                    self.cells[row][col].stateHasChanged = True

    def nextGeneration(self) -> None:
        # Running Game of life rules
        # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        old_cells = deepcopy(self.cells)
        for row in range(1, self.columns-1):
            for col in range(1, self.columns-1):
                living_neighbours = 0
                living_neighbours_dna = [0 for i in range(len(self.colors))]
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
                    self.cells[row][col].isAlive = False
                    self.cells[row][col].stateHasChanged = True

                elif old_cells[row][col].isAlive == True and (living_neighbours == 2 or living_neighbours == 3):
                    self.cells[row][col].isAlive = old_cells[row][col].isAlive
                    self.cells[row][col].stateHasChanged = False

                elif old_cells[row][col].isAlive == False and foundThreeLivingNeighbours == True:
                    self.cells[row][col].isAlive = True
                    self.cells[row][col].stateHasChanged = True
                    self.cells[row][col].dna = dnaId
                    self.cells[row][col].color = self.colors[dnaId]

                else:
                    self.cells[row][col].isAlive = old_cells[row][col].isAlive
                    self.cells[row][col].stateHasChanged = False
