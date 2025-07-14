import threading
import time
from service.tcp_client import EMGTCPClient
from service.tcp_server import EMGTCPServer
# from tcp_client import EMGTCPClient
# from tcp_server import EMGTCPServer
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

        self.live_window_size = 2048 #TODO set size to equivalent of 10s
        self.num_channels = 32

        self.live_signal_buffer = LiveSignalBuffer()
        self.live_window = np.zeros((self.num_channels, self.live_window_size), dtype=np.float32) # main output of this class

    def start_server(self):
        self.server_thread = threading.Thread(target=self.tcp_server.start, daemon=True)
        self.server_thread.start()
        time.sleep(1)

    def start_client(self):
        self.client_thread = threading.Thread(target=self.run_client, daemon=True)
        self.client_thread.start()

    def run_client(self):
        self.tcp_client.connect()
        while self.tcp_client.connected:
            new_data = self.tcp_client.receive_data()
            if new_data is not None:
                self.live_window = self.live_signal_buffer.update(new_data)
    
    def generate_signal(self):
        self.start_server()
        self.start_client()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # Initialize processor
    processor = SignalProcessor()
    processor.generate_signal()  # starts server and client

    # Setup interactive plotting
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(np.zeros(processor.live_window_size))
    ax.set_ylim(-1, 1)  # adjust depending on expected signal range
    ax.set_title("Live EMG Signal - Channel 0")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")

    try:
        while True:
            signal = processor.live_window[0, :]  # channel 0
            line.set_ydata(signal)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.05)  # match your QTimer update rate (50ms)
    except KeyboardInterrupt:
        print("Stopped.")