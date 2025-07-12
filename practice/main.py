from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtWidgets import QMainWindow

import sys

app = QApplication(sys.argv)

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Werner Window")
        self.setFixedSize(500,500)

        button = QPushButton("Hello, World!")
        button.setCheckable(True)
        button.clicked.connect(self.onButtonClicked)
        button.clicked.connect(self.buttonState)

        self.setCentralWidget(button)

    def onButtonClicked(self):
        print("Aua!")

    def buttonState(self, state):
        print("state", state)


window = MainView()
window.show()

app.exec()