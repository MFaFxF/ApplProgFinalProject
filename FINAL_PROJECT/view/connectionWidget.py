from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
)

class ConnectionWidget(QWidget):
    """
    Header widget for managing connection, includes title

    This widget includes:
    - A toggle button to start/stop the connection
    - A status label indicating connection state
    - A centered header label
    """

    # Emit state of connect button when pressed
    toggled = pyqtSignal(bool)

    def __init__(self):
        """
        Initialize the widget layout and components.

        Sets up horizontal layout with:
        - Toggle button (Connect/Disconnect)
        - Status label (Connected/Disconnected)
        - Header
        """
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

        # Left-aligned button and status
        layout.addWidget(self.toggle_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.status_label, alignment=Qt.AlignLeft)

        # Spacer between controls and header
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Centered header label
        layout.addWidget(self.header_label, alignment=Qt.AlignLeft)

        # Spacer between header and right edge
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Final layout setup
        self.setLayout(layout)

    def toggle_connection(self):
        """
        Toggle the connection state between connected and disconnected.

        This method updates the UI and emits the `toggled` signal.
        """
        self.connected = not self.connected
        self.update_button_style()
        self.update_status_style()
        self.toggled.emit(self.connected)

    def set_connection_status(self, connected: bool):
        """
        Explicitly set connection status, update appearance of connect button / status label.

        Parameters:
        - connected (bool): Whether the connection is active.
        """
        self.connected = connected
        self.update_button_style()
        self.update_status_style()

    def update_button_style(self):
        """
        Update the appearance of the toggle button, depending on connection state.
        
        Green for connect, red for disconnect.
        """
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
        """
        Update the appearance of the status label.

        Green for connected, red for disconnected.
        """
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
