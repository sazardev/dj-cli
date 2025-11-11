"""
Sound Generator - Synthesize various types of sounds
"""

from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, WhiteNoise
import numpy as np
from typing import Optional


class SoundGenerator:
    """Generate synthesized sounds and drum samples"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
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
        Generate a kick drum sound
        
        Args:
            duration: Duration in seconds
        
        Returns:
            Kick drum AudioSegment
        """
        # Kick drum: pitch sweep from high to low frequency
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Frequency sweep from 150Hz to 40Hz
        freq_start = 150
        freq_end = 40
        freq = np.logspace(np.log10(freq_start), np.log10(freq_end), samples)
        
        # Generate sine wave with frequency sweep
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        kick = np.sin(phase)
        
        # Apply exponential decay envelope
        envelope = np.exp(-5 * t / duration)
        kick = kick * envelope
        
        # Normalize and convert to AudioSegment
        kick = (kick * 32767).astype(np.int16)
        audio = AudioSegment(
            kick.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        # Add some punch with overdrive
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
        Generate an arpeggio (notes played in sequence)
        
        Args:
            frequencies: List of frequencies in Hz
            note_duration: Duration of each note in seconds
        
        Returns:
            Arpeggio AudioSegment
        """
        if not frequencies:
            raise ValueError("No frequencies provided")
        
        # Generate first note
        arpeggio = self.generate_synth(note_duration, frequencies[0])
        
        # Append remaining notes
        for freq in frequencies[1:]:
            note = self.generate_synth(note_duration, freq)
            arpeggio = arpeggio + note
        
        return arpeggio
