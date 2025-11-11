"""
Effects Processor - Apply audio effects using Pedalboard
"""

from pydub import AudioSegment
from pedalboard import (
    Pedalboard, Reverb, Delay, Distortion, Chorus, 
    LadderFilter, Phaser, Compressor, Gain, Limiter
)
from pedalboard.io import AudioFile
import numpy as np
import tempfile
import os


class EffectsProcessor:
    """Apply various audio effects to audio files"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def apply_effect(self, input_file: str, effect_type: str, 
                     mix: float = 0.5, intensity: float = 0.5) -> AudioSegment:
        """
        Apply an effect to an audio file
        
        Args:
            input_file: Path to input audio file
            effect_type: Type of effect (reverb, delay, distortion, etc.)
            mix: Wet/dry mix (0.0 = dry, 1.0 = wet)
            intensity: Effect intensity (0.0 to 1.0)
        
        Returns:
            Processed AudioSegment
        """
        effect_type = effect_type.lower()
        
        if effect_type == "reverb":
            return self._apply_reverb(input_file, mix, intensity)
        elif effect_type == "delay":
            return self._apply_delay(input_file, mix, intensity)
        elif effect_type == "distortion":
            return self._apply_distortion(input_file, mix, intensity)
        elif effect_type == "chorus":
            return self._apply_chorus(input_file, mix, intensity)
        elif effect_type == "filter":
            return self._apply_filter(input_file, mix, intensity)
        elif effect_type == "phaser":
            return self._apply_phaser(input_file, mix, intensity)
        elif effect_type == "bitcrush":
            return self._apply_bitcrush(input_file, intensity)
        else:
            raise ValueError(f"Unknown effect type: {effect_type}")
    
    def _process_with_pedalboard(self, input_file: str, board: Pedalboard, 
                                  mix: float = 1.0) -> AudioSegment:
        """
        Process audio file with a pedalboard
        
        Args:
            input_file: Input file path
            board: Pedalboard with effects
            mix: Wet/dry mix
        
        Returns:
            Processed AudioSegment
        """
        # Read input file
        with AudioFile(input_file) as f:
            audio = f.read(f.frames)
            sample_rate = f.samplerate
        
        # Process with pedalboard
        effected = board(audio, sample_rate)
        
        # Mix dry and wet signals
        if mix < 1.0:
            effected = (1 - mix) * audio + mix * effected
        
        # Convert back to AudioSegment
        return self._array_to_audiosegment(effected, sample_rate)
    
    def _array_to_audiosegment(self, audio_array: np.ndarray, sample_rate: int) -> AudioSegment:
        """Convert numpy array to AudioSegment"""
        # Ensure audio is 2D (channels, samples)
        if audio_array.ndim == 1:
            audio_array = audio_array.reshape(1, -1)
        
        # Normalize and convert to int16
        audio_array = audio_array.T  # Transpose to (samples, channels)
        audio_array = np.clip(audio_array, -1.0, 1.0)
        audio_int16 = (audio_array * 32767).astype(np.int16)
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Write to temporary file
            channels = audio_int16.shape[1] if audio_int16.ndim > 1 else 1
            audio_segment = AudioSegment(
                audio_int16.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=channels
            )
            audio_segment.export(tmp_path, format='wav')
            
            # Read back as AudioSegment
            result = AudioSegment.from_wav(tmp_path)
            return result
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def _apply_reverb(self, input_file: str, mix: float, intensity: float) -> AudioSegment:
        """Apply reverb effect"""
        # Map intensity to reverb parameters
        room_size = 0.1 + (intensity * 0.8)  # 0.1 to 0.9
        damping = 0.5
        wet_level = mix
        dry_level = 1.0 - mix
        
        board = Pedalboard([
            Reverb(room_size=room_size, damping=damping, 
                   wet_level=wet_level, dry_level=dry_level)
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=1.0)
    
    def _apply_delay(self, input_file: str, mix: float, intensity: float) -> AudioSegment:
        """Apply delay effect"""
        # Map intensity to delay time
        delay_seconds = 0.1 + (intensity * 0.4)  # 0.1 to 0.5 seconds
        feedback = 0.3 + (intensity * 0.4)  # 0.3 to 0.7
        
        board = Pedalboard([
            Delay(delay_seconds=delay_seconds, feedback=feedback, mix=mix)
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=1.0)
    
    def _apply_distortion(self, input_file: str, mix: float, intensity: float) -> AudioSegment:
        """Apply distortion effect"""
        # Map intensity to drive amount
        drive_db = 5 + (intensity * 35)  # 5 to 40 dB
        
        board = Pedalboard([
            Distortion(drive_db=drive_db),
            Gain(gain_db=-6)  # Compensate for volume increase
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=mix)
    
    def _apply_chorus(self, input_file: str, mix: float, intensity: float) -> AudioSegment:
        """Apply chorus effect"""
        # Map intensity to chorus parameters
        rate_hz = 0.5 + (intensity * 4.5)  # 0.5 to 5 Hz
        depth = 0.1 + (intensity * 0.4)    # 0.1 to 0.5
        
        board = Pedalboard([
            Chorus(rate_hz=rate_hz, depth=depth, centre_delay_ms=7.0, 
                   feedback=0.0, mix=mix)
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=1.0)
    
    def _apply_filter(self, input_file: str, mix: float, intensity: float) -> AudioSegment:
        """Apply lowpass filter effect"""
        # Map intensity to cutoff frequency
        # Lower intensity = lower cutoff (more filtering)
        cutoff_hz = 200 + (intensity * 4800)  # 200 Hz to 5000 Hz
        
        board = Pedalboard([
            LadderFilter(mode=LadderFilter.Mode.LPF12, cutoff_hz=cutoff_hz, 
                        resonance=0.3, drive=1.0)
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=mix)
    
    def _apply_phaser(self, input_file: str, mix: float, intensity: float) -> AudioSegment:
        """Apply phaser effect"""
        # Map intensity to phaser parameters
        rate_hz = 0.5 + (intensity * 4.5)  # 0.5 to 5 Hz
        depth = 0.5 + (intensity * 0.5)    # 0.5 to 1.0
        
        board = Pedalboard([
            Phaser(rate_hz=rate_hz, depth=depth, centre_frequency_hz=1300.0,
                   feedback=0.5, mix=mix)
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=1.0)
    
    def _apply_bitcrush(self, input_file: str, intensity: float) -> AudioSegment:
        """Apply bitcrush effect (lo-fi)"""
        # Load audio
        audio = AudioSegment.from_file(input_file)
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # Map intensity to bit depth (lower intensity = more crushing)
        # intensity 0.0 = 4 bits, 1.0 = 16 bits
        bit_depth = int(4 + (intensity * 12))
        
        # Reduce bit depth
        max_val = 2 ** bit_depth
        samples = np.round(samples / (32768 / max_val)) * (32768 / max_val)
        samples = np.clip(samples, -32768, 32767).astype(np.int16)
        
        # Create new AudioSegment
        return AudioSegment(
            samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
    
    def create_chain(self, input_file: str, effects: list) -> AudioSegment:
        """
        Apply a chain of effects
        
        Args:
            input_file: Input audio file
            effects: List of effect dicts with 'type', 'mix', 'intensity'
        
        Returns:
            Processed AudioSegment
        """
        audio = AudioSegment.from_file(input_file)
        
        # Create temporary file for intermediate processing
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            audio.export(tmp_path, format='wav')
            
            # Apply each effect in sequence
            for effect in effects:
                effect_type = effect.get('type', 'reverb')
                mix = effect.get('mix', 0.5)
                intensity = effect.get('intensity', 0.5)
                
                audio = self.apply_effect(tmp_path, effect_type, mix, intensity)
                audio.export(tmp_path, format='wav')
            
            return audio
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def compress(self, input_file: str, threshold_db: float = -20, 
                 ratio: float = 4) -> AudioSegment:
        """
        Apply dynamic range compression
        
        Args:
            input_file: Input audio file
            threshold_db: Compression threshold in dB
            ratio: Compression ratio
        
        Returns:
            Compressed AudioSegment
        """
        board = Pedalboard([
            Compressor(threshold_db=threshold_db, ratio=ratio),
            Limiter(threshold_db=-1.0)  # Prevent clipping
        ])
        
        return self._process_with_pedalboard(input_file, board, mix=1.0)
