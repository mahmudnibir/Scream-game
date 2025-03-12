import numpy as np
import sounddevice as sd
from scipy.fft import fft
from collections import deque
import threading
import time

class SoundProcessor:
    def __init__(self, sample_rate=44100, window_size=1024, history_size=10):
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.history_size = history_size
        
        # Sound intensity tracking
        self.current_intensity = 0
        self.intensity_history = deque(maxlen=history_size)
        self.frequency_peaks = []
        
        # Thresholds (can be calibrated)
        self.noise_floor = 0.05  # Increased noise floor
        self.walk_threshold = 0.1  # Increased walk threshold
        self.jump_threshold = 0.2
        self.dash_threshold = 0.15
        
        # Debounce settings
        self.last_action_time = 0
        self.action_cooldown = 0.1  # Seconds between actions
        self.sustained_threshold = 0.05  # How long sound must be sustained
        self.action_start_time = 0
        
        # Frequency ranges for different actions
        self.whistle_range = (1000, 3000)  # Hz
        self.hum_range = (100, 400)        # Hz
        
        # State tracking
        self.is_calibrating = False
        self.calibration_samples = []
        
        # Start audio stream
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            callback=self._audio_callback,
            blocksize=self.window_size
        )
        self.stream.start()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Status: {status}")
            return
            
        # Calculate current intensity with smoothing
        new_intensity = np.linalg.norm(indata) / np.sqrt(len(indata))
        self.current_intensity = self.current_intensity * 0.7 + new_intensity * 0.3  # Smoothing
        self.intensity_history.append(self.current_intensity)
        
        # Perform FFT for frequency analysis
        if len(indata) >= self.window_size:
            fft_data = fft(indata[:self.window_size, 0])
            frequencies = np.fft.fftfreq(self.window_size, 1/self.sample_rate)
            self.frequency_peaks = frequencies[np.argsort(np.abs(fft_data))[-5:]]
        
        # Update calibration if active
        if self.is_calibrating:
            self.calibration_samples.append(self.current_intensity)

    def start_calibration(self, duration=5):
        """Start microphone calibration"""
        self.is_calibrating = True
        self.calibration_samples = []
        time.sleep(duration)
        self.is_calibrating = False
        
        if self.calibration_samples:
            # Update thresholds based on calibration
            ambient_noise = np.mean(self.calibration_samples)
            self.noise_floor = ambient_noise * 1.5
            self.walk_threshold = ambient_noise * 3
            self.jump_threshold = ambient_noise * 8
            self.dash_threshold = ambient_noise * 6
        
        return {
            "noise_floor": self.noise_floor,
            "walk_threshold": self.walk_threshold,
            "jump_threshold": self.jump_threshold,
            "dash_threshold": self.dash_threshold
        }

    def get_action(self):
        """Determine the current action based on sound input"""
        current_time = time.time()
        
        # Enforce cooldown between actions
        if current_time - self.last_action_time < self.action_cooldown:
            return "none"
            
        # Check if sound is sustained enough
        if self.current_intensity > self.noise_floor:
            if self.action_start_time == 0:
                self.action_start_time = current_time
            elif current_time - self.action_start_time < self.sustained_threshold:
                return "none"
        else:
            self.action_start_time = 0
            return "none"
            
        # Reset cooldown timer
        self.last_action_time = current_time
            
        if self.current_intensity <= self.noise_floor:
            return "none"
            
        # Check for whistle (dash) using frequency analysis
        if any(self.whistle_range[0] <= freq <= self.whistle_range[1] 
               for freq in self.frequency_peaks):
            if self.current_intensity >= self.dash_threshold:
                return "dash"
        
        # Check for humming (crouch)
        if any(self.hum_range[0] <= freq <= self.hum_range[1] 
               for freq in self.frequency_peaks):
            return "crouch"
        
        # Check for jump (scream)
        if self.current_intensity >= self.jump_threshold:
            return "jump"
        
        # Check for walk (talking)
        if self.current_intensity >= self.walk_threshold:
            # Additional check for sustained sound
            if len(self.intensity_history) >= 3:
                if all(i >= self.walk_threshold for i in list(self.intensity_history)[-3:]):
                    return "walk"
            
        return "none"

    def get_intensity(self):
        """Get current sound intensity"""
        return self.current_intensity

    def get_average_intensity(self):
        """Get average intensity over history window"""
        return np.mean(self.intensity_history) if self.intensity_history else 0

    def cleanup(self):
        """Clean up resources"""
        if self.stream:
            self.stream.stop()
            self.stream.close() 