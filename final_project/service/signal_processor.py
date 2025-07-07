import time
import threading
import numpy as np
from final_project.service.tcp_client import EMGTCPClient
from final_project.service.tcp_server import EMGTCPServer


class SignalProcessor:
    def __init__(self):
        self.tcp_server = EMGTCPServer()
        self.tcp_client = EMGTCPClient()
        self.data=np.ndarray

    def start_server(self):
        server_thread = threading.Thread(target=self.tcp_server.start, daemon=True)
        # Create and start the server
        try:
            server_thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server_thread.start()

    def run_client(self):
        self.tcp_client.connect()
        try:
            while self.tcp_client.connected:
                self.data = self.tcp_client.receive_data()
                if self.data is not None:
                    pass
                    # Print the received data
                    #self.tcp_client.print_data(data)
                    #print(self.data)

        except KeyboardInterrupt:
            print("\nStopping client...")
        finally:
            self.tcp_client.close()

    def get_signal(self):
        self.start_server()
        # Give the server a moment to start
        time.sleep(1)
        client_thread = threading.Thread(target=self.run_client, daemon=True)
        client_thread.start()


if __name__ == "__main__":
    signal_processor = SignalProcessor()
    # signal_processor.get_signal()
