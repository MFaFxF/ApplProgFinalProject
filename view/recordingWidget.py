import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QSizePolicy, QButtonGroup , QSpacerItem
)
from PyQt5.QtCore import Qt

class RecordingPlotWidget(QWidget):
    """
    Widget for displaying and managing recorded EMG data.

    This widget includes:
    - A matplotlib plot area with toolbar
    - A control panel for:
        - Channel selection
        - Signal processing mode (Raw, RMS, Envelope, Filter)
        - Exporting the current recording
        - Clearing the recorded data
    """

    def __init__(self, view_model):
        """
        Initialize the recording plot widget.

        Parameters:
        - view_model: Reference to the main ViewModel for triggering exports and state control.
        """
        super().__init__()
        self.view_model = view_model
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.channel = 0

        # === Main layout ===
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # === Plot container (matplotlib canvas + toolbar) ===
        plot_container = QWidget()
        plot_layout = QVBoxLayout()
        plot_container.setLayout(plot_layout)
        plot_container.setStyleSheet("border : 1px solid white")

        with plt.style.context('dark_background'):
            self.figure = Figure(constrained_layout=True)
            self.ax = self.figure.add_subplot(111)
            self.ax.set_facecolor("black")
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
                padding: 6px ;
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

        # === Horizontal layout for plot and controls ===
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(plot_container, stretch=6)

        # === Control panel frame ===
        control_layout = QVBoxLayout()
        control_layout.setAlignment(Qt.AlignTop)
        control_layout.setContentsMargins(10, 10, 10, 10)
        

        control_frame = QWidget()
        control_frame.setLayout(control_layout)
        control_frame.setStyleSheet("background-color: #1e1e1e; border: 1.5px solid white; border-radius: 4px")

        horizontal_layout.addWidget(control_frame , stretch= 1)

        # === Channel selector ===
        self.channel_selector = QSpinBox()
        self.channel_selector.setRange(1, 32)
        self.channel_selector.setPrefix("Ch ")
        self.channel_selector.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.channel_selector.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                padding: 6px ;
                color: white;
                background-color: #333;
                border-radius: 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
            }
        """)
        control_layout.addWidget(self.channel_selector)

        # === Signal Mode Buttons ===
        self.mode_button_group = QButtonGroup(self)
        self.mode_button_group.setExclusive(True)

        self.raw_button = QPushButton("Raw")
        self.raw_button.setCheckable(True)
        self.raw_button.setChecked(True)

        self.filter_button = QPushButton("Filter")
        self.filter_button.setCheckable(True)

        self.rms_button = QPushButton("RMS")
        self.rms_button.setCheckable(True)

        self.envelope_button = QPushButton("Envelope")
        self.envelope_button.setCheckable(True)

        for btn in [self.raw_button, self.rms_button, self.envelope_button, self.filter_button]:
            btn.setSizePolicy(QSizePolicy.Preferred , QSizePolicy.Fixed)
            btn.setMinimumWidth(160)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 12px;
                    padding: 6px;
                    background-color: #2c2c2c;
                    color: white;
                    border: 1px solid #444;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
                QPushButton:checked {
                    background-color: #2196F3;
                }
            """)
            self.mode_button_group.addButton(btn)
            control_layout.addWidget(btn)

        # === Export button ===
        self.export_button = QPushButton("Export")
        
        self.export_button.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-size: 12px;
            padding: 6px ;
            border-radius: 4px;
            border: none ;                             
        }
        QPushButton:hover {
            background-color: #555;
        }
        """)
        self.export_button.clicked.connect(self.view_model.export_results)
        control_layout.addWidget(self.export_button)


        # === Clear plot button ===
        self.clear_button = QPushButton("Clear Recording")
        self.clear_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.clear_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
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

        main_layout.addLayout(horizontal_layout)
    
    def toggle_toolbar_visible(self, visible):
        """
        Toggle the visibility of the matplotlib toolbar.

        Parameters:
        - visible (bool): True to show, False to hide.
        """
        self.toolbar.setVisible(visible)

    def clear_plot(self):
        """
        Clear the plot area and redraw an empty chart.
        """
        self.ax.clear()
        # self.ax.plot([0, 1], [0, 0] ,color='white', linewidth=1)
        self.ax.set_facecolor("black")
        self.ax.set_title("EMG Recording", color='white')
        self.ax.set_xlabel("Time (s)", color='white')
        self.ax.set_ylabel("EMG Signal", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(True, color='white', linestyle='-', linewidth=0.1)
        # self.ax.set_xlim(left=0 , right= 1)
        # self.ax.margins(x=0)
        self.canvas.draw()

    def update_data(self, time_axis, data):
        """
        Update the plot with new recorded signal data.

        Parameters:
        - time_axis (np.ndarray): 1D array of time values.
        - data (np.ndarray): 1D array of signal values.
        """
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
        if len(time_axis) > 1 and self.time_axis[-1] > 0:
            self.ax.set_xlim(left=0, right=self.time_axis[-1])
        else:
            self.ax.set_xlim(left=0, right=1)
        self.ax.margins(x=0)

        self.canvas.draw()
        self.canvas.flush_events()
