"""
Advanced Mastering Chain - Professional multi-pass mastering
Intelligent EQ, parallel compression, analog saturation, transparent limiting
"""

import numpy as np
from scipy import signal
from pydub import AudioSegment
from pedalboard import (
    Pedalboard, Compressor, Limiter, Gain, 
    Reverb, Delay
)
from typing import Dict, Optional, Tuple
import warnings


class AdvancedMasteringChain:
    """
    Professional-grade mastering processor
    - Intelligent EQ (frequency balance correction)
    - Parallel compression (punch & dynamics)
    - Analog-style saturation (warmth & harmonics)
    - Multi-band dynamics
    - Transparent limiting (loudness)
    - Stereo enhancement
    """
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
    
    def master_audio(self, audio: AudioSegment,
                    target_lufs: float = -11.0,         # LOUDER! (was -14.0) - club standard
                    target_style: str = "balanced",
                    apply_saturation: bool = True,
                    enhance_stereo: bool = True,
                    verbose: bool = True) -> AudioSegment:
        """
        Apply AGGRESSIVE professional mastering chain (CLUB/RADIO READY)
        
        Args:
            audio: Input AudioSegment
            target_lufs: Target loudness in LUFS (default -11.0 for club/radio, -14.0 for streaming)
            target_style: "warm", "balanced", "bright", "aggressive"
            apply_saturation: Add analog-style harmonic saturation (MORE AGGRESSIVE)
            enhance_stereo: Enhance stereo width (MORE WIDTH)
            verbose: Print processing steps
        
        Returns:
            Professionally mastered AudioSegment (LOUD, PUNCHY, WIDE)
        """
        if verbose:
            print("\n🎚️  ADVANCED MASTERING CHAIN")
            print("="*60)
        
        # Convert to numpy
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)
        
        # Ensure stereo for better processing
        if audio.channels == 1:
            samples = np.stack([samples, samples], axis=1).flatten()
            is_mono_input = True
        else:
            samples = samples.reshape(-1, 2)
            is_mono_input = False
        
        left = samples[:, 0] if len(samples.shape) > 1 else samples[::2]
        right = samples[:, 1] if len(samples.shape) > 1 else samples[1::2]
        
        # === PASS 1: Corrective Processing ===
        if verbose:
            print("📍 Pass 1: Corrective EQ & Cleanup")
        
        left, right = self._corrective_eq(left, right, target_style)
        left, right = self._remove_dc_offset(left, right)
        left, right = self._tame_resonances(left, right)
        
        # === PASS 2: Dynamic Processing ===
        if verbose:
            print("📍 Pass 2: Dynamics & Compression")
        
        left, right = self._multi_band_compression(left, right)
        left, right = self._parallel_compression(left, right, style=target_style)
        
        # === PASS 3: Color & Character ===
        if verbose:
            print("📍 Pass 3: Saturation & Color")
        
        if apply_saturation:
            left, right = self._analog_saturation(left, right, style=target_style)
        
        # === PASS 4: Spatial Processing ===
        if verbose:
            print("📍 Pass 4: Stereo Enhancement")
        
        if enhance_stereo:
            left, right = self._enhance_stereo(left, right)
        
        # === PASS 5: Final Loudness & Limiting ===
        if verbose:
            print("📍 Pass 5: Loudness Maximization")
        
        left, right = self._intelligent_limiting(left, right, target_lufs)
        
        # === PASS 6: Final Polish ===
        if verbose:
            print("📍 Pass 6: Final Polish & Dither")
        
        left, right = self._final_polish(left, right)
        left, right = self._apply_dither(left, right)
        
        # Combine channels
        if len(samples.shape) > 1:
            output = np.stack([left, right], axis=1).flatten()
        else:
            output = np.zeros(len(left) * 2)
            output[::2] = left
            output[1::2] = right
        
        # Convert back to mono if input was mono
        if is_mono_input:
            # Simple mono sum
            output = output.reshape(-1, 2)
            output = np.mean(output, axis=1)
        
        # Convert to AudioSegment
        output = np.clip(output, -1.0, 1.0)
        output = (output * (2**15)).astype(np.int16)
        
        result = AudioSegment(
            output.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1 if is_mono_input else 2
        )
        
        if verbose:
            print("="*60)
            print("✅ Mastering Complete!\n")
        
        return result
    
    def _corrective_eq(self, left: np.ndarray, right: np.ndarray, 
                      style: str) -> Tuple[np.ndarray, np.ndarray]:
        """Apply intelligent corrective EQ based on style"""
        
        # Style-specific EQ curves
        eq_styles = {
            'warm': {
                'sub_bass': 1.0,    # Leave sub-bass alone
                'bass': 1.05,       # Slight boost
                'low_mid': 0.98,    # Slight cut (reduce boxiness)
                'mid': 0.95,        # Cut (reduce harshness)
                'high_mid': 1.02,   # Slight boost (presence)
                'high': 0.92,       # Cut (soften)
            },
            'balanced': {
                'sub_bass': 0.98,
                'bass': 1.02,
                'low_mid': 1.0,
                'mid': 1.0,
                'high_mid': 1.03,
                'high': 1.02,
            },
            'bright': {
                'sub_bass': 0.95,
                'bass': 0.98,
                'low_mid': 0.98,
                'mid': 1.02,
                'high_mid': 1.08,
                'high': 1.12,
            },
            'aggressive': {
                'sub_bass': 1.05,
                'bass': 1.08,
                'low_mid': 1.0,
                'mid': 0.95,
                'high_mid': 1.10,
                'high': 1.08,
            },
        }
        
        eq = eq_styles.get(style, eq_styles['balanced'])
        
        # Apply EQ using filter banks
        left = self._apply_multiband_eq(left, eq)
        right = self._apply_multiband_eq(right, eq)
        
        return left, right
    
    def _apply_multiband_eq(self, signal_data: np.ndarray, 
                           eq_gains: Dict[str, float]) -> np.ndarray:
        """Apply multi-band EQ"""
        
        # Define frequency bands
        bands = [
            ('sub_bass', 20, 60),
            ('bass', 60, 250),
            ('low_mid', 250, 500),
            ('mid', 500, 2000),
            ('high_mid', 2000, 6000),
            ('high', 6000, 20000),
        ]
        
        output = np.zeros_like(signal_data)
        
        for band_name, low_freq, high_freq in bands:
            # Create bandpass filter
            sos = signal.butter(4, [low_freq, high_freq], 'bandpass', 
                              fs=self.sample_rate, output='sos')
            
            # Extract band
            band_signal = signal.sosfilt(sos, signal_data)
            
            # Apply gain
            gain = eq_gains.get(band_name, 1.0)
            output += band_signal * gain
        
        return output
    
    def _remove_dc_offset(self, left: np.ndarray, right: np.ndarray) -> Tuple:
        """Remove DC offset"""
        left = left - np.mean(left)
        right = right - np.mean(right)
        return left, right
    
    def _tame_resonances(self, left: np.ndarray, right: np.ndarray) -> Tuple:
        """Tame problematic resonances"""
        # Notch filters at common problematic frequencies
        problem_freqs = [120, 240, 500, 1000, 2500]  # Hz
        
        for freq in problem_freqs:
            # Very narrow notch
            q_factor = 20
            b, a = signal.iirnotch(freq, q_factor, fs=self.sample_rate)
            
            # Very subtle reduction
            left_notched = signal.lfilter(b, a, left)
            right_notched = signal.lfilter(b, a, right)
            
            # Blend (only 10% notch)
            left = left * 0.9 + left_notched * 0.1
            right = right * 0.9 + right_notched * 0.1
        
        return left, right
    
    def _multi_band_compression(self, left: np.ndarray, 
                                right: np.ndarray) -> Tuple:
        """Multi-band compression for balance"""
        
        # Define bands
        bands = [
            (20, 250),    # Low
            (250, 2000),  # Mid
            (2000, 20000) # High
        ]
        
        compression_params = [
            {'threshold': 0.6, 'ratio': 3.0, 'attack': 0.010, 'release': 0.100},  # Low
            {'threshold': 0.5, 'ratio': 4.0, 'attack': 0.005, 'release': 0.050},  # Mid
            {'threshold': 0.4, 'ratio': 3.5, 'attack': 0.001, 'release': 0.030},  # High
        ]
        
        left_out = np.zeros_like(left)
        right_out = np.zeros_like(right)
        
        for (low, high), params in zip(bands, compression_params):
            # Extract band
            sos = signal.butter(4, [low, high], 'bandpass', 
                              fs=self.sample_rate, output='sos')
            
            left_band = signal.sosfilt(sos, left)
            right_band = signal.sosfilt(sos, right)
            
            # Compress
            left_band = self._compress_signal(left_band, **params)
            right_band = self._compress_signal(right_band, **params)
            
            left_out += left_band
            right_out += right_band
        
        return left_out, right_out
    
    def _parallel_compression(self, left: np.ndarray, right: np.ndarray,
                             style: str = "balanced") -> Tuple:
        """Parallel compression (New York style)"""
        
        # Compression settings based on style
        if style == "aggressive":
            threshold, ratio, mix = 0.3, 8.0, 0.4
        elif style == "warm":
            threshold, ratio, mix = 0.5, 4.0, 0.25
        else:  # balanced/bright
            threshold, ratio, mix = 0.4, 6.0, 0.3
        
        # Heavy compression on parallel channel
        left_compressed = self._compress_signal(
            left, threshold=threshold, ratio=ratio,
            attack=0.003, release=0.080
        )
        right_compressed = self._compress_signal(
            right, threshold=threshold, ratio=ratio,
            attack=0.003, release=0.080
        )
        
        # Mix compressed with dry
        left = left * (1 - mix) + left_compressed * mix
        right = right * (1 - mix) + right_compressed * mix
        
        return left, right
    
    def _compress_signal(self, signal_data: np.ndarray,
                        threshold: float = 0.5,
                        ratio: float = 4.0,
                        attack: float = 0.005,
                        release: float = 0.100) -> np.ndarray:
        """Simple compressor implementation"""
        
        # Convert times to samples
        attack_samples = int(attack * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        # Envelope follower
        envelope = np.zeros_like(signal_data)
        envelope[0] = abs(signal_data[0])
        
        for i in range(1, len(signal_data)):
            if abs(signal_data[i]) > envelope[i-1]:
                # Attack
                alpha = 1.0 - np.exp(-1.0 / attack_samples)
            else:
                # Release
                alpha = 1.0 - np.exp(-1.0 / release_samples)
            
            envelope[i] = alpha * abs(signal_data[i]) + (1 - alpha) * envelope[i-1]
        
        # Compute gain reduction
        gain = np.ones_like(envelope)
        above_threshold = envelope > threshold
        
        # Gain reduction for samples above threshold
        gain[above_threshold] = threshold / envelope[above_threshold]
        gain[above_threshold] = gain[above_threshold] ** (1.0 / ratio - 1.0)
        
        # Apply makeup gain
        makeup_gain = 1.0 / (threshold ** (1.0 / ratio - 1.0))
        gain *= makeup_gain
        
        return signal_data * gain
    
    def _analog_saturation(self, left: np.ndarray, right: np.ndarray,
                          style: str = "balanced") -> Tuple:
        """Add analog-style harmonic saturation"""
        
        # Saturation amount based on style
        saturation_amounts = {
            'warm': 0.4,
            'balanced': 0.2,
            'bright': 0.15,
            'aggressive': 0.5,
        }
        
        amount = saturation_amounts.get(style, 0.2)
        
        # Soft clipping with asymmetry (like tubes/tape)
        def saturate(x, amt):
            # Drive
            x_driven = x * (1 + amt)
            
            # Soft clip (hyperbolic tangent)
            x_saturated = np.tanh(x_driven)
            
            # Add even harmonics (asymmetric distortion)
            x_saturated += np.tanh(x_driven * 2) * amt * 0.1
            
            # Blend
            return x * (1 - amt * 0.5) + x_saturated * (amt * 0.5)
        
        left = saturate(left, amount)
        right = saturate(right, amount)
        
        # Slight high-frequency roll-off (analog character)
        sos = signal.butter(1, 16000, 'lowpass', fs=self.sample_rate, output='sos')
        left = signal.sosfilt(sos, left)
        right = signal.sosfilt(sos, right)
        
        return left, right
    
    def _enhance_stereo(self, left: np.ndarray, right: np.ndarray,
                       amount: float = 0.3) -> Tuple:
        """Enhance stereo width without phase issues"""
        
        # Mid-side processing
        mid = (left + right) / 2.0
        side = (left - right) / 2.0
        
        # Enhance side (but only above 200Hz to avoid phase issues in bass)
        sos = signal.butter(2, 200, 'highpass', fs=self.sample_rate, output='sos')
        side_filtered = signal.sosfilt(sos, side)
        
        # Boost side
        side_enhanced = side * (1 - amount) + side_filtered * (1 + amount)
        
        # Convert back to L/R
        left = mid + side_enhanced
        right = mid - side_enhanced
        
        return left, right
    
    def _intelligent_limiting(self, left: np.ndarray, right: np.ndarray,
                             target_lufs: float) -> Tuple:
        """Transparent look-ahead limiter with LUFS targeting"""
        
        # Measure current LUFS (approximation via RMS)
        current_rms_left = np.sqrt(np.mean(left**2))
        current_rms_right = np.sqrt(np.mean(right**2))
        current_rms = (current_rms_left + current_rms_right) / 2.0
        
        # Approximate LUFS from RMS (rough conversion)
        current_lufs = 20 * np.log10(current_rms + 1e-10) - 23
        
        # Calculate required gain
        gain_db = target_lufs - current_lufs
        gain_linear = 10 ** (gain_db / 20.0)
        
        # Limit gain boost (safety)
        gain_linear = min(gain_linear, 3.0)  # Max +9.5dB
        
        # Apply pre-gain
        left *= gain_linear
        right *= gain_linear
        
        # True peak limiter
        ceiling = 0.95  # -0.44dBFS
        
        # Look-ahead limiter (5ms)
        lookahead_samples = int(0.005 * self.sample_rate)
        
        left = self._apply_limiter(left, ceiling, lookahead_samples)
        right = self._apply_limiter(right, ceiling, lookahead_samples)
        
        return left, right
    
    def _apply_limiter(self, signal_data: np.ndarray, 
                      ceiling: float, lookahead: int) -> np.ndarray:
        """Apply look-ahead peak limiter"""
        
        # Pad signal for lookahead
        padded = np.pad(signal_data, (lookahead, lookahead), mode='edge')
        
        # Find peaks in lookahead window
        gain = np.ones_like(padded)
        
        for i in range(len(signal_data)):
            # Look ahead
            window = padded[i:i+lookahead*2]
            peak = np.max(np.abs(window))
            
            if peak > ceiling:
                gain[i+lookahead] = ceiling / peak
        
        # Smooth gain reduction (attack/release)
        attack_samples = int(0.001 * self.sample_rate)
        release_samples = int(0.050 * self.sample_rate)
        
        smooth_gain = np.zeros_like(gain)
        smooth_gain[0] = gain[0]
        
        for i in range(1, len(gain)):
            if gain[i] < smooth_gain[i-1]:
                # Attack
                alpha = 1.0 - np.exp(-1.0 / attack_samples)
            else:
                # Release
                alpha = 1.0 - np.exp(-1.0 / release_samples)
            
            smooth_gain[i] = alpha * gain[i] + (1 - alpha) * smooth_gain[i-1]
        
        # Apply gain (remove padding)
        output = padded[lookahead:-lookahead] * smooth_gain[lookahead:-lookahead]
        
        return output
    
    def _final_polish(self, left: np.ndarray, right: np.ndarray) -> Tuple:
        """Final polish (subtle high-shelf boost for air)"""
        
        # Very gentle high-shelf boost at 12kHz
        # Design high-shelf filter
        freq = 12000
        q = 0.7
        gain_db = 0.5
        
        w0 = 2 * np.pi * freq / self.sample_rate
        A = 10 ** (gain_db / 40.0)
        
        cos_w0 = np.cos(w0)
        sin_w0 = np.sin(w0)
        alpha = sin_w0 / (2 * q)
        
        # High-shelf coefficients
        b0 = A * ((A + 1) + (A - 1) * cos_w0 + 2 * np.sqrt(A) * alpha)
        b1 = -2 * A * ((A - 1) + (A + 1) * cos_w0)
        b2 = A * ((A + 1) + (A - 1) * cos_w0 - 2 * np.sqrt(A) * alpha)
        a0 = (A + 1) - (A - 1) * cos_w0 + 2 * np.sqrt(A) * alpha
        a1 = 2 * ((A - 1) - (A + 1) * cos_w0)
        a2 = (A + 1) - (A - 1) * cos_w0 - 2 * np.sqrt(A) * alpha
        
        # Normalize
        b = np.array([b0, b1, b2]) / a0
        a = np.array([1, a1 / a0, a2 / a0])
        
        # Apply filter
        left = signal.lfilter(b, a, left)
        right = signal.lfilter(b, a, right)
        
        return left, right
    
    def _apply_dither(self, left: np.ndarray, right: np.ndarray) -> Tuple:
        """Apply TPDF dither for 16-bit conversion"""
        
        # Triangular PDF dither
        dither_amplitude = 1.0 / (2**16)  # LSB amplitude
        
        # Generate TPDF dither (sum of two uniform distributions)
        dither_left = (np.random.rand(len(left)) - 0.5) * dither_amplitude
        dither_left += (np.random.rand(len(left)) - 0.5) * dither_amplitude
        
        dither_right = (np.random.rand(len(right)) - 0.5) * dither_amplitude
        dither_right += (np.random.rand(len(right)) - 0.5) * dither_amplitude
        
        # Add dither
        left += dither_left
        right += dither_right
        
        return left, right
