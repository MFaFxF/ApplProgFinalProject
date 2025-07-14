from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vispy import app, scene
import numpy as np

class VisPyPlotWidget(QWidget):
    """
    A widget that displays live plotting using VisPy.

    This class is part of the View layer in the MVVM architecture. It:
    - Creates and manages the VisPy canvas
    - Handles the visualization of the signal
    - Maintains a fixed view range
    - Updates the plot with new data

    The widget uses VisPy for high-performance OpenGL-based plotting,
    which is essential for smooth real-time updates.
    """

    def __init__(self, parent=None):
        """
        Initialize the plot widget with VisPy canvas and view.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create VisPy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 400))
        layout.addWidget(self.canvas.native)

        # Create view
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'panzoom'

        # Create line plot
        self.line = scene.Line(np.array([[0, 0]]), parent=self.view.scene)

        # Set up the view with fixed range
        self.view.camera.set_range(x=(0, 1), y=(-10, 10))

    def update_data(self, time_points, data):
        """
        Update the plot with new data.

        This method is called whenever new data is available. It:
        - Creates a new line data array from time and signal data
        - Updates the plot with the new data
        - Maintains the fixed view range

        Args:
            time_points (np.ndarray): Array of time values
            data (np.ndarray): Array of signal values
        """
        # Create the line data
        line_data = np.column_stack((time_points, data))
        self.line.set_data(line_data)

        # Keep the view fixed
        self.view.camera.set_range(x=(0, 1), y=(-10, 10))
        self.canvas.update()