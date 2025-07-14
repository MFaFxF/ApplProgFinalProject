
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor

class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)
    full_data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()

        self.channel = 0
        self.connected_to_live_signal = False
        self.recording_active = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(50)

        self.live_data_time_axis = np.linspace(0, 10000, self.signal_processor.live_window_size)
        self.recorded_data = []

    def set_channel(self, channel):
        self.channel = channel - 1

    def update_data(self):
        if not self.connected_to_live_signal:
            return

        window = self.signal_processor.live_window
        self.live_data_updated.emit(self.live_data_time_axis, window[self.channel, :])

        if self.recording_active:
            self.recorded_data.append(window[:, -1])  # Record last sample

    def start_recording(self):
        self.recorded_data = []
        self.connected_to_live_signal = True
        self.recording_active = True

    def stop_recording(self):
        self.connected_to_live_signal = False
        self.recording_active = False

        if self.recorded_data:
            full_data = np.array(self.recorded_data).T
            time_axis = np.linspace(0, full_data.shape[1], full_data.shape[1])
            self.full_data_updated.emit(time_axis, full_data[self.channel, :])
