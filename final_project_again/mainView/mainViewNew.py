from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QHBoxLayout
from .lifePlotView import LivePlotWidget
from .recordPlotView import RecordingPlotWidget
import time

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.setFixedSize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        live_plot_widget = LivePlotWidget()
        live_plot_widget.setFixedHeight(400)

        recording_widget = RecordingPlotWidget()

        live_view_layout = QHBoxLayout()
        live_view_layout.addWidget(live_plot_widget)

        # add buttons to live view
        live_button_layout = QVBoxLayout()
        button = QPushButton("Start/Stop")
        live_button_layout.addWidget(button)
        button = QPushButton("Raw Signal")
        live_button_layout.addWidget(button)
        button = QPushButton("RMS")
        live_button_layout.addWidget(button)
        button = QPushButton("Envelope")
        live_button_layout.addWidget(button)
        live_view_layout.addLayout(live_button_layout)

        recording_plot_widget = QHBoxLayout()
        recording_plot_widget.addWidget(recording_widget)
        recording_plot_widget.addLayout(live_button_layout)

        recording_button_layout = QVBoxLayout()
        button = QPushButton("Start/Stop")
        recording_button_layout.addWidget(button)
        button = QPushButton("Raw Signal")
        recording_button_layout.addWidget(button)
        button = QPushButton("RMS")
        recording_button_layout.addWidget(button)
        button = QPushButton("Envelope")
        recording_button_layout.addWidget(button)
        recording_plot_widget.addLayout(recording_button_layout)

        layout.addLayout(live_view_layout)
        layout.addLayout(recording_plot_widget)

        self.view_model.live_data_updated.connect(live_plot_widget.update_data)
        self.view_model.full_data_updated.connect(recording_widget.update_data)

