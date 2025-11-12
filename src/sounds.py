"""
Sound Generator - Synthesize various types of sounds
"""

from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, WhiteNoise
import numpy as np
from typing import Optional


class SoundGenerator:
    """Generate synthesized sounds and drum samples with premium quality"""
    
    def __init__(self, sample_rate: int = 96000):  # Premium 96kHz for maximum quality
        self.sample_rate = sample_rate
        self.noise_floor = -96  # dB - Very low noise floor
        
    def _normalize_premium(self, signal: np.ndarray, target_db: float = -6.0) -> np.ndarray:
        """
        Premium normalization with headroom and RMS balancing
        
        Args:
            signal: Input signal
            target_db: Target dB level (default -6dB for headroom)
        
        Returns:
            Normalized signal
        """
        # Calculate RMS
        rms = np.sqrt(np.mean(signal ** 2))
        
        if rms > 0:
            # Target RMS based on dB
            target_rms = 10 ** (target_db / 20)
            # Normalize to target RMS
            signal = signal * (target_rms / rms)
        
        # Prevent clipping
        max_val = np.max(np.abs(signal))
        if max_val > 1.0:
            signal = signal / max_val * 0.99
        
        return signal
    
    def _apply_noise_gate(self, signal: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """
        Apply noise gate to remove low-level noise
        
        Args:
            signal: Input signal
            threshold: Gate threshold (0-1)
        
        Returns:
            Gated signal
        """
        mask = np.abs(signal) > threshold
        return signal * mask
    
    def _add_subtle_analog_warmth(self, signal: np.ndarray, amount: float = 0.02) -> np.ndarray:
        """
        Add subtle analog-style warmth (very subtle harmonic distortion)
        
        Args:
            signal: Input signal
            amount: Amount of warmth (0-1)
        
        Returns:
            Warmed signal
        """
        # Very subtle soft clipping for warmth
        warmed = np.tanh(signal * (1 + amount * 0.5)) / (1 + amount * 0.5)
        return warmed
    
    def generate(self, sound_type: str, duration: float = 1.0, frequency: Optional[int] = None) -> AudioSegment:
        """
        Generate a sound based on type
        
        Args:
            sound_type: Type of sound (kick, snare, hihat, bass, synth, noise)
            duration: Duration in seconds
            frequency: Frequency in Hz (for tonal sounds)
        
        Returns:
            Generated AudioSegment
        """
        sound_type = sound_type.lower()
        
        if sound_type == "kick":
            return self.generate_kick(duration)
        elif sound_type == "snare":
            return self.generate_snare(duration)
        elif sound_type == "hihat":
            return self.generate_hihat(duration)
        elif sound_type == "bass":
            freq = frequency or 80
            return self.generate_bass(duration, freq)
        elif sound_type == "synth":
            freq = frequency or 440
            return self.generate_synth(duration, freq)
        elif sound_type == "noise":
            return self.generate_noise(duration)
        else:
            raise ValueError(f"Unknown sound type: {sound_type}")
    
    def generate_kick(self, duration: float = 0.5) -> AudioSegment:
        """
        Generate a kick drum sound with improved quality
        
        Args:
            duration: Duration in seconds
        
        Returns:
            Kick drum AudioSegment
        """
        # Kick drum: pitch sweep from high to low frequency
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Frequency sweep from 200Hz to 50Hz for punchier kick
        freq_start = 200
        freq_end = 50
        freq = np.logspace(np.log10(freq_start), np.log10(freq_end), samples)
        
        # Generate sine wave with frequency sweep
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        kick = np.sin(phase)
        
        # Add harmonics for more punch
        kick += 0.3 * np.sin(2 * phase)
        kick += 0.15 * np.sin(3 * phase)
        
        # Improved envelope with sharper attack
        attack_samples = int(0.005 * self.sample_rate)  # 5ms attack
        decay_samples = samples - attack_samples
        
        envelope = np.ones(samples)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[attack_samples:] = np.exp(-5 * np.linspace(0, 1, decay_samples))
        
        kick = kick * envelope
        
        # Add click for attack
        click = np.random.randn(int(0.01 * self.sample_rate)) * 0.2
        click_env = np.exp(-100 * np.linspace(0, 1, len(click)))
        click = click * click_env
        
        # Combine kick with click
        kick[:len(click)] += click
        
        # Normalize and convert to AudioSegment
        kick = (kick / np.max(np.abs(kick)) * 32767 * 0.95).astype(np.int16)
        audio = AudioSegment(
            kick.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        # Add some punch with boost
        return audio + 6  # +6dB boost
    
    def generate_snare(self, duration: float = 0.2) -> AudioSegment:
        """
        Generate a snare drum sound
        
        Args:
            duration: Duration in seconds
        
        Returns:
            Snare drum AudioSegment
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Combine sine wave (body) and noise (snare)
        # Body: 200Hz tone
        body = np.sin(2 * np.pi * 200 * t)
        
        # Snare: filtered white noise
        noise = np.random.randn(samples)
        
        # Mix: 40% body, 60% noise
        snare = 0.4 * body + 0.6 * noise
        
        # Apply sharp decay envelope
        envelope = np.exp(-10 * t / duration)
        snare = snare * envelope
        
        # Normalize
        snare = snare / np.max(np.abs(snare))
        snare = (snare * 32767 * 0.8).astype(np.int16)
        
        return AudioSegment(
            snare.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
    
    def generate_hihat(self, duration: float = 0.1) -> AudioSegment:
        """
        Generate a hi-hat sound
        
        Args:
            duration: Duration in seconds
        
        Returns:
            Hi-hat AudioSegment
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Hi-hat: high-frequency filtered noise
        noise = np.random.randn(samples)
        
        # High-pass filter simulation (combine multiple high frequencies)
        hihat = noise
        for freq in [8000, 10000, 12000]:
            hihat += np.sin(2 * np.pi * freq * t) * noise
        
        # Very sharp decay
        envelope = np.exp(-30 * t / duration)
        hihat = hihat * envelope
        
        # Normalize
        hihat = hihat / np.max(np.abs(hihat))
        hihat = (hihat * 32767 * 0.6).astype(np.int16)
        
        return AudioSegment(
            hihat.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
    
    def generate_bass(self, duration: float = 1.0, frequency: int = 80) -> AudioSegment:
        """
        Generate a bass tone
        
        Args:
            duration: Duration in seconds
            frequency: Frequency in Hz (default 80Hz)
        
        Returns:
            Bass AudioSegment
        """
        # Use sawtooth wave for rich bass sound
        generator = Sawtooth(frequency)
        audio = generator.to_audio_segment(duration=int(duration * 1000))
        
        # Add sub harmonic
        sub = Sine(frequency / 2).to_audio_segment(duration=int(duration * 1000))
        audio = audio.overlay(sub - 6)  # Sub at -6dB
        
        # Apply ADSR envelope
        attack = int(duration * 1000 * 0.05)  # 5% attack
        release = int(duration * 1000 * 0.2)   # 20% release
        
        audio = audio.fade_in(attack).fade_out(release)
        
        return audio
    
    def generate_synth(self, duration: float = 1.0, frequency: int = 440, waveform: str = "sine") -> AudioSegment:
        """
        Generate a synthesizer tone
        
        Args:
            duration: Duration in seconds
            frequency: Frequency in Hz (default 440Hz = A4)
            waveform: Waveform type (sine, square, sawtooth)
        
        Returns:
            Synth AudioSegment
        """
        duration_ms = int(duration * 1000)
        
        if waveform == "sine":
            generator = Sine(frequency)
        elif waveform == "square":
            generator = Square(frequency)
        elif waveform == "sawtooth":
            generator = Sawtooth(frequency)
        else:
            generator = Sine(frequency)
        
        audio = generator.to_audio_segment(duration=duration_ms)
        
        # Apply envelope
        attack = min(50, duration_ms // 10)
        release = min(100, duration_ms // 5)
        
        audio = audio.fade_in(attack).fade_out(release)
        
        return audio
    
    def generate_noise(self, duration: float = 1.0, color: str = "white") -> AudioSegment:
        """
        Generate noise
        
        Args:
            duration: Duration in seconds
            color: Type of noise (white, pink)
        
        Returns:
            Noise AudioSegment
        """
        duration_ms = int(duration * 1000)
        
        if color == "white":
            generator = WhiteNoise()
            audio = generator.to_audio_segment(duration=duration_ms)
        else:
            # White noise fallback
            generator = WhiteNoise()
            audio = generator.to_audio_segment(duration=duration_ms)
        
        # Reduce volume to prevent clipping
        audio = audio - 10
        
        return audio
    
    def generate_chord(self, frequencies: list[int], duration: float = 1.0) -> AudioSegment:
        """
        Generate a chord from multiple frequencies
        
        Args:
            frequencies: List of frequencies in Hz
            duration: Duration in seconds
        
        Returns:
            Chord AudioSegment
        """
        if not frequencies:
            raise ValueError("No frequencies provided")
        
        # Generate first note
        chord = self.generate_synth(duration, frequencies[0])
        
        # Overlay remaining notes
        for freq in frequencies[1:]:
            note = self.generate_synth(duration, freq)
            chord = chord.overlay(note)
        
        # Normalize to prevent clipping
        chord = chord - 6  # Reduce by 6dB
        
        return chord
    
    def generate_arpeggio(self, frequencies: list[int], note_duration: float = 0.25) -> AudioSegment:
        """
        Generate an arpeggio (sequential chord notes)
        
        Args:
            frequencies: List of frequencies for the chord
            note_duration: Duration of each note in seconds
        
        Returns:
            Arpeggio AudioSegment
        """
        arpeggio = AudioSegment.silent(duration=0)
        for freq in frequencies:
            note = self.generate_synth(note_duration, freq)
            arpeggio += note
        return arpeggio
    
    def generate_piano(self, frequency: int, duration: float = 1.0, velocity: float = 0.8) -> AudioSegment:
        """
        Generate a realistic piano sound using additive synthesis
        
        Args:
            frequency: Base frequency in Hz
            duration: Duration in seconds
            velocity: Note velocity (0.0 to 1.0)
        
        Returns:
            Piano note AudioSegment
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Piano harmonics with decreasing amplitudes
        harmonics = [
            (1.0, 1.0),      # Fundamental
            (2.0, 0.8),      # 2nd harmonic
            (3.0, 0.6),      # 3rd harmonic
            (4.0, 0.4),      # 4th harmonic
            (5.0, 0.25),     # 5th harmonic
            (6.0, 0.15),     # 6th harmonic
            (7.0, 0.1),      # 7th harmonic
            (8.0, 0.05),     # 8th harmonic
        ]
        
        # Generate complex waveform
        signal = np.zeros(samples)
        for harmonic, amplitude in harmonics:
            signal += amplitude * np.sin(2 * np.pi * frequency * harmonic * t)
        
        # ADSR Envelope (Attack, Decay, Sustain, Release)
        attack_time = 0.01  # 10ms attack
        decay_time = 0.1    # 100ms decay
        sustain_level = 0.7
        release_time = 0.3  # 300ms release
        
        attack_samples = int(attack_time * self.sample_rate)
        decay_samples = int(decay_time * self.sample_rate)
        release_samples = int(release_time * self.sample_rate)
        sustain_samples = samples - attack_samples - decay_samples - release_samples
        
        envelope = np.zeros(samples)
        
        # Attack
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        decay_start = attack_samples
        decay_end = decay_start + decay_samples
        envelope[decay_start:decay_end] = np.linspace(1, sustain_level, decay_samples)
        
        # Sustain
        sustain_start = decay_end
        sustain_end = sustain_start + sustain_samples
        envelope[sustain_start:sustain_end] = sustain_level
        
        # Release
        if release_samples > 0:
            envelope[sustain_end:] = np.linspace(sustain_level, 0, release_samples)
        
        # Apply envelope and velocity
        signal = signal * envelope * velocity
        
        # Normalize to 16-bit range
        signal = np.int16(signal / np.max(np.abs(signal)) * 32767 * 0.9)
        
        # Convert to AudioSegment with higher bit depth
        audio = AudioSegment(
            signal.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        return audio
    
    def generate_pad(self, frequency: int, duration: float = 2.0, brightness: float = 0.5) -> AudioSegment:
        """
        Generate an ambient pad sound
        
        Args:
            frequency: Base frequency in Hz
            duration: Duration in seconds
            brightness: Filter brightness (0.0 to 1.0)
        
        Returns:
            Pad AudioSegment
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Multiple detuned oscillators for richness
        detune_amounts = [-7, -3, 0, 3, 7]  # cents
        signal = np.zeros(samples)
        
        for cents in detune_amounts:
            freq_detune = frequency * (2 ** (cents / 1200))
            
            # Mix of sine and sawtooth for warmth
            sine_wave = np.sin(2 * np.pi * freq_detune * t)
            saw_wave = 2 * (t * freq_detune % 1) - 1
            
            signal += 0.6 * sine_wave + 0.4 * saw_wave
        
        signal /= len(detune_amounts)
        
        # Slow attack and release for pad characteristics
        attack_samples = int(0.5 * self.sample_rate)
        release_samples = int(0.8 * self.sample_rate)
        
        envelope = np.ones(samples)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples) ** 2
        envelope[-release_samples:] = np.linspace(1, 0, release_samples) ** 2
        
        signal = signal * envelope
        
        # Apply low-pass filter based on brightness
        cutoff_freq = 500 + brightness * 3000
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        from scipy import signal as scipy_signal
        b, a = scipy_signal.butter(2, normalized_cutoff, btype='low')
        signal = scipy_signal.filtfilt(b, a, signal)
        
        # Normalize
        signal = np.int16(signal / np.max(np.abs(signal)) * 32767 * 0.7)
        
        audio = AudioSegment(
            signal.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        return audio
    
    def generate_sub_bass(self, frequency: int, duration: float = 1.0) -> AudioSegment:
        """
        Generate a sub-bass sound (below 100Hz)
        
        Args:
            frequency: Base frequency in Hz (typically 40-80Hz)
            duration: Duration in seconds
        
        Returns:
            Sub-bass AudioSegment
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Pure sine wave for sub-bass
        signal = np.sin(2 * np.pi * frequency * t)
        
        # Add slight harmonics for presence
        signal += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
        signal += 0.1 * np.sin(2 * np.pi * frequency * 3 * t)
        
        # Envelope
        attack_samples = int(0.02 * self.sample_rate)
        release_samples = int(0.1 * self.sample_rate)
        
        envelope = np.ones(samples)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if release_samples > 0 and release_samples < samples:
            envelope[-release_samples:] = np.linspace(1, 0, release_samples)
        
        signal = signal * envelope
        
        # Normalize
        signal = np.int16(signal / np.max(np.abs(signal)) * 32767 * 0.95)
        
        audio = AudioSegment(
            signal.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        return audio
    
    def generate_ambient_texture(self, duration: float = 4.0, 
                                 texture_type: str = 'warm') -> AudioSegment:
        """
        Generate ambient texture/atmosphere
        
        Args:
            duration: Duration in seconds
            texture_type: Type of texture ('warm', 'dark', 'bright', 'spacey')
        
        Returns:
            Ambient texture AudioSegment
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        if texture_type == 'warm':
            # Warm pad-like texture
            frequencies = [220, 277, 330, 440]  # A3, C#4, E4, A4
        elif texture_type == 'dark':
            frequencies = [55, 82, 110, 165]    # A1, E2, A2, E3
        elif texture_type == 'bright':
            frequencies = [440, 554, 659, 880]  # A4, C#5, E5, A5
        else:  # spacey
            frequencies = [110, 165, 220, 330]  # A2, E3, A3, E4
        
        signal = np.zeros(samples)
        
        for freq in frequencies:
            # Generate evolving sine waves with LFO
            lfo = 0.2 * np.sin(2 * np.pi * 0.1 * t)  # Slow modulation
            phase = 2 * np.pi * freq * t + lfo
            signal += np.sin(phase)
        
        signal /= len(frequencies)
        
        # Very slow fade in/out
        fade_samples = samples // 4
        envelope = np.ones(samples)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples) ** 3
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples) ** 3
        
        signal = signal * envelope
        
        # Add subtle noise for texture
        noise = np.random.randn(samples) * 0.05
        signal += noise
        
        # Normalize
        signal = np.int16(signal / np.max(np.abs(signal)) * 32767 * 0.6)
        
        audio = AudioSegment(
            signal.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        return audio
