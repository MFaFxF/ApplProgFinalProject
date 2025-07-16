from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor
from scipy.signal import hilbert, butter, lfilter

class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)
    recorded_data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()
        self.signal_processor.generate_signal()
        self.sampling_rate = self.signal_processor.sampling_rate

        self.sleep_time = self.signal_processor.sleep_time

        self.live_data = self.signal_processor.live_signal
        self.live_data_time_points = np.linspace(0, self.signal_processor.live_window_size / self.sampling_rate, self.signal_processor.live_window_size)

        self.processed_live_data = self.live_data  # Initially, processed data is the same as live data

        self.recorded_data = self.live_data.copy()  # Start with the same data as live
        self.processed_recorded_data = self.recorded_data  # Initially, processed data is the same as recorded data

        self.live_processing_mode = 'raw'
        self.recording_processing_mode = 'raw'
        self.rms_window_size = 200 # 100ms
        self.filter_cutoff = 0.1  # Hz, example cutoff frequency for low-pass filter

        self.live_channel = 0
        self.recording_channel = 0
        self.is_receiving = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_live_data)
        self.timer.timeout.connect(self.update_recorded_data)
        self.timer.start(int(self.sleep_time * 1000))  # Synchronize with tcp server


    def set_live_channel(self, channel):
        self.live_channel = channel
        self.update_live_data()


    def set_live_processing_mode(self, mode):
        self.live_processing_mode = mode
        self.update_live_data()

    
    def set_recording_channel(self, channel):
        self.recording_channel = channel
        self.update_recorded_data()


    def set_recording_processing_mode(self, mode):
        self.recording_processing_mode = mode
        self.update_recorded_data()


    def process_signal(self, data, mode):
        if mode == 'raw':
            return data
        elif mode == 'rms':
            print("Processing RMS", data.shape)
            print("after processing RMS", self.apply_rms(data).shape)
            return self.apply_rms(data)
        elif mode == 'envelope':
            return self.apply_envelope(data)
        elif mode == 'filter':
            return self.apply_filter(data)
        return data
    

    def apply_rms(self, data):
        squared = np.square(data)
        window = np.ones(self.rms_window_size) / self.rms_window_size
        return np.sqrt(np.convolve(squared, window, 'same'))


    def apply_envelope(self, data):
        """Calculate envelope of the live signal using Hilbert transform"""
        return np.abs(hilbert(data))
    

    def apply_filter(self, data):
        """Apply low-pass filter to live data"""
        b, a = butter(4, self.filter_cutoff, btype="low")
        return lfilter(b, a, data)


    def update_live_data(self):
        if self.is_receiving:
            self.live_data = self.signal_processor.live_signal
        
        # process data of current channel
        print("live data size: ", self.live_data.shape)
        self.processed_live_data = self.process_signal(self.live_data[self.live_channel, :], self.live_processing_mode)
        print("no of live time points: ", self.processed_live_data.shape[0])
        # exit()

        self.live_data_updated.emit(self.live_data_time_points, self.processed_live_data)


    def update_recorded_data(self):
        if self.is_receiving:
            self.recorded_data = np.concatenate((self.recorded_data, self.signal_processor.live_signal), axis=1)

        # process data of current channel
        self.processed_recorded_data = self.process_signal(self.recorded_data[self.recording_channel, :], self.recording_processing_mode)
        self.recorded_data_time_points = np.linspace(0, self.processed_recorded_data.shape[0] / self.sampling_rate, self.processed_recorded_data.shape[0])
        print("no of time points: ", self.recorded_data_time_points.shape[0])
        self.recorded_data_updated.emit(self.recorded_data_time_points, self.processed_recorded_data)
