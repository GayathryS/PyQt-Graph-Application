import sys

from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import csv
import pandas
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.filename = ''
        self.mdi = QMdiArea()
        self.mdi2 = QMdiArea()

        widget1 = QWidget(self)
        layout1 = QHBoxLayout(widget1)

        widget2 = QWidget(self)
        layout2 = QHBoxLayout(widget2)

        #grid = QGridLayout()

        self.button1 = QPushButton('Plot scatter point', self.mdi)
        self.button1.resize(250, 50)
        self.button1.move(50, 50)
        self.button1.clicked.connect(self.p1)

        self.button2 = QPushButton('Plot scatter point with smooth lines',self.mdi)
        self.button2.resize(250, 50)
        self.button2.move(300, 50)
        self.button2.clicked.connect(self.p2)

        self.button3 = QPushButton('Plot lines', self.mdi)
        self.button3.resize(250, 50)
        self.button3.move(550, 50)
        self.button3.clicked.connect(self.p3)

        self.model = QStandardItemModel(self)
        self.tableView = QTableView(self.mdi2)
        self.tableView.setModel(self.model)

        self.tableView.clicked.connect(self.cell_was_clicked)

        layout1.addWidget(self.button1)
        layout1.addWidget(self.button2)
        layout1.addWidget(self.button3)

        layout2.addWidget(self.tableView)

        central_widget = QWidget(self)
        vlayout = QVBoxLayout(central_widget)
        vlayout.addWidget(widget1)
        vlayout.addWidget(widget2)

        self.setCentralWidget(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.rows = []
        self.win = QMdiSubWindow()
        mwid = QWidget()
        vlayout2 = QVBoxLayout(mwid)
        vlayout2.addWidget(self.toolbar)
        vlayout2.addWidget(self.canvas)

        self.win.setWidget(mwid)

        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("Load")
        edit = bar.addMenu("Edit")
        edit.addAction("Edit data")
        file.addAction("Add data")
        file.addAction("Save")
        file.addAction("Save as PNG")
        self.setWindowTitle("Main Window")
        file.triggered[QAction].connect(self.windowaction)


    def cell_was_clicked(self,index):
        self.rows = []
        for i in range(1,self.model.rowCount()):
            self.rows.append(float(index.sibling(i,index.column()).data()))
        print(self.rows)

    def p1(self):
        self.win.setWindowTitle('Scatter Plot')
        ax = self.figure.add_subplot(111)
        ax.clear()
        x = [int(x) for x in range(len(self.rows))]
        y = self.rows
        ax.plot(x,y,'ro')
        ax.set_title('Scatter Plot')
        self.canvas.draw()
        self.win.show()

    def p2(self):
        self.win.setWindowTitle('Scatter Plot with Smooth Line')
        ax = self.figure.add_subplot(111)
        ax.clear()
        x = [int(x) for x in range(len(self.rows))]
        y = self.rows
        ax.plot(x, y,'-o')
        ax.set_title('Scatter Plot with Smooth Line')
        self.canvas.draw()
        self.win.show()

    def p3(self):
        self.win.setWindowTitle('Smooth Line Plot')
        ax = self.figure.add_subplot(111)
        ax.clear()
        x = [int(x) for x in range(len(self.rows))]
        y = self.rows
        ax.plot(x, y)
        ax.set_title('Smooth Line Plot')
        self.canvas.draw()
        self.win.show()


    def writeCsv(self, fileName):
        with open(fileName, "w",newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber,columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                print(fields)
                writer.writerow(fields)

    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

    def windowaction(self, q):
        if q.text() == "Load":
            filename = QFileDialog.getOpenFileName(self, 'Open file',
                                                   'e:\\personal\Github\pyqt', "CSV files (*.csv)")
            print(filename)
            self.filename = filename
            self.loadCsv(self.filename)
            data = pandas.read_csv(self.filename)
        elif q.text() == "Edit data":
            self.filename = filename
            self.writeCsv(self.filename)
        elif q.text() == "Add data":
            self.model.appendRow([])
        elif q.text() == "Save":
            self.writeCsv(self.filename)
        elif q.text()=="Save as PNG":
            self.take_screenshot()

    def take_screenshot(self):
        self.p = QPixmap.grabWindow(self.win.winId())
        self.p.save('screen.png', 'png')

def main():
    app = QApplication(sys.argv)

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


main()