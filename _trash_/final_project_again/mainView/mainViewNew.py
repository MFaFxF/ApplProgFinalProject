
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from .lifePlotView import LivePlotWidget
from .recordPlotView import RecordingPlotWidget

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.setFixedSize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.live_plot_widget = LivePlotWidget()
        self.live_plot_widget.setFixedHeight(400)

        self.recording_widget = RecordingPlotWidget()
        self.recording_widget.setFixedHeight(400)

        live_view_layout = QHBoxLayout()
        live_view_layout.addWidget(self.live_plot_widget)

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
        live_button_layout.addWidget(self.btn_start_stop)


        recording_layout = QHBoxLayout()
        recording_layout.addWidget(self.recording_widget)
        recording_layout.addLayout(live_button_layout)

        layout.addLayout(live_view_layout)
        layout.addLayout(recording_layout)

        self.view_model.live_data_updated.connect(self.live_plot_widget.update_data)
        self.view_model.full_data_updated.connect(self.recording_widget.update_data)

    def handle_start_stop(self):
        if self.btn_start_stop.isChecked():
            self.btn_start_stop.setText("Stop")
            self.btn_start_stop.setStyleSheet("background-color: #f44336; color: white;")
            self.view_model.start_recording()
        else:
            self.btn_start_stop.setText("Start")
            self.btn_start_stop.setStyleSheet("background-color: #4CAF50; color: white;")
            self.view_model.stop_recording()