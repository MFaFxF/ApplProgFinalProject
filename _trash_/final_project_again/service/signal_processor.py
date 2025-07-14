
import threading
import time
from service.tcp_client import EMGTCPClient
from service.tcp_server import EMGTCPServer
import numpy as np

class LiveSignalBuffer:
    def __init__(self, channels=32, window_samples=2048):
        self.buffer = np.zeros((channels, window_samples), dtype=np.float32)

    def update(self, new_data):
        _, num_new_samples = new_data.shape
        self.buffer = np.roll(self.buffer, -num_new_samples, axis=1)
        self.buffer[:, -num_new_samples:] = new_data
        return self.buffer

class SignalProcessor:
    def __init__(self):
        self.tcp_server = EMGTCPServer()
        self.tcp_client = EMGTCPClient()

        self.server_thread = None
        self.client_thread = None

        self.live_window_size = 2048
        self.num_channels = 32

        self.live_window = np.zeros((self.num_channels, self.live_window_size), dtype=np.float32)
        self.running = False

        self.start()

    def start(self):
        self.running = True
        self.start_server()
        time.sleep(1)
        self.start_client()

    def start_server(self):
        self.server_thread = threading.Thread(target=self.tcp_server.start, daemon=True)
        self.server_thread.start()

    def start_client(self):
        self.client_thread = threading.Thread(target=self.run_client, daemon=True)
        self.client_thread.start()

    def run_client(self):
        self.tcp_client.connect()
        live_signal_buffer = LiveSignalBuffer()

        while self.running and self.tcp_client.connected:
            new_data = self.tcp_client.receive_data()
            if new_data is not None:
                self.live_window = live_signal_buffer.update(new_data)

    def stop(self):
        self.running = False
        self.tcp_client.close()
        self.tcp_server.stop()