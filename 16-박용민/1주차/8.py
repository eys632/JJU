import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QPixmap

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Exit Action
        exitAction = QAction(QIcon('C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/images.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # Save Action
        saveAction = QAction(QIcon('C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/images.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save the application state')
        saveAction.triggered.connect(self.save)

        # About Action
        aboutAction = QAction(QIcon('C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/images.png'), 'About', self)
        aboutAction.setShortcut('Ctrl+I')
        aboutAction.setStatusTip('Show information about the application')
        aboutAction.triggered.connect(self.showAbout)
        
        # Menubar setup
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        # File Menu3
        fileMenu = menubar.addMenu('안녕하세요')
        fileMenu.addAction(exitAction)

        # Edit Menu
        editMenu = menubar.addMenu('저는')
        editMenu.addAction(saveAction)

        helpMenu = menubar.addMenu('전주대학교를 다니는')
        helpMenu.addAction(aboutAction)
        # Help Menu
        helpMenu = menubar.addMenu('박용민')
        helpMenu.addAction(aboutAction)

        helpMenu = menubar.addMenu('2003년생')
        helpMenu.addAction(aboutAction)

        helpMenu = menubar.addMenu('생일은 0214입니다')
        helpMenu.addAction(aboutAction)

        # Status Bar
        self.statusBar().showMessage('Ready')

        # Create a button with an image
        self.imageButton = QPushButton(self)
        pixmap = QPixmap('C:/Users/박용민/OneDrive/바탕 화면/비트컴퓨터/jju.png')  # 이미지 경로

        # Set custom size for the image button
        custom_width = 1820  # 원하는 너비
        custom_height = 910  # 원하는 높이
        scaled_pixmap = pixmap.scaled(custom_width, custom_height)  # 이미지 크기 조정

        # Convert QPixmap to QIcon and set the icon
        self.imageButton.setIcon(QIcon(scaled_pixmap))
        self.imageButton.setIconSize(scaled_pixmap.size())
        self.imageButton.setGeometry(50, 50, custom_width, custom_height)  # 버튼 크기와 위치 설정

        # Connect the button click event to the close method
        self.imageButton.clicked.connect(self.closeWindow)

        # Main Window settings
        self.setWindowTitle('박용민의 작품')
        self.setGeometry(300, 300, 400, 300)  # 창 크기 조정
        self.show()

    def save(self):
        # Save action logic
        self.statusBar().showMessage('Save action triggered!')

    def showAbout(self):
        # Show About MessageBox
        QMessageBox.information(self, 'About', 'This is a simple PyQt5 application.\nVersion 1.0')

    def closeWindow(self):
        # Close the application when the image button is clicked
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
