import time

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from PyQt5.QtWidgets import QApplication

from final_project.service.signal_processor import SignalProcessor


class MainViewModel(QObject):
    """"""

    # Signal container
    data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        """"""
        super().__init__()
        self.signalProcessor = SignalProcessor()
        self.signalProcessor.get_signal()


if __name__ == '__main__':
    mainViewModel = MainViewModel()
    while True:
        time.sleep(1)
        print(mainViewModel.signalProcessor.data[0])
