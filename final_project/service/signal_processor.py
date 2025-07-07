import time
from tcp_client import EMGTCPClient
from tcp_server import EMGTCPServer

def main():
    # Create and start the TCP server
    server = EMGTCPServer()
    try:
        server.start()
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop() 

    # Create and start the TCP client
    client = EMGTCPClient()
    client.connect()

    try:
        # Receive and process data
        while client.connected:
            data = client.receive_data()
            if data is not None:
                # Print the received data
                client.print_data(data)
            
            # No need for additional sleep as we're already receiving at 1 chunk per second

    except KeyboardInterrupt:
        print("\nStopping client...")
    finally:
        client.close()
    
if __name__ == "__main__":
    main() 