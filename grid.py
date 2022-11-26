from cell import *
from graphics import *
from random import *

class Grid():
    def __init__(self, win, columns, cellSize):
        self.columns = columns
        self.cellSize = cellSize
        self.gridWidth = self.columns * self.cellSize
        self.win = win
        self.cells = [[Cell() for i in range(self.columns)] for j in range(self.columns)]

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

    def setCellColor(self, colors: list, distMode: str) -> None:
        for row in range(self.columns):
            for col in range(self.columns):
                if row != 0 and row != self.columns - 1 and col != 0 and col != self.columns - 1:
                    if distMode == "rand":
                        if self.cells[row][col].isAlive:
                            colorId = randint(a=0, b=len(colors) - 1)
                            self.cells[row][col].color = colors[colorId]
                            self.cells[row][col].dna = colorId
                            # self.cells[row][col].addDna(colorId)
                    elif distMode == "equal":
                        pass

    def initGridWithShape(self, shape: str) -> None:
        pass

    def drawCell(self, x: int, y: int, cell: Cell) -> None:
        if cell.stateHasChanged:
            # Need to draw this cell as its state has changed
            cellToDraw = Rectangle(Point(x, y), Point(x + self.cellSize, y + self.cellSize))
            cellToDraw.setOutline("white")        

            # Living cell in black, dead cell in white
            if cell.isAlive:
                cellToDraw.setFill(color_rgb(cell.color[0], cell.color[1], cell.color[2]))
            else:
                cellToDraw.setFill("white")
            
            cellToDraw.draw(self.win)
    
    def drawCells(self) -> None:
        for row in range(self.columns):
            for col in range(self.columns):
                x = row * self.cellSize
                y = col * self.cellSize
                self.drawCell(x, y, self.cells[row][col])
        # Refresh the window 
        update(30)

    def printCellsToConsole(self) -> None:
        print("\n---=== Cell population Start ===---")
        for row in range(self.columns):
            line = ""
            for col in range(self.columns):
                cell = "."
                if self.cells[row][col].isAlive:
                    # cell = str(self.cells[row][col].dna[0])
                    cell = str(self.cells[row][col].dna)
                line += cell + "."
            print(line)
        print()
        print("---=== Cell population End ===---")

    def writeCellsToFile(self, file) -> None:
        file.write("\n---=== Cell population Start ===---\n")
        for row in range(self.columns):
            line = ""
            for col in range(self.columns):
                cell = "."
                if self.cells[row][col].isAlive:
                    # cell = str(self.cells[row][col].dna[0])
                    cell = str(self.cells[row][col].dna)
                line += cell + "."
            line += "\n"
            file.write(line)        
        file.write("---=== Cell population End ===---\n")

# def shapes(grid, shape):
#     if shape == "SHAPE_1":
#         grid[10][15] = 1
#         grid[11][14] = 1
#         grid[11][15] = 1
#         grid[11][16] = 1
#         grid[12][15] = 1
#     elif shape == "SHAPE_2":
#         grid[5][5] = 1
#         grid[6][5] = 1
#         grid[7][5] = 1
#     elif shape == "SHAPE_3":
#         grid[5][25] = 1
#         grid[6][25] = 1
#         grid[7][25] = 1
#         grid[7][26] = 1
#         grid[6][27] = 1
#     elif shape == "SHAPE_4":
#         grid[20][15] = 1
#         grid[21][15] = 1
#         grid[22][15] = 1
#         grid[22][16] = 1
#         grid[22][17] = 1
#         grid[21][17] = 1
#         grid[23][17] = 1        