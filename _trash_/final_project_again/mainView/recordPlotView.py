import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

class RecordingPlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
    
    def update_data(self, time_axis, data):
        time_axis = np.linspace(0, 10, len(data))
        self.ax.clear()
        self.ax.plot(time_axis, data)
        self.ax.set_title("EMG Recording")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("EMG Signal")

        self.canvas.draw()
        # self.canvas.flush_events()