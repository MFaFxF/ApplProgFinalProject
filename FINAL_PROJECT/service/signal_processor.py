from service.tcp_client import EMGTCPClient
from service.tcp_server import EMGTCPServer
import numpy as np
import threading
import time


class LiveSignalBuffer:
    """
    Rolling buffer for latest live signal data
    for visualization or further processing.
    Stores all 32 channels. Fixed length.
    """

    def __init__(self, channels=32, window_samples=20000):
        """
        Initialize the live signal buffer.

        Parameters:
        - channels (int): Number of channels (e.g., 32 EMG electrodes).
        - window_samples (int): Number of samples to retain in the buffer.
          Typically calculated as (sampling_rate * window_size).
        """
        self.buffer = np.zeros((channels, window_samples), dtype=np.float32)
        self.t0 = time.time()

    def update(self, new_data):
        """
        Update the buffer with new incoming data.

        Parameters:
        - new_data (np.ndarray): New signal data of shape (channels, samples).

        Returns:
        - np.ndarray: Buffer of same length with added new_data.
        """
        _, num_new_samples = new_data.shape
        self.buffer = np.roll(self.buffer, -num_new_samples, axis=1)
        self.buffer[:, -num_new_samples:] = new_data
        return self.buffer


class SignalProcessor:
    """
    Manages live signal processing via TCP client-server communication.

    This class:
    - Starts a TCP server to simulate live EMG data acquisition.
    - Connects a client to receive data.
    - Buffers live signal data for visualization.
    - Saves a recording of the live signal.
    - Exposes them for visualization or further processing.
    """

    def __init__(self):
        """
        Initialize the signal processor with TCP client and server.

        Set up:
        - TCP server and client
        - Sampling configuration
        - Live signal buffer and output
        - Signal recording
        """
        # Initialize TCP server and client
        self.tcp_server = EMGTCPServer()
        self.tcp_client = EMGTCPClient()


        # Configure sampling parameters
        self.sampling_rate = self.tcp_server.sampling_rate
        self.sleep_time = self.tcp_server.sleep_time
        self.live_window_time = 5  # seconds
        self.live_window_size = self.live_window_time * self.tcp_server.sampling_rate # 5 seconds of data
        self.num_channels = 32

        # Create buffer for live signal data
        self.live_signal_buffer = LiveSignalBuffer(
            channels=self.num_channels, 
            window_samples=self.live_window_size
        )

        # Initialize live signal and recording storage
        self.live_signal = np.zeros((self.num_channels, self.live_window_size), dtype=np.float32)
        self.recorded_signal = self.live_signal.copy()

        # Recording state
        self.is_recording = False

    def start_server(self):
        """
        Start the TCP server thread.
        """
        self.server_thread = threading.Thread(target=self.tcp_server.start, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Give server time to start

    def start_client(self):
        """
        Start the TCP client thread
        """
        self.client_thread = threading.Thread(target=self.run_client, daemon=True)
        self.client_thread.start()

    def run_client(self):
        """
        Connect the client and continuously receive data.
        Update live signal and recording.
        """
        self.tcp_client.connect()

        while self.tcp_client.connected:
            # Receive the latest data from the server
            new_data = self.tcp_client.receive_data()

            # If recording is active, update the live signal buffer and recorded signal
            if not self.is_recording:
                continue
            if new_data is not None:
                self.live_signal = self.live_signal_buffer.update(new_data)
                self.recorded_signal = np.concatenate((self.recorded_signal, new_data), axis=1)
            else:
                print("No new data received, waiting...")

    def generate_signal(self):
        """
        Main entry point for signal generation.
        Start TCP server and client to begin live data streaming.
        """
        self.start_server()
        self.start_client()
        print("Signal generation started.")

    def stop_signal(self):
        """
        Stop data acquisition by closing the client and server.
        """
        self.tcp_client.close()
        self.tcp_server.stop()
        print("Signal generation stopped.")

    def clear_recording(self):
        """
        Reset the recorded signal to one sample of zeroes.
        """
        self.recorded_signal = np.zeros_like(self.live_signal[:, -1:])
