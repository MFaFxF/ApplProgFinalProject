from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor

class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data
    full_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()
        self.signal_processor.process_signal()

        self.channel = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)  # Update every 100 ms

        self.live_data_time_axis = np.linspace(0, 10000, self.signal_processor.live_window_size)

    def set_channel(self, channel):
        self.channel = channel

    def do_sth(self):
        live_window = self.signal_processor.live_window
        full_window = self.signal_processor.full_window

    def update_data(self):
        print("Updating data in MainViewModel, channel:", self.channel)
        self.live_data_updated.emit(self.live_data_time_axis, self.signal_processor.live_window[self.channel])

if __name__ == "__main__":
    print("ÖÖÖÖÖÖÖÖÖÖÖÖ")