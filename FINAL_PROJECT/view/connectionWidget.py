from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal

class ConnectionWidget(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.connected = False  # Initial state: disconnected

        # === Button ===
        self.toggle_button = QPushButton("Connect")
        self.toggle_button.setFixedSize(100, 40)
        self.toggle_button.clicked.connect(self.toggle_connection)
        self.update_button_style()

        # === Status Label ===
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFixedSize(120, 40)
        self.update_status_style()

        # === Header Label (Centered) ===
        self.header_label = QLabel("EMG Data Visualization")
        self.header_label.setAlignment(Qt.AlignLeft)
        self.header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
        """)

        # === Layout ===
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)

        # Left-aligned controls
        layout.addWidget(self.toggle_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.status_label, alignment=Qt.AlignLeft)

        # Spacer between header and buttons
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Centered header
        layout.addWidget(self.header_label, alignment=Qt.AlignLeft)

        # Spacer between header and right border
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))


        # Final layout setup
        self.setLayout(layout)

    def toggle_connection(self):
        self.connected = not self.connected
        self.update_button_style()
        self.update_status_style()
        self.toggled.emit(self.connected) 

    def set_connection_status(self, connected: bool):
        self.connected = connected
        self.update_button_style()
        self.update_status_style()

    def update_button_style(self):
        if self.connected:
            self.toggle_button.setText("Disconnect")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #b00020;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
        else:
            self.toggle_button.setText("Connect")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #2e7d32;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388e3c;
                }
            """)

    def update_status_style(self):
        if self.connected:
            self.status_label.setText("Status:\nConnected")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #a5d6a7;
                    color: black;
                    border-radius: 6px;
                    font-weight: bold;
                }
            """)
        else:
            self.status_label.setText("Status:\nDisconnected")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #ef9a9a;
                    color: black;
                    border-radius: 6px;
                    font-weight: bold;
                }
            """)
