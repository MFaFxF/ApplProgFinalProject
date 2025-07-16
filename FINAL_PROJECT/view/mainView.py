
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFrame, QSizePolicy

from .recordingWidget import RecordingPlotWidget
from .livePlotWidget import LivePlotWidget

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        # Set window title, size
        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.setFixedSize(1200, 800)

        # Central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)

        # -- live signal widget --

        # add widget
        live_plot_widget = LivePlotWidget()
        central_layout.addWidget(live_plot_widget)

        # connect Buttons
        live_plot_widget.start_stop_button.clicked.connect(self.handle_start_stop)
        live_plot_widget.channel_selector.valueChanged.connect(self.view_model.set_live_channel)

        live_plot_widget.raw_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('raw') if checked else None)
        live_plot_widget.rms_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('rms') if checked else None)
        live_plot_widget.envelope_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('envelope') if checked else None)
        live_plot_widget.filter_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('filter') if checked else None)

        # connect data
        view_model.live_data_updated.connect(live_plot_widget.update_data)

        # Horizontal line separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: gray; margin-top: 10px; margin-bottom: 10px;")

        central_layout.addWidget(separator)

        # -- recording widget --
        recording_widget = RecordingPlotWidget()
        central_layout.addWidget(recording_widget)

        # connect buttons
        recording_widget.channel_selector.valueChanged.connect(view_model.set_recording_channel)
        recording_widget.record_raw_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('raw') if checked else None)
        recording_widget.record_rms_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('rms') if checked else None)
        recording_widget.record_envelope_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('envelope') if checked else None)
        recording_widget.record_filter_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('filter') if checked else None)

        # connect data
        view_model.recorded_data_updated.connect(recording_widget.update_data)
        

    def handle_start_stop(self):
        if self.view_model.is_receiving:
            self.view_model.is_receiving = False
            self.view_model.timer.stop()
        else:
            self.view_model.is_receiving = True
            self.view_model.timer.start(int(self.view_model.sleep_time))