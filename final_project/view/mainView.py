from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from final_project.view.plotView import VisPyPlotWidget


class MainView(QMainWindow):

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        # Set up the main window
        self.setWindowTitle("Live RMS Plot")
        self.setGeometry(100, 100, 800, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create plot widget
        self.plot_widget = VisPyPlotWidget()
        layout.addWidget(self.plot_widget)
        self.view_model.data_updated.connect(self.plot_widget.update_data)

        self.view_model.start_plotting()
