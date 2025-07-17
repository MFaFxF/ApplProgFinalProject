
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor
from scipy.signal import hilbert, butter, lfilter


class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # Optional if still needed
    processed_live_data_updated = pyqtSignal(np.ndarray, np.ndarray)
    live_processing_mode_changed = pyqtSignal(str)

    recorded_data_updated = pyqtSignal(np.ndarray, np.ndarray)
    processed_recorded_data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()
        self.signal_processor.generate_signal()

        self.rms_values = []
        self.live_processing_fns = {
            'raw' : lambda x:x , 
            'rms' : self._calculate_live_rms,
            'envelope' : self._calculate_live_envelope,
            'filter': self._apply_live_filter
        }

        self.current_live_mode = 'raw'
        self.rms_window_size = 100 
        self.filter_cutoff = 0.1 

        self.channel = 0

        self.live_data_time_points = np.linspace(0, 10, self.signal_processor.live_window_size) #TODO meaningful value

        self.is_receiving = False
        self.live_signal = np.zeros((32, self.signal_processor.live_window_size), dtype=np.float32)
        
        self.recorded_signal = np.zeros((32, self.signal_processor.live_window_size), dtype=np.float32)
        # self.is_recording = False
        # self.got_new_data = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)

    def _calculate_live_rms(self, data):
        # calculate rms of the current data
        squared = np.square(data)
        window = np.ones(self.rms_window_size)/self.rms_window_size
        return np.sqrt(np.convolve(squared, window, 'valid'))
    
    def _calculate_live_envelope(self , data):
        """Calculate envelope of the live signal using Hilbert transform  """
        return np.abs(hilbert(data))
    
    def _apply_live_filter(self , data):
        """Apply low-pass filter to live data"""
        b , a = butter(4 , self.filter_cutoff ,btype="low")
        return lfilter(b , a , data)

    def set_processing_mode(self , mode):
        """Switch between processing modes """
        if not hasattr(self ,'live_processing_fns'):
            self.live_processing_fns = {
                'raw': lambda x: x,
                'rms': self._calculate_live_rms,
                'envelope': self._calculate_live_envelope,
                'filter': self._apply_live_filter
            }

        if mode in self.live_processing_fns:
            self.current_live_mode = mode 
            self.live_processing_mode_changed.emit(mode)
            self._update_processed_data()
        else:
            print(f"Warning: Unknown processing mode '{mode}'")    

    def _update_processed_data(self):
        """Calculate and emit processed data"""

        raw_data =  self.live_signal[self.channel]
        processor = self.live_processing_fns[self.current_live_mode]
        processed_data = processor(raw_data)

        # Adjust time axis if processing shortens the data 

        processed_time = self.live_data_time_points[:len(processed_data)]
        self.processed_live_data_updated.emit(processed_time, processed_data)

    def set_channel(self, channel):
        self.channel = channel - 1
        print("Switched to channel: ", channel)

    def start_receiving(self):
        self.is_receiving = True

    def stop_receiving(self):
        self.is_receiving = False
    
    def clear_recording(self):
        """Clear the recorded signal"""
        self.signal_processor.clear_recording()
        
    def update_data(self):
        """Update live data and emit signals"""
        if not self.is_receiving:
            return
        
        self.live_data_updated.emit(self.live_data_time_points, self.signal_processor.live_window)

        if self.current_live_mode != 'raw': 
            self._update_processed_data()

        recorded = self.signal_processor.recorded_signal
        if recorded is not None and recorded.shape[1] > 0:
            recorded_time = np.linspace(0, recorded.shape[1] / 2000, recorded.shape[1])  # 2000Hz
            self.recorded_data_updated.emit(recorded_time, recorded)