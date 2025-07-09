import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication

from final_project_2.service.signal_processor import SignalProcessor


class MainViewModel(QObject):

    data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()

        self.signal_processor = SignalProcessor()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.setInterval(33)  # 1000ms/30Hz ≈ 33ms

        self.fixed_time_window = np.linspace(0, 10, 18)

    def update_data(self):
        data_window = self.signal_processor.data[0]

        self.data_updated.emit(self.fixed_time_window, data_window)



if __name__ == '__main__':
    mainViewModel = MainViewModel()
    while True:
        print(mainViewModel.signal_processor.data.size)
