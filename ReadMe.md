# EMG Data Viewer

An interactive desktop application for visualizing, processing, and recording EMG (electromyography) signal data using a live TCP data stream.

---

## 🚀 Getting Started

To run the application:

```bash
python main.py
```

This will launch the EMG Viewer window.

---

## 🖥️ Usage

### 1. Connect to Signal Source

- Click the **“Connect”** button to start both the TCP server and client.
- The application begins generating and receiving EMG data.
- To stop the stream, click **“Disconnect”**.

---

### 2. Start/Stop Live Plotting

- Click the **“Start”** button to begin plotting live EMG data.
- While active:
  - The current channel is displayed in real time.
  - The full 32-channel data is added to the **recorded buffer**.
- Click **“Stop”** to pause live plotting and recording.
  - The data stream **continues running in the background**.

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

- **Channel Selector**: Same as Live View — selects which recorded channel to display.
- **Signal Processing Modes**: Identical to the live view.
- **Export Recording**: Save the processed recording for the selected channel as a `.csv` file with columns for `Time` and `Value`

- **Clear Recording**: Clears the current buffer to prepare for a new recording session.

---

## Notes

- All 32 channels are continuously recorded during live viewing.
- Signal processing is applied per view and is non-destructive.
- Export includes only the **visible** (processed) channel.

---

## 📎 Next Sections (To be added)

- [ ] TCP Connection Specifications
- [ ] Data Format & Structure
- [ ] MVVM Architecture Overview
