# System imports
import sys, os
from datetime import datetime
from random import *
import time
import json
import yaml

# PyQT imports
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, QSize, QReadWriteLock, QSize
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPaintEvent, QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QStatusBar,
    QComboBox,
    QFileDialog
)

# Game of Life related class imports
from cell import *

# Game of Life constant parameters
columns = 70
genNumber = 10000
colors = [["#000000"], ["#0000FF", "#00FF00"], ["#0000FF", "#00FF00", "#FF0000"]]
tempo = 0.1

# Create the log path and log file to save the Game of Life starting parameters
# if it doesn't exist
confFilePath = "./config/"
if not os.path.exists(confFilePath):
    os.makedirs(confFilePath)
# now = datetime.now()
# fileName = "./config/" + now.strftime("%Y%m%d-%H%M%S") + " - GOL Config.txt"
# confFile = open(fileName, "w")

# Create the grid containing the cells and initialize all cells
cellGrid = CellGrid(columns, colors[0])
# Create a read/write lock needed to synchronize next generation calculation and refreshing the UI
lock = QReadWriteLock() 

class CalcGenerationsWorker(QObject):
    finished = pyqtSignal()
    drawGeneration = pyqtSignal(int)
    shouldRun = False

    def __init__(self):
        super().__init__()

    def run(self):
        for gen in range(genNumber):
            if self.shouldRun == False:
                break
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
        # TODO: Remove columns from the app properties. This property belongs to the CellGrid
        self.columns = columns
        self.cellSize = int(800 / self.columns)
        self.width = self.columns * self.cellSize
        self.height = (self.columns * self.cellSize) + (self.toolbarHeight + self.statusbarHeight)        
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)        
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.size()) 

        # Define actions to be used in toolbar and menus
        self.runGen = QAction(QIcon("./icons/control.png"), "Run", self)
        self.runGen.triggered.connect(self.onClickStartBtn)
        self.stopGen = QAction(QIcon("./icons/control-stop-square.png"), "Stop", self)
        self.stopGen.triggered.connect(self.onClickStopBtn) 
        self.stopGen.setEnabled(False)     
        self.resetGen = QAction(QIcon("./icons/arrow-circle-225-left.png"), "Reset", self)
        self.resetGen.triggered.connect(self.onClickReset)      
        self.openFile = QAction(QIcon("./icons/folder-horizontal-open.png"), "Open grid", self)
        self.openFile.triggered.connect(self.onClickOpenFile)    
        self.saveFile = QAction(QIcon("./icons/disk.png"), "Save current grid", self)
        self.saveFile.triggered.connect(self.onClickSaveFile)                     
        
        # Define the combo boxes
        self.populationComboBox = QComboBox(self)
        populationList = ["1 population", "2 populations", "3 populations"]
        self.populationComboBox.addItems(populationList)
        self.populationComboBox.currentIndexChanged.connect(self.onChangePopulation)
        self.gridSizeComboBox = QComboBox(self)
        gridSizeList = ["10 x 10", "30 x 30", "50 x 50", "70 x 70", "90 x 90", "110 x 110"]
        self.gridSizeComboBox.addItems(gridSizeList)
        self.gridSizeComboBox.setCurrentIndex(3)
        self.gridSizeComboBox.currentIndexChanged.connect(self.onChangeGridSize)

        # Toobar initialization
        self.toolbar = QToolBar("Game of Life toolbar")
        self.toolbar.setIconSize(QSize(16,16))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)         
        self.toolbar.addAction(self.runGen)
        self.toolbar.addAction(self.stopGen) 
        self.toolbar.addAction(self.resetGen) 
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.openFile) 
        self.toolbar.addAction(self.saveFile) 
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.populationComboBox)
        self.toolbar.addWidget(self.gridSizeComboBox)

        # Status bar initialization
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.show()        

    def onChangePopulation(self, index):
        cellGrid.colors = colors[index]
        cellGrid.setCellColor("rand")
        self.update()

    def onChangeGridSize(self, index):
        self.columns = (20 * index) + 10
        # TODO: Below 4 lines of code should be placedin a function
        self.cellSize = int(800 / self.columns)
        self.setFixedSize(QSize((self.columns * self.cellSize), ((self.columns * self.cellSize) + (self.toolbarHeight + self.statusbarHeight)))) 
        cellGrid.reInit(self.columns, colors[self.populationComboBox.currentIndex()])
        self.update()

    def onClickStopBtn(self, s):
        self.worker.shouldRun = False
        self.changeToolbarBtnsState(True)

    def onClickStartBtn(self, s):
        self.changeToolbarBtnsState(False)
        self.runGenerations()

    def onClickReset(self, s):
        cellGrid.initRandGrid()
        cellGrid.setCellColor("rand")
        self.update()

    def onClickOpenFile(self, s):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', confFilePath, "Json Files (*.json)")
        if fileName[0]:
            with open(fileName[0], 'r', encoding ='utf8') as file:
                cellGrid.load(file)
                self.columns = cellGrid.columns
                self.cellSize = int(800 / self.columns)
                self.setFixedSize(QSize((self.columns * self.cellSize), ((self.columns * self.cellSize) + (self.toolbarHeight + self.statusbarHeight))))  
                self.update()               
                file.close()


    def onClickSaveFile(self, s):
        fileName = QFileDialog.getSaveFileName(self, 'Save file', confFilePath, "Json Files (*.json)")
        if fileName[0]:
            with open(fileName[0], 'w', encoding ='utf8') as file:
                cellGrid.dump(file)
                file.close()

    def changeToolbarBtnsState(self, state: bool):
        # Disable controls in toolbar
        self.runGen.setEnabled(state)
        self.resetGen.setEnabled(state)
        self.openFile.setEnabled(state)
        self.saveFile.setEnabled(state)
        self.populationComboBox.setEnabled(state)
        self.gridSizeComboBox.setEnabled(state)

        # Enable controls in toolbar
        self.stopGen.setEnabled(not(state))

    def drawGeneration(self, n):
        self.statusBar.showMessage("Generation: " + str(n))
        self.update()

    def runGenerations(self):
        self.thread = QThread()
        self.worker = CalcGenerationsWorker()
        self.worker.shouldRun = True
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
        # painter.setBrush(QBrush(QColor("#0000FF"), Qt.BrushStyle.SolidPattern))

        lock.lockForRead()
        for row in range(self.columns):
            for col in range(self.columns):
                cell = cellGrid.getCell(row=row, col=col)
                if cell.isAlive == True:
                    color = cell.color
                elif cell.isAlive == False:
                    color = "#FFFFFF"
                # if cell.stateHasChanged == True:
                painter.setBrush(QBrush(QColor(color), Qt.BrushStyle.SolidPattern))
                painter.drawRect((self.cellSize * row), self.toolbarHeight + (self.cellSize * col), self.cellSize, self.cellSize)
        lock.unlock()
        return super().paintEvent(a0)        

# Save the starting configuration in a file
# totalPopulation = cellGrid.getCellPopulation()
# gridSizeStr = "Grid size: " + str(columns) + " x " + str(columns)
# populationStr = "Maximum population: " + str(columns * columns) + " cells"
# cellPopulationStr = "Total cell population: " + str(totalPopulation) + " cells"
# percentOccupancyStr = "Percentage occupancy: " + str(int((totalPopulation / (columns * columns)) * 100)) + "%"
# confFile.write(gridSizeStr + "\n")
# confFile.write(populationStr + "\n")
# confFile.write(cellPopulationStr + "\n")
# confFile.write(percentOccupancyStr + "\n")
# confFile.write(cellGrid.outputCellGrid())    
# confFile.close()

# Run the Qt app
app = QApplication(sys.argv)
gol = GolWindow()
gol.show()
sys.exit(app.exec())