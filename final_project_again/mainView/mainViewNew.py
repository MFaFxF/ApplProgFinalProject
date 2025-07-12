from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QHBoxLayout
from .lifePlotView import LivePlotWidget
from .recordPlotView import RecordingView
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

        recording_widget = RecordingView()

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

        recording_view_layout = QHBoxLayout()
        recording_view_layout.addWidget(recording_widget)
        recording_view_layout.addLayout(live_button_layout)
        
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

        layout.addLayout(live_view_layout)
        layout.addLayout(recording_view_layout)

        self.view_model.live_data_updated.connect(live_plot_widget.update_data)

