from PyQt5.QtCore import QObject, pyqtSignal, QTimer 
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
from service.signal_processor import SignalProcessor
from scipy.signal import hilbert, butter, lfilter
import time
import csv

class MainViewModel(QObject):
    """
    ViewModel layer for managing signal processing, state, and communication 
    between the SignalProcessor and UI components.

    Responsibilities:
    - Handles live and recorded EMG data updates
    - Applies signal processing (RMS, envelope, filter)
    - Coordinates plotting updates and recording logic
    - Manages export functionality
    """

    # Updated signals, emitted when data changes
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)
    recorded_data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        """
        Initialize the MainViewModel.

        Sets up:
        - Signal processor and sampling config
        - Live/recorded data containers
        - Default processing modes and timers
        """
        super().__init__()

        self.signal_processor = SignalProcessor()
        self.sampling_rate = self.signal_processor.sampling_rate
        self.sleep_time = self.signal_processor.sleep_time

        # Live signal state
        self.live_data = self.signal_processor.live_signal
        self.live_window_size = self.signal_processor.live_window_size
        self.live_data_time_points = np.linspace(0, self.live_window_size / self.sampling_rate, self.live_window_size)
        self.processed_live_data = self.live_data

        # Recorded signal state
        self.recorded_data = self.live_data.copy()
        self.processed_recorded_data = self.recorded_data

        # Processing settings
        self.live_processing_mode = 'raw'
        self.recording_processing_mode = 'raw'
        self.rms_window_size = 200  # 100 ms at 2000 Hz
        self.filter_cutoff = 0.1    # TODO calibrate

        # Channel selection (0-indexed)
        self.live_channel = 0
        self.recording_channel = 0

        # Reception flag
        self.is_receiving = False

        # Timers for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_live_data)
        self.timer.timeout.connect(self.update_recorded_data)
        self.timer.start(9)  # Synchronize with tcp server

    def set_live_channel(self, channel):
        """
        Set the active channel for live data processing.

        Parameters:
        - channel (int): Channel index (1-based)
        """
        self.live_channel = channel - 1
        self.update_live_data()

    def set_live_processing_mode(self, mode):
        """
        Set the signal processing mode for live data.

        Parameters:
        - mode (str): 'raw', 'rms', 'envelope', or 'filter'
        """
        self.live_processing_mode = mode
        self.update_live_data()

    def set_recording_channel(self, channel):
        """
        Set the active channel for recorded data processing.

        Parameters:
        - channel (int): Channel index (1-based)
        """
        self.recording_channel = channel - 1
        self.update_recorded_data()

    def set_recording_processing_mode(self, mode):
        """
        Set the signal processing mode for recorded data.

        Parameters:
        - mode (str): 'raw', 'rms', 'envelope', or 'filter'
        """
        self.recording_processing_mode = mode
        self.update_recorded_data()

    def clear_recording(self):
        """
        Clear the recorded signal and refresh view.
        """
        self.signal_processor.clear_recording()
        self.update_recorded_data()

    def process_signal(self, data, mode):
        """
        Apply the selected signal processing method.

        Parameters:
        - data (np.ndarray): Input 1D signal
        - mode (str): Processing type ('raw', 'rms', etc.)

        Returns:
        - np.ndarray: Processed signal
        """
        if mode == 'raw':
            return data
        elif mode == 'rms':
            return self.apply_rms(data)
        elif mode == 'envelope':
            return self.apply_envelope(data)
        elif mode == 'filter':
            return self.apply_filter(data)
        return data

    def apply_rms(self, data):
        """
        Compute the RMS (Root Mean Square) of the signal.

        Parameters:
        - data (np.ndarray): Input signal

        Returns:
        - np.ndarray: RMS-smoothed signal
        """
        # TODO why not use ex 4?
        squared = np.square(data)
        window = np.ones(self.rms_window_size) / self.rms_window_size
        return np.sqrt(np.convolve(squared, window, 'same'))

    def apply_envelope(self, data):
        """
        Compute the envelope of the signal using Hilbert transform.

        Parameters:
        - data (np.ndarray): Input signal

        Returns:
        - np.ndarray: Envelope of the signal
        """
        return np.abs(hilbert(data))

    def apply_filter(self, data):
        """
        Apply a 4th-order low-pass Butterworth filter.

        Parameters:
        - data (np.ndarray): Input signal

        Returns:
        - np.ndarray: Filtered signal
        """
        b, a = butter(4, self.filter_cutoff, btype="low")
        return lfilter(b, a, data)

    def export_results(self):
        """
        Export the recorded signal (time, value) to a CSV file.

        Uses a QFileDialog for file selection. Emits success/failure messages.
        """
        if self.recorded_data is None or self.processed_recorded_data is None:
            QMessageBox.warning(None, "Export Failed", "No data to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            None, "Export data", "", "CSV Files (*.csv);;Text Files (*.txt)"
        )
        if not file_path:
            return  # Cancelled by user

        try:
            with open(file_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Value"])  # CSV header
                for t, v in zip(self.recorded_data_time_points, self.processed_recorded_data):
                    writer.writerow([t, v])
            QMessageBox.information(None, "Export successful", f"Data saved to: {file_path}")
        except Exception as e:
            QMessageBox.critical(None, "Export failed", str(e))

    def update_live_data(self):
        """
        Update the live signal view with current data.

        Applies processing mode and emits to connected plots.
        """
        #if self.is_receiving:
        self.live_data = self.signal_processor.live_signal

        self.processed_live_data = self.process_signal(
            self.live_data[self.live_channel, :],
            self.live_processing_mode
        )
        self.live_data_updated.emit(self.live_data_time_points, self.processed_live_data)

    def update_recorded_data(self):
        """
        Update the recorded signal view with current data and emit signal.

        Applies processing mode and recalculates time axis.
        """
        if self.is_receiving:
            self.recorded_data = self.signal_processor.recorded_signal

        if self.recorded_data is None:
            # Use fallback if recorded data not yet initialized
            self.recorded_data = np.zeros_like(self.signal_processor.live_signal[:, -1:])

        self.processed_recorded_data = self.process_signal(
            self.recorded_data[self.recording_channel, :],
            self.recording_processing_mode
        )

        self.recorded_data_time_points = np.linspace(
            0,
            self.processed_recorded_data.shape[0] / self.sampling_rate,
            self.processed_recorded_data.shape[0]
        )
        self.recorded_data_updated.emit(
            self.recorded_data_time_points, self.processed_recorded_data
        )
