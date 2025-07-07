# TCP Communication Guide

## What is TCP?
TCP (Transmission Control Protocol) is a reliable, connection-oriented protocol that ensures data is delivered correctly and in order between applications running on different devices. Think of it like a phone call - you need to establish a connection first, then you can talk, and finally, you hang up.

## TCP vs UDP
- TCP: Reliable, ordered delivery (like a phone call)
- UDP: Fast but unreliable (like sending a letter)

## TCP Connection Lifecycle
1. **Connection Establishment** (Three-way handshake)
   - Client sends SYN (Synchronize)
   - Server responds with SYN-ACK (Synchronize-Acknowledge)
   - Client sends ACK (Acknowledge)

2. **Data Transfer**
   - Data is sent in packets
   - Each packet is acknowledged
   - If a packet is lost, it's retransmitted

3. **Connection Termination**
   - Either side can initiate closing
   - Four-way handshake to close cleanly

## Python TCP Example

### Server Example
```python
import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print(f"Server listening on {server_address}")

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    
    try:
        print(f"Connection from {client_address}")
        
        # Receive data
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            
            # Send response
            response = "Data received!"
            client_socket.sendall(response.encode())
            
    finally:
        # Clean up the connection
        client_socket.close()
```

### Client Example
```python
import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

try:
    # Send data
    message = "Hello, Server!"
    client_socket.sendall(message.encode())
    
    # Receive response
    response = client_socket.recv(1024)
    print(f"Received: {response.decode()}")
    
finally:
    client_socket.close()
```

## TCP in Your Project

### Data Format
For your signal visualization project, the TCP data should be formatted as follows:
```
[channel1_value],[channel2_value],...,[channel32_value]\n
```

Example:
```
0.5,0.3,0.7,...,0.2\n
```

### Connection Details
- Server IP: (Will be provided during testing)
- Port: (Will be provided during testing)
- Buffer size: 1024 bytes
- Encoding: UTF-8

### Error Handling
Always implement proper error handling for:
1. Connection failures
2. Data parsing errors
3. Connection timeouts
4. Buffer overflows

Example error handling:
```python
try:
    # TCP operations here
    client_socket.connect(server_address)
except ConnectionRefusedError:
    print("Connection refused. Is the server running?")
except TimeoutError:
    print("Connection timed out")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()
```

## Testing Your TCP Connection
1. Start the server first
2. Run the client
3. Monitor the connection using tools like:
   - Wireshark
   - netstat
   - TCPView (Windows)

## Common Issues and Solutions
1. **Connection Refused**
   - Check if server is running
   - Verify port number
   - Check firewall settings

2. **Data Not Received**
   - Check buffer size
   - Verify data format
   - Ensure proper encoding/decoding

3. **Connection Drops**
   - Implement reconnection logic
   - Add heartbeat mechanism
   - Check network stability

## Best Practices
1. Always close connections properly
2. Use context managers (`with` statement) when possible
3. Implement proper error handling
4. Use appropriate buffer sizes
5. Consider implementing a heartbeat mechanism
6. Log important events and errors

## Additional Resources
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [TCP/IP Protocol Suite](https://en.wikipedia.org/wiki/TCP/IP_protocol_suite)
- [Network Programming in Python](https://realpython.com/python-sockets/)

## Example: Continuous Data Receiver
Here's an example of a TCP client that handles chunked data reception, which is more similar to what you'll need for the signal visualization project (Its copied from one of my project so you may need to do some adjustments):

```python
import socket
import time
import numpy as np

class SignalReceiver:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.CHANNELS = 408
        self.SAMPLES_PER_CHANNEL = 32
        self.TOTAL_VALUES = self.CHANNELS * self.SAMPLES_PER_CHANNEL

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def receive_data(self):
        if not self.connected:
            print("Not connected to server")
            return None

        try:
            # Receive data (adjust buffer size for chunk size)
            # Each value is a float (4 bytes)
            buffer_size = self.TOTAL_VALUES * 4
            data = self.socket.recv(buffer_size)
            
            if not data:
                print("Connection closed by server")
                self.connected = False
                return None
            
            # Decode and parse the received data
            # Format: ch1_sample1,ch1_sample2,...,ch32_sample18
            decoded_data = data.decode('utf-8').strip()
            values = decoded_data.split(',')
            
            if len(values) != self.TOTAL_VALUES:
                print(f"Invalid data size. Expected {self.TOTAL_VALUES} values, got {len(values)}")
                return None
            
            # Convert values to float and reshape into channels × samples
            data_values = [float(x) for x in values]
            channel_data = np.array(data_values).reshape(self.CHANNELS, self.SAMPLES_PER_CHANNEL)
            
            return {
                'data': channel_data
            }
            
        except Exception as e:
            print(f"Error receiving data: {e}")
            self.connected = False
            return None

    def close(self):
        if self.socket:
            self.socket.close()
            self.connected = False
            print("Connection closed")

# Example usage:
if __name__ == "__main__":
    receiver = SignalReceiver()
    
    if receiver.connect():
        try:
            while receiver.connected:
                data = receiver.receive_data()
                if data:
                    print(f"\nReceived data chunk:")
                    print(f"Shape of data: {data['data'].shape}")
                    print(f"Channel 0 first 3 samples: {data['data'][0, :3]}")
                    print(f"Channel 31 last 3 samples: {data['data'][31, -3:]}")
                time.sleep(0.1)  # Small delay to prevent CPU overuse
        except KeyboardInterrupt:
            print("\nStopping receiver...")
        finally:
            receiver.close()
```

This example shows:
1. Handling of chunked data (32 channels × 18 samples)
2. Proper buffer sizing for the data chunks
3. Data reshaping into a channel × sample matrix
4. Basic data validation

Key features:
- Calculates correct buffer size based on data structure
- Reshapes received data into a 32×18 matrix
- Validates received data size
- Uses numpy for efficient data handling

To use this in your project:
1. Create an instance of `SignalReceiver`
2. Connect to the server
3. Start receiving data in a loop
4. Process the received data in your ViewModel layer
5. Update your visualization with the channel × sample matrix

Note: The actual data values will be different in your implementation. This example uses placeholder values for demonstration purposes. 
