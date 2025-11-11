"""
Audio Engine - Core audio playback and manipulation
"""

from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf
import librosa
import numpy as np
from typing import Optional, Dict, List
import os


class AudioEngine:
    """Main audio engine for playback and processing"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def play_file(self, file_path: str, volume: float = 1.0, loop: bool = False):
        """
        Play an audio file
        
        Args:
            file_path: Path to audio file
            volume: Volume level (0.0 to 2.0)
            loop: Whether to loop playback
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        audio = AudioSegment.from_file(file_path)
        
        # Adjust volume (in dB)
        if volume != 1.0:
            # Convert linear volume to dB
            db_change = 20 * np.log10(volume)
            audio = audio + db_change
        
        if loop:
            # Loop until interrupted
            while True:
                try:
                    play(audio)
                except KeyboardInterrupt:
                    break
        else:
            play(audio)
    
    def load_audio(self, file_path: str) -> AudioSegment:
        """Load an audio file and return AudioSegment"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        return AudioSegment.from_file(file_path)
    
    def mix_files(self, file_paths: List[str], crossfade: int = 0) -> AudioSegment:
        """
        Mix multiple audio files together
        
        Args:
            file_paths: List of audio file paths
            crossfade: Crossfade duration in milliseconds
        
        Returns:
            Mixed AudioSegment
        """
        if not file_paths:
            raise ValueError("No files provided for mixing")
        
        # Load first file
        mixed = self.load_audio(file_paths[0])
        
        # Mix/append remaining files
        for file_path in file_paths[1:]:
            audio = self.load_audio(file_path)
            
            if crossfade > 0:
                mixed = mixed.append(audio, crossfade=crossfade)
            else:
                # Overlay on top of existing audio
                mixed = mixed.overlay(audio)
        
        return mixed
    
    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze audio file and return information
        
        Args:
            file_path: Path to audio file
        
        Returns:
            Dictionary with audio properties
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Load audio with pydub for basic info
        audio = AudioSegment.from_file(file_path)
        
        # Load with librosa for advanced analysis
        y, sr = librosa.load(file_path, sr=None)
        
        # Detect tempo (BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Detect key (pitch class)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key = np.argmax(np.sum(chroma, axis=1))
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Calculate RMS energy
        rms = librosa.feature.rms(y=y)[0]
        avg_energy = float(np.mean(rms))
        
        return {
            "Duration": f"{len(audio) / 1000:.2f} seconds",
            "Channels": audio.channels,
            "Sample Rate": f"{audio.frame_rate} Hz",
            "Bit Depth": f"{audio.sample_width * 8} bit",
            "BPM": f"{tempo:.1f}",
            "Detected Key": key_names[key],
            "Average Energy": f"{avg_energy:.4f}",
            "File Size": f"{os.path.getsize(file_path) / 1024:.1f} KB"
        }
    
    def trim(self, audio: AudioSegment, start_ms: int, end_ms: int) -> AudioSegment:
        """
        Trim audio segment
        
        Args:
            audio: AudioSegment to trim
            start_ms: Start time in milliseconds
            end_ms: End time in milliseconds
        
        Returns:
            Trimmed AudioSegment
        """
        return audio[start_ms:end_ms]
    
    def change_speed(self, audio: AudioSegment, speed: float) -> AudioSegment:
        """
        Change playback speed (also affects pitch)
        
        Args:
            audio: AudioSegment to modify
            speed: Speed multiplier (2.0 = double speed, 0.5 = half speed)
        
        Returns:
            Modified AudioSegment
        """
        # Change frame rate
        sound_with_altered_frame_rate = audio._spawn(
            audio.raw_data,
            overrides={"frame_rate": int(audio.frame_rate * speed)}
        )
        # Convert back to standard frame rate
        return sound_with_altered_frame_rate.set_frame_rate(audio.frame_rate)
    
    def normalize(self, audio: AudioSegment, headroom: float = 0.1) -> AudioSegment:
        """
        Normalize audio to maximum volume without clipping
        
        Args:
            audio: AudioSegment to normalize
            headroom: Headroom in dB (default 0.1)
        
        Returns:
            Normalized AudioSegment
        """
        # Calculate the change needed to hit the target peak
        change_in_dBFS = -(audio.max_dBFS) - headroom
        return audio.apply_gain(change_in_dBFS)
    
    def fade_in_out(self, audio: AudioSegment, fade_in_ms: int = 100, fade_out_ms: int = 100) -> AudioSegment:
        """
        Apply fade in and fade out
        
        Args:
            audio: AudioSegment to modify
            fade_in_ms: Fade in duration in milliseconds
            fade_out_ms: Fade out duration in milliseconds
        
        Returns:
            AudioSegment with fades applied
        """
        return audio.fade_in(fade_in_ms).fade_out(fade_out_ms)
    
    def reverse(self, audio: AudioSegment) -> AudioSegment:
        """Reverse audio playback"""
        return audio.reverse()
    
    def concatenate(self, audio_segments: List[AudioSegment], gap_ms: int = 0) -> AudioSegment:
        """
        Concatenate multiple audio segments
        
        Args:
            audio_segments: List of AudioSegment objects
            gap_ms: Gap between segments in milliseconds
        
        Returns:
            Concatenated AudioSegment
        """
        if not audio_segments:
            raise ValueError("No audio segments provided")
        
        result = audio_segments[0]
        
        if gap_ms > 0:
            silence = AudioSegment.silent(duration=gap_ms)
            for segment in audio_segments[1:]:
                result = result + silence + segment
        else:
            for segment in audio_segments[1:]:
                result = result + segment
        
        return result
