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
        recording_widget = RecordingView()

        live_view_layout = QHBoxLayout()
        live_view_layout.addWidget(live_plot_widget)

        # add buttons to live view
        just_a_fucking_button = QPushButton("Hallo. Alles gut?").setMaximumWidth(50)
        live_view_layout.addWidget(just_a_fucking_button)
        live_view_layout.addWidget(QPushButton("Gesundheit"))


        recording_view_layout = QHBoxLayout()
        recording_view_layout.addWidget(recording_widget)

        layout.addLayout(live_view_layout)
        layout.addLayout(recording_view_layout)

        self.view_model.live_data_updated.connect(live_plot_widget.update_data)

