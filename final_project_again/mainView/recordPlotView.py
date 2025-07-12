import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RecordingView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Data for the plot
        x = np.linspace(0, 10, 1000)
        y = np.sin(x**1.2)

        # Create the matplotlib Figure and Axes
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Plot the data
        self.ax.plot(x, y)
        self.ax.set_title("Sine Wave")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("sin(x)")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)