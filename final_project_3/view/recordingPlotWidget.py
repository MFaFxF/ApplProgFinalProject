import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QFrame, QSizePolicy
from PyQt5.QtCore import Qt

class RecordingPlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Matplotlib Plot
        self.figure = Figure(facecolor="black")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("black")
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Control Panel
        control_layout = QVBoxLayout()

        self.record_button = QPushButton("Record")
        self.record_button.setCheckable(True)
        self.record_button.setFixedSize(100, 100)
        self.record_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            """
        )
        self.record_button.clicked.connect(self._toggle_recording_style)
        control_layout.addWidget(self.record_button)

        # Optional: Channel Selector
        self.channel_selector = QSpinBox()
        self.channel_selector.setRange(1, 32)
        self.channel_selector.setPrefix("Ch ")
        self.channel_selector.setFixedSize(100, 50)
        self.channel_selector.setStyleSheet(
            """
            QSpinBox {
                font-size: 14px;
                padding: 4px;
                color: white;
                background-color: #333;
                border-radius: 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
            }
            """
        )
        control_layout.addWidget(self.channel_selector)

        control_layout.setAlignment(Qt.AlignTop)
        layout.addLayout(control_layout)

    def _toggle_recording_style(self):
        if self.record_button.isChecked():
            self.record_button.setText("Stop")
            self.record_button.setStyleSheet("background-color: #388E3C; color: white;")
        else:
            self.record_button.setText("Record")
            self.record_button.setStyleSheet("background-color: #d32f2f; color: white;")

    def update_data(self, time_axis, data):
        self.ax.clear()
        self.ax.plot(time_axis, data, color='lime', linewidth=1)
        self.ax.set_title("EMG Recording")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("EMG Signal")
        self.ax.set_xlim(time_axis[0], time_axis[-1])

        # Re-apply dark theme
        self.ax.set_facecolor("black")
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

        self.canvas.draw()
        self.canvas.flush_events()
