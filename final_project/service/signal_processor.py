import time
import threading
from tcp_client import EMGTCPClient
from tcp_server import EMGTCPServer


class SignalProcessor:
    """"""
    def __init__(self):
        self.tcp_server = EMGTCPServer()
        self.tcp_client = EMGTCPClient()

    def start_server(self):
        # Create and start the server
        try:
            self.tcp_server.start()
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.tcp_server.stop()

    def start_client(self):
        # Create and connect the client
        self.tcp_client.connect()

        try:
            # Receive and process data
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
        self.start_client()

    
if __name__ == "__main__":
    signal_processor = SignalProcessor()
    signal_processor.get_signal()