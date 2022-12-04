# System imports
import sys
from datetime import datetime
from random import *
import time

# PyQT imports
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt6.QtCore import QReadWriteLock
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPaintEvent
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Game of Life related class imports
from cell import *

# Game of Life constant parameters
columns = 70
cellSize = 10
genNumber = 5000
colors = ["#000000"]
# colors = ["#0000FF", "#00FF00"]
# colors = ["#0000FF", "#00FF00", "#FF0000"]
# colors = ["#0000FF", "#00FF00", "#FF0000", "#808080"]
tempo = 0.1

# Create the log path and log file to save the Game of Life starting parameters
# if it doesn't exist
confFilePath = "./config/"
if not os.path.exists(confFilePath):
    os.makedirs(confFilePath)
now = datetime.now()
fileName = "./config/" + now.strftime("%Y%m%d-%H%M%S") + " - GOL Config.txt"
confFile = open(fileName, "w")

# Create the grid containing the cells and initialize all cells
cellGrid = CellGrid(columns, colors)
# Create a read/write lock needed to synchronize next generation calculation and refreshing the UI
lock = QReadWriteLock() 

# class Life():
#     def __init__(self) -> None:
#         pass
        
class CalcGenerationsWorker(QObject):
    finished = pyqtSignal()
    drawGeneration = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        for gen in range(genNumber):
            lock.lockForWrite()
            cellGrid.nextGeneration()
            lock.unlock()
            self.drawGeneration.emit(gen + 1)            
            time.sleep(tempo)
        self.finished.emit()

class GolWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        super().__init__()
        self.title = "Conway's Game of Life"
        self.top= 550
        self.left= 50
        self.width = columns * cellSize
        self.height = columns * cellSize
        self.InitWindow()
        self.runLongTask()

    def InitWindow(self):
        self.setWindowTitle(self.title)        
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.size())
        self.show()        

    def drawGeneration(self, n):
        self.update()

    def runLongTask(self):
        self.thread = QThread()
        self.worker = CalcGenerationsWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.drawGeneration.connect(self.drawGeneration)
        self.thread.start()

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QPen(QColor("#FFFFFF") , 1, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(QColor("#0000FF"), Qt.BrushStyle.SolidPattern))

        lock.lockForRead()
        for row in range(columns):
            for col in range(columns):
                cell = cellGrid.getCell(row=row, col=col)
                if cell.isAlive == True:
                    color = cell.color
                elif cell.isAlive == False:
                    color = "#FFFFFF"
                painter.setBrush(QBrush(QColor(color), Qt.BrushStyle.SolidPattern))
                painter.drawRect(cellSize * row, cellSize * col, cellSize, cellSize)
        lock.unlock()
        return super().paintEvent(a0)        

# Save the starting configuration in a file
totalPopulation = cellGrid.getCellPopulation()
gridSizeStr = "Grid size: " + str(columns) + " x " + str(columns)
populationStr = "Maximum population: " + str(columns * columns) + " cells"
cellPopulationStr = "Total cell population: " + str(totalPopulation) + " cells"
percentOccupancyStr = "Percentage occupancy: " + str(int((totalPopulation / (columns * columns)) * 100)) + "%"
confFile.write(gridSizeStr + "\n")
confFile.write(populationStr + "\n")
confFile.write(cellPopulationStr + "\n")
confFile.write(percentOccupancyStr + "\n")
confFile.write(cellGrid.outputCellGrid())    
confFile.close()

# Run the Qt app
app = QApplication(sys.argv)
gol = GolWindow()
gol.show()
sys.exit(app.exec())