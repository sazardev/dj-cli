"""
Music Theory - Scales, chords, progressions, and musical structures
"""

import random
from typing import List, Dict, Tuple
import numpy as np


class MusicTheory:
    """Music theory fundamentals for composition"""
    
    # Note frequencies (A4 = 440Hz as reference)
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Scale patterns (semitone intervals)
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'pentatonic_major': [0, 2, 4, 7, 9],
        'pentatonic_minor': [0, 3, 5, 7, 10],
        'blues': [0, 3, 5, 6, 7, 10],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'phrygian': [0, 1, 3, 5, 7, 8, 10],
        'lydian': [0, 2, 4, 6, 7, 9, 11],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
        'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    }
    
    # Common chord progressions by genre
    PROGRESSIONS = {
        'pop': [
            ['I', 'V', 'vi', 'IV'],
            ['I', 'IV', 'V', 'IV'],
            ['vi', 'IV', 'I', 'V'],
            ['I', 'vi', 'IV', 'V'],
        ],
        'jazz': [
            ['ii', 'V', 'I', 'VI'],
            ['I', 'vi', 'ii', 'V'],
            ['iii', 'vi', 'ii', 'V'],
            ['I', 'IV', 'iii', 'vi'],
        ],
        'edm': [
            ['i', 'VI', 'III', 'VII'],
            ['i', 'v', 'VI', 'III'],
            ['i', 'III', 'VII', 'VI'],
            ['i', 'VII', 'VI', 'V'],
        ],
        'lofi': [
            ['i', 'iv', 'VII', 'III'],
            ['i', 'VII', 'VI', 'V'],
            ['i', 'III', 'iv', 'V'],
            ['i', 'VI', 'iv', 'VII'],
        ],
        'funk': [
            ['i', 'iv', 'i', 'iv'],
            ['i', 'IV', 'v', 'IV'],
            ['i', 'III', 'IV', 'v'],
        ],
    }
    
    def __init__(self):
        self.base_freq = 440.0  # A4
    
    def note_to_freq(self, note: str, octave: int = 4) -> float:
        """
        Convert note name and octave to frequency
        
        Args:
            note: Note name (C, C#, D, etc.)
            octave: Octave number (default 4)
        
        Returns:
            Frequency in Hz
        """
        if note not in self.NOTE_NAMES:
            raise ValueError(f"Invalid note: {note}")
        
        # Calculate semitones from A4
        note_index = self.NOTE_NAMES.index(note)
        a_index = self.NOTE_NAMES.index('A')
        
        # Semitones from A4
        semitones = (octave - 4) * 12 + (note_index - a_index)
        
        # Calculate frequency
        return self.base_freq * (2 ** (semitones / 12))
    
    def get_scale_notes(self, root: str, scale_type: str = 'major', 
                        octave: int = 4) -> List[Tuple[str, float]]:
        """
        Get notes and frequencies for a scale
        
        Args:
            root: Root note (C, D, E, etc.)
            scale_type: Type of scale
            octave: Starting octave
        
        Returns:
            List of (note_name, frequency) tuples
        """
        if scale_type not in self.SCALES:
            raise ValueError(f"Unknown scale type: {scale_type}")
        
        root_index = self.NOTE_NAMES.index(root)
        pattern = self.SCALES[scale_type]
        
        notes = []
        for interval in pattern:
            note_index = (root_index + interval) % 12
            note_name = self.NOTE_NAMES[note_index]
            
            # Calculate octave adjustment
            octave_adjust = (root_index + interval) // 12
            note_octave = octave + octave_adjust
            
            freq = self.note_to_freq(note_name, note_octave)
            notes.append((note_name, freq))
        
        return notes
    
    def get_chord(self, root: str, chord_type: str = 'major', 
                  octave: int = 3) -> List[float]:
        """
        Get frequencies for a chord
        
        Args:
            root: Root note
            chord_type: Type of chord (major, minor, seventh, etc.)
            octave: Octave for root note
        
        Returns:
            List of frequencies
        """
        root_index = self.NOTE_NAMES.index(root)
        
        # Chord intervals (in semitones from root)
        chord_patterns = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'dim': [0, 3, 6],
            'aug': [0, 4, 8],
            'sus2': [0, 2, 7],
            'sus4': [0, 5, 7],
            'maj7': [0, 4, 7, 11],
            'min7': [0, 3, 7, 10],
            'dom7': [0, 4, 7, 10],
            'maj9': [0, 4, 7, 11, 14],
            'min9': [0, 3, 7, 10, 14],
        }
        
        if chord_type not in chord_patterns:
            chord_type = 'major'
        
        pattern = chord_patterns[chord_type]
        frequencies = []
        
        for interval in pattern:
            note_index = (root_index + interval) % 12
            note_name = self.NOTE_NAMES[note_index]
            octave_adjust = (root_index + interval) // 12
            freq = self.note_to_freq(note_name, octave + octave_adjust)
            frequencies.append(freq)
        
        return frequencies
    
    def roman_to_chord(self, roman: str, key: str, scale: str = 'major') -> Tuple[str, str]:
        """
        Convert Roman numeral to chord
        
        Args:
            roman: Roman numeral (I, ii, iii, etc.)
            key: Key signature
            scale: Scale type
        
        Returns:
            (root_note, chord_type)
        """
        # Parse roman numeral
        roman_clean = roman.strip().upper()
        is_minor = roman.islower() or roman.startswith('i')
        
        # Roman to scale degree
        roman_map = {
            'I': 0, 'II': 1, 'III': 2, 'IV': 3, 
            'V': 4, 'VI': 5, 'VII': 6
        }
        
        degree = roman_map.get(roman_clean, 0)
        
        # Get scale notes
        scale_notes = self.get_scale_notes(key, scale)
        root_note = scale_notes[degree % len(scale_notes)][0]
        
        # Determine chord type
        chord_type = 'minor' if is_minor else 'major'
        
        return (root_note, chord_type)
    
    def get_progression(self, key: str, style: str = 'pop') -> List[Tuple[str, str]]:
        """
        Get a chord progression
        
        Args:
            key: Key signature
            style: Musical style (pop, jazz, edm, etc.)
        
        Returns:
            List of (root_note, chord_type) tuples
        """
        if style not in self.PROGRESSIONS:
            style = 'pop'
        
        # Pick a random progression from the style
        progression_pattern = random.choice(self.PROGRESSIONS[style])
        
        # Convert to actual chords
        chords = []
        scale = 'minor' if style in ['edm', 'lofi'] else 'major'
        
        for roman in progression_pattern:
            chord = self.roman_to_chord(roman, key, scale)
            chords.append(chord)
        
        return chords
    
    def generate_melody(self, scale_notes: List[Tuple[str, float]], 
                       length: int = 8, style: str = 'smooth') -> List[float]:
        """
        Generate a melody based on a scale
        
        Args:
            scale_notes: List of (note, freq) tuples
            length: Number of notes
            style: Melody style (smooth, jumpy, ascending, descending)
        
        Returns:
            List of frequencies
        """
        melody = []
        current_index = len(scale_notes) // 2  # Start in middle
        
        for i in range(length):
            melody.append(scale_notes[current_index][1])
            
            if style == 'smooth':
                # Move by small steps
                step = random.choice([-1, -1, 0, 1, 1])
            elif style == 'jumpy':
                # Larger intervals
                step = random.choice([-3, -2, -1, 1, 2, 3])
            elif style == 'ascending':
                step = random.choice([0, 1, 1, 2])
            elif style == 'descending':
                step = random.choice([-2, -1, -1, 0])
            else:
                step = random.choice([-1, 0, 1])
            
            current_index = (current_index + step) % len(scale_notes)
        
        return melody
    
    def generate_bassline(self, chord_progression: List[Tuple[str, str]], 
                         octave: int = 2, pattern: str = 'root') -> List[float]:
        """
        Generate a bassline from chord progression
        
        Args:
            chord_progression: List of (root, chord_type)
            octave: Bass octave
            pattern: Bassline pattern (root, fifth, walking)
        
        Returns:
            List of frequencies for bassline
        """
        bassline = []
        
        for root, chord_type in chord_progression:
            root_freq = self.note_to_freq(root, octave)
            
            if pattern == 'root':
                # Just play the root
                bassline.extend([root_freq] * 4)
            
            elif pattern == 'fifth':
                # Root and fifth
                root_index = self.NOTE_NAMES.index(root)
                fifth_index = (root_index + 7) % 12
                fifth = self.NOTE_NAMES[fifth_index]
                fifth_freq = self.note_to_freq(fifth, octave)
                
                bassline.extend([root_freq, root_freq, fifth_freq, root_freq])
            
            elif pattern == 'walking':
                # Walking bass (chromatic approach)
                root_index = self.NOTE_NAMES.index(root)
                
                # Current root
                bassline.append(root_freq)
                
                # Chromatic notes
                for i in range(1, 4):
                    walk_index = (root_index + i) % 12
                    walk_note = self.NOTE_NAMES[walk_index]
                    walk_freq = self.note_to_freq(walk_note, octave)
                    bassline.append(walk_freq)
        
        return bassline
    
    def get_bpm_for_genre(self, genre: str) -> int:
        """Get typical BPM for genre"""
        bpm_ranges = {
            'lofi': (70, 90),
            'relax': (60, 80),
            'ambient': (60, 90),
            'funk': (100, 120),
            'disco': (110, 130),
            'house': (120, 130),
            'techno': (125, 135),
            'electro': (125, 135),
            'trance': (130, 145),
            'dnb': (160, 180),
            'dubstep': (135, 145),
            'trap': (135, 160),
        }
        
        min_bpm, max_bpm = bpm_ranges.get(genre.lower(), (120, 130))
        return random.randint(min_bpm, max_bpm)
