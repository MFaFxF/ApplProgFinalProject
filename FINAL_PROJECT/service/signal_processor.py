import threading
import time
from service.tcp_client import EMGTCPClient
from service.tcp_server import EMGTCPServer
# from tcp_client import EMGTCPClient
# from tcp_server import EMGTCPServer
import numpy as np


class LiveSignalBuffer:
    def __init__(self, channels=32, window_samples=20000):
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

        self.sampling_rate = self.tcp_server.sampling_rate
        self.sleep_time = self.tcp_server.sleep_time
        self.live_window_size = 10 * self.tcp_server.sampling_rate
        self.num_channels = 32

        self.live_signal_buffer = LiveSignalBuffer(channels=self.num_channels, window_samples=self.live_window_size)
        self.live_signal = np.zeros((self.num_channels, self.live_window_size), dtype=np.float32) # main output of this class

        self.recorded_signal = None

        self.got_new_data = False

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
                self.got_new_data = True
                self.live_signal = self.live_signal_buffer.update(new_data)
                if self.recorded_signal is not None:
                    self.recorded_signal = np.concatenate((self.recorded_signal, new_data), axis=1)
                else:
                    self.recorded_signal = new_data
            else:
                print("No new data received, waiting...")
    
    def generate_signal(self):
        self.start_server()
        self.start_client()
        print("Signal generation started.")

    def stop_signal(self):
        self.tcp_client.close()
        self.tcp_server.stop()
        print("Signal generation stopped.")

    def clear_recording(self):
        self.recorded_signal = None

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
            signal = processor.live_signal[0, :]  # channel 0
            line.set_ydata(signal)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.05)  # match your QTimer update rate (50ms)
    except KeyboardInterrupt:
        print("Stopped.")