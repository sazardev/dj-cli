"""
Continuous Generator - Generate evolving, continuous music
"""

from pydub import AudioSegment
from src.composer import AutoComposer
from src.music_theory import MusicTheory
import random
from typing import List, Dict, Optional


class ContinuousGenerator:
    """Generate continuous, evolving music tracks"""
    
    def __init__(self):
        self.composer = AutoComposer()
        self.theory = MusicTheory()
    
    def generate_continuous(self, genre: str, total_bars: int = 64,
                           key: Optional[str] = None, structure: Optional[str] = None) -> AudioSegment:
        """
        Generate a continuous track with evolving sections
        
        Args:
            genre: Musical genre
            total_bars: Total length in bars
            key: Musical key (auto-selected if None)
            structure: Song structure (auto if None)
        
        Returns:
            Complete continuous track
        """
        # Auto-select key if not provided
        if key is None:
            key = random.choice(['C', 'D', 'E', 'F', 'G', 'A'])
        
        # Get structure
        if structure is None:
            structure = self._get_default_structure(total_bars)
        else:
            structure = self._parse_structure(structure, total_bars)
        
        # Generate sections
        track = AudioSegment.silent(duration=0)
        
        for section_type, bars in structure:
            section = self.composer.compose_section(genre, section_type, bars, key)
            track = track + section
        
        return track
    
    def _get_default_structure(self, total_bars: int) -> List[tuple]:
        """
        Get default song structure based on length
        
        Args:
            total_bars: Total number of bars
        
        Returns:
            List of (section_type, bars) tuples
        """
        if total_bars <= 16:
            # Short track
            return [
                ('intro', 4),
                ('verse', 8),
                ('outro', 4),
            ]
        
        elif total_bars <= 32:
            # Medium track
            return [
                ('intro', 4),
                ('verse', 8),
                ('chorus', 8),
                ('verse', 8),
                ('outro', 4),
            ]
        
        else:
            # Long track with variations
            structure = [
                ('intro', 4),
                ('verse', 8),
                ('chorus', 8),
                ('break', 4),
                ('verse', 8),
                ('chorus', 8),
            ]
            
            remaining = total_bars - sum(b for _, b in structure)
            
            if remaining >= 8:
                structure.append(('chorus', 8))
                remaining -= 8
            
            if remaining >= 4:
                structure.append(('outro', 4))
                remaining -= 4
            
            if remaining > 0:
                structure.append(('verse', remaining))
            
            return structure
    
    def _parse_structure(self, structure_str: str, total_bars: int) -> List[tuple]:
        """
        Parse structure string like "intro:4,verse:8,chorus:8"
        
        Args:
            structure_str: Structure description
            total_bars: Total bars to fill
        
        Returns:
            List of (section_type, bars) tuples
        """
        parts = structure_str.split(',')
        structure = []
        
        for part in parts:
            if ':' in part:
                section, bars_str = part.split(':')
                bars = int(bars_str)
                structure.append((section.strip(), bars))
        
        return structure
    
    def generate_infinite(self, genre: str, bars_per_section: int = 8,
                         key: Optional[str] = None, variation: str = 'medium') -> 'InfiniteGenerator':
        """
        Create an infinite music generator
        
        Args:
            genre: Musical genre
            bars_per_section: Bars per generated section
            key: Musical key
            variation: Variation level
        
        Returns:
            InfiniteGenerator instance
        """
        if key is None:
            key = random.choice(['C', 'D', 'E', 'F', 'G', 'A'])
        
        return InfiniteGenerator(self.composer, genre, bars_per_section, key, variation)
    
    def generate_mixtape(self, genres: List[str], bars_per_genre: int = 16,
                        transitions: bool = True) -> AudioSegment:
        """
        Generate a mixtape with multiple genres
        
        Args:
            genres: List of genres to include
            bars_per_genre: Bars for each genre
            transitions: Add crossfade transitions
        
        Returns:
            Complete mixtape
        """
        mixtape = AudioSegment.silent(duration=0)
        
        for i, genre in enumerate(genres):
            # Random key for each section
            key = random.choice(['C', 'D', 'E', 'F', 'G', 'A'])
            
            # Generate section
            section = self.generate_continuous(genre, bars_per_genre, key)
            
            # Add transition
            if transitions and i > 0:
                # Crossfade between genres
                crossfade_ms = 2000
                mixtape = mixtape.append(section, crossfade=crossfade_ms)
            else:
                mixtape = mixtape + section
        
        return mixtape
    
    def generate_variations(self, genre: str, bars: int, 
                           count: int = 3, key: str = 'C') -> List[AudioSegment]:
        """
        Generate multiple variations of a track
        
        Args:
            genre: Musical genre
            bars: Track length
            count: Number of variations
            key: Musical key
        
        Returns:
            List of track variations
        """
        variations = []
        
        for _ in range(count):
            track = self.composer.compose_track(genre, bars, key)
            variations.append(track)
        
        return variations


class InfiniteGenerator:
    """Generator for infinite music streams"""
    
    def __init__(self, composer: AutoComposer, genre: str, 
                 bars_per_section: int, key: str, variation: str):
        self.composer = composer
        self.genre = genre
        self.bars_per_section = bars_per_section
        self.key = key
        self.variation = variation
        self.section_types = ['verse', 'chorus', 'break', 'verse', 'chorus']
        self.current_section = 0
    
    def next_section(self) -> AudioSegment:
        """Generate next section in the infinite stream"""
        # Get next section type
        section_type = self.section_types[self.current_section % len(self.section_types)]
        self.current_section += 1
        
        # Add variation
        if self.variation == 'high':
            # Change key occasionally
            if random.random() < 0.3:
                self.key = random.choice(['C', 'D', 'E', 'F', 'G', 'A'])
        
        # Generate section
        return self.composer.compose_section(
            self.genre, section_type, self.bars_per_section, self.key
        )
    
    def generate_stream(self, total_bars: int) -> AudioSegment:
        """Generate a stream of given length"""
        stream = AudioSegment.silent(duration=0)
        bars_generated = 0
        
        while bars_generated < total_bars:
            section = self.next_section()
            stream = stream + section
            bars_generated += self.bars_per_section
        
        # Trim to exact length if needed
        return stream
