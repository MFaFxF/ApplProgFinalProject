
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFrame, QLabel, QSizePolicy
import time
from PyQt5.QtCore import QTimer

from .connectionWidget import ConnectionWidget
from .recordingWidget import RecordingPlotWidget
from .livePlotWidget import LivePlotWidget

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.signal_processor = view_model.signal_processor

        # Set window title, size
        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.resize(1200, 800)

        # Central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)
        central_widget.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Expanding)

        # connection widget
        self.connection_widget = ConnectionWidget()
        central_layout.addWidget(self.connection_widget)

        # handle button toggle
        self.connection_widget.toggled.connect(self.handle_connection_toggled)

        # -- live signal widget --

        # add widget
        live_plot_widget = LivePlotWidget()
        central_layout.addWidget(live_plot_widget)
        live_plot_widget.setStyleSheet("background-color: #ccffcc;")  # Light green
        central_layout.setContentsMargins(10, 10, 10, 10)
        central_layout.setSpacing(15)

        live_plot_widget.view.camera.set_range(x=(1, 5), y=(-50000, 50000))

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
        separator.setStyleSheet("background-color: black; margin-top: 10px; margin-bottom: 10px; width: 2px ;")

        central_layout.addWidget(separator)

        # -- recording widget --
        recording_widget = RecordingPlotWidget(self.view_model)
        central_layout.addWidget(recording_widget)
        recording_widget.setStyleSheet("background-color: #1e1e1e;")

        # connect buttons
        recording_widget.channel_selector.valueChanged.connect(view_model.set_recording_channel)
        recording_widget.record_raw_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('raw') if checked else None)
        recording_widget.record_rms_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('rms') if checked else None)
        recording_widget.record_envelope_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('envelope') if checked else None)
        recording_widget.record_filter_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('filter') if checked else None)

        # connect data
        view_model.recorded_data_updated.connect(recording_widget.update_data)
        recording_widget.clear_button.clicked.connect(view_model.clear_recording)

        
    def handle_start_stop(self):
        if self.view_model.is_receiving:
            self.view_model.is_receiving = False
            self.signal_processor.is_recording = False
            self.view_model.timer.stop()
        else:
            self.view_model.is_receiving = True
            self.signal_processor.is_recording = True
            self.view_model.timer.start(int(self.view_model.sleep_time))


    def handle_connection_toggled(self, connected: bool):
        self.connection_widget.toggle_button.setEnabled(False)

        if connected:
            self.connection_widget.status_label.setText("Connecting...")
            QTimer.singleShot(50, self._do_connect)
        else:
            self.connection_widget.status_label.setText("Disconnecting...")
            QTimer.singleShot(50, self._do_disconnect)


    def _do_disconnect(self):
        self.signal_processor.stop_signal()
        time.sleep(1)  # Allow time for disconnection
        self.connection_widget.set_connection_status(self.signal_processor.tcp_client.connected)
        self.connection_widget.toggle_button.setEnabled(True)

    def _do_connect(self):
        self.signal_processor.generate_signal()
        time.sleep(1)
        self.connection_widget.set_connection_status(self.signal_processor.tcp_client.connected)
        self.connection_widget.toggle_button.setEnabled(True)
