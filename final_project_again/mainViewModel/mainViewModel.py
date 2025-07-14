from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from service.signal_processor import SignalProcessor
from scipy.signal import hilbert , butter , lfilter

class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data
    full_data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data
    rms_valued_updated = pyqtSignal(float)
    live_processing_mode_changed = pyqtSignal(str)
    live_processing_data_updated = pyqtSignal(np.ndarray , np.ndarray) #time , processed_data

    def __init__(self):
        super().__init__()
        self.signal_processor = SignalProcessor()
        self.signal_processor.process_signal()
        self.rms_values = []
        self.live_processing_fns = {
            'raw' : lambda x:x , 
            'rms' : self._calculate_live_rms,
            'envelope' : self._calculate_live_envelope,
            'filter': self._apply_live_filter
        }

        self.current_live_mode = 'raw'
        self.channel = 0
        self.rms_window_size = 100 
        self.filter_cutoff = 0.1 

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)  # Update every 100 ms

        self.live_data_time_axis = np.linspace(0, 10000, self.signal_processor.live_window_size)


    def _calculate_live_rms(self, data):
        # calculate rms of the current data
        squared = np.square(data)
        window = np.ones(self.rms_window_size)/self.rms_window_size
        return np.sqrt(np.convolve(squared, window, 'valid'))
    def _calculate_live_envelope(self , data):
            """Calculate envelope of the live signal using Helbert transform  """
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
        raw_data =  self.signal_processor.live_window[self.channel]
        processor = self.live_processing_fns[self.current_live_mode]
        processed_data = processor(raw_data)

        # Adjust time axis if processing shortens the data 

        processed_time = self.live_data_time_axis[:len(processed_data)]
        self.live_processing_data_updated.emit(processed_time , processed_data)



    def set_channel(self, channel):
        self.channel = channel - 1

    def do_sth(self):
        live_window = self.signal_processor.live_window
        full_window = self.signal_processor.full_window
    def calculate_rms(self):
        """Calculate RMS  for the current channel"""
        try:
            # get the current channel data 
            channel_data = self.signal_processor.live_window[self.channel]

            #calculate the rms 
            rms_value = np.sqrt(np.mean(np.square(channel_data)))

            self.rms_values.append(rms_value)
            print(self.rms_values)
            self.rms_valued_updated.emit(rms_value)
            return rms_value
        except Exception as e :
            print(f"Error: calculation of the rms {e}")
            return 0.0 
        
    def update_data(self):
        #print("Updating data in MainViewModel, channel:", self.channel)
        self.live_data_updated.emit(self.live_data_time_axis, self.signal_processor.live_window[self.channel])
        if self.current_live_mode != 'raw': 
            self._update_processed_data()


if __name__ == "__main__":
    print("ÖÖÖÖÖÖÖÖÖÖÖÖ")