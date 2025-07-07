import time
import threading
from tcp_client import EMGTCPClient
from tcp_server import EMGTCPServer


class SignalProcessor:
    def __init__(self):
        self.tcp_server = EMGTCPServer()
        self.tcp_client = EMGTCPClient()

    def start_server(self):
        server_thread = threading.Thread(target=self.tcp_server.start, daemon=True)
        server_thread.start()
        # Create and start the server
        try:
            server_thread.start()
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server_thread.start()

    def start_client(self):
        self.tcp_client.connect()
        try:
            while self.tcp_client.connected:
                data = self.tcp_client.receive_data()
                if data is not None:
                    # Print the received data
                    self.tcp_client.print_data(data)

        except KeyboardInterrupt:
            print("\nStopping client...")
        finally:
            self.tcp_client.close()

    def get_signal(self):
        self.start_server()
        # Give the server a moment to start
        time.sleep(1)
        self.start_client()


if __name__ == "__main__":
    signal_processor = SignalProcessor()
    signal_processor.get_signal()
