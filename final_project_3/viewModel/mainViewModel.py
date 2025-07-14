
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor


class MainViewModel(QObject):
    live_signal_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()
        self.signal_processor.generate_signal()

        self.channel = 0

        self.time_points_live_signal = np.linspace(0, 10, self.signal_processor.live_window_size) #TODO meaningful value

        self.live_signal = None
        self.is_receiving = False

        self.filter_mode_live_signal = "none"

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(50)

    def set_channel(self, channel):
        self.channel = channel - 1
        print("Switched to channel: ", channel)

    def update_data(self):
        if self.is_receiving:
            # get current signal
            self.live_signal = self.signal_processor.live_signal

            # apply filter
            self.live_signal = self.process_signal(self.live_signal, self.filter_mode_live_signal)

            self.live_signal_updated.emit(self.time_points_live_signal, self.live_signal[self.channel, :])

    def start_recording(self):
        self.is_receiving = True

    def stop_recording(self):
        self.is_receiving = False

    def process_signal(self, signal, filter_mode):
        if filter_mode == "none":
            return signal
        
    def apply_rms(self, signal):
        # do stuff
        pass