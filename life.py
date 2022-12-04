# System imports
import sys
from datetime import datetime
from random import *
import time

# PyQT imports
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, QSize, QReadWriteLock
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPaintEvent, QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QStatusBar
)

# Game of Life related class imports
from cell import *

# Game of Life constant parameters
columns = 120
cellSize = 7
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
    toolbarHeight = 26
    statusbarHeight = 25

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        super().__init__()
        self.title = "Conway's Game of Life"
        self.top= 550
        self.left= 50
        self.width = columns * cellSize
        self.height = (columns * cellSize) + (self.toolbarHeight + self.statusbarHeight)
        self.InitWindow()
        self.runGenerations()

    def InitWindow(self):
        self.setWindowTitle(self.title)        
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.size()) 

        # Define actions to be used in toolbar and menus
        runGen = QAction(QIcon("./icons/control.png"), "&Your button", self)
        # runGen.setStatusTip("This is your button")
        runGen.triggered.connect(self.onMyToolBarButtonClick)
        pauseGen = QAction(QIcon("./icons/control-pause.png"), "Your button&2", self)
        # pauseGen.setStatusTip("This is your button 2")
        pauseGen.triggered.connect(self.onMyToolBarButtonClick)   
        stopGen = QAction(QIcon("./icons/control-stop-square.png"), "Your button&3", self)
        # stopGen.setStatusTip("This is your button 3")
        stopGen.triggered.connect(self.onMyToolBarButtonClick)      
        openFile = QAction(QIcon("./icons/folder-horizontal-open.png"), "Your button&3", self)
        # openFile.setStatusTip("This is your button 3")
        openFile.triggered.connect(self.onMyToolBarButtonClick)    
        saveFile = QAction(QIcon("./icons/disk.png"), "Your button&3", self)
        # saveFile.setStatusTip("This is your button 3")
        saveFile.triggered.connect(self.onMyToolBarButtonClick)                     
        
        # Toobar initialization
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)         
        toolbar.addAction(runGen)
        toolbar.addAction(pauseGen) 
        toolbar.addAction(stopGen) 
        toolbar.addSeparator()
        toolbar.addAction(openFile) 
        toolbar.addAction(saveFile) 

        # Status bar initialization
        self.statusBar = QStatusBar(self)
        self.statusBar.showMessage("Pipolaki popol")
        self.setStatusBar(self.statusBar)

        self.show()        

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def drawGeneration(self, n):
        self.statusBar.showMessage("Generation: " + str(n))
        self.update()

    def runGenerations(self):
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
                painter.drawRect((cellSize * row), self.toolbarHeight + (cellSize * col), cellSize, cellSize)
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