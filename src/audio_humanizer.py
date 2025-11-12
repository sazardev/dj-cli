"""
Audio Humanizer - Make synthesized audio sound more natural and less robotic
Adds micro-variations in timing, velocity, pitch, and groove
"""

import numpy as np
from scipy import signal, interpolate
from pydub import AudioSegment
from typing import List, Tuple, Optional
import random


class AudioHumanizer:
    """
    Humanize synthesized audio to sound more natural
    - Timing drift (not perfectly quantized)
    - Velocity variations (not all notes at same volume)
    - Pitch wobble (slight detuning, vibrato)
    - Groove swing (human feel)
    """
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
    
    def humanize_audio(self, audio: AudioSegment, 
                      timing_drift: float = 0.6,         # Increased from 0.3
                      velocity_variation: float = 0.35,   # Increased from 0.2
                      pitch_wobble: float = 0.25,        # Increased from 0.15
                      groove_amount: float = 0.6,        # Increased from 0.4
                      analog_warmth: float = 0.5) -> AudioSegment:  # Increased from 0.3
        """
        Apply DEEP comprehensive humanization (PROFESSIONAL STANDARDS)
        
        Args:
            audio: Input AudioSegment
            timing_drift: Amount of timing variation (0.0-1.0) - NOW MORE AGGRESSIVE
            velocity_variation: Amount of volume variation (0.0-1.0) - NOW MORE DYNAMIC
            pitch_wobble: Amount of pitch variation (0.0-1.0) - NOW MORE NATURAL
            groove_amount: Amount of groove/swing (0.0-1.0) - NOW MORE PRONOUNCED
            analog_warmth: Amount of analog-style warmth (0.0-1.0) - NOW MORE AUTHENTIC
        
        Returns:
            Deeply Humanized AudioSegment with professional natural feel
        """
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)  # Normalize
        
        # Handle stereo
        if audio.channels == 2:
            samples = samples.reshape(-1, 2)
            left = samples[:, 0]
            right = samples[:, 1]
            
            # Humanize each channel separately (slightly different)
            left = self._apply_humanization(left, timing_drift, velocity_variation, 
                                           pitch_wobble, groove_amount, analog_warmth)
            right = self._apply_humanization(right, timing_drift * 0.95, velocity_variation * 1.05, 
                                            pitch_wobble * 1.02, groove_amount * 0.98, analog_warmth)
            
            samples = np.stack([left, right], axis=1).flatten()
        else:
            samples = self._apply_humanization(samples, timing_drift, velocity_variation,
                                              pitch_wobble, groove_amount, analog_warmth)
        
        # Convert back to AudioSegment
        samples = np.clip(samples, -1.0, 1.0)
        samples = (samples * (2**15)).astype(np.int16)
        
        return AudioSegment(
            samples.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=audio.channels
        )
    
    def _apply_humanization(self, samples: np.ndarray,
                           timing_drift: float,
                           velocity_variation: float,
                           pitch_wobble: float,
                           groove_amount: float,
                           analog_warmth: float) -> np.ndarray:
        """Apply all humanization effects to mono signal"""
        
        # 1. Subtle pitch wobble (like tape speed variation)
        if pitch_wobble > 0:
            samples = self._apply_pitch_wobble(samples, pitch_wobble)
        
        # 2. Micro-timing variations
        if timing_drift > 0:
            samples = self._apply_timing_drift(samples, timing_drift)
        
        # 3. Dynamic velocity envelope (not perfectly flat)
        if velocity_variation > 0:
            samples = self._apply_velocity_variation(samples, velocity_variation)
        
        # 4. Groove/swing feel
        if groove_amount > 0:
            samples = self._apply_groove(samples, groove_amount)
        
        # 5. Analog warmth (harmonic saturation, noise)
        if analog_warmth > 0:
            samples = self._apply_analog_warmth(samples, analog_warmth)
        
        return samples
    
    def _apply_pitch_wobble(self, samples: np.ndarray, amount: float) -> np.ndarray:
        """
        Apply subtle pitch variations (like tape wow & flutter)
        Uses time-stretching to simulate pitch changes
        """
        # Create slow LFO for wow (0.5-2Hz)
        duration = len(samples) / self.sample_rate
        t = np.linspace(0, duration, len(samples))
        
        # Multiple LFOs at different frequencies
        lfo1 = np.sin(2 * np.pi * 0.8 * t) * amount * 0.003  # Main wow
        lfo2 = np.sin(2 * np.pi * 3.2 * t) * amount * 0.001  # Flutter
        lfo3 = np.sin(2 * np.pi * 0.3 * t) * amount * 0.002  # Slow drift
        
        # Combine LFOs
        pitch_variation = lfo1 + lfo2 + lfo3
        
        # Apply pitch shift via resampling
        # pitch_variation is in semitones, convert to rate change
        rate_change = 2 ** (pitch_variation / 12.0)
        
        # Create new time axis with variable rate
        new_indices = np.cumsum(rate_change)
        new_indices = new_indices / new_indices[-1] * (len(samples) - 1)
        
        # Interpolate to get new samples
        f = interpolate.interp1d(np.arange(len(samples)), samples, 
                                kind='cubic', bounds_error=False, fill_value=0)
        
        return f(new_indices)
    
    def _apply_timing_drift(self, samples: np.ndarray, amount: float) -> np.ndarray:
        """
        Apply micro-timing variations (not perfectly quantized)
        Simulates human timing imperfections
        """
        # Detect transients (note onsets)
        # Use envelope follower
        envelope = self._get_envelope(samples, attack_ms=5, release_ms=50)
        
        # Find peaks in envelope (note onsets)
        peaks, _ = signal.find_peaks(envelope, height=0.1, distance=self.sample_rate//20)
        
        if len(peaks) == 0:
            return samples
        
        # Apply random timing shifts to each peak
        output = np.zeros_like(samples)
        
        for i, peak in enumerate(peaks):
            # Random timing shift (MUCH MORE AGGRESSIVE for natural feel)
            shift_ms = (random.random() * 2 - 1) * amount * 15  # ±15ms max (was 5ms)
            shift_samples = int(shift_ms * self.sample_rate / 1000)
            
            # Determine segment boundaries
            if i == 0:
                start = 0
            else:
                start = (peaks[i-1] + peak) // 2
            
            if i == len(peaks) - 1:
                end = len(samples)
            else:
                end = (peak + peaks[i+1]) // 2
            
            # Apply shift
            segment = samples[start:end]
            new_start = max(0, min(len(output) - len(segment), start + shift_samples))
            new_end = new_start + len(segment)
            
            # Crossfade to avoid clicks
            if new_end <= len(output):
                # Fade in/out edges
                fade_len = min(100, len(segment) // 10)
                fade_in = np.linspace(0, 1, fade_len)
                fade_out = np.linspace(1, 0, fade_len)
                
                if fade_len > 0:
                    segment[:fade_len] *= fade_in
                    segment[-fade_len:] *= fade_out
                
                output[new_start:new_end] += segment
        
        # Normalize
        max_val = np.max(np.abs(output))
        if max_val > 0:
            output = output / max_val * np.max(np.abs(samples))
        
        return output
    
    def _apply_velocity_variation(self, samples: np.ndarray, amount: float) -> np.ndarray:
        """
        Apply dynamic variations (not all notes at same volume)
        Creates natural volume fluctuations
        """
        # Create smooth random volume curve
        duration = len(samples) / self.sample_rate
        num_points = int(duration * 4)  # 4 points per second
        
        # Generate random velocity points (MORE DYNAMIC RANGE)
        velocities = 1.0 + (np.random.randn(num_points) * amount * 0.30)  # 30% variation (was 15%)
        velocities = np.clip(velocities, 0.70, 1.30)  # Wider range (was 0.85-1.15)
        
        # Interpolate to full length
        x_points = np.linspace(0, len(samples)-1, num_points)
        x_full = np.arange(len(samples))
        
        f = interpolate.interp1d(x_points, velocities, kind='cubic', 
                                bounds_error=False, fill_value=1.0)
        velocity_curve = f(x_full)
        
        return samples * velocity_curve
    
    def _apply_groove(self, samples: np.ndarray, amount: float) -> np.ndarray:
        """
        Apply groove/swing feel
        Subtle rhythm variations that make it feel more human
        """
        # Similar to timing drift but more rhythmic
        # Apply subtle compression with rhythm
        duration = len(samples) / self.sample_rate
        
        # Create groove pattern (emphasize certain beats)
        # Assume 4/4 time, ~120 BPM average
        bpm = 120
        beat_duration = 60.0 / bpm
        num_beats = int(duration / beat_duration)
        
        groove_pattern = np.ones(len(samples))
        
        for beat in range(num_beats):
            beat_start = int(beat * beat_duration * self.sample_rate)
            beat_end = min(len(samples), int((beat + 1) * beat_duration * self.sample_rate))
            
            # Emphasize beats 1 and 3, slight swing on 2 and 4
            if beat % 4 == 0:  # Beat 1
                emphasis = 1.0 + amount * 0.08
            elif beat % 4 == 2:  # Beat 3
                emphasis = 1.0 + amount * 0.05
            elif beat % 4 in [1, 3]:  # Beats 2 and 4
                emphasis = 1.0 - amount * 0.03
            else:
                emphasis = 1.0
            
            groove_pattern[beat_start:beat_end] *= emphasis
        
        return samples * groove_pattern
    
    def _apply_analog_warmth(self, samples: np.ndarray, amount: float) -> np.ndarray:
        """
        Add analog-style warmth
        - Subtle harmonic saturation
        - Tape hiss/vinyl noise
        - Low-frequency rumble
        """
        # 1. Subtle harmonic saturation (soft clipping)
        saturation_amount = amount * 0.2
        saturated = np.tanh(samples * (1 + saturation_amount)) / (1 + saturation_amount * 0.5)
        
        # 2. Very subtle tape hiss (filtered white noise)
        noise_amplitude = amount * 0.002
        noise = np.random.randn(len(samples)) * noise_amplitude
        
        # Filter noise to high frequencies (tape hiss character)
        sos = signal.butter(4, 4000, 'highpass', fs=self.sample_rate, output='sos')
        noise = signal.sosfilt(sos, noise)
        
        # 3. Very subtle low-frequency rumble
        rumble_amplitude = amount * 0.001
        rumble_freq = 30 + np.random.randn() * 5  # ~30Hz
        t = np.arange(len(samples)) / self.sample_rate
        rumble = np.sin(2 * np.pi * rumble_freq * t) * rumble_amplitude
        
        # 4. Slight high-frequency roll-off (analog character)
        sos_rolloff = signal.butter(1, 16000, 'lowpass', fs=self.sample_rate, output='sos')
        saturated = signal.sosfilt(sos_rolloff, saturated)
        
        # Combine all
        output = saturated + noise + rumble
        
        # Blend with original
        blend = 0.6 + amount * 0.4
        output = output * blend + samples * (1 - blend)
        
        return output
    
    def _get_envelope(self, samples: np.ndarray, 
                     attack_ms: float = 5, release_ms: float = 50) -> np.ndarray:
        """Get amplitude envelope of signal"""
        # Rectify
        rectified = np.abs(samples)
        
        # Convert times to samples
        attack_samples = int(attack_ms * self.sample_rate / 1000)
        release_samples = int(release_ms * self.sample_rate / 1000)
        
        # Create envelope follower
        envelope = np.zeros_like(rectified)
        envelope[0] = rectified[0]
        
        for i in range(1, len(rectified)):
            if rectified[i] > envelope[i-1]:
                # Attack
                alpha = 1.0 - np.exp(-1.0 / attack_samples)
            else:
                # Release
                alpha = 1.0 - np.exp(-1.0 / release_samples)
            
            envelope[i] = alpha * rectified[i] + (1 - alpha) * envelope[i-1]
        
        return envelope
    
    def add_room_ambience(self, audio: AudioSegment, room_size: str = "small",
                         mix: float = 0.15) -> AudioSegment:
        """
        Add subtle room ambience (early reflections)
        
        Args:
            audio: Input audio
            room_size: "small", "medium", "large"
            mix: Wet/dry mix (0.0-1.0)
        """
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)
        
        # Room parameters
        room_params = {
            'small': {'delays': [7, 11, 13, 17], 'decay': 0.3},
            'medium': {'delays': [17, 23, 29, 37], 'decay': 0.4},
            'large': {'delays': [37, 47, 59, 71], 'decay': 0.5},
        }
        
        params = room_params.get(room_size, room_params['small'])
        
        # Create early reflections
        reflections = np.zeros_like(samples)
        
        for i, delay_ms in enumerate(params['delays']):
            delay_samples = int(delay_ms * self.sample_rate / 1000)
            if delay_samples < len(samples):
                # Each reflection is slightly quieter
                gain = params['decay'] ** (i + 1)
                
                # Add reflection with slight filtering
                reflection = np.zeros_like(samples)
                reflection[delay_samples:] = samples[:-delay_samples] * gain
                
                # Slight low-pass filter on each reflection
                cutoff = 8000 - (i * 1000)
                sos = signal.butter(2, cutoff, 'lowpass', fs=self.sample_rate, output='sos')
                reflection = signal.sosfilt(sos, reflection)
                
                reflections += reflection
        
        # Mix with dry signal
        output = samples * (1 - mix) + reflections * mix
        
        # Convert back
        output = np.clip(output, -1.0, 1.0)
        output = (output * (2**15)).astype(np.int16)
        
        return AudioSegment(
            output.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=audio.channels
        )
