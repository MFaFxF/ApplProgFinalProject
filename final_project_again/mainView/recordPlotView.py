import sys
import numpy as np
import matplotlib.pyplot as plt


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RecordingPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMG Recording")
        # self.setGeometry

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.update_data(np.linspace(0, 10, 18), np.zeros(18))
        layout.addWidget(self.canvas)

    
    def update_data(self, time_axis, data):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.ax.plot(time_axis, data)
        self.ax.set_title("EMG Recording")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("EMG Signal")