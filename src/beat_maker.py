"""
Beat Maker - Create drum patterns and beats
"""

from pydub import AudioSegment
from src.sounds import SoundGenerator
from typing import List, Dict


class BeatMaker:
    """Create drum beats and patterns with premium quality"""
    
    def __init__(self, sample_rate: int = 96000):  # Premium quality
        self.sample_rate = sample_rate
        self.generator = SoundGenerator(sample_rate)
    
    def create_beat(self, bpm: int = 120, bars: int = 4, pattern: str = "basic") -> AudioSegment:
        """
        Create a drum beat
        
        Args:
            bpm: Beats per minute
            bars: Number of bars (4 beats per bar)
            pattern: Beat pattern name
        
        Returns:
            Complete beat AudioSegment
        """
        pattern = pattern.lower()
        
        if pattern == "basic":
            return self._create_basic_beat(bpm, bars)
        elif pattern == "trap":
            return self._create_trap_beat(bpm, bars)
        elif pattern == "dnb":
            return self._create_dnb_beat(bpm, bars)
        elif pattern == "house":
            return self._create_house_beat(bpm, bars)
        elif pattern == "techno":
            return self._create_techno_beat(bpm, bars)
        else:
            raise ValueError(f"Unknown pattern: {pattern}")
    
    def _calculate_timing(self, bpm: int) -> Dict[str, float]:
        """Calculate note timings based on BPM"""
        beat_duration = 60.0 / bpm  # Duration of one beat in seconds
        
        return {
            "bar": beat_duration * 4,      # 4 beats per bar
            "beat": beat_duration,          # Quarter note
            "eighth": beat_duration / 2,    # Eighth note
            "sixteenth": beat_duration / 4, # Sixteenth note
        }
    
    def _create_basic_beat(self, bpm: int, bars: int) -> AudioSegment:
        """
        Create a basic 4/4 beat
        Pattern: Kick on 1,3 | Snare on 2,4 | Hi-hat on eighth notes
        """
        timing = self._calculate_timing(bpm)
        
        # Generate sounds
        kick = self.generator.generate_kick(0.3)
        snare = self.generator.generate_snare(0.2)
        hihat = self.generator.generate_hihat(0.05)
        
        # Create one bar
        bar_duration_ms = int(timing["bar"] * 1000)
        beat_duration_ms = int(timing["beat"] * 1000)
        eighth_duration_ms = int(timing["eighth"] * 1000)
        
        # Start with silence
        bar = AudioSegment.silent(duration=bar_duration_ms)
        
        # Add kicks on beats 1 and 3
        bar = bar.overlay(kick, position=0)
        bar = bar.overlay(kick, position=beat_duration_ms * 2)
        
        # Add snares on beats 2 and 4
        bar = bar.overlay(snare, position=beat_duration_ms)
        bar = bar.overlay(snare, position=beat_duration_ms * 3)
        
        # Add hi-hats on every eighth note
        for i in range(8):
            bar = bar.overlay(hihat, position=eighth_duration_ms * i)
        
        # Repeat for number of bars
        beat = bar
        for _ in range(bars - 1):
            beat = beat + bar
        
        return beat
    
    def _create_trap_beat(self, bpm: int, bars: int) -> AudioSegment:
        """
        Create a trap beat
        Pattern: Kick on 1,3.5 | Snare on 2,4 | Hi-hat rolls on sixteenth notes
        """
        timing = self._calculate_timing(bpm)
        
        # Generate sounds
        kick = self.generator.generate_kick(0.3)
        snare = self.generator.generate_snare(0.2)
        hihat = self.generator.generate_hihat(0.03)
        hihat_open = self.generator.generate_hihat(0.1)
        
        # Create one bar
        bar_duration_ms = int(timing["bar"] * 1000)
        beat_duration_ms = int(timing["beat"] * 1000)
        sixteenth_duration_ms = int(timing["sixteenth"] * 1000)
        
        bar = AudioSegment.silent(duration=bar_duration_ms)
        
        # Kick pattern: 1, 3.5
        bar = bar.overlay(kick, position=0)
        bar = bar.overlay(kick, position=beat_duration_ms * 2 + beat_duration_ms // 2)
        
        # Snare on 2 and 4
        bar = bar.overlay(snare, position=beat_duration_ms)
        bar = bar.overlay(snare, position=beat_duration_ms * 3)
        
        # Hi-hat rolls (trap-style)
        for i in range(16):
            # Accent certain hi-hats
            if i % 4 == 0:
                bar = bar.overlay(hihat_open - 3, position=sixteenth_duration_ms * i)
            else:
                bar = bar.overlay(hihat - 6, position=sixteenth_duration_ms * i)
        
        # Repeat for number of bars
        beat = bar
        for _ in range(bars - 1):
            beat = beat + bar
        
        return beat
    
    def _create_dnb_beat(self, bpm: int, bars: int) -> AudioSegment:
        """
        Create a drum and bass beat
        Pattern: Amen break inspired - complex kick/snare pattern
        """
        timing = self._calculate_timing(bpm)
        
        # Generate sounds
        kick = self.generator.generate_kick(0.2)
        snare = self.generator.generate_snare(0.15)
        hihat = self.generator.generate_hihat(0.03)
        
        bar_duration_ms = int(timing["bar"] * 1000)
        beat_duration_ms = int(timing["beat"] * 1000)
        sixteenth_duration_ms = int(timing["sixteenth"] * 1000)
        
        bar = AudioSegment.silent(duration=bar_duration_ms)
        
        # DnB kick pattern
        kick_positions = [0, sixteenth_duration_ms * 7, beat_duration_ms * 2, 
                         beat_duration_ms * 3 + sixteenth_duration_ms * 2]
        for pos in kick_positions:
            bar = bar.overlay(kick, position=pos)
        
        # DnB snare pattern (syncopated)
        snare_positions = [sixteenth_duration_ms * 4, sixteenth_duration_ms * 12]
        for pos in snare_positions:
            bar = bar.overlay(snare, position=pos)
        
        # Fast hi-hats
        for i in range(16):
            bar = bar.overlay(hihat - 8, position=sixteenth_duration_ms * i)
        
        # Repeat for number of bars
        beat = bar
        for _ in range(bars - 1):
            beat = beat + bar
        
        return beat
    
    def _create_house_beat(self, bpm: int, bars: int) -> AudioSegment:
        """
        Create a house beat
        Pattern: Four-on-the-floor kick, hi-hat on offbeats
        """
        timing = self._calculate_timing(bpm)
        
        # Generate sounds
        kick = self.generator.generate_kick(0.3)
        hihat_closed = self.generator.generate_hihat(0.05)
        hihat_open = self.generator.generate_hihat(0.15)
        
        bar_duration_ms = int(timing["bar"] * 1000)
        beat_duration_ms = int(timing["beat"] * 1000)
        eighth_duration_ms = int(timing["eighth"] * 1000)
        
        bar = AudioSegment.silent(duration=bar_duration_ms)
        
        # Four-on-the-floor kicks (every beat)
        for i in range(4):
            bar = bar.overlay(kick, position=beat_duration_ms * i)
        
        # Hi-hats on offbeats (eighth notes)
        for i in range(8):
            if i % 2 == 1:  # Offbeats
                if i == 3 or i == 7:  # Open hi-hat occasionally
                    bar = bar.overlay(hihat_open - 3, position=eighth_duration_ms * i)
                else:
                    bar = bar.overlay(hihat_closed, position=eighth_duration_ms * i)
        
        # Repeat for number of bars
        beat = bar
        for _ in range(bars - 1):
            beat = beat + bar
        
        return beat
    
    def _create_techno_beat(self, bpm: int, bars: int) -> AudioSegment:
        """
        Create a techno beat
        Pattern: Four-on-the-floor kick, offbeat hi-hats, occasional snare
        """
        timing = self._calculate_timing(bpm)
        
        # Generate sounds
        kick = self.generator.generate_kick(0.3)
        snare = self.generator.generate_snare(0.15)
        hihat = self.generator.generate_hihat(0.05)
        
        bar_duration_ms = int(timing["bar"] * 1000)
        beat_duration_ms = int(timing["beat"] * 1000)
        sixteenth_duration_ms = int(timing["sixteenth"] * 1000)
        
        bar = AudioSegment.silent(duration=bar_duration_ms)
        
        # Four-on-the-floor kicks
        for i in range(4):
            bar = bar.overlay(kick, position=beat_duration_ms * i)
        
        # Snare on 2 and 4 (lighter than in other genres)
        bar = bar.overlay(snare - 12, position=beat_duration_ms)
        bar = bar.overlay(snare - 12, position=beat_duration_ms * 3)
        
        # Sixteenth note hi-hats
        for i in range(16):
            # Accent every 4th hi-hat
            if i % 4 == 0:
                bar = bar.overlay(hihat - 3, position=sixteenth_duration_ms * i)
            else:
                bar = bar.overlay(hihat - 8, position=sixteenth_duration_ms * i)
        
        # Repeat for number of bars
        beat = bar
        for _ in range(bars - 1):
            beat = beat + bar
        
        return beat
    
    def create_custom_pattern(self, bpm: int, bars: int, pattern: List[Dict]) -> AudioSegment:
        """
        Create a custom beat from a pattern definition
        
        Args:
            bpm: Beats per minute
            bars: Number of bars
            pattern: List of dict with 'sound', 'position' (in beats)
                    Example: [{'sound': 'kick', 'position': 0}, ...]
        
        Returns:
            Custom beat AudioSegment
        """
        timing = self._calculate_timing(bpm)
        bar_duration_ms = int(timing["bar"] * 1000)
        beat_duration_ms = int(timing["beat"] * 1000)
        
        # Create empty bar
        bar = AudioSegment.silent(duration=bar_duration_ms)
        
        # Add sounds according to pattern
        for event in pattern:
            sound_type = event['sound']
            position = event['position']  # Position in beats
            position_ms = int(position * beat_duration_ms)
            
            # Generate sound
            if sound_type == 'kick':
                sound = self.generator.generate_kick(0.3)
            elif sound_type == 'snare':
                sound = self.generator.generate_snare(0.2)
            elif sound_type == 'hihat':
                sound = self.generator.generate_hihat(0.05)
            else:
                continue
            
            # Overlay sound
            if position_ms < bar_duration_ms:
                bar = bar.overlay(sound, position=position_ms)
        
        # Repeat for number of bars
        beat = bar
        for _ in range(bars - 1):
            beat = beat + bar
        
        return beat
