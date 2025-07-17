import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QSizePolicy, QButtonGroup , QMessageBox ,QFileDialog
)
import csv
from PyQt5.QtCore import Qt



class RecordingPlotWidget(QWidget):
    def __init__(self , view_model):
        super().__init__()
        self.view_model = view_model
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        self.channel = 0

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # === Plot Area (Canvas + Toolbar) ===
        plot_container = QWidget()
        plot_layout = QVBoxLayout()
        plot_layout.setContentsMargins(5, 5, 5, 5)
        plot_container.setLayout(plot_layout)
        # plot_container.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Expanding)


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
        control_layout.setContentsMargins(10,10,10,10)
        
        control_frame = QWidget()
        control_frame.setLayout(control_layout)
        control_frame.setStyleSheet("background-color: #1e1e1e; border: 1px solid #333;")
        horizontal_layout.addWidget(control_frame)

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

        self.export_button = QPushButton("Export")
        self.export_button.setCheckable(True)

        for btn in [self.record_raw_button, self.record_rms_button, self.record_envelope_button, self.record_filter_button]:
            btn.setMaximumSize(100, 40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #2c2c2c;
                    color: white;
                    border: 1px solid #555;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
                QPushButton:checked {
                    background-color: #2196F3;
                }
            """)
            self.record_mode_group.addButton(btn)
            control_layout.addWidget(btn)


        self.export_button.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-size: 14px;
            padding: 6px 12px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #555;
        }
        """)
        self.export_button.clicked.connect(self.view_model.export_results)
        control_layout.addWidget(self.export_button)
        control_layout.setSpacing(10)
        


    def update_data(self, time_axis, data):
        """Update the plot with new data"""
        self.time_axis = time_axis
        self.data = data

        self.ax.clear()
        self.ax.plot(time_axis, data, color='lime', linewidth=1)

        self.ax.set_facecolor("black")
        self.ax.set_title("EMG Recording", color='white')
        self.ax.set_xlabel("Time (s)", color='white')
        self.ax.set_ylabel("EMG Signal", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(True, color='white', linestyle='--', linewidth=0.5)
        self.ax.set_xlim(time_axis[0], time_axis[-1])

        self.figure.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()

"""
    def export_results(self):
        if hasattr(self ,  'recorded_data') or self.recorded_data is None :
            QMessageBox.warning(self , "Export Failed" , "No data exported")
            return


        file_path , _ = QFileDialog.getSaveFileName(
            self , "Export data " , "", "CSV Files (*.csv);;Text Files (*.txt)"
        ) 

        if not file_path:
            return # User cancel it 
            
        try:
            with open(file_path , "w" , newline='') as f:
                writer =  csv(f)
                writer.writerow(["Time" , "Value"]) # Headers 
                for t , v in zip(self.recorded_data_time_points , self.processed_recorded_data):
                    writer.writerow([t,v])
            QMessageBox.information("Data Uploaded Succefully" , f"data uploaded to : {file_path}")
        except Exception as e:
            QMessageBox.critical(self , "export failed ", str(e))
            """