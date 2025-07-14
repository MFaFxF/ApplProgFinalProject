import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication

from service.signal_processor import SignalProcessor


class MainViewModel(QObject):
    data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()

        self.signal_processor = SignalProcessor()
        self.signal_processor.generate_signal()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.setInterval(3)  # 1000ms/30Hz ≈ 33ms

        self.window_samples = 2048
        self.sampling_rate = 2000  # match your signal source
        self.time_axis = np.linspace(0, self.window_samples / self.sampling_rate, self.window_samples)

    def start_plotting(self):
        self.timer.start()

    def update_data(self):
        data = self.signal_processor.data

        if isinstance(data, np.ndarray) and data.shape[1] == self.window_samples:
            channel_1 = data[0]  # use first channel
            self.data_updated.emit(self.time_axis, channel_1 / 10000)

if __name__ == '__main__':
    mainViewModel = MainViewModel()
    mainViewModel.start_plotting()

    while True:
        print(mainViewModel.data_updated)
