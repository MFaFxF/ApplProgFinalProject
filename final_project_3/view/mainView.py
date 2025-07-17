
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFrame, QSizePolicy

from .recordingPlotWidget import RecordingPlotWidget
from .lifePlotWidget import LivePlotWidget

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.setFixedSize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)

        self.live_plot_widget = LivePlotWidget()

        # Live Signal View
        live_view_layout = QHBoxLayout()
        live_view_layout.addWidget(self.live_plot_widget)

        # connect buttons
        self.live_plot_widget.start_stop_button.clicked.connect(self.handle_start_stop_live)
        self.live_plot_widget.channel_selector.valueChanged.connect(self.set_live_channel)
        self.live_plot_widget.raw_button.toggled.connect(lambda checked: self.view_model.set_processing_mode('raw') if checked else None)
        self.live_plot_widget.rms_button.toggled.connect(lambda checked: self.view_model.set_processing_mode('rms') if checked else None)
        self.live_plot_widget.envelope_button.toggled.connect(lambda checked: self.view_model.set_processing_mode('envelope') if checked else None)
        self.live_plot_widget.filter_button.toggled.connect(lambda checked: self.view_model.set_processing_mode('filter') if checked else None)

        central_layout.addLayout(live_view_layout)

        # connect view model to live plot widget
        self.view_model.live_data_updated.connect(self.live_plot_widget.update_data)
        # self.view_model.processed_live_data_updated.connect(self.live_plot_widget.update_data)

        # Horizontal line separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: gray; margin-top: 10px; margin-bottom: 10px;")

        central_layout.addWidget(separator)

        # Recording Widget
        self.recording_widget = RecordingPlotWidget()
        recording_layout = QVBoxLayout()
        recording_layout.addWidget(self.recording_widget)
        central_layout.addLayout(recording_layout)

        self.view_model.recorded_data_updated.connect(self.recording_widget.update_data)


    def handle_start_stop_live(self):
        if self.live_plot_widget.start_stop_button.isChecked():
            self.view_model.clear_recording()
            self.view_model.start_receiving()
        else:
            self.view_model.stop_receiving()

    def set_live_channel(self, channel):
        self.view_model.set_channel(channel)

    def set_recording_channel(self, channel):
        self.recording_widget.set_channel(channel)
