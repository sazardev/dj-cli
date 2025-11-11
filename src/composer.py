"""
Auto Composer - Automatic music composition and generation
"""

from pydub import AudioSegment
from src.music_theory import MusicTheory
from src.sounds import SoundGenerator
from src.beat_maker import BeatMaker
import random
from typing import Dict, List, Optional
import numpy as np


class AutoComposer:
    """Automatic music composition engine"""
    
    def __init__(self):
        self.theory = MusicTheory()
        self.generator = SoundGenerator(sample_rate=48000)  # Higher quality
        self.beat_maker = BeatMaker(sample_rate=48000)
    
    def compose_track(self, genre: str = 'lofi', duration_bars: int = 16,
                     key: str = 'C', variation: str = 'medium') -> AudioSegment:
        """
        Compose a complete track automatically
        
        Args:
            genre: Musical genre (lofi, electro, funk, relax, etc.)
            duration_bars: Track length in bars
            key: Musical key
            variation: Amount of variation (low, medium, high)
        
        Returns:
            Complete composed track
        """
        # Get genre preset
        preset = self.get_genre_preset(genre)
        
        # Generate BPM
        bpm = self.theory.get_bpm_for_genre(genre)
        
        # Get chord progression
        progression = self.theory.get_progression(key, preset['progression_style'])
        
        # Generate elements
        drums = self._generate_drums(bpm, duration_bars, preset)
        bass = self._generate_bass(progression, bpm, duration_bars, preset)
        chords = self._generate_chords(progression, bpm, duration_bars, preset)
        melody = self._generate_melody(key, preset['scale'], bpm, duration_bars, preset)
        
        # Mix all elements
        track = drums
        track = track.overlay(bass - preset.get('bass_volume', 3))
        track = track.overlay(chords - preset.get('chord_volume', 6))
        track = track.overlay(melody - preset.get('melody_volume', 3))
        
        # Apply genre-specific effects
        track = self._apply_genre_effects(track, genre)
        
        return track
    
    def get_genre_preset(self, genre: str) -> Dict:
        """Get composition preset for genre"""
        presets = {
            'lofi': {
                'scale': 'minor',
                'progression_style': 'lofi',
                'beat_pattern': 'lofi',
                'melody_style': 'smooth',
                'bass_pattern': 'root',
                'chord_voicing': 'warm',
                'melody_octave': 5,
                'bass_volume': 4,
                'chord_volume': 8,
                'melody_volume': 5,
                'swing': 0.6,
                'reverb': 0.4,
            },
            'electro': {
                'scale': 'minor',
                'progression_style': 'edm',
                'beat_pattern': 'house',
                'melody_style': 'jumpy',
                'bass_pattern': 'fifth',
                'chord_voicing': 'bright',
                'melody_octave': 6,
                'bass_volume': 2,
                'chord_volume': 6,
                'melody_volume': 3,
                'swing': 0,
                'reverb': 0.3,
            },
            'funk': {
                'scale': 'minor',
                'progression_style': 'funk',
                'beat_pattern': 'funk',
                'melody_style': 'syncopated',
                'bass_pattern': 'walking',
                'chord_voicing': 'funky',
                'melody_octave': 5,
                'bass_volume': 1,
                'chord_volume': 7,
                'melody_volume': 4,
                'swing': 0.7,
                'reverb': 0.2,
            },
            'relax': {
                'scale': 'major',
                'progression_style': 'pop',
                'beat_pattern': 'ambient',
                'melody_style': 'smooth',
                'bass_pattern': 'root',
                'chord_voicing': 'soft',
                'melody_octave': 5,
                'bass_volume': 6,
                'chord_volume': 5,
                'melody_volume': 4,
                'swing': 0,
                'reverb': 0.6,
            },
            'ambient': {
                'scale': 'major',
                'progression_style': 'pop',
                'beat_pattern': None,  # No drums
                'melody_style': 'smooth',
                'bass_pattern': 'root',
                'chord_voicing': 'pad',
                'melody_octave': 5,
                'bass_volume': 8,
                'chord_volume': 4,
                'melody_volume': 5,
                'swing': 0,
                'reverb': 0.8,
            },
            'synthwave': {
                'scale': 'minor',
                'progression_style': 'edm',
                'beat_pattern': 'synthwave',
                'melody_style': 'arpeggio',
                'bass_pattern': 'fifth',
                'chord_voicing': 'synth',
                'melody_octave': 6,
                'bass_volume': 3,
                'chord_volume': 6,
                'melody_volume': 2,
                'swing': 0,
                'reverb': 0.5,
            },
        }
        
        return presets.get(genre.lower(), presets['lofi'])
    
    def _generate_drums(self, bpm: int, bars: int, preset: Dict) -> AudioSegment:
        """Generate drum pattern"""
        beat_pattern = preset.get('beat_pattern')
        
        if beat_pattern is None or beat_pattern == 'ambient':
            # No drums or very minimal
            duration_ms = int((60000 / bpm) * 4 * bars)
            return AudioSegment.silent(duration=duration_ms)
        
        if beat_pattern == 'lofi':
            return self._generate_lofi_drums(bpm, bars)
        elif beat_pattern == 'funk':
            return self._generate_funk_drums(bpm, bars)
        elif beat_pattern == 'synthwave':
            return self._generate_synthwave_drums(bpm, bars)
        else:
            # Use existing beat maker
            return self.beat_maker.create_beat(bpm, bars, beat_pattern)
    
    def _generate_lofi_drums(self, bpm: int, bars: int) -> AudioSegment:
        """Generate lo-fi style drums with swing"""
        # Similar to basic but with swing and softer sounds
        beat_ms = int(60000 / bpm)
        bar_ms = beat_ms * 4
        
        # Generate softer drum sounds
        kick = self.generator.generate_kick(0.3) - 3
        snare = self.generator.generate_snare(0.15) - 6
        hihat = self.generator.generate_hihat(0.05) - 8
        
        bar = AudioSegment.silent(duration=bar_ms)
        
        # Kick on 1 and 3
        bar = bar.overlay(kick, position=0)
        bar = bar.overlay(kick, position=beat_ms * 2)
        
        # Snare on 2 and 4 (slightly delayed for swing)
        swing_delay = int(beat_ms * 0.1)
        bar = bar.overlay(snare, position=beat_ms + swing_delay)
        bar = bar.overlay(snare, position=beat_ms * 3 + swing_delay)
        
        # Sparse hi-hats
        for i in [0, 2, 4, 6]:
            pos = int(beat_ms * i / 2)
            bar = bar.overlay(hihat, position=pos)
        
        # Repeat bars
        result = bar
        for _ in range(bars - 1):
            result = result + bar
        
        return result
    
    def _generate_funk_drums(self, bpm: int, bars: int) -> AudioSegment:
        """Generate funky drum pattern"""
        beat_ms = int(60000 / bpm)
        bar_ms = beat_ms * 4
        sixteenth_ms = beat_ms // 4
        
        kick = self.generator.generate_kick(0.25)
        snare = self.generator.generate_snare(0.15)
        hihat = self.generator.generate_hihat(0.04)
        
        bar = AudioSegment.silent(duration=bar_ms)
        
        # Funky kick pattern
        kick_positions = [0, sixteenth_ms * 6, beat_ms * 2, sixteenth_ms * 14]
        for pos in kick_positions:
            bar = bar.overlay(kick, position=pos)
        
        # Snare on 2 and 4
        bar = bar.overlay(snare, position=beat_ms)
        bar = bar.overlay(snare, position=beat_ms * 3)
        
        # Sixteenth note hi-hats
        for i in range(16):
            # Ghost notes on off-beats
            volume_adjust = -3 if i % 2 == 0 else -8
            bar = bar.overlay(hihat + volume_adjust, position=sixteenth_ms * i)
        
        result = bar
        for _ in range(bars - 1):
            result = result + bar
        
        return result
    
    def _generate_synthwave_drums(self, bpm: int, bars: int) -> AudioSegment:
        """Generate synthwave style drums"""
        # Electronic, quantized, four-on-the-floor
        return self.beat_maker.create_beat(bpm, bars, 'house')
    
    def _generate_bass(self, progression: List, bpm: int, bars: int, 
                      preset: Dict) -> AudioSegment:
        """Generate bassline"""
        pattern = preset.get('bass_pattern', 'root')
        octave = 2
        
        # Get bassline frequencies
        bassline_freqs = self.theory.generate_bassline(progression, octave, pattern)
        
        # Calculate timing
        beat_ms = int(60000 / bpm)
        note_duration = 0.8  # Slightly shorter for groove
        
        # Generate bass sounds
        bass = AudioSegment.silent(duration=0)
        
        # Repeat bassline for all bars
        repeats = bars // len(progression)
        if bars % len(progression) != 0:
            repeats += 1
        
        for _ in range(repeats):
            for freq in bassline_freqs:
                note = self.generator.generate_bass(note_duration, int(freq))
                # Add slight silence between notes
                note = note + AudioSegment.silent(duration=int(beat_ms - len(note)))
                bass = bass + note
        
        # Trim to exact length
        total_duration = beat_ms * 4 * bars
        return bass[:total_duration]
    
    def _generate_chords(self, progression: List, bpm: int, bars: int,
                        preset: Dict) -> AudioSegment:
        """Generate chord progression"""
        beat_ms = int(60000 / bpm)
        chord_duration = (beat_ms * 4) / 1000  # Duration in seconds
        
        chords_audio = AudioSegment.silent(duration=0)
        
        # Repeat progression for all bars
        repeats = bars // len(progression)
        if bars % len(progression) != 0:
            repeats += 1
        
        for _ in range(repeats):
            for root, chord_type in progression:
                # Get chord frequencies
                freqs = self.theory.get_chord(root, chord_type, octave=3)
                
                # Generate chord
                chord = self.generator.generate_chord(
                    [int(f) for f in freqs], 
                    duration=chord_duration
                )
                
                chords_audio = chords_audio + chord
        
        # Trim to exact length
        total_duration = beat_ms * 4 * bars
        return chords_audio[:total_duration]
    
    def _generate_melody(self, key: str, scale: str, bpm: int, bars: int,
                        preset: Dict) -> AudioSegment:
        """Generate melody"""
        # Get scale notes
        octave = preset.get('melody_octave', 5)
        scale_notes = self.theory.get_scale_notes(key, scale, octave)
        
        # Extend scale to multiple octaves
        scale_notes_extended = scale_notes + [
            (n, f * 2) for n, f in scale_notes
        ]
        
        # Generate melody pattern
        notes_per_bar = 8  # Eighth notes
        total_notes = bars * notes_per_bar
        
        melody_style = preset.get('melody_style', 'smooth')
        melody_freqs = self.theory.generate_melody(
            scale_notes_extended, 
            total_notes, 
            melody_style
        )
        
        # Generate audio
        beat_ms = int(60000 / bpm)
        note_duration = (beat_ms / 2) / 1000  # Eighth note in seconds
        
        melody_audio = AudioSegment.silent(duration=0)
        
        for freq in melody_freqs:
            # Random note duration variation
            duration = note_duration * random.uniform(0.8, 1.0)
            note = self.generator.generate_synth(duration, int(freq), 'sine')
            
            # Add gap between notes
            gap = int((note_duration * 1000) - len(note))
            if gap > 0:
                note = note + AudioSegment.silent(duration=gap)
            
            melody_audio = melody_audio + note
        
        return melody_audio
    
    def _apply_genre_effects(self, track: AudioSegment, genre: str) -> AudioSegment:
        """Apply genre-specific processing"""
        # Normalize first
        target_dBFS = -14.0
        change_in_dBFS = target_dBFS - track.dBFS
        track = track.apply_gain(change_in_dBFS)
        
        # Genre-specific EQ and character
        if genre == 'lofi':
            # Lo-fi character: reduce highs, add warmth
            track = track.low_pass_filter(8000)
            track = track.high_pass_filter(80)
        
        elif genre in ['electro', 'synthwave']:
            # Crisp and bright
            track = track.high_pass_filter(40)
        
        elif genre == 'relax':
            # Warm and smooth
            track = track.low_pass_filter(10000)
        
        return track
    
    def compose_section(self, genre: str, section_type: str, 
                       duration_bars: int = 4, key: str = 'C') -> AudioSegment:
        """
        Compose a specific section (intro, verse, chorus, break, outro)
        
        Args:
            genre: Musical genre
            section_type: Type of section
            duration_bars: Length in bars
            key: Musical key
        
        Returns:
            Section audio
        """
        preset = self.get_genre_preset(genre)
        
        if section_type == 'intro':
            # Minimal intro - chords and melody only
            return self._compose_intro(genre, duration_bars, key, preset)
        
        elif section_type == 'verse':
            # Full arrangement but subdued
            return self.compose_track(genre, duration_bars, key)
        
        elif section_type == 'chorus':
            # Full energy
            track = self.compose_track(genre, duration_bars, key)
            # Boost volume slightly
            return track + 2
        
        elif section_type == 'break':
            # Drums and bass only
            return self._compose_break(genre, duration_bars, key, preset)
        
        elif section_type == 'outro':
            # Fade out with chords
            return self._compose_outro(genre, duration_bars, key, preset)
        
        else:
            return self.compose_track(genre, duration_bars, key)
    
    def _compose_intro(self, genre: str, bars: int, key: str, preset: Dict) -> AudioSegment:
        """Compose intro section"""
        bpm = self.theory.get_bpm_for_genre(genre)
        progression = self.theory.get_progression(key, preset['progression_style'])
        
        chords = self._generate_chords(progression, bpm, bars, preset)
        melody = self._generate_melody(key, preset['scale'], bpm, bars, preset)
        
        intro = chords.overlay(melody - 3)
        return self._apply_genre_effects(intro, genre)
    
    def _compose_break(self, genre: str, bars: int, key: str, preset: Dict) -> AudioSegment:
        """Compose break section"""
        bpm = self.theory.get_bpm_for_genre(genre)
        progression = self.theory.get_progression(key, preset['progression_style'])
        
        drums = self._generate_drums(bpm, bars, preset)
        bass = self._generate_bass(progression, bpm, bars, preset)
        
        break_section = drums.overlay(bass - 3)
        return self._apply_genre_effects(break_section, genre)
    
    def _compose_outro(self, genre: str, bars: int, key: str, preset: Dict) -> AudioSegment:
        """Compose outro section"""
        bpm = self.theory.get_bpm_for_genre(genre)
        progression = self.theory.get_progression(key, preset['progression_style'])
        
        chords = self._generate_chords(progression, bpm, bars, preset)
        chords = chords.fade_out(int(len(chords) * 0.8))
        
        return self._apply_genre_effects(chords, genre)
