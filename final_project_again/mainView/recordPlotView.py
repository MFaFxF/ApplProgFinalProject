import sys
import numpy as np
import matplotlib.pyplot as plt


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RecordingPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.line = None
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.canvas)
        
        # Set default style
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
    
    def update_data(self, time_axis, data, processing_type="raw"):
        """Update plot with new data and processing type"""
        self.ax.clear()
        
        # Plot with different styles based on processing type
        if processing_type == 'raw':
            color = 'b'
            label = 'Raw Signal'
            alpha = 0.7
        elif processing_type == 'rms':
            color = 'r'
            label = 'RMS'
            alpha = 1.0
        elif processing_type == 'envelope':
            color = 'g'
            label = 'Envelope'
            alpha = 0.8
        else:  # filtered
            color = 'm'
            label = 'Filtered'
            alpha = 0.9
        
        self.line, = self.ax.plot(time_axis, data, 
                                color=color, 
                                label=label,
                                alpha=alpha)
        
        # Update labels and title
        self.ax.set_title(f"EMG Recording ({processing_type.capitalize()})")
        self.ax.legend()
        self.canvas.draw()