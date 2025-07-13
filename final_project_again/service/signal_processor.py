import threading
import time
from service.tcp_client import EMGTCPClient
from service.tcp_server import EMGTCPServer
import numpy as np
import matplotlib.pyplot as plt

class LiveSignalBuffer:
    def __init__(self, channels=32, window_samples=2048):
        self.buffer = np.zeros((channels, window_samples), dtype=np.float32)

    def update(self, new_data):
        _, num_new_samples = new_data.shape  # (32, 18)
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

        self.new_data = None

        self.live_window = np.zeros((self.num_channels, self.live_window_size), dtype=np.float32)
        self.full_window = np.zeros((self.num_channels, self.live_window_size), dtype=np.float32)

        self.running = False
        self.start_server()

    def start_server(self):
        self.server_thread = threading.Thread(target=self.tcp_server.start, daemon=True)
        self.server_thread.start()

    def run_client(self):
        self.tcp_client.connect()
        live_signal_buffer = LiveSignalBuffer()
        # print("Client connected to server, waiting for data...")
        try:
            while self.tcp_client.connected:
                self.new_data = self.tcp_client.receive_data()
                if self.new_data is not None:
                    self.live_window = live_signal_buffer.update(self.new_data)
                    if self.full_window is None:
                        self.full_window = self.live_window
                    else:
                        self.full_window = np.hstack((self.full_window, self.new_data))

        except KeyboardInterrupt:
            print("\nStopping client...")
        finally:
            self.tcp_client.close()

    def start_signal(self):
        self.running = True
        self.client_thread = threading.Thread(target=self.run_client, daemon=True)
        self.client_thread.start()

    def stop_client(self):
        self.running = False
        self.tcp_client.close()

    def stop_server(self):
        self.tcp_server.stop()

if __name__ == '__main__':
    signal_processor = SignalProcessor()
    signal_processor.start_signal()

    plt.ion()
    fig, ax = plt.subplots()

    while True:
        time.sleep(0.1)  # Faster update for smoother plot
        if signal_processor.live_window is not None:
            ax.clear()

            num_samples = signal_processor.live_window.shape[1]
            x_axis = np.linspace(0, num_samples, num_samples)

            # Plot Channel 1 (index 0)
            ax.plot(x_axis, signal_processor.live_window[2, :], label='Channel 1')
            ax.set_xlabel('Samples')
            ax.set_ylabel('Amplitude')
            ax.set_title('Live Circular Buffer (Rolling Window)')
            ax.legend()

            fig.canvas.draw()
            fig.canvas.flush_events()
