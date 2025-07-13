from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor

class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data
    full_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()

        self.channel = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)  # Update every 100 ms #TODO set meaningful value

        self.live_data_time_axis = np.linspace(0, 10000, self.signal_processor.live_window_size)
        self.full_data_time_axis = np.linspace(0, 10000, self.signal_processor.full_window.shape[1])

        self.connected_to_live_signal = True

        self.recording = None

    def set_channel(self, channel):
        self.channel = channel - 1

    def start_signal(self):
        self.is_running = True
        self.signal_processor.start_signal()

    def stop_signal(self):
        self.is_running = False

    def update_data(self):
        # print("Updating data in MainViewModel, channel:", self.channel)
        self.live_data_updated.emit(self.live_data_time_axis, self.signal_processor.live_window[self.channel])
        
        # change this to recording whicj is stored in viewModel(here)
        self.full_data_updated.emit(self.full_data_time_axis, self.signal_processor.full_window[self.channel])

if __name__ == "__main__":
    print("ÖÖÖÖÖÖÖÖÖÖÖÖ")