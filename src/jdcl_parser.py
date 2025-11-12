"""
JDCL Parser - Parse .jdcl files (JSON DJ Composition Language)
A human-readable music composition language
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class InstrumentType(Enum):
    """Available instrument types"""
    PIANO = "piano"
    SYNTH = "synth"
    PAD = "pad"
    BASS = "bass"
    SUB_BASS = "sub_bass"
    KICK = "kick"
    SNARE = "snare"
    HIHAT = "hihat"
    CLAP = "clap"
    AMBIENT = "ambient"
    TEXTURE = "texture"


class NoteValue(Enum):
    """Musical note durations"""
    WHOLE = 1.0
    HALF = 0.5
    QUARTER = 0.25
    EIGHTH = 0.125
    SIXTEENTH = 0.0625
    DOTTED_QUARTER = 0.375
    DOTTED_EIGHTH = 0.1875


@dataclass
class Note:
    """Represents a musical note"""
    pitch: str  # "C4", "D#5", etc. or "rest"
    duration: float  # In beats
    velocity: float = 0.8  # 0.0 to 1.0
    
    def is_rest(self) -> bool:
        return self.pitch.lower() == "rest" or self.pitch == "-"


@dataclass
class Pattern:
    """Represents a musical pattern"""
    name: str
    instrument: str
    notes: List[Note]
    volume: float = 1.0
    effects: Dict[str, Any] = field(default_factory=dict)
    variation: float = 0.5


@dataclass
class Section:
    """Represents a song section"""
    name: str
    bars: int
    patterns: List[str]  # Pattern names to play
    tempo: Optional[int] = None  # Override global tempo
    key: Optional[str] = None  # Override global key
    effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Composition:
    """Complete composition structure"""
    title: str
    artist: str
    genre: str
    tempo: int
    key: str
    time_signature: Tuple[int, int] = (4, 4)
    patterns: Dict[str, Pattern] = field(default_factory=dict)
    sections: List[Section] = field(default_factory=list)
    structure: List[str] = field(default_factory=list)  # Section order
    global_effects: Dict[str, Any] = field(default_factory=dict)


class JDCLParser:
    """Parser for .jdcl files"""
    
    def __init__(self):
        self.composition: Optional[Composition] = None
        
        # Note duration shortcuts
        self.duration_map = {
            "w": NoteValue.WHOLE.value,
            "h": NoteValue.HALF.value,
            "q": NoteValue.QUARTER.value,
            "e": NoteValue.EIGHTH.value,
            "s": NoteValue.SIXTEENTH.value,
            "q.": NoteValue.DOTTED_QUARTER.value,
            "e.": NoteValue.DOTTED_EIGHTH.value,
            "whole": NoteValue.WHOLE.value,
            "half": NoteValue.HALF.value,
            "quarter": NoteValue.QUARTER.value,
            "eighth": NoteValue.EIGHTH.value,
            "sixteenth": NoteValue.SIXTEENTH.value,
        }
    
    def parse_file(self, filepath: str) -> Composition:
        """
        Parse a .jdcl file
        
        Args:
            filepath: Path to .jdcl file
            
        Returns:
            Parsed Composition object
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return self.parse_json(data)
    
    def parse_json(self, data: Dict) -> Composition:
        """Parse JSON data into Composition"""
        
        # Parse metadata
        metadata = data.get("metadata", {})
        composition = Composition(
            title=metadata.get("title", "Untitled"),
            artist=metadata.get("artist", "Unknown"),
            genre=metadata.get("genre", "lofi"),
            tempo=metadata.get("tempo", 120),
            key=metadata.get("key", "C"),
            time_signature=self._parse_time_signature(
                metadata.get("time_signature", "4/4")
            ),
            global_effects=data.get("global_effects", {})
        )
        
        # Parse patterns
        patterns_data = data.get("patterns", {})
        for pattern_name, pattern_data in patterns_data.items():
            pattern = self._parse_pattern(pattern_name, pattern_data)
            composition.patterns[pattern_name] = pattern
        
        # Parse sections
        sections_data = data.get("sections", {})
        for section_name, section_data in sections_data.items():
            section = self._parse_section(section_name, section_data)
            composition.sections.append(section)
        
        # Parse structure (order of sections)
        composition.structure = data.get("structure", [])
        
        self.composition = composition
        return composition
    
    def _parse_time_signature(self, time_sig: str) -> Tuple[int, int]:
        """Parse time signature string like '4/4' or '3/4'"""
        parts = time_sig.split('/')
        return (int(parts[0]), int(parts[1]))
    
    def _parse_pattern(self, name: str, data: Dict) -> Pattern:
        """Parse a pattern definition"""
        instrument = data.get("instrument", "synth")
        volume = data.get("volume", 1.0)
        effects = data.get("effects", {})
        variation = data.get("variation", 0.5)
        
        # Parse notes
        notes = []
        notes_data = data.get("notes", [])
        
        if isinstance(notes_data, str):
            # Compact string notation: "C4:q D4:q E4:h -:q"
            notes = self._parse_note_string(notes_data)
        elif isinstance(notes_data, list):
            # Array notation
            for note_data in notes_data:
                notes.append(self._parse_note_object(note_data))
        
        return Pattern(
            name=name,
            instrument=instrument,
            notes=notes,
            volume=volume,
            effects=effects,
            variation=variation
        )
    
    def _parse_note_string(self, note_string: str) -> List[Note]:
        """
        Parse compact note notation
        Format: "C4:q D#4:e E4:h -:q"
        Pitch:Duration pairs separated by spaces
        """
        notes = []
        tokens = note_string.split()
        
        for token in tokens:
            if ':' in token:
                parts = token.split(':')
                pitch = parts[0]
                duration_str = parts[1] if len(parts) > 1 else 'q'
                velocity = float(parts[2]) if len(parts) > 2 else 0.8
                
                duration = self.duration_map.get(duration_str, 0.25)
                notes.append(Note(pitch=pitch, duration=duration, velocity=velocity))
            else:
                # Just pitch, default quarter note
                notes.append(Note(pitch=token, duration=0.25, velocity=0.8))
        
        return notes
    
    def _parse_note_object(self, note_data: Dict) -> Note:
        """Parse note from object notation"""
        pitch = note_data.get("pitch", "C4")
        
        # Parse duration
        duration_input = note_data.get("duration", "quarter")
        if isinstance(duration_input, str):
            duration = self.duration_map.get(duration_input, 0.25)
        else:
            duration = float(duration_input)
        
        velocity = note_data.get("velocity", 0.8)
        
        return Note(pitch=pitch, duration=duration, velocity=velocity)
    
    def _parse_section(self, name: str, data: Dict) -> Section:
        """Parse a section definition"""
        bars = data.get("bars", 4)
        patterns = data.get("patterns", [])
        tempo = data.get("tempo")
        key = data.get("key")
        effects = data.get("effects", {})
        
        return Section(
            name=name,
            bars=bars,
            patterns=patterns,
            tempo=tempo,
            key=key,
            effects=effects
        )
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the parsed composition
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        if not self.composition:
            return False, ["No composition loaded"]
        
        # Check that all patterns in sections exist
        for section in self.composition.sections:
            for pattern_name in section.patterns:
                if pattern_name not in self.composition.patterns:
                    errors.append(
                        f"Section '{section.name}' references undefined pattern '{pattern_name}'"
                    )
        
        # Check that all sections in structure exist
        section_names = {s.name for s in self.composition.sections}
        for section_ref in self.composition.structure:
            if section_ref not in section_names:
                errors.append(
                    f"Structure references undefined section '{section_ref}'"
                )
        
        return len(errors) == 0, errors
    
    def get_total_duration_bars(self) -> int:
        """Calculate total duration in bars"""
        if not self.composition:
            return 0
        
        total = 0
        section_map = {s.name: s for s in self.composition.sections}
        
        for section_name in self.composition.structure:
            if section_name in section_map:
                total += section_map[section_name].bars
        
        return total
    
    def print_summary(self):
        """Print a human-readable summary of the composition"""
        if not self.composition:
            print("No composition loaded")
            return
        
        c = self.composition
        
        print(f"\n🎵 {c.title}")
        print(f"👤 Artist: {c.artist}")
        print(f"🎸 Genre: {c.genre}")
        print(f"⏱️  Tempo: {c.tempo} BPM")
        print(f"🎹 Key: {c.key}")
        print(f"📊 Time: {c.time_signature[0]}/{c.time_signature[1]}")
        print(f"\n📋 Patterns ({len(c.patterns)}):")
        for name, pattern in c.patterns.items():
            print(f"  • {name}: {pattern.instrument} ({len(pattern.notes)} notes)")
        
        print(f"\n🎼 Sections ({len(c.sections)}):")
        for section in c.sections:
            print(f"  • {section.name}: {section.bars} bars, {len(section.patterns)} patterns")
        
        print(f"\n🏗️  Structure:")
        print(f"  {' → '.join(c.structure)}")
        print(f"\n⏳ Total Duration: {self.get_total_duration_bars()} bars")
