from vispy import app, scene
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, 
    QButtonGroup, QFrame, QSizePolicy ,  QSpacerItem
)
from PyQt5.QtCore import Qt
import numpy as np


class LivePlotWidget(QWidget):
    """
    Widget for displaying and interacting with live EMG signal data.

    This widget includes:
    - A VisPy canvas for real-time plotting
    - A start/stop toggle button
    - A channel selector (1-32)
    - Signal mode buttons: Raw, Filter, RMS, Envelope
    """

    def __init__(self):
        """
        Initialize the LivePlotWidget.

        Sets up:
        - VisPy canvas for plotting, incl. y-axis and title on a grid layout
        - Toolbar with controls for starting/stopping, channel selection, and signal modes
        """
        super().__init__()
        self.setWindowTitle("Live Plot")
        self.channel = 0  # Default channel

        # === Main layout ===
        layout = QHBoxLayout()
        self.setLayout(layout)

        # === VisPy canvas ===
        self.canvas = scene.SceneCanvas(keys='interactive')
        layout.addWidget(self.canvas.native, stretch=6)
        
        # === Grid layout on canvas ===
        grid = self.canvas.central_widget.add_grid(margin=0)
        grid.spacing = 10
        grid.border_color = 'white'
        
        # === Plot title ===
        title = scene.Label("Live View", color='white')
        title.height_max = 40
        grid.add_widget(title, row=0, col=0, col_span=2)

        # === Y Axis ===
        yaxis = scene.AxisWidget(
            orientation='left',
            axis_label='EMG Signal',
            axis_font_size=10,
            axis_label_margin=50,
            tick_label_margin=5,
        )
        yaxis.width_max = 80
        yaxis.border_color = 'white'
        grid.add_widget(yaxis, row=1, col=0)

        # === Main plot view ===
        self.view = grid.add_view(row=1, col=1)
        self.view.camera = 'panzoom'
        self.view.camera.react_padding = 0
        self.view.border_color = 'white'
        self.view.padding = 0 
        
      


        yaxis.link_view(self.view)  # Sync y-axis with plot view

        # === Grid lines ===
        scene.visuals.GridLines(parent=self.view.scene, color='grey')

        # === Line plot ===
        self.line = scene.Line(np.array([[0, 0]]), parent=self.view.scene , width=2)
        self.view.camera.set_range(x=(0, 10), y=(-50000, 50000) ) #TODO dynamic range

        # === Toolbar layout ===
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)

        # === Start/Stop Button ===
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.setChecked(False)
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
            }
                QPushButton[state="stopped"] { background-color: #4CAF50; }
                              
                QPushButton[state="stopped"]:hover { background-color: #45a049;}
                              
                QPushButton[state="running"]{ background-color : #f44336;}        
                                    
                QPushButton[state="running"]:hover {background-color: #d73833;}
                    
        """)
        self.start_stop_button.setMaximumSize(100 , 100)
        self.start_stop_button.clicked.connect(self.change_button_style)

        # === Channel Selector (1–32) ===
        self.channel_selector = QSpinBox()
        self.channel_selector.setRange(1, 32)
        self.channel_selector.setPrefix("Ch ")
        self.channel_selector.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.channel_selector.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                padding: 4px;
                color: white;
                border-radius: 4px;
                background-color: #333;
                background: "black"
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
            }
        """)

        # === Signal Mode Buttons ===
        self.mode_button_group = QButtonGroup(self)
        self.mode_button_group.setExclusive(True)  # Only one active at a time

        self.raw_button = QPushButton("Raw")
        self.raw_button.setCheckable(True)
        self.raw_button.setChecked(True)

        self.filter_button = QPushButton("Filter")
        self.filter_button.setCheckable(True)

        self.rms_button = QPushButton("RMS")
        self.rms_button.setCheckable(True)

        self.envelope_button = QPushButton("Envelope")
        self.envelope_button.setCheckable(True)

        for btn in [self.raw_button, self.filter_button, self.rms_button, self.envelope_button]:
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c2c2c;
                    color: white;
                    font-size: 12px;
                    border: 1px solid #444;
                    border-radius: 4px;
                    padding: 6px;
                    margin : 3px ;          
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
                QPushButton:checked {
                    background-color: #007acc;
                    border: 1px solid #005f99;
                }                                        
            """)
            self.mode_button_group.addButton(btn)

        # === Wrap toolbar with white border ===
        toolbar_frame = QWidget()
        toolbar_frame.setStyleSheet("""
            QWidget {
                border: 1.5px solid white;
                border-radius: 4px;
            }
        """)
        toolbar_layout = QVBoxLayout()
        toolbar_layout.setSpacing(10)
        toolbar_layout.setContentsMargins(10, 10, 10, 10)

        toolbar_layout.addWidget(self.start_stop_button)
        toolbar_layout.addWidget(self.channel_selector)
        toolbar_layout.addWidget(self.raw_button)
        toolbar_layout.addWidget(self.filter_button)
        toolbar_layout.addWidget(self.rms_button)
        toolbar_layout.addWidget(self.envelope_button)
        toolbar_layout.setAlignment(Qt.AlignTop)
        #toolbar_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        toolbar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        toolbar_frame.setLayout(toolbar_layout)
        toolbar_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)


        button_layout.setSpacing(10)
        button_layout.addWidget(toolbar_frame)

        # === Add toolbar to main layout ===
        layout.addLayout(button_layout)

    def update_data(self, time_points, data):
        """
        Update the live plot with new signal data.

        Parameters:
        - time_points (np.ndarray): 1D array of time stamps.
        - data (np.ndarray): 1D array of signal values.
        """
        x_start = self.view.camera.rect.left
        x_end = self.view.camera.rect.right


        self.live_data_time_points = time_points
        self.live_signal = data

        padded_time = np.concatenate([[x_start] , time_points , [x_end]])
        padded_data = np.concatenate([[data[0]], data, [data[-1]]])
        #line_data = np.column_stack((time_points, data))  # Combine into (x, y)
        line_data = np.column_stack((padded_time, padded_data))
        self.line.set_data(line_data)
        self.canvas.native.update()

    def change_button_style(self):
        """
        Toggle the start/stop button text and color based on its state.
        """
        if self.start_stop_button.isChecked():
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setProperty("state","running")
        else:
            self.start_stop_button.setText("Start")
            self.start_stop_button.setProperty("state","stopped")

        self.start_stop_button.style().unpolish(self.start_stop_button)
        self.start_stop_button.style().polish(self.start_stop_button)






        
