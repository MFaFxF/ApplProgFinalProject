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
        recording_widget.setFixedHeight(400)

        live_view_layout = QHBoxLayout()
        live_view_layout.addWidget(live_plot_widget)

        # add buttons to live view
        live_button_layout = QVBoxLayout()
        self.btn_start_stop = QPushButton("Start")
        self.btn_start_stop.setCheckable(True)
        self.btn_start_stop.setFixedSize(100,100)
        self.btn_start_stop.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
            padding: 8px;
            background-color: #4CAF50;  /* Green */
            color: white;
            border: none;
            border-radius: 4px;
            }
            QPushButton:hover {
            background-color: #45a049;
            }
            """
            )
        
        live_view_layout.addWidget(self.btn_start_stop)
        self.btn_start_stop.clicked.connect(self.handle_start_stop)

        recording_plot_widget = QHBoxLayout()
        recording_plot_widget.addWidget(recording_widget)
        recording_plot_widget.addLayout(live_button_layout)

        layout.addLayout(live_view_layout)
        layout.addLayout(recording_plot_widget)

        self.view_model.live_data_updated.connect(live_plot_widget.update_data)
        self.view_model.full_data_updated.connect(recording_widget.update_data)

    def handle_start_stop(self):
        if self.btn_start_stop.isChecked():
            self.btn_start_stop.setText("Stop")
            self.btn_start_stop.setStyleSheet("background: #f44336")

            self.view_model.start_signal()
        else:
            self.btn_start_stop.setText("Start")
            self.btn_start_stop.setStyleSheet("background: #4caf50")

            self.view_model.stop_signal()