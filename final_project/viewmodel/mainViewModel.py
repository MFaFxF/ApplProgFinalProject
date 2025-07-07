from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np

class MainViewModel(QObject):
    """"""

    # Signal container
    data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        """"""
        super().__init__()
