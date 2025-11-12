"""
Silence Fill System - Intelligently fill silence gaps with ambient textures
Eliminates awkward gaps and empty spaces in music
"""

import numpy as np
from scipy import signal
from pydub import AudioSegment
from typing import List, Tuple, Optional
import random


class SilenceFiller:
    """
    Detect silence gaps and fill them with appropriate ambient content
    - Vinyl/tape noise
    - Room tone
    - Ambient pads
    - Crossfade transitions
    """
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
    
    def fill_silence_gaps(self, audio: AudioSegment,
                         min_gap_duration: float = 0.3,  # STRICTER! (was 0.5s)
                         fill_style: str = "smart",
                         fill_volume: float = 0.35) -> AudioSegment:  # More present (was 0.3)
        """
        Detect and fill silence gaps (STRICT DETECTION)
        
        Args:
            audio: Input AudioSegment
            min_gap_duration: Minimum gap duration to fill (seconds) - NOW STRICTER
            fill_style: "vinyl", "ambient", "room", "smart" (intelligent auto-detect)
            fill_volume: Volume of fill material (0.0-1.0) - NOW MORE PRESENT
        
        Returns:
            AudioSegment with professionally filled gaps
        """
        # Detect silence gaps
        gaps = self._detect_silence_gaps(audio, min_gap_duration)
        
        if not gaps:
            return audio  # No gaps to fill
        
        # Convert to numpy for processing
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)
        
        # Handle stereo
        if audio.channels == 2:
            samples = samples.reshape(-1, 2)
        
        # Fill each gap
        for start_time, duration in gaps:
            start_sample = int(start_time * self.sample_rate)
            end_sample = int((start_time + duration) * self.sample_rate)
            
            if end_sample > len(samples):
                end_sample = len(samples)
            
            gap_length = end_sample - start_sample
            
            # Determine fill style
            if fill_style == "smart":
                # Choose based on gap length and surrounding context
                if duration < 1.0:
                    style = "vinyl"
                elif duration < 3.0:
                    style = "room"
                else:
                    style = "ambient"
            else:
                style = fill_style
            
            # Generate fill material
            if style == "vinyl":
                fill_audio = self._generate_vinyl_noise(gap_length)
            elif style == "ambient":
                fill_audio = self._generate_ambient_pad(gap_length, start_time)
            elif style == "room":
                fill_audio = self._generate_room_tone(gap_length)
            else:
                fill_audio = self._generate_vinyl_noise(gap_length)
            
            # Apply volume
            fill_audio = fill_audio * fill_volume
            
            # Crossfade into/out of the gap
            fade_length = min(gap_length // 10, int(0.1 * self.sample_rate))
            
            if fade_length > 0:
                fade_in = np.linspace(0, 1, fade_length)
                fade_out = np.linspace(1, 0, fade_length)
                
                if audio.channels == 2:
                    fill_audio[:fade_length, :] *= fade_in[:, np.newaxis]
                    fill_audio[-fade_length:, :] *= fade_out[:, np.newaxis]
                    
                    # Crossfade with existing audio
                    samples[start_sample:start_sample+fade_length] *= (1 - fade_in[:, np.newaxis])
                    samples[end_sample-fade_length:end_sample] *= (1 - fade_out[:, np.newaxis])
                else:
                    fill_audio[:fade_length] *= fade_in
                    fill_audio[-fade_length:] *= fade_out
                    
                    samples[start_sample:start_sample+fade_length] *= (1 - fade_in)
                    samples[end_sample-fade_length:end_sample] *= (1 - fade_out)
            
            # Insert fill material
            samples[start_sample:end_sample] += fill_audio
        
        # Convert back to AudioSegment
        if audio.channels == 2:
            samples = samples.flatten()
        
        samples = np.clip(samples, -1.0, 1.0)
        samples = (samples * (2**15)).astype(np.int16)
        
        return AudioSegment(
            samples.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=audio.channels
        )
    
    def _detect_silence_gaps(self, audio: AudioSegment, 
                            min_duration: float) -> List[Tuple[float, float]]:
        """
        Detect silence gaps
        Returns list of (start_time, duration) tuples
        """
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)
        
        # Convert stereo to mono for detection
        if audio.channels == 2:
            samples = samples.reshape(-1, 2)
            samples = np.mean(samples, axis=1)
        
        # Silence threshold (STRICTER: -55dB instead of -60dB)
        silence_threshold = 0.0018  # Catch more subtle gaps
        
        # Detect silent regions
        is_silent = np.abs(samples) < silence_threshold
        
        # Find contiguous silent regions
        gaps = []
        in_silence = False
        silence_start = 0
        
        for i, silent in enumerate(is_silent):
            if silent and not in_silence:
                in_silence = True
                silence_start = i
            elif not silent and in_silence:
                in_silence = False
                duration = (i - silence_start) / self.sample_rate
                
                if duration >= min_duration:
                    start_time = silence_start / self.sample_rate
                    gaps.append((start_time, duration))
        
        # Handle case where audio ends in silence
        if in_silence:
            duration = (len(samples) - silence_start) / self.sample_rate
            if duration >= min_duration:
                start_time = silence_start / self.sample_rate
                gaps.append((start_time, duration))
        
        return gaps
    
    def _generate_vinyl_noise(self, num_samples: int) -> np.ndarray:
        """
        Generate vinyl/tape noise (crackle, hiss, rumble)
        """
        # Base noise
        noise = np.random.randn(num_samples) * 0.05
        
        # Add crackle (random pops)
        num_pops = int(num_samples / self.sample_rate * 3)  # ~3 pops per second
        for _ in range(num_pops):
            pop_pos = random.randint(0, num_samples - 100)
            pop_amplitude = random.uniform(0.1, 0.3) * random.choice([-1, 1])
            
            # Short pop with exponential decay
            pop_length = random.randint(20, 80)
            decay = np.exp(-np.arange(pop_length) / 10)
            pop = pop_amplitude * decay
            
            noise[pop_pos:pop_pos+pop_length] += pop
        
        # Filter to vinyl character
        # High-pass to remove DC
        sos_hp = signal.butter(2, 20, 'highpass', fs=self.sample_rate, output='sos')
        noise = signal.sosfilt(sos_hp, noise)
        
        # Slight low-pass for warmth
        sos_lp = signal.butter(1, 12000, 'lowpass', fs=self.sample_rate, output='sos')
        noise = signal.sosfilt(sos_lp, noise)
        
        # Add subtle rumble (very low frequency)
        t = np.arange(num_samples) / self.sample_rate
        rumble = np.sin(2 * np.pi * 33 * t) * 0.02  # 33Hz (like turntable)
        rumble += np.sin(2 * np.pi * 45 * t + 1.2) * 0.015
        
        # Stereo version (slightly different L/R)
        left = noise + rumble
        right = noise * 0.95 + rumble * 1.05
        
        return np.stack([left, right], axis=1)
    
    def _generate_ambient_pad(self, num_samples: int, 
                             start_time: float) -> np.ndarray:
        """
        Generate ambient pad texture (sustained tones)
        """
        t = np.arange(num_samples) / self.sample_rate
        
        # Choose frequencies based on time (for variety)
        seed = int(start_time * 100)
        random.seed(seed)
        
        # Base frequencies (musical intervals)
        root_freq = random.choice([65.41, 82.41, 110.0, 130.81])  # C2, E2, A2, C3
        
        # Generate multiple sine waves (chord)
        pad = np.zeros(num_samples)
        
        # Root
        pad += np.sin(2 * np.pi * root_freq * t) * 0.3
        
        # Fifth
        pad += np.sin(2 * np.pi * root_freq * 1.5 * t) * 0.25
        
        # Octave
        pad += np.sin(2 * np.pi * root_freq * 2.0 * t) * 0.2
        
        # Major third (slight detune for shimmer)
        pad += np.sin(2 * np.pi * root_freq * 1.25 * t + 0.1) * 0.15
        
        # Add subtle vibrato
        vibrato_lfo = np.sin(2 * np.pi * 0.3 * t) * 0.002
        pad_vibrato = np.sin(2 * np.pi * root_freq * t * (1 + vibrato_lfo)) * 0.3
        pad = pad * 0.7 + pad_vibrato * 0.3
        
        # Envelope (slow attack and release)
        attack_samples = min(num_samples // 4, int(2.0 * self.sample_rate))
        release_samples = min(num_samples // 4, int(2.0 * self.sample_rate))
        
        envelope = np.ones(num_samples)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples) ** 2
        envelope[-release_samples:] = np.linspace(1, 0, release_samples) ** 2
        
        pad *= envelope
        
        # Apply filtering for warmth
        sos = signal.butter(2, 3000, 'lowpass', fs=self.sample_rate, output='sos')
        pad = signal.sosfilt(sos, pad)
        
        # Add subtle white noise for texture
        noise = np.random.randn(num_samples) * 0.02
        sos_noise = signal.butter(2, [800, 4000], 'bandpass', fs=self.sample_rate, output='sos')
        noise = signal.sosfilt(sos_noise, noise)
        pad += noise
        
        # Stereo (slightly detuned L/R)
        right = np.sin(2 * np.pi * root_freq * 1.001 * t) * 0.3  # Slightly sharp
        right += np.sin(2 * np.pi * root_freq * 1.5 * 0.999 * t) * 0.25
        right += np.sin(2 * np.pi * root_freq * 2.0 * t) * 0.2
        right *= envelope
        right = signal.sosfilt(sos, right)
        right += noise * 0.95
        
        return np.stack([pad, right], axis=1)
    
    def _generate_room_tone(self, num_samples: int) -> np.ndarray:
        """
        Generate room tone (subtle background ambience)
        """
        # Very low amplitude pink noise
        # Generate white noise
        white_noise = np.random.randn(num_samples)
        
        # Convert to pink noise (1/f spectrum)
        # Use simple filter approximation
        pink_noise = np.zeros_like(white_noise)
        
        # Pinking filter (simple approximation)
        b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
        a = np.array([1, -2.494956002, 2.017265875, -0.522189400])
        
        pink_noise = signal.lfilter(b, a, white_noise)
        
        # Very low amplitude
        pink_noise *= 0.03
        
        # Filter to "room" character (mostly low-mids)
        sos = signal.butter(2, [100, 2000], 'bandpass', fs=self.sample_rate, output='sos')
        room_tone = signal.sosfilt(sos, pink_noise)
        
        # Add very subtle low-frequency rumble
        t = np.arange(num_samples) / self.sample_rate
        rumble = np.sin(2 * np.pi * 40 * t) * 0.01
        rumble += np.sin(2 * np.pi * 55 * t + 0.7) * 0.008
        
        room_tone += rumble
        
        # Stereo (uncorrelated noise for width)
        right_noise = np.random.randn(num_samples)
        right_pink = signal.lfilter(b, a, right_noise) * 0.03
        right_room = signal.sosfilt(sos, right_pink) + rumble * 1.05
        
        return np.stack([room_tone, right_room], axis=1)
    
    def add_continuous_ambience(self, audio: AudioSegment,
                               ambience_type: str = "subtle",
                               volume: float = 0.1) -> AudioSegment:
        """
        Add continuous ambient layer throughout entire track
        
        Args:
            audio: Input audio
            ambience_type: "subtle", "vinyl", "tape", "room"
            volume: Ambience volume (0.0-1.0)
        """
        num_samples = int(audio.duration_seconds * self.sample_rate)
        
        if ambience_type == "vinyl":
            ambience = self._generate_vinyl_noise(num_samples)
        elif ambience_type == "tape":
            # Similar to vinyl but less crackle
            ambience = self._generate_vinyl_noise(num_samples) * 0.7
        elif ambience_type == "room":
            ambience = self._generate_room_tone(num_samples)
        else:  # subtle
            # Combination of room tone and very quiet vinyl
            ambience = self._generate_room_tone(num_samples) * 0.7
            ambience += self._generate_vinyl_noise(num_samples) * 0.3
        
        # Apply volume
        ambience *= volume
        
        # Convert original audio to numpy
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)
        
        if audio.channels == 2:
            samples = samples.reshape(-1, 2)
        else:
            # Convert mono to stereo for mixing
            samples = np.stack([samples, samples], axis=1)
        
        # Ensure ambience matches length
        if len(ambience) > len(samples):
            ambience = ambience[:len(samples)]
        elif len(ambience) < len(samples):
            # Pad with zeros
            padding = np.zeros((len(samples) - len(ambience), 2))
            ambience = np.vstack([ambience, padding])
        
        # Mix
        output = samples + ambience
        
        # Convert back
        output = output.flatten()
        output = np.clip(output, -1.0, 1.0)
        output = (output * (2**15)).astype(np.int16)
        
        return AudioSegment(
            output.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=2  # Always output stereo
        )
