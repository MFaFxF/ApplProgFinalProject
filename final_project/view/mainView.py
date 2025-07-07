from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class MainView(QMainWindow):
    """
    """
    def __init__(self, view_model):
        """
        :param view_model:
        """
        super().__init__()
        self.view_model = view_model

        # Main Window
        self.setWindowTitle('Main Window') #TODO title
        self.setGeometry(100, 100, 1000, 800)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # TODO PLotwidget?

        # Create control button?
        self.control_button = QPushButton("Start Plotting")
        self.control_button.clicked.connect(self.toggle_plotting)
        layout.addWidget(self.control_button)

        # Connect view model signals
        self.view_model.data_updated.connect(self.plot_widget.update_data)

    def toggle_plotting(self):
        pass