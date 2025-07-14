from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QSpinBox, QHBoxLayout, QSizePolicy, QMessageBox , QButtonGroup)
from .lifePlotView import LivePlotWidget
from .recordPlotView import RecordingPlotWidget

import time

class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setWindowTitle("Applied Programming - EMG Data Viewer")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create plot widgets
        self.live_plot_widget = LivePlotWidget()
        self.live_plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.recording_widget = RecordingPlotWidget()
        self.recording_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Live view layout
        live_view_layout = QHBoxLayout()
        live_view_layout.addWidget(self.live_plot_widget)

        # Button layout
        button_layout = QVBoxLayout()
        
        # Start/Stop button
        self.btn_start_stop = QPushButton("Start")
        self.btn_start_stop.setCheckable(True)
        self.btn_start_stop.setFixedSize(100, 100)
        self.btn_start_stop.setStyleSheet("""
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
        """)
        
        # # RMS button
        # self.btn_rms = QPushButton("RMS")
        # self.btn_rms.setFixedSize(100, 40)
        # self.btn_rms.setStyleSheet("""
        #     QPushButton {
        #         font-size: 14px;
        #         padding: 8px;
        #         background-color: #2196F3;
        #         color: white;
        #         border: none;
        #         border-radius: 4px;
        #     }
        #     QPushButton:hover {
        #         background-color: #0b7dda;
        #     }
        # """)
        
        self.processing_buttons = {
            'raw': self._create_processing_button("Raw", "#607D8B" , True),
            'rms': self._create_processing_button("RMS", "#FF5722"),
            'envelope': self._create_processing_button("Envelope", "#4CAF50"),
            'filter': self._create_processing_button("Filter", "#9C27B0")
        }

        # for btn in self.processing_buttons.values():
        #     button_layout.addWidget(btn)

        # add buttons for processing data to the button layout 
        self.processing_btn_group = QButtonGroup()
        for mode ,btn in self.processing_buttons.items():
            self.processing_btn_group.addButton(btn)
            button_layout.addWidget(btn)


        # Add button start/stop  to layout
        button_layout.addWidget(self.btn_start_stop)
        # button_layout.addWidget(self.btn_rms)
        button_layout.addStretch()
        
        live_view_layout.addLayout(button_layout)

        # Recording plot layout
        recording_plot_layout = QHBoxLayout()
        recording_plot_layout.addWidget(self.recording_widget)

        # Main layout
        layout.addLayout(live_view_layout)
        layout.addLayout(recording_plot_layout)

    def _connect_signals(self):
        self.btn_start_stop.clicked.connect(self.handle_start_stop)
       # self.btn_rms.clicked.connect(self.handle_rms_calculation)
        self.view_model.live_data_updated.connect(self.live_plot_widget.update_data)
        self.view_model.full_data_updated.connect(self.recording_widget.update_data)
        self.view_model.rms_valued_updated.connect(self.show_rms_value)

        for mode, btn in self.processing_buttons.items():
            btn.clicked.connect(lambda _, m=mode : self._handle_processing_click(m))
        self.view_model.live_processing_mode_changed.connect(self.live_plot_widget.set_display_mode)
        self.view_model.live_processing_data_updated.connect(self.live_plot_widget.update_processed_data)

    def _handle_processing_click(self ,  mode):
        """handle processing click """
        self.view_model.set_processing_mode(mode)

        for m , btn in self.processing_buttons.items():
            btn.setChecked(m == mode)



    def handle_start_stop(self):
        if self.btn_start_stop.isChecked():
            self.btn_start_stop.setText("Stop")
            self.btn_start_stop.setStyleSheet("background: #f44336")
        else:
            self.btn_start_stop.setText("Start")
            self.btn_start_stop.setStyleSheet("background: #4caf50")

    def handle_rms_calculation(self):
        """Handle RMS button click"""
        rms_value = self.view_model.calculate_rms()
        self.show_rms_value(rms_value)

    def show_rms_value(self, value):
        """Display RMS value to user"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"RMS Value: {value:.4f}")
        msg.setWindowTitle("RMS Calculation")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    def _create_processing_button(self, text, color, checked=False):
            """Create a processing button with consistent styling"""
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(checked)
            btn.setFixedSize(100, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 14px;
                    padding: 8px;
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton:checked {{
                    background-color: #FF9800;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #0b7dda;
                }}
            """)
            return btn
            