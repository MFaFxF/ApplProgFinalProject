from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFrame, QSizePolicy, QSplitter)
import time
from PyQt5.QtCore import QTimer, Qt

from .connectionWidget import ConnectionWidget
from .recordingWidget import RecordingPlotWidget
from .livePlotWidget import LivePlotWidget


class MainView(QMainWindow):
    """
    Main application window / entry point for the EMG Data Viewer application.

    This view integrates:
    - A connection control widget (connect/disconnect)
    - A live signal visualization widget with processing options
    - A recording widget with processing options, export button

    It links UI components to the ViewModel and sets up all necessary signal-slot connections.
    """

    def __init__(self, view_model):
        """
        Initialize the MainView.

        Parameters:
        - view_model: The main ViewModel instance coordinating signal flow and state.
        """
        super().__init__()
        self.view_model = view_model
        self.signal_processor = view_model.signal_processor
        self.setStyleSheet("background-color: #121212;")
        # === Main window setup ===
        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.resize(1200, 800)

        # === Central layout setup ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)
        central_widget.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Expanding)

        # === Connection Widget ===
        self.connection_widget = ConnectionWidget()
        central_layout.addWidget(self.connection_widget)
        central_layout.setContentsMargins(10, 10, 10, 10)
        central_layout.setSpacing(15)

        # Handle connect/disconnect button press
        self.connection_widget.toggled.connect(self.handle_connection_toggled)

        # === Live Plot Widget ===
        live_plot_widget = LivePlotWidget(self.signal_processor.live_window_time)
        #central_layout.addWidget(live_plot_widget , stretch=1)
        live_plot_widget.setStyleSheet("background-color: #1e1e1e;")  # Light green background

        # Connect control buttons and channel selector
        live_plot_widget.start_stop_button.clicked.connect(self.handle_start_stop)
        live_plot_widget.channel_selector.valueChanged.connect(self.view_model.set_live_channel)

        # Connect signal processing mode buttons
        live_plot_widget.raw_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('raw') if checked else None)
        live_plot_widget.rms_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('rms') if checked else None)
        live_plot_widget.envelope_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('envelope') if checked else None)
        live_plot_widget.filter_button.toggled.connect(lambda checked: self.view_model.set_live_processing_mode('filter') if checked else None)

        # Connect data update signal
        view_model.live_data_updated.connect(live_plot_widget.update_data)

        # === Horizontal Separator ===
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: black; margin-top: 10px; margin-bottom: 10px; width: 2px;")
        central_layout.addWidget(separator)

        # === Recording Plot Widget ===
        self.recording_widget = RecordingPlotWidget(self.view_model)
        self.recording_widget.setStyleSheet("background-color: #1e1e1e;")  # Dark theme

        # Connect recording controls
        self.recording_widget.channel_selector.valueChanged.connect(view_model.set_recording_channel)
        self.recording_widget.raw_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('raw') if checked else None)
        self.recording_widget.rms_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('rms') if checked else None)
        self.recording_widget.envelope_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('envelope') if checked else None)
        self.recording_widget.filter_button.toggled.connect(lambda checked: view_model.set_recording_processing_mode('filter') if checked else None)

        # Connect recorded data update and clear button
        view_model.recorded_data_updated.connect(self.recording_widget.update_data)
        self.recording_widget.clear_button.clicked.connect(self.clear_recording_and_plot)
        
        # Splitter to scale live plot and recording plot
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(live_plot_widget)
        splitter.addWidget(self.recording_widget)
        splitter.setSizes([1, 1])  # Initial 50/50 split
        central_layout.addWidget(splitter, stretch=1)

    def clear_recording_and_plot(self):
        """
        Clear both the ViewModel's recording data and the associated plot.
        """
        self.view_model.clear_recording()
        self.recording_widget.clear_plot()

    def handle_start_stop(self):
        """
        Toggle the data reception state for live signal processing.

        Starts or stops the ViewModel's timer and updates the recording flag.
        Toggles the visibility of the recording toolbar.
        """
        if self.view_model.is_receiving:
            self.view_model.is_receiving = False
            self.signal_processor.is_recording = False
            self.view_model.timer.stop()
            self.recording_widget.toggle_toolbar_visible(True)
        else:
            self.view_model.is_receiving = True
            self.signal_processor.is_recording = True
            self.view_model.timer.start(int(self.view_model.sleep_time))
            self.recording_widget.toggle_toolbar_visible(False)

    def handle_connection_toggled(self, connected: bool):
        """
        Respond to user toggling the connection button.

        Parameters:
        - connected (bool): True if user wants to connect, False to disconnect.
        """
        self.connection_widget.toggle_button.setEnabled(False)

        if connected:
            self.connection_widget.status_label.setText("Connecting...")
            # Handle connection in a separate thread to avoid blocking the UI
            QTimer.singleShot(50, self._do_connect_on_widget)
        else:
            self.connection_widget.status_label.setText("Disconnecting...")
            # Handle connection in a separate thread to avoid blocking the UI
            QTimer.singleShot(50, self._do_disconnect_on_widget)

    def _do_disconnect_on_widget(self):
        """
        Internal helper to stop signal streaming and update UI after disconnect.
        """
        self.signal_processor.stop_signal()
        time.sleep(1)  # Allow time for disconnection
        self.connection_widget.set_connection_status(self.signal_processor.tcp_client.connected)
        self.connection_widget.toggle_button.setEnabled(True)

    def _do_connect_on_widget(self):
        """
        Internal helper to start signal streaming and update UI after connect.
        """
        self.signal_processor.generate_signal()
        time.sleep(1)  # Allow time to establish connection
        self.connection_widget.set_connection_status(self.signal_processor.tcp_client.connected)
        self.connection_widget.toggle_button.setEnabled(True)
