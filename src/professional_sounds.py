"""
Professional Sound Generator - High-quality realistic sounds using advanced synthesis
Combines FluidSynth soundfonts with enhanced physical modeling
"""

import numpy as np
from pydub import AudioSegment
from scipy import signal
from typing import Optional, Dict, List
import random
import warnings

# Try to import FluidSynth, but don't fail if not available
try:
    import fluidsynth
    FLUIDSYNTH_AVAILABLE = True
except ImportError:
    FLUIDSYNTH_AVAILABLE = False
    warnings.warn("FluidSynth not available. Using enhanced synthesis fallback.")


class ProfessionalSoundGenerator:
    """Generate professional-quality realistic sounds"""
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
        self.fs = None
        self.soundfont_path = None
        
        # Try to initialize FluidSynth with default soundfont
        if FLUIDSYNTH_AVAILABLE:
            self._try_init_fluidsynth()
    
    def _try_init_fluidsynth(self):
        """Try to initialize FluidSynth with available soundfonts"""
        # Common soundfont locations
        possible_soundfonts = [
            '/usr/share/sounds/sf2/FluidR3_GM.sf2',
            '/usr/share/soundfonts/FluidR3_GM.sf2',
            '/usr/share/sounds/sf2/default.sf2',
            'FluidR3_GM.sf2',
        ]
        
        try:
            self.fs = fluidsynth.Synth(samplerate=float(self.sample_rate))
            self.fs.start()
            
            # Try to load a soundfont
            for sf_path in possible_soundfonts:
                try:
                    sfid = self.fs.sfload(sf_path)
                    if sfid != -1:
                        self.soundfont_path = sf_path
                        self.fs.program_select(0, sfid, 0, 0)  # Piano
                        print(f"✓ Loaded soundfont: {sf_path}")
                        break
                except:
                    continue
                    
            if not self.soundfont_path:
                print("⚠ No soundfont found. Using enhanced synthesis.")
                self.fs = None
                
        except Exception as e:
            print(f"⚠ FluidSynth initialization failed: {e}")
            self.fs = None
    
    def generate_realistic_kick(self, variation: float = 0.5) -> AudioSegment:
        """
        Generate ultra-realistic kick drum using multi-layer synthesis
        Models real acoustic kick drum physics
        """
        duration = 0.6  # 600ms
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Layer 1: Sub-bass click (beater hitting the drum head)
        attack_freq = 150 + random.uniform(-10, 10) * variation
        decay_freq = 45 + random.uniform(-3, 3) * variation
        freq_envelope = attack_freq * np.exp(-30 * t) + decay_freq
        phase = 2 * np.pi * np.cumsum(freq_envelope) / self.sample_rate
        
        # Ultra-fast attack for beater impact (1ms)
        attack_samples = int(0.001 * self.sample_rate)
        attack_env = np.ones(samples)
        attack_env[:attack_samples] = np.linspace(0, 1, attack_samples) ** 0.3
        
        layer1 = np.sin(phase) * attack_env
        
        # Layer 2: Body resonance (drum shell)
        body_freq = 65 + random.uniform(-2, 2) * variation
        body_wave = np.sin(2 * np.pi * body_freq * t)
        
        # Add octave for thickness
        body_wave += 0.5 * np.sin(2 * np.pi * body_freq * 2 * t)
        
        # Realistic body envelope
        body_envelope = np.exp(-3.5 * t) * (1 - np.exp(-50 * t))
        layer2 = body_wave * body_envelope
        
        # Layer 3: High-frequency beater click (2-6kHz transient)
        click_freq = 3500 + random.uniform(-500, 500) * variation
        click_wave = np.sin(2 * np.pi * click_freq * t)
        click_envelope = np.exp(-250 * t)  # Very fast decay
        layer3 = click_wave * click_envelope * 0.3
        
        # Layer 4: Noise layer (drumhead texture)
        noise = np.random.uniform(-1, 1, samples)
        # Bandpass filter for realistic drum noise (200-800 Hz)
        b_noise, a_noise = signal.butter(4, [200, 800], btype='bandpass', 
                                         fs=self.sample_rate)
        noise_filtered = signal.filtfilt(b_noise, a_noise, noise)
        noise_envelope = np.exp(-40 * t)
        layer4 = noise_filtered * noise_envelope * 0.15
        
        # Layer 5: Room resonance (low-frequency room mode)
        room_freq = 80
        room_wave = np.sin(2 * np.pi * room_freq * t)
        room_envelope = np.exp(-2 * t) * (1 - np.exp(-10 * t))
        layer5 = room_wave * room_envelope * 0.2
        
        # Mix all layers
        kick = (layer1 * 0.9 + layer2 * 0.85 + layer3 * 0.4 + 
                layer4 * 0.25 + layer5 * 0.3)
        
        # Master envelope
        master_envelope = np.exp(-3.8 * t)
        kick *= master_envelope
        
        # Apply soft saturation for analog warmth
        kick = np.tanh(kick * 1.2)
        
        # Normalize with punch preservation
        peak = np.max(np.abs(kick))
        if peak > 0:
            kick = kick / peak * 0.92
        
        # Convert to int32 (24-bit in 32-bit container)
        kick_int = (kick * (2**23 - 1)).astype(np.int32)
        
        # Create AudioSegment
        audio = AudioSegment(
            kick_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,
            channels=1
        )
        
        return audio
    
    def generate_realistic_snare(self, variation: float = 0.5) -> AudioSegment:
        """
        Generate ultra-realistic snare drum using physical modeling
        """
        duration = 0.25  # 250ms
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Layer 1: Drum head tone (fundamental ~200Hz)
        head_freq = 200 + random.uniform(-15, 15) * variation
        head_wave = np.sin(2 * np.pi * head_freq * t)
        
        # Add overtones for realistic drum head
        head_wave += 0.4 * np.sin(2 * np.pi * head_freq * 1.7 * t)  # Non-harmonic
        head_wave += 0.2 * np.sin(2 * np.pi * head_freq * 2.3 * t)
        
        head_envelope = np.exp(-18 * t)
        layer1 = head_wave * head_envelope
        
        # Layer 2: Snare wires (high-frequency buzzing)
        wire_noise = np.random.uniform(-1, 1, samples)
        
        # Bandpass for snare wire character (3kHz-10kHz)
        b_wire, a_wire = signal.butter(6, [3000, 10000], btype='bandpass',
                                       fs=self.sample_rate)
        wire_filtered = signal.filtfilt(b_wire, a_wire, wire_noise)
        
        # Snare wire envelope (longer than body)
        wire_envelope = np.exp(-12 * t) + 0.15 * np.exp(-6 * t)
        layer2 = wire_filtered * wire_envelope
        
        # Layer 3: Stick attack transient
        attack_noise = np.random.uniform(-1, 1, samples)
        b_attack, a_attack = signal.butter(4, [2000, 8000], btype='bandpass',
                                          fs=self.sample_rate)
        attack_filtered = signal.filtfilt(b_attack, a_attack, attack_noise)
        attack_envelope = np.exp(-80 * t)
        layer3 = attack_filtered * attack_envelope * 0.8
        
        # Layer 4: Body resonance
        body_freq = 350 + random.uniform(-20, 20) * variation
        body_wave = np.sin(2 * np.pi * body_freq * t)
        body_envelope = np.exp(-25 * t)
        layer4 = body_wave * body_envelope * 0.3
        
        # Mix layers
        snare = (layer1 * 0.5 + layer2 * 0.9 + layer3 * 0.6 + layer4 * 0.4)
        
        # Apply compression-like saturation
        snare = np.tanh(snare * 1.5)
        
        # Normalize
        peak = np.max(np.abs(snare))
        if peak > 0:
            snare = snare / peak * 0.88
        
        # Convert to int32
        snare_int = (snare * (2**23 - 1)).astype(np.int32)
        
        audio = AudioSegment(
            snare_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,
            channels=1
        )
        
        return audio
    
    def generate_realistic_hihat(self, closed: bool = True, 
                                 variation: float = 0.3) -> AudioSegment:
        """
        Generate realistic hi-hat using metallic resonance modeling
        """
        duration = 0.15 if closed else 0.35
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Generate metallic noise spectrum
        noise = np.random.uniform(-1, 1, samples)
        
        if closed:
            # Closed hi-hat: tighter frequency range (6kHz-14kHz)
            b, a = signal.butter(8, [6000, 14000], btype='bandpass',
                                fs=self.sample_rate)
            decay_rate = 35 + random.uniform(-5, 5) * variation
        else:
            # Open hi-hat: wider frequency range (4kHz-16kHz)
            b, a = signal.butter(8, [4000, 16000], btype='bandpass',
                                fs=self.sample_rate)
            decay_rate = 8 + random.uniform(-2, 2) * variation
        
        hihat = signal.filtfilt(b, a, noise)
        
        # Add metallic resonances (specific frequencies for cymbal)
        resonances = [7500, 9300, 11200, 13400]
        for freq in resonances:
            resonance = np.sin(2 * np.pi * (freq + random.uniform(-100, 100)) * t)
            hihat += resonance * 0.15
        
        # Envelope
        envelope = np.exp(-decay_rate * t)
        
        # Add stick attack
        attack_samples = int(0.002 * self.sample_rate)
        attack = np.ones(samples)
        attack[:attack_samples] = np.linspace(0, 1, attack_samples) ** 0.2
        
        hihat = hihat * envelope * attack
        
        # Subtle saturation
        hihat = np.tanh(hihat * 1.1)
        
        # Normalize
        peak = np.max(np.abs(hihat))
        if peak > 0:
            hihat = hihat / peak * (0.65 if closed else 0.7)
        
        # Convert to int32
        hihat_int = (hihat * (2**23 - 1)).astype(np.int32)
        
        audio = AudioSegment(
            hihat_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,
            channels=1
        )
        
        return audio
    
    def generate_realistic_piano(self, frequency: float, duration: float,
                                velocity: float = 0.8,
                                variation: float = 0.5) -> AudioSegment:
        """
        Generate ultra-realistic piano using FluidSynth or advanced physical modeling
        """
        # Try FluidSynth first for maximum realism
        if self.fs and self.soundfont_path:
            return self._generate_soundfont_piano(frequency, duration, velocity)
        
        # Fallback to enhanced physical modeling
        return self._generate_modeled_piano(frequency, duration, velocity, variation)
    
    def _generate_soundfont_piano(self, frequency: float, duration: float,
                                 velocity: float) -> AudioSegment:
        """Generate piano using FluidSynth soundfont (most realistic)"""
        # Convert frequency to MIDI note
        midi_note = int(69 + 12 * np.log2(frequency / 440.0))
        midi_velocity = int(velocity * 127)
        
        # Generate note
        self.fs.noteon(0, midi_note, midi_velocity)
        
        # Calculate samples needed
        samples = int(duration * self.sample_rate)
        
        # Get audio from FluidSynth
        audio_data = self.fs.get_samples(samples)
        audio_array = np.array(audio_data, dtype=np.float32)
        
        # Stop note
        self.fs.noteoff(0, midi_note)
        
        # Normalize
        peak = np.max(np.abs(audio_array))
        if peak > 0:
            audio_array = audio_array / peak * 0.85
        
        # Convert to int32
        audio_int = (audio_array * (2**23 - 1)).astype(np.int32)
        
        audio = AudioSegment(
            audio_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,
            channels=1
        )
        
        return audio
    
    def _generate_modeled_piano(self, frequency: float, duration: float,
                               velocity: float, variation: float) -> AudioSegment:
        """
        Enhanced physical modeling piano (fallback when FluidSynth not available)
        Improved from previous version with better inharmonicity and resonance
        """
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # 16 harmonics with advanced inharmonicity (better piano physics)
        num_harmonics = 16
        inharmonicity = 0.0003 * (1 + variation * 0.1)
        
        signal_sum = np.zeros(samples)
        
        for n in range(1, num_harmonics + 1):
            # Inharmonic frequency (real piano string behavior)
            freq_n = frequency * n * np.sqrt(1 + inharmonicity * n**2)
            
            # Harmonic amplitude (depends on hammer position and string)
            if n == 1:
                amplitude = 1.0
            elif n <= 3:
                amplitude = 0.6 / n
            elif n <= 7:
                amplitude = 0.4 / n
            else:
                amplitude = 0.2 / n**1.5
            
            # Velocity affects brightness (more high harmonics at high velocity)
            amplitude *= (1.0 if n == 1 else velocity ** (0.5 + n * 0.05))
            
            # Individual decay rates (higher harmonics decay faster)
            decay_rate = 0.8 + n * 0.15 + random.uniform(-0.05, 0.05) * variation
            
            # Generate harmonic with decay
            harmonic = amplitude * np.sin(2 * np.pi * freq_n * t)
            harmonic *= np.exp(-decay_rate * t)
            
            signal_sum += harmonic
        
        # Advanced ADSR with random humanization
        attack_time = random.uniform(0.008, 0.012) * (1 + variation * 0.3)
        decay_time = random.uniform(0.12, 0.16) * (1 + variation * 0.2)
        sustain_level = random.uniform(0.65, 0.75)
        release_start = duration * 0.7
        
        envelope = np.ones(samples)
        
        # Attack
        attack_samples = int(attack_time * self.sample_rate)
        if attack_samples > 0:
            envelope[:attack_samples] = (np.linspace(0, 1, attack_samples) ** 1.5)
        
        # Decay
        decay_samples = int(decay_time * self.sample_rate)
        decay_end = attack_samples + decay_samples
        if decay_samples > 0 and decay_end < samples:
            envelope[attack_samples:decay_end] = np.linspace(1, sustain_level, 
                                                             decay_samples)
            envelope[decay_end:] = sustain_level
        
        # Release
        release_sample = int(release_start * self.sample_rate)
        release_samples = samples - release_sample
        if release_samples > 0:
            envelope[release_sample:] *= np.linspace(1, 0, release_samples) ** 2
        
        signal_sum *= envelope
        
        # Add vibrato on sustain (natural piano string vibration)
        vibrato_rate = random.uniform(5.2, 5.8)
        vibrato_depth = 0.006
        vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
        vibrato[:attack_samples] = 1  # No vibrato during attack
        signal_sum *= vibrato
        
        # Sympathetic string resonances (other strings vibrating)
        octave_resonance = 0.08 * np.sin(2 * np.pi * frequency * 2 * t)
        octave_resonance *= np.exp(-1.5 * t)
        signal_sum += octave_resonance
        
        # Soundboard resonance (piano body)
        board_resonances = [frequency * 1.5, frequency * 2.5]
        for board_freq in board_resonances:
            resonance = 0.04 * np.sin(2 * np.pi * board_freq * t)
            resonance *= np.exp(-2.5 * t)
            signal_sum += resonance
        
        # Room reflections (improved - more realistic)
        reflection_delays = [0.008, 0.017, 0.025, 0.033, 0.042]
        for delay in reflection_delays:
            delay_samples = int(delay * self.sample_rate)
            if delay_samples < samples:
                reflection = np.zeros(samples)
                reflection[delay_samples:] = signal_sum[:-delay_samples]
                signal_sum += reflection * (0.12 / (1 + delay * 10))
        
        # Subtle analog warmth
        signal_sum = np.tanh(signal_sum * 0.9)
        
        # Normalize
        peak = np.max(np.abs(signal_sum))
        if peak > 0:
            signal_sum = signal_sum / peak * 0.82
        
        # Convert to int32
        piano_int = (signal_sum * (2**23 - 1)).astype(np.int32)
        
        audio = AudioSegment(
            piano_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,
            channels=1
        )
        
        return audio
    
    def cleanup(self):
        """Clean up FluidSynth resources"""
        if self.fs:
            self.fs.delete()
