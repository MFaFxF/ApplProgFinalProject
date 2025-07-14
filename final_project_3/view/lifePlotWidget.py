from vispy import app, scene
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QButtonGroup, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, QSize
import numpy as np

class LivePlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Plot")

        # self.setGeometry(100, 100, 800, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 400))
        layout.addWidget(self.canvas.native)

        grid = self.canvas.central_widget.add_grid(margin=0)
        grid.spacing = 0
        grid.border_color = 'white'

        # Title
        title = scene.Label("Live View", color='white')
        title.height_max = 40
        grid.add_widget(title, row=0, col=0, col_span=2)

        # Y Axis (left)
        yaxis = scene.AxisWidget(
            orientation='left',
            axis_label='Y Axis',
            axis_font_size=12,
            axis_label_margin=50,
            tick_label_margin=5,
        )

        yaxis.width_max = 80
        yaxis.border_color = 'white'
        grid.add_widget(yaxis, row=1, col=0)

        # View (main plot)
        self.view = grid.add_view(row=1, col=1)
        self.view.camera = 'panzoom'
        self.view.border_color = 'white'
        yaxis.link_view(self.view)

        scene.visuals.GridLines(parent=self.view.scene)

        # Line plot
        self.line = scene.Line(np.array([[0, 0]]), parent=self.view.scene)
        self.view.camera.set_range(x=(1, 10), y=(-50000, 50000))

        # Buttons (right column)
        button_layout = QVBoxLayout()

        # Start/Stop Button
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.setFixedSize(100, 100)
        self.start_stop_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        self.start_stop_button.clicked.connect(self.update_button_style_start_stop)
        button_layout.addWidget(self.start_stop_button)

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
                border-radius: 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
            }
            """
        )
        button_layout.addWidget(self.channel_selector)

        # --- Mode Buttons (Raw / Filter / RMS) ---
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

        for btn in [self.raw_button, self.filter_button, self.rms_button, self.envelope_button]:
            btn.setFixedSize(100, 40)
            btn.setStyleSheet(
                """
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
                """
            )
            self.mode_button_group.addButton(btn)

        # Wrap mode buttons in a frame for white border
        mode_button_frame = QWidget()
        mode_button_frame.setStyleSheet(
            """
            QWidget {
                border: 2px solid white;
                border-radius: 4px;
            }
            """
        )
        mode_layout = QVBoxLayout()
        # mode_layout.setSpacing(1)
        # mode_layout.setContentsMargins(6, 6, 6, 6)
        mode_layout.addWidget(self.raw_button)
        mode_layout.addWidget(self.filter_button)
        mode_layout.addWidget(self.rms_button)
        mode_layout.addWidget(self.envelope_button)
        mode_layout.setAlignment(Qt.AlignTop)
        mode_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        mode_button_frame.setLayout(mode_layout)
        mode_button_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout.addWidget(mode_button_frame)

        layout.addLayout(button_layout)

    def update_data(self, time_points, data):
        line_data = np.column_stack((time_points, data))
        self.line.set_data(line_data)
        self.canvas.update()

    def update_button_style_start_stop(self):
        if self.start_stop_button.isChecked():
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setStyleSheet("background-color: #f44336; color: white;")
        else:
            self.start_stop_button.setText("Start")
            self.start_stop_button.setStyleSheet("background-color: #4CAF50; color: white;")
