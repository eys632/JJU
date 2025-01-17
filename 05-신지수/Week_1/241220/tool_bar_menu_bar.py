import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Exit action
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # Save action
        saveAction = QAction(QIcon('save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save file')
        # saveAction.triggered.connect(self.save)  # Add save functionality here

        self.statusBar()

        # Menu bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Edit')
        # Add actions to editMenu here

        helpMenu = menubar.addMenu('&Help')
        # Add actions to helpMenu here

        # Tool bar
        self.toolbar = self.addToolBar('Save')
        self.toolbar.addAction(saveAction)

        self.setWindowTitle('Toolbar and Menubar')
        self.setGeometry(300, 300, 400, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
