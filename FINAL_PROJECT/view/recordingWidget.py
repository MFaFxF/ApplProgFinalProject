import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QSizePolicy, QButtonGroup
)
from PyQt5.QtCore import Qt



class RecordingPlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        self.channel = 0

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # === Plot Area (Canvas + Toolbar) ===
        plot_container = QWidget()
        plot_layout = QVBoxLayout()
        plot_layout.setContentsMargins(0, 0, 0, 0)
        plot_container.setLayout(plot_layout)


        with plt.style.context('dark_background'):
            self.figure = Figure()
            self.ax = self.figure.add_subplot(111)

            self.ax.set_facecolor("black")
            self.ax.set_title("EMG Recording", color='white')
            self.ax.set_xlabel("Time (s)", color='white')
            self.ax.set_ylabel("EMG Signal", color='white')
            self.ax.tick_params(colors='white')
            self.ax.grid(True, color='white', linestyle='--', linewidth=0.5)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: white;
                border: none;
            }
            QToolButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #ddd;
            }
            QToolButton:checked {
                background-color: #bbb;
            }
        """)


        plot_layout.addWidget(self.canvas)
        plot_layout.addWidget(self.toolbar)

        # === Horizontal Layout: Plot + Controls ===
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(plot_container)

        # === Control Panel ===
        control_layout = QVBoxLayout()
        control_layout.setAlignment(Qt.AlignTop)

        # Channel Selector
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
                background: "black"
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
            }
            """
        )

        control_layout.addWidget(self.channel_selector)

        horizontal_layout.addLayout(control_layout)
        main_layout.addLayout(horizontal_layout)

        self.record_mode_group = QButtonGroup(self)
        self.record_mode_group.setExclusive(True)

        self.record_raw_button = QPushButton("Raw")
        self.record_raw_button.setCheckable(True)
        self.record_raw_button.setChecked(True)

        self.record_rms_button = QPushButton("RMS")
        self.record_rms_button.setCheckable(True)

        self.record_envelope_button = QPushButton("Envelope")
        self.record_envelope_button.setCheckable(True)

        self.record_filter_button = QPushButton("Filter")
        self.record_filter_button.setCheckable(True)

        for btn in [self.record_raw_button, self.record_rms_button, self.record_envelope_button, self.record_filter_button]:
            btn.setFixedSize(100, 40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 13px;
                    padding: 6px;
                    background-color: #444;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    background-color: #2196F3;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)
            self.record_mode_group.addButton(btn)
            control_layout.addWidget(btn)

        # Clear Recording Button
        self.clear_button = QPushButton("Clear Recording")
        self.clear_button.setFixedSize(140, 40)
        self.clear_button.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                padding: 6px;
                background-color: #b00020;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #7f0000;
            }
        """)
        control_layout.addWidget(self.clear_button)

    
    def toggle_toolbar_visible(self, visible):
        """Toggle visibility of the toolbar"""
        self.toolbar.setVisible(visible)
        if visible:
            self.toolbar.show()
        else:
            self.toolbar.hide()


    def update_data(self, time_axis, data):
        """Update the plot with new data"""
        self.time_axis = time_axis
        self.data = data

        self.ax.clear()
        self.ax.plot(time_axis, data, color='white', linewidth=1)

        self.ax.set_facecolor("black")
        self.ax.set_title("EMG Recording", color='white')
        self.ax.set_xlabel("Time (s)", color='white')
        self.ax.set_ylabel("EMG Signal", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(True, color='white', linestyle='-', linewidth=0.1)
        # self.ax.set_xlim(time_axis[0], time_axis[-1])

        self.canvas.draw()
        self.canvas.flush_events()