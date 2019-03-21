import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from csvfinal import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.filename = ''
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtGui.QTableView(self.mdi)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.setCentralWidget(self.tableView)
        # self.tableView.isFullScreen()
        # self.tableView.showFullScreen()

        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("Load")
        edit = bar.addMenu("Edit")
        edit.addAction("Edit data")
        data = file.addMenu("Add data")
        data.addAction("Row")
        data.addAction("Column")
        file.addAction("Save")
        file.addAction("Save as PNG")
        self.setWindowTitle("Main WIndow")
        file.triggered[QAction].connect(self.windowaction)

        # self.layoutVertical = QtGui.QVBoxLayout(self)
        # self.layoutVertical.addWidget(self.tableView)

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
                    QtGui.QStandardItem(field)
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
        elif q.text() == "Edit data":
            # to be completed
            pass
        elif q.text() == "Row":
            self.model.appendRow([])
        elif q.text() == "Column":
            self.model.appendColumn([])
        elif q.text() == "Save":
            self.writeCsv(self.filename)
        elif q.text() == "Save as PNG":
            pass


def main():
    app = QApplication(sys.argv)

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


main()



