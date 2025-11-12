"""
Sound Generator - Synthesize various types of sounds
"""

from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, WhiteNoise
import numpy as np
import random
from typing import Optional

# Import professional sound generator
try:
    from .professional_sounds import ProfessionalSoundGenerator
    PROFESSIONAL_MODE = True
except ImportError:
    PROFESSIONAL_MODE = False
    print("⚠ Professional sounds not available, using standard synthesis")


class SoundGenerator:
    """Generate synthesized sounds and drum samples with premium quality"""
    
    def __init__(self, sample_rate: int = 96000, use_professional: bool = True):
        """
        Initialize sound generator
        
        Args:
            sample_rate: Sample rate in Hz (default 96kHz)
            use_professional: Use professional realistic sounds if available
        """
        self.sample_rate = sample_rate
        self.noise_floor = -96  # dB - Very low noise floor
        self.use_professional = use_professional and PROFESSIONAL_MODE
        
        # Initialize professional sound generator if available
        if self.use_professional:
            self.pro_gen = ProfessionalSoundGenerator(sample_rate)
            print("✓ Professional realistic sound engine active")
        else:
            self.pro_gen = None
        
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
    
    def generate_kick(self, duration: float = 0.5, variation: float = 0.0) -> AudioSegment:
        """
        Generate a premium kick drum with advanced synthesis
        Uses professional realistic synthesis if available
        
        Args:
            duration: Duration in seconds
            variation: Random variation amount (0-1)
        
        Returns:
            Premium kick drum AudioSegment
        """
        # Use professional realistic kick if available
        if self.use_professional and self.pro_gen:
            return self.pro_gen.generate_realistic_kick(variation)
        
        # Fallback to enhanced synthesis
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Random variations within musical rules
        start_freq = 200 + random.uniform(-10, 10) * variation
        end_freq = 50 + random.uniform(-5, 5) * variation
        
        # More complex frequency sweep with multiple curves
        freq_sweep = np.logspace(np.log10(start_freq), np.log10(end_freq), samples)
        
        # Add micro-variations to frequency (simulates analog)
        if variation > 0:
            freq_modulation = 1 + 0.01 * variation * np.sin(2 * np.pi * 10 * t)
            freq_sweep = freq_sweep * freq_modulation
        
        # Generate multiple oscillators for richness
        phase = 2 * np.pi * np.cumsum(freq_sweep) / self.sample_rate
        
        # Main oscillator (sine)
        kick = np.sin(phase)
        
        # Add harmonics with careful tuning
        kick += 0.25 * np.sin(2 * phase)  # 2nd harmonic
        kick += 0.12 * np.sin(3 * phase)  # 3rd harmonic
        kick += 0.06 * np.sin(4 * phase)  # 4th harmonic
        
        # Advanced envelope with curves
        attack_samples = int(0.003 * self.sample_rate)  # 3ms ultra-fast attack
        decay_samples = samples - attack_samples
        
        envelope = np.ones(samples)
        
        # Attack with exponential curve
        if attack_samples > 0:
            envelope[:attack_samples] = 1 - np.exp(-5 * np.linspace(0, 1, attack_samples))
        
        # Decay with custom curve for punch
        decay_curve = np.linspace(0, 1, decay_samples)
        envelope[attack_samples:] = np.exp(-4.5 * decay_curve) * (1 - 0.3 * decay_curve)
        
        kick = kick * envelope
        
        # Add transient click for definition
        click_samples = int(0.008 * self.sample_rate)
        click = np.random.randn(click_samples) * 0.15
        click_env = np.exp(-150 * np.linspace(0, 1, click_samples))
        click = click * click_env
        
        # Combine with careful gain staging
        kick[:len(click)] += click
        
        # Premium normalization
        kick = self._normalize_premium(kick, target_db=-3.0)
        
        # Apply noise gate
        kick = self._apply_noise_gate(kick, threshold=0.005)
        
        # Add subtle analog warmth
        kick = self._add_subtle_analog_warmth(kick, amount=0.015)
        
        # Convert to 24-bit integer for higher resolution
        kick = np.int32(kick * (2**23 - 1))
        
        # Convert to AudioSegment
        audio = AudioSegment(
            kick.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,  # 32-bit (24-bit in container)
            channels=1
        )
        
        return audio
    
    def generate_snare(self, duration: float = 0.2, variation: float = 0.5) -> AudioSegment:
        """
        Generate a snare drum sound
        Uses professional realistic synthesis if available
        
        Args:
            duration: Duration in seconds
            variation: Random variation amount (0-1)
        
        Returns:
            Snare drum AudioSegment
        """
        # Use professional realistic snare if available
        if self.use_professional and self.pro_gen:
            return self.pro_gen.generate_realistic_snare(variation)
        
        # Fallback to basic synthesis
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
    
    def generate_hihat(self, duration: float = 0.1, closed: bool = True, 
                      variation: float = 0.3) -> AudioSegment:
        """
        Generate a hi-hat sound
        Uses professional realistic synthesis if available
        
        Args:
            duration: Duration in seconds
            closed: True for closed hi-hat, False for open
            variation: Random variation amount (0-1)
        
        Returns:
            Hi-hat AudioSegment
        """
        # Use professional realistic hi-hat if available
        if self.use_professional and self.pro_gen:
            return self.pro_gen.generate_realistic_hihat(closed, variation)
        
        # Fallback to basic synthesis
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
    
    def generate_piano(self, frequency: int, duration: float = 1.0, 
                      velocity: float = 0.8, variation: float = 0.0) -> AudioSegment:
        """
        Generate a premium realistic piano sound with intelligent variations
        Uses professional soundfont or advanced physical modeling if available
        
        Args:
            frequency: Base frequency in Hz
            duration: Duration in seconds
            velocity: Note velocity (0.0 to 1.0)
            variation: Random variation amount (0-1) for humanization
        
        Returns:
            Premium piano note AudioSegment
        """
        # Use professional realistic piano if available (soundfont or enhanced modeling)
        if self.use_professional and self.pro_gen:
            return self.pro_gen.generate_realistic_piano(frequency, duration, velocity, variation)
        
        # Fallback to standard synthesis
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Intelligent harmonic structure with mathematical precision
        # Based on real piano string physics
        harmonics = [
            (1.0, 1.000, 0.00),   # Fundamental
            (2.0, 0.850, 0.02),   # 2nd - slightly detuned
            (3.0, 0.650, 0.01),   # 3rd
            (4.0, 0.450, 0.03),   # 4th - more detuned
            (5.0, 0.280, 0.02),   # 5th
            (6.0, 0.180, 0.04),   # 6th
            (7.0, 0.120, 0.03),   # 7th - inharmonicity
            (8.0, 0.070, 0.05),   # 8th - more inharmonicity
            (9.0, 0.045, 0.04),   # 9th
            (10.0, 0.028, 0.06),  # 10th
            (11.0, 0.018, 0.05),  # 11th
            (12.0, 0.011, 0.07),  # 12th
        ]
        
        # Generate complex waveform with inharmonicity
        signal = np.zeros(samples)
        
        for harmonic_num, amplitude, inharmonicity in harmonics:
            # Add slight random variation for realism
            freq_variation = 1.0
            amp_variation = 1.0
            
            if variation > 0:
                freq_variation = 1 + (random.uniform(-0.002, 0.002) * variation)
                amp_variation = 1 + (random.uniform(-0.1, 0.1) * variation)
            
            # Inharmonic frequency (higher harmonics are progressively more sharp)
            freq_ratio = harmonic_num * (1 + inharmonicity * harmonic_num)
            actual_freq = frequency * freq_ratio * freq_variation
            
            # Phase with slight randomness for realism
            phase_offset = random.uniform(0, 2 * np.pi) * variation if variation > 0 else 0
            
            # Generate harmonic
            harmonic_signal = amplitude * amp_variation * np.sin(
                2 * np.pi * actual_freq * t + phase_offset
            )
            
            # Each harmonic decays at different rate (higher = faster)
            decay_rate = 2.0 + harmonic_num * 0.3
            harmonic_env = np.exp(-decay_rate * t / duration)
            
            signal += harmonic_signal * harmonic_env
        
        # Advanced ADSR Envelope with realistic piano characteristics
        attack_time = 0.008 + random.uniform(-0.002, 0.002) * variation  # 6-10ms
        decay_time = 0.12 + random.uniform(-0.02, 0.02) * variation      # 100-140ms
        sustain_level = 0.65 + random.uniform(-0.05, 0.05) * variation   # 60-70%
        release_time = 0.35 + random.uniform(-0.05, 0.05) * variation    # 300-400ms
        
        attack_samples = int(attack_time * self.sample_rate)
        decay_samples = int(decay_time * self.sample_rate)
        release_samples = int(release_time * self.sample_rate)
        sustain_samples = samples - attack_samples - decay_samples - release_samples
        
        if sustain_samples < 0:
            sustain_samples = 0
            release_samples = samples - attack_samples - decay_samples
        
        envelope = np.zeros(samples)
        idx = 0
        
        # Attack - exponential curve for natural piano strike
        if attack_samples > 0:
            attack_curve = 1 - np.exp(-5 * np.linspace(0, 1, attack_samples))
            envelope[idx:idx+attack_samples] = attack_curve
            idx += attack_samples
        
        # Decay - logarithmic curve
        if decay_samples > 0:
            decay_curve = np.logspace(0, np.log10(sustain_level), decay_samples)
            envelope[idx:idx+decay_samples] = decay_curve
            idx += decay_samples
        
        # Sustain - with subtle vibrato
        if sustain_samples > 0:
            vibrato_freq = 5.5 + random.uniform(-0.5, 0.5) * variation  # 5-6 Hz
            vibrato_depth = 0.008 * variation  # Subtle
            sustain_curve = sustain_level * (1 + vibrato_depth * np.sin(
                2 * np.pi * vibrato_freq * np.linspace(0, sustain_samples/self.sample_rate, sustain_samples)
            ))
            envelope[idx:idx+sustain_samples] = sustain_curve
            idx += sustain_samples
        
        # Release - smooth exponential
        if release_samples > 0 and idx < samples:
            actual_release = min(release_samples, samples - idx)
            release_curve = sustain_level * np.exp(-4 * np.linspace(0, 1, actual_release))
            envelope[idx:idx+actual_release] = release_curve
        
        # Apply envelope and velocity
        signal = signal * envelope * velocity
        
        # Add very subtle room ambience (early reflections)
        if variation > 0:
            room_delay_ms = [8, 15, 23, 31]  # Early reflection times
            for delay_ms in room_delay_ms:
                delay_samples = int(delay_ms * self.sample_rate / 1000)
                if delay_samples < len(signal):
                    reflection_gain = 0.03 * variation
                    padded_signal = np.pad(signal, (delay_samples, 0))[:len(signal)]
                    signal += padded_signal * reflection_gain
        
        # Premium normalization
        signal = self._normalize_premium(signal, target_db=-8.0)
        
        # Noise gate to remove any low-level artifacts
        signal = self._apply_noise_gate(signal, threshold=0.002)
        
        # Subtle analog warmth
        signal = self._add_subtle_analog_warmth(signal, amount=0.01)
        
        # Convert to 24-bit
        signal = np.int32(signal * (2**23 - 1))
        
        audio = AudioSegment(
            signal.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,
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
