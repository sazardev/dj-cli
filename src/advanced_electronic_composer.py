"""
Advanced Electronic Music Composer
Dubstep, wobble bass, complex automation, professional EDM production
"""

import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, WhiteNoise
from scipy import signal
from typing import List, Tuple, Dict, Optional
import random


class WobbleBassGenerator:
    """Generate authentic dubstep wobble bass with LFO modulation"""
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
    
    def generate_wobble(self, 
                       frequency: float,
                       duration: float,
                       wobble_rate: float = 4.0,  # Hz
                       wobble_depth: float = 0.9,
                       distortion: float = 0.7,
                       sub_mix: float = 0.6) -> AudioSegment:
        """
        Generate wobble bass with LFO filter modulation
        
        Args:
            frequency: Base frequency (Hz)
            duration: Duration in seconds
            wobble_rate: LFO rate in Hz (typical: 2-8 Hz)
            wobble_depth: Filter modulation depth (0-1)
            distortion: Harmonic distortion amount (0-1)
            sub_mix: Sub-bass layer mix (0-1)
        """
        num_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, num_samples, endpoint=False)
        
        # 1. Generate rich harmonics with multiple oscillators
        osc1 = np.sin(2 * np.pi * frequency * t)  # Fundamental
        osc2 = 0.5 * signal.sawtooth(2 * np.pi * frequency * t)  # Sawtooth for harmonics
        osc3 = 0.3 * signal.square(2 * np.pi * frequency * 1.5 * t)  # Detuned square
        
        # Mix oscillators
        raw_signal = osc1 + osc2 + osc3
        
        # 2. Apply waveshaping distortion for more harmonics
        if distortion > 0:
            raw_signal = np.tanh(raw_signal * (1 + distortion * 3))
        
        # 3. Generate LFO for filter cutoff modulation
        lfo = np.sin(2 * np.pi * wobble_rate * t)
        
        # Map LFO to filter cutoff (200 Hz to 8000 Hz)
        min_cutoff = 200
        max_cutoff = 8000
        cutoff_freq = min_cutoff + (max_cutoff - min_cutoff) * (0.5 + 0.5 * lfo * wobble_depth)
        
        # 4. Apply time-varying lowpass filter (wobble effect)
        filtered = self._apply_variable_lowpass(raw_signal, cutoff_freq, self.sample_rate)
        
        # 5. Add resonance peaks
        filtered = self._add_resonance(filtered, cutoff_freq, self.sample_rate, q_factor=8.0)
        
        # 6. Generate sub-bass layer (clean sine wave)
        sub_bass = np.sin(2 * np.pi * frequency * 0.5 * t)  # One octave down
        
        # Mix main wobble with sub-bass
        mixed = filtered * (1 - sub_mix) + sub_bass * sub_mix
        
        # 7. Apply envelope (ADSR)
        envelope = self._generate_adsr_envelope(num_samples, 
                                               attack=0.01, decay=0.1, 
                                               sustain=0.8, release=0.15)
        mixed *= envelope
        
        # 8. Normalize and convert to AudioSegment
        mixed = self._normalize(mixed, target_db=-3.0)
        
        return self._array_to_audiosegment(mixed)
    
    def _apply_variable_lowpass(self, audio: np.ndarray, 
                               cutoff_freqs: np.ndarray,
                               sample_rate: int) -> np.ndarray:
        """Apply time-varying lowpass filter"""
        filtered = np.zeros_like(audio)
        chunk_size = 1024
        
        for i in range(0, len(audio), chunk_size):
            end = min(i + chunk_size, len(audio))
            chunk = audio[i:end]
            
            # Use average cutoff for this chunk
            avg_cutoff = np.mean(cutoff_freqs[i:end])
            nyquist = sample_rate / 2
            normalized_cutoff = avg_cutoff / nyquist
            normalized_cutoff = np.clip(normalized_cutoff, 0.001, 0.999)
            
            # Design and apply butterworth filter
            b, a = signal.butter(4, normalized_cutoff, btype='low')
            filtered[i:end] = signal.filtfilt(b, a, chunk)
        
        return filtered
    
    def _add_resonance(self, audio: np.ndarray, 
                      cutoff_freqs: np.ndarray,
                      sample_rate: int,
                      q_factor: float = 8.0) -> np.ndarray:
        """Add resonance peak at cutoff frequency"""
        resonant = np.zeros_like(audio)
        chunk_size = 1024
        
        for i in range(0, len(audio), chunk_size):
            end = min(i + chunk_size, len(audio))
            chunk = audio[i:end]
            
            avg_cutoff = np.mean(cutoff_freqs[i:end])
            nyquist = sample_rate / 2
            normalized_cutoff = avg_cutoff / nyquist
            normalized_cutoff = np.clip(normalized_cutoff, 0.01, 0.99)
            
            # Peaking EQ at cutoff frequency
            b, a = signal.iirpeak(normalized_cutoff, q_factor)
            resonant[i:end] = signal.filtfilt(b, a, chunk)
        
        # Mix resonance with original
        return audio * 0.7 + resonant * 0.3
    
    def _generate_adsr_envelope(self, num_samples: int,
                               attack: float, decay: float,
                               sustain: float, release: float) -> np.ndarray:
        """Generate ADSR envelope"""
        envelope = np.ones(num_samples)
        sample_rate = self.sample_rate
        
        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        release_samples = int(release * sample_rate)
        
        # Attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        if decay_samples > 0:
            decay_end = attack_samples + decay_samples
            envelope[attack_samples:decay_end] = np.linspace(1, sustain, decay_samples)
        
        # Sustain (already set to 1, will be multiplied by sustain level)
        sustain_start = attack_samples + decay_samples
        sustain_end = num_samples - release_samples
        if sustain_end > sustain_start:
            envelope[sustain_start:sustain_end] = sustain
        
        # Release
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
        
        return envelope
    
    def _normalize(self, audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
        """Normalize audio to target dB"""
        max_val = np.abs(audio).max()
        if max_val > 0:
            target_amplitude = 10 ** (target_db / 20.0)
            audio = audio * (target_amplitude / max_val)
        return audio
    
    def _array_to_audiosegment(self, audio: np.ndarray) -> AudioSegment:
        """Convert numpy array to AudioSegment"""
        # Convert to 16-bit PCM
        audio_int = np.int16(audio * 32767)
        return AudioSegment(
            audio_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )


class DubstepPatternGenerator:
    """Generate authentic dubstep drum patterns"""
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
    
    def generate_halfstep_pattern(self, bpm: int, bars: int) -> Dict[str, List[float]]:
        """
        Generate dubstep half-time pattern
        Kick on 1, snare on 3 (half-time feel at 70 BPM when track is 140 BPM)
        """
        beat_duration = 60.0 / bpm  # Duration of one beat in seconds
        bar_duration = beat_duration * 4
        
        kick_hits = []
        snare_hits = []
        hihat_hits = []
        
        for bar in range(bars):
            bar_start = bar * bar_duration
            
            # Kick on beat 1 and 1.5 (syncopation)
            kick_hits.append(bar_start)
            kick_hits.append(bar_start + beat_duration * 0.5)
            
            # Snare on beat 3 (half-time)
            snare_hits.append(bar_start + beat_duration * 2)
            
            # Hi-hats on 16th notes (creates tension)
            for sixteenth in range(16):
                hihat_hits.append(bar_start + sixteenth * (beat_duration / 4))
        
        return {
            'kick': kick_hits,
            'snare': snare_hits,
            'hihat': hihat_hits
        }
    
    def generate_snare_roll(self, start_time: float, duration: float, 
                           density: str = 'medium') -> List[float]:
        """
        Generate snare roll build-up
        density: 'low' (8th), 'medium' (16th), 'high' (32nd), 'insane' (64th)
        """
        densities = {
            'low': 8,
            'medium': 16,
            'high': 32,
            'insane': 64
        }
        
        num_hits = densities.get(density, 16)
        interval = duration / num_hits
        
        return [start_time + i * interval for i in range(num_hits)]
    
    def generate_glitch_hits(self, start_time: float, duration: float,
                            num_hits: int = 8) -> List[Tuple[float, float]]:
        """
        Generate random glitch hits with varying pitch
        Returns list of (time, pitch_shift) tuples
        """
        hits = []
        for i in range(num_hits):
            time = start_time + random.uniform(0, duration)
            pitch_shift = random.uniform(-12, 12)  # Semitones
            hits.append((time, pitch_shift))
        
        return sorted(hits)


class AdvancedElectronicComposer:
    """Professional dubstep/electronic music composer"""
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
        self.wobble_gen = WobbleBassGenerator(sample_rate)
        self.pattern_gen = DubstepPatternGenerator(sample_rate)
    
    def compose_dubstep_track(self, 
                             bpm: int = 140,
                             key: str = 'E',
                             total_bars: int = 64) -> AudioSegment:
        """
        Compose complete dubstep track with:
        - Atmospheric intro
        - Intense build-up with risers
        - Massive drop with wobble bass
        - Emotional breakdown
        - Second drop even heavier
        - Outro
        """
        print("\n🎼 ADVANCED DUBSTEP COMPOSER")
        print("="*60)
        print(f"🎵 Creating epic dubstep track: {bpm} BPM in {key}")
        print(f"📊 Structure: {total_bars} bars")
        print("="*60)
        
        # Calculate timing
        beat_duration = 60.0 / bpm
        bar_duration = beat_duration * 4
        
        # Define structure
        structure = {
            'intro': {'bars': 8, 'start': 0},
            'buildup1': {'bars': 8, 'start': 8},
            'drop1': {'bars': 16, 'start': 16},
            'breakdown': {'bars': 8, 'start': 32},
            'buildup2': {'bars': 8, 'start': 40},
            'drop2': {'bars': 16, 'start': 48},
            'outro': {'bars': 8, 'start': 64}
        }
        
        # Initialize empty track
        total_duration = total_bars * bar_duration * 1000  # milliseconds
        track = AudioSegment.silent(duration=int(total_duration))
        
        print("\n🏗️  Building sections...")
        
        # 1. INTRO - Atmospheric
        print("  📍 Intro (atmospheric pads & ambient)")
        intro_audio = self._create_intro_section(
            structure['intro']['start'] * bar_duration,
            structure['intro']['bars'] * bar_duration,
            key, bpm
        )
        track = track.overlay(intro_audio)
        
        # 2. BUILD-UP 1 - Tension rising
        print("  📍 Build-up 1 (snare rolls, risers, tension)")
        buildup1_audio = self._create_buildup_section(
            structure['buildup1']['start'] * bar_duration,
            structure['buildup1']['bars'] * bar_duration,
            key, bpm, intensity=0.7
        )
        track = track.overlay(buildup1_audio)
        
        # 3. DROP 1 - MASSIVE
        print("  📍 Drop 1 (WOBBLE BASS, heavy drums)")
        drop1_audio = self._create_drop_section(
            structure['drop1']['start'] * bar_duration,
            structure['drop1']['bars'] * bar_duration,
            key, bpm, wobble_intensity=0.8
        )
        track = track.overlay(drop1_audio)
        
        # 4. BREAKDOWN - Emotional
        print("  📍 Breakdown (emotional, melodic)")
        breakdown_audio = self._create_breakdown_section(
            structure['breakdown']['start'] * bar_duration,
            structure['breakdown']['bars'] * bar_duration,
            key, bpm
        )
        track = track.overlay(breakdown_audio)
        
        # 5. BUILD-UP 2 - Even more intense
        print("  📍 Build-up 2 (INTENSE snare rolls)")
        buildup2_audio = self._create_buildup_section(
            structure['buildup2']['start'] * bar_duration,
            structure['buildup2']['bars'] * bar_duration,
            key, bpm, intensity=1.0
        )
        track = track.overlay(buildup2_audio)
        
        # 6. DROP 2 - ABSOLUTELY MASSIVE
        print("  📍 Drop 2 (EPIC wobble, all out)")
        drop2_audio = self._create_drop_section(
            structure['drop2']['start'] * bar_duration,
            structure['drop2']['bars'] * bar_duration,
            key, bpm, wobble_intensity=1.0
        )
        track = track.overlay(drop2_audio)
        
        # 7. OUTRO
        print("  📍 Outro (fade out)")
        outro_audio = self._create_outro_section(
            structure['outro']['start'] * bar_duration,
            structure['outro']['bars'] * bar_duration,
            key, bpm
        )
        track = track.overlay(outro_audio)
        
        print("\n✅ Composition complete!")
        print("="*60)
        
        return track
    
    def _create_intro_section(self, start_time: float, duration: float,
                             key: str, bpm: int) -> AudioSegment:
        """Create atmospheric intro"""
        # Placeholder - would generate ambient pads, atmospheric sounds
        return AudioSegment.silent(duration=int(duration * 1000))
    
    def _create_buildup_section(self, start_time: float, duration: float,
                               key: str, bpm: int, intensity: float) -> AudioSegment:
        """Create build-up with risers and snare rolls"""
        # Placeholder - would generate risers, white noise, snare rolls
        return AudioSegment.silent(duration=int(duration * 1000))
    
    def _create_drop_section(self, start_time: float, duration: float,
                            key: str, bpm: int, wobble_intensity: float) -> AudioSegment:
        """Create massive drop with wobble bass"""
        section = AudioSegment.silent(duration=int(duration * 1000))
        
        # Generate wobble bass pattern
        bar_duration = (60.0 / bpm) * 4
        num_bars = int(duration / bar_duration)
        
        for bar in range(num_bars):
            bar_start = bar * bar_duration * 1000  # milliseconds
            
            # Generate wobble bass note (E2 = 82.41 Hz)
            wobble = self.wobble_gen.generate_wobble(
                frequency=82.41,
                duration=bar_duration * 0.9,
                wobble_rate=random.uniform(3.5, 6.0),
                wobble_depth=wobble_intensity,
                distortion=0.7 + wobble_intensity * 0.2
            )
            
            section = section.overlay(wobble, position=int(bar_start))
        
        return section
    
    def _create_breakdown_section(self, start_time: float, duration: float,
                                 key: str, bpm: int) -> AudioSegment:
        """Create emotional breakdown"""
        # Placeholder - would generate melodic elements
        return AudioSegment.silent(duration=int(duration * 1000))
    
    def _create_outro_section(self, start_time: float, duration: float,
                             key: str, bpm: int) -> AudioSegment:
        """Create outro with fade"""
        # Placeholder - would fade out elements
        return AudioSegment.silent(duration=int(duration * 1000))
