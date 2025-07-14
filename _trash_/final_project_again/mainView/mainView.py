from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QHBoxLayout
from .lifePlotView import LivePlotWidget
import time

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self.setWindowTitle("Walter Window")
        self.setFixedSize(1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Channel selector with arrows
        control_layout = QHBoxLayout()
        self.channel_selector = QSpinBox()
        self.channel_selector.setRange(1, 32)  # assuming 32 channels
        self.channel_selector.setPrefix("Ch ")
        self.channel_selector.valueChanged.connect(self.view_model.set_channel)
        control_layout.addWidget(QLabel("Select Channel:"))
        control_layout.addWidget(self.channel_selector)

        self.plot_widget = LivePlotWidget()
        layout.addWidget(self.plot_widget)
        
        layout.addLayout(control_layout)
        # Connect view model signals
        self.view_model.live_data_updated.connect(self.plot_widget.update_data)

        