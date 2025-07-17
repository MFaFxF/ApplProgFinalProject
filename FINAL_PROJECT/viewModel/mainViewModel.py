from PyQt5.QtCore import QObject, pyqtSignal, QTimer 
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
from service.signal_processor import SignalProcessor
from scipy.signal import hilbert, butter, lfilter
import time
import csv

class MainViewModel(QObject):
    live_data_updated = pyqtSignal(np.ndarray, np.ndarray)
    recorded_data_updated = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()

        self.signal_processor = SignalProcessor()
        # self.signal_processor.generate_signal()
        self.sampling_rate = self.signal_processor.sampling_rate

        self.sleep_time = self.signal_processor.sleep_time

        self.live_data = self.signal_processor.live_signal
        self.live_window_size = self.signal_processor.live_window_size
        self.live_data_time_points = np.linspace(0, self.live_window_size / self.sampling_rate, self.signal_processor.live_window_size)

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
        self.timer.start(9)  # Synchronize with tcp server

        # self.point_counter_timer = QTimer()
        # t0 = time.time()
        # self.point_counter_timer.timeout.connect(lambda: print(f"Recorded Data Points: {self.recorded_data.shape[1]}, Time: {time.time() - t0:.2f} s"))
        # self.point_counter_timer.start(1000)  # Print every second

    def set_live_channel(self, channel):
        self.live_channel = channel - 1
        self.update_live_data()


    def set_live_processing_mode(self, mode):
        self.live_processing_mode = mode
        self.update_live_data()

    
    def set_recording_channel(self, channel):
        self.recording_channel = channel - 1
        self.update_recorded_data()


    def set_recording_processing_mode(self, mode):
        self.recording_processing_mode = mode
        self.update_recorded_data()
        
    def clear_recording(self):
        # self.recorded_data = None
        # self.processed_recorded_data = None
        self.signal_processor.clear_recording()
        self.update_recorded_data()


    def process_signal(self, data, mode):
        if mode == 'raw':
            return data
        elif mode == 'rms':
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
    

    def export_results(self):
        
        if self.recorded_data is None or self.processed_recorded_data is None:
            QMessageBox.warning(None , "Export Failed" , "No data exported")
            return


        file_path , _ = QFileDialog.getSaveFileName(
            None , "Export data " , "", "CSV Files (*.csv);;Text Files (*.txt)"
        ) 

        if not file_path:
            return # User cancel it 
        
        try:
            with open(file_path , "w" , newline='') as f:
                writer =  csv.writer(f)
                writer.writerow(["Time" , "Value"]) # Headers 
                for t , v in zip(self.recorded_data_time_points , self.processed_recorded_data):
                    writer.writerow([t,v])
            QMessageBox.information( None, "Data Uploaded Succefully" , f"data uploaded to : {file_path}")
        except Exception as e:
            QMessageBox.critical(None , "export failed ", str(e))


    def update_live_data(self):
        if self.is_receiving:
            self.live_data = self.signal_processor.live_signal
        
        self.processed_live_data = self.process_signal(self.live_data[self.live_channel, :], self.live_processing_mode)
        self.live_data_updated.emit(self.live_data_time_points, self.processed_live_data)


    def update_recorded_data(self):
        if self.is_receiving:
            # Update recorded data with the latest live signal

            # self.recorded_data = np.concatenate((self.recorded_data, self.signal_processor.live_signal[:, -18:]), axis=1)
            self.recorded_data = self.signal_processor.recorded_signal

        if self.recorded_data is None:
            self.recorded_data = np.zeros_like(self.signal_processor.live_signal[:, -18:])  # Start with the last 18 samples
        # process data of current channel
        self.processed_recorded_data = self.process_signal(self.recorded_data[self.recording_channel, :], self.recording_processing_mode)
        self.recorded_data_time_points = np.linspace(0, self.processed_recorded_data.shape[0] / self.sampling_rate, self.processed_recorded_data.shape[0])
        
        self.recorded_data_updated.emit(self.recorded_data_time_points, self.processed_recorded_data)
