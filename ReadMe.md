# Applied Programming - EMG Data Viewer

A PyQt application for visualization, processing and recording of a simulated multi-channel EMG Signal

---

## Getting Started

Run the application from the root folder:

```bash
python main.py
```

This will launch the EMG Viewer window.

---

## 🖥️ Usage

### 1. Connect to Signal Source

- Click the **“Connect”** button to start both the TCP server and client.
- The application begins generating and receiving EMG data in the background.
- To stop the stream, click **“Disconnect”**.

---

### 2. Start/Stop Live Plotting

Click the **“Start”** button to begin plotting live EMG data.
While active:
  - The signal of the current channel is shown in the upper window, with the selected transformation
  - The full 32-channel data is added to the recording, seen below.
Click **“Stop”** to pause live plotting and recording.
The signal continues in the background.

---

### 3. Live View Controls

- **Channel Selector**: Choose one of 32 channels to view.  
  > Only one channel is shown, but all channels are being recorded.
  
- **Signal Processing Modes**:

  | Mode      | Description                                |
  |-----------|--------------------------------------------|
  | `Raw`     | Unprocessed signal                         |
  | `RMS`     | Root Mean Square                           |
  | `Filter`  | Low-pass Butterworth filter                |
  | `Envelope`| Signal envelope using Hilbert function     |

---

### 4. Recording Controls

- **Channel Selector**: Selects which recorded channel to display.
- **Signal Processing Modes**: Processing modes, same as in the live view.
- **Export Recording**: Save the processed recording for the selected channel as a `.csv` file with columns for `Time` and `Value`
- **Clear Recording**: Clears the current recording, starts a new one.

---

## TCP Connection Specifications

The application uses a custom TCP-based client-server architecture to simulate a real-time EMG data stream.

### Server (class EMGTCPServer)
- Host: `localhost`
- Port: `12345`
- Behavior:
  - Loads EMG data from a `recording.pkl` file
  - Sends data packages to connected clients
  - Automatically loops the signal when it reaches the end

### Client (class EMGTCPClient)
- Connects to the server at `localhost:12345`.
- Receives data to simulate real EMG device
- Decodes each data packet into a NumPy array of shape `(32, 18)` — 32 channels, 18 samples per packet.

---

###  Packet Format
Each packet contains:

- Data Shape: (32 channels × 18 samples)
- Data Type: float32
- Total Size: 32 * 18 * 4 = 2304 bytes per packet
- Transmission Rate: One packet every **9 ms** (based on `sleep_time = 18 / 2000`)

---

### Timing and Flow

- The server uses a timer-based loop to maintain precise timing between transmissions.
- The client expects exactly 2304 bytes per read and reshapes it into a `(32, 18)` matrix.
- Both server and client continue streaming until manually stopped.
- When the end of the data is reached, it is restarted from the beginning.

##  MVVM Architecture Implementation

The application closely follows a **Model-View-ViewModel (MVVM)** architecture to separate data handling, business logic, and user interface logic.

---

### Model: `SignalProcessor`

- Located in `signal_processor.py`
- Manages core data flow:
  - Starts the TCP server and client
  - Receives live data from the EMG stream
  - Buffers and records incoming signals
- Exposes:
  - `live_signal`: current buffer (rolling window)
  - `recorded_signal`: full accumulation of all recorded data

---

### ViewModel: `MainViewModel`

- Located in `main_view_model.py`
- Acts as the central state and logic controller:
  - Connects to `SignalProcessor`
  - Manages current channel and processing modes (raw, RMS, filter, envelope)
  - Applies real-time and historical signal processing
  - Emits Qt signals to update the UI:
    - `live_data_updated`
    - `recorded_data_updated`
- Handles:
  - Timer-driven updates
  - Channel switching
  - Recording state
  - CSV export of processed data

---

### Views

#### `MainView`
- Root layout controller (`main_view.py`)
- Composes all widgets:
  - `ConnectionWidget`
  - `LivePlotWidget`
  - `RecordingPlotWidget`
- Connects UI events (button presses, toggles) to ViewModel methods

#### `LivePlotWidget`
- Displays real-time EMG signals using VisPy
- Allows selection of channel and processing mode

#### `RecordingPlotWidget`
- Displays accumulated signal using Matplotlib
- Offers export and clear functionality

#### `ConnectionWidget`
- UI widget to connect/disconnect the TCP stream
- Visually reflects connection status

---

### 🔄 Data Flow Summary

```
SignalProcessor  <--->  MainViewModel  <--->  Views (LivePlot, Recording, etc)
      ▲                                      ▲
      │                                      │
   TCP I/O                         User interaction (UI)
```

- The **Model** handles raw data and network.
- The **ViewModel** transforms that data and drives UI behavior.
- The **Views** are presentation-only and signal user intent back to the ViewModel.

