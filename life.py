# System imports
import sys, os
from random import *
import time
import json

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

# TODO: Need to add some meaningful comments

# Game of Life related class imports
from cell import *

# Create the log path and log file to save the Game of Life starting parameters
# if it doesn't exist
confFilePath = "./gol-files/"
if not os.path.exists(confFilePath):
    os.makedirs(confFilePath)

# Starting grid size
columns = 70

# Create a read/write lock needed to synchronize next generation calculation and refreshing the UI
lock = QReadWriteLock() 

class CalcGenerationsWorker(QObject):
    finished = pyqtSignal()
    drawGeneration = pyqtSignal(int)
    shouldRun = False
    genNumber = 10000
    tempo = 0.1

    def __init__(self, cellGrid: CellGrid):
        super().__init__()
        self.cellGrid = cellGrid

    def run(self):
        for gen in range(self.genNumber):
            if self.shouldRun == False:
                break
            lock.lockForWrite()
            self.cellGrid.nextGeneration()
            lock.unlock()
            self.drawGeneration.emit(gen + 1)            
            time.sleep(self.tempo)
        self.finished.emit()

class GolWindow(QMainWindow):
    toolbarHeight = 26
    statusbarHeight = 25
    maxWindowSize = 700

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cellGrid = CellGrid(columns, 0)
        self.setupUi()

    def setupUi(self):
        super().__init__()
        self.title = "Conway's Game of Life"
        self.columns = self.cellGrid.columns
        self.setWindowSize()
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)        

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
        gridSizeList = ["10 x 10", "30 x 30", "50 x 50", "70 x 70", "90 x 90", "100 x 100"]
        self.gridSizeComboBox.addItems(gridSizeList)
        self.gridSizeComboBox.setCurrentIndex(self.getIndexFromColumns(self.cellGrid.columns))
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

    def setWindowSize(self) -> None:
        self.cellSize = int(self.maxWindowSize / self.columns)
        self.setFixedSize(QSize((self.columns * self.cellSize), ((self.columns * self.cellSize) + (self.toolbarHeight + self.statusbarHeight))))     

    def getColumnsFromIndex(self, index) -> int:
        columns = 10
        if index == 0:
            columns = 10
        elif index == 1:
            columns = 30
        elif index == 2:
            columns = 50
        elif index == 3:
            columns = 70
        elif index == 4:
            columns = 90
        elif index == 5:
            columns = 100
        return columns       

    def getIndexFromColumns(self, columns) -> int:
        index = 0
        if columns == 10:
            index = 0
        elif columns == 30:
            index = 1
        elif columns == 50:
            index = 2
        elif columns == 70:
            index = 3
        elif columns == 90:
            index = 4
        elif columns == 110:
            index = 5
        return index

    def onChangePopulation(self, index):
        self.cellGrid.setPopulation(index)
        self.cellGrid.setCellColor()
        self.update()

    def onChangeGridSize(self, index):
        self.columns = self.getColumnsFromIndex(index)
        self.setWindowSize()
        self.cellGrid.reInit(self.columns, self.populationComboBox.currentIndex())
        self.update()

    def onClickStopBtn(self, s):
        self.worker.shouldRun = False
        self.changeToolbarBtnsState(True)

    def onClickStartBtn(self, s):
        self.changeToolbarBtnsState(False)
        self.runGenerations()

    def onClickReset(self, s):
        self.cellGrid.initRandGrid()
        self.cellGrid.setCellColor()
        self.update()

    def onClickOpenFile(self, s):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', confFilePath, "Json Files (*.json)")
        if fileName[0]:
            with open(fileName[0], 'r', encoding ='utf8') as file:
                grid = json.load(file)
                self.cellGrid.loadd(grid)
                self.columns = self.cellGrid.columns
                self.setWindowSize()
                self.populationComboBox.setCurrentIndex(int(grid["grid-config"]["population"]) - 1)
                self.gridSizeComboBox.setCurrentIndex(self.getIndexFromColumns(int(grid["grid-config"]["columns"])))
                self.update()               
                file.close()

    def onClickSaveFile(self, s):
        fileName = QFileDialog.getSaveFileName(self, 'Save file', confFilePath, "Json Files (*.json)")
        if fileName[0]:
            with open(fileName[0], 'w', encoding ='utf8') as file:
                grid = self.cellGrid.dumpd()
                json.dump(grid, fp=file, indent=0)
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
        self.worker = CalcGenerationsWorker(self.cellGrid)
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

        lock.lockForRead()
        for row in range(self.columns):
            for col in range(self.columns):
                cell = self.cellGrid.getCell(row=row, col=col)
                if cell.isAlive == True:
                    color = cell.color
                elif cell.isAlive == False:
                    color = "#FFFFFF"
                painter.setBrush(QBrush(QColor(color), Qt.BrushStyle.SolidPattern))
                painter.drawRect((self.cellSize * row), self.toolbarHeight + (self.cellSize * col), self.cellSize, self.cellSize)
        lock.unlock()
        return super().paintEvent(a0)        

# Run the Qt app
app = QApplication(sys.argv)
gol = GolWindow()
gol.show()
sys.exit(app.exec())