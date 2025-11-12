"""
Variation Engine - Intelligent musical variation generation
"""

import random
import numpy as np
from typing import List, Tuple, Dict


class VariationEngine:
    """
    Generate intelligent musical variations based on music theory rules
    """
    
    def __init__(self):
        # Probability matrices for intelligent variation
        self.rhythm_patterns = {
            'lofi': [
                [1, 0, 0, 0.5, 0, 0, 0.7, 0],  # Laid-back
                [1, 0, 0.3, 0, 0.6, 0, 0, 0.4],  # Syncopated
                [1, 0, 0, 0.7, 0, 0.4, 0, 0],  # Swung
            ],
            'electro': [
                [1, 0, 0.8, 0, 1, 0, 0.8, 0],  # Four-on-floor variation
                [1, 0.6, 0.8, 0.6, 1, 0.6, 0.8, 0.6],  # Busy
                [1, 0, 0.5, 0.5, 1, 0, 0.5, 0.5],  # Subdivided
            ],
            'funk': [
                [1, 0, 0.7, 0.3, 0.5, 0.7, 0.3, 0],  # Classic funk
                [1, 0.4, 0, 0.6, 0.8, 0, 0.4, 0.6],  # Syncopated
                [1, 0.3, 0.6, 0.3, 1, 0.3, 0.6, 0.3],  # Dense
            ],
        }
        
        # Melodic motion probabilities (step, leap, repeat)
        self.melodic_motion = {
            'smooth': {'step': 0.65, 'leap': 0.20, 'repeat': 0.15},
            'jumpy': {'step': 0.35, 'leap': 0.50, 'repeat': 0.15},
            'syncopated': {'step': 0.50, 'leap': 0.35, 'repeat': 0.15},
            'arpeggio': {'step': 0.25, 'leap': 0.60, 'repeat': 0.15},
        }
        
        # Harmonic tension probabilities
        self.tension_resolution = {
            'low': 0.2,    # 20% chance of tension
            'medium': 0.4, # 40% chance
            'high': 0.6,   # 60% chance
        }
        
    def generate_rhythm_variation(self, genre: str, bars: int = 4) -> List[float]:
        """
        Generate intelligent rhythm variation based on genre
        
        Args:
            genre: Musical genre
            bars: Number of bars
        
        Returns:
            List of rhythm weights (0-1)
        """
        patterns = self.rhythm_patterns.get(genre, self.rhythm_patterns['lofi'])
        
        rhythm = []
        steps_per_bar = 16  # 16th note resolution
        
        for bar in range(bars):
            # Choose a pattern for this bar (with intelligent variation)
            if bar % 2 == 0:
                pattern = random.choice(patterns)
            else:
                # Complement the previous pattern
                pattern = random.choice(patterns)
            
            # Add micro-variations
            for step in pattern:
                # Add humanization (slight timing variations)
                variation = step * random.uniform(0.85, 1.15)
                rhythm.append(max(0, min(1, variation)))
        
        return rhythm
    
    def generate_melodic_contour(self, scale_notes: List[Tuple[str, float]], 
                                 length: int, style: str = 'smooth',
                                 key_center: int = None) -> List[int]:
        """
        Generate intelligent melodic contour with music theory rules
        
        Args:
            scale_notes: Available scale notes
            length: Number of notes to generate
            style: Melodic style (smooth, jumpy, etc.)
            key_center: Index of the tonic note
        
        Returns:
            List of note indices
        """
        if key_center is None:
            key_center = len(scale_notes) // 2
        
        motion_probs = self.melodic_motion.get(style, self.melodic_motion['smooth'])
        
        melody_indices = [key_center]  # Start on tonic
        current_idx = key_center
        direction = 1  # Start going up
        
        for i in range(1, length):
            # Decide on motion type
            motion_type = random.choices(
                ['step', 'leap', 'repeat'],
                weights=[motion_probs['step'], motion_probs['leap'], motion_probs['repeat']]
            )[0]
            
            if motion_type == 'repeat':
                next_idx = current_idx
            
            elif motion_type == 'step':
                # Step by 1-2 scale degrees
                step_size = random.choice([1, 2]) * direction
                next_idx = current_idx + step_size
                
            else:  # leap
                # Leap by 3-5 scale degrees
                leap_size = random.choice([3, 4, 5]) * direction
                next_idx = current_idx + leap_size
            
            # Boundary checking and direction change
            if next_idx >= len(scale_notes):
                next_idx = len(scale_notes) - 1
                direction = -1  # Change direction
            elif next_idx < 0:
                next_idx = 0
                direction = 1  # Change direction
            
            # Tendency towards key center (gravity)
            if i % 4 == 3:  # Every 4th note
                # Pull towards tonic or dominant
                if random.random() < 0.4:
                    # Move towards tonic
                    if next_idx > key_center:
                        next_idx -= 1
                    elif next_idx < key_center:
                        next_idx += 1
            
            # Add to melody
            melody_indices.append(next_idx)
            current_idx = next_idx
            
            # Occasional direction change for interest
            if random.random() < 0.25:
                direction *= -1
        
        # Ensure ending on strong degree (tonic or dominant)
        strong_degrees = [key_center, key_center + 4]  # Tonic and dominant
        if melody_indices[-1] not in strong_degrees:
            melody_indices[-1] = random.choice([idx for idx in strong_degrees if idx < len(scale_notes)])
        
        return melody_indices
    
    def add_chord_extensions(self, base_freqs: List[float], 
                            complexity: float = 0.5) -> List[float]:
        """
        Add jazz extensions to chords based on complexity
        
        Args:
            base_freqs: Base chord frequencies (root, 3rd, 5th)
            complexity: How complex extensions (0-1)
        
        Returns:
            Extended chord frequencies
        """
        extended = list(base_freqs)
        
        # Add 7th
        if random.random() < complexity * 0.8:
            # Minor 7th or Major 7th
            if random.random() < 0.7:
                extended.append(base_freqs[0] * 1.782)  # Minor 7th
            else:
                extended.append(base_freqs[0] * 1.888)  # Major 7th
        
        # Add 9th
        if random.random() < complexity * 0.6:
            extended.append(base_freqs[0] * 2.246)  # 9th
        
        # Add 11th or 13th
        if random.random() < complexity * 0.4:
            if random.random() < 0.5:
                extended.append(base_freqs[0] * 2.667)  # 11th
            else:
                extended.append(base_freqs[0] * 3.364)  # 13th
        
        return extended
    
    def generate_bass_groove(self, root_freqs: List[float], 
                            bpm: int, bars: int, 
                            groove_type: str = 'root') -> List[Tuple[float, float, float]]:
        """
        Generate intelligent bass groove with variations
        
        Args:
            root_freqs: Root note frequencies for progression
            bpm: Tempo
            bars: Number of bars
            groove_type: Type of groove pattern
        
        Returns:
            List of (frequency, start_time, duration) tuples
        """
        beat_duration = 60.0 / bpm
        bar_duration = beat_duration * 4
        
        bass_notes = []
        
        for bar_idx in range(bars):
            chord_idx = bar_idx % len(root_freqs)
            root = root_freqs[chord_idx]
            fifth = root * 1.5  # Perfect fifth
            octave = root * 2.0  # Octave
            
            bar_start = bar_idx * bar_duration
            
            if groove_type == 'root':
                # Simple root notes on 1 and 3
                bass_notes.append((root, bar_start, beat_duration))
                bass_notes.append((root, bar_start + beat_duration * 2, beat_duration))
            
            elif groove_type == 'fifth':
                # Root and fifth alternating
                bass_notes.append((root, bar_start, beat_duration))
                bass_notes.append((fifth, bar_start + beat_duration * 2, beat_duration))
            
            elif groove_type == 'walking':
                # Walking bass with passing tones
                bass_notes.append((root, bar_start, beat_duration * 0.8))
                bass_notes.append((fifth, bar_start + beat_duration, beat_duration * 0.8))
                
                # Passing tone (approach next chord)
                next_chord_idx = (chord_idx + 1) % len(root_freqs)
                approach = root_freqs[next_chord_idx] * 0.94  # Half step below
                bass_notes.append((approach, bar_start + beat_duration * 3, beat_duration * 0.8))
            
            # Add ghost notes randomly for groove
            if random.random() < 0.3:
                ghost_time = bar_start + beat_duration * random.uniform(0.5, 3.5)
                ghost_dur = beat_duration * 0.2
                bass_notes.append((root * 0.5, ghost_time, ghost_dur))
        
        return bass_notes
    
    def apply_swing(self, timings: List[float], amount: float = 0.6) -> List[float]:
        """
        Apply swing timing to note events
        
        Args:
            timings: Original timing positions
            amount: Swing amount (0-1, where 0.5 is straight, 0.67 is classic swing)
        
        Returns:
            Swung timings
        """
        swung = []
        
        for i, time in enumerate(timings):
            # Apply swing to off-beats
            if i % 2 == 1:  # Off-beat
                # Delay the off-beat
                swing_offset = amount * 0.15  # Up to 15% delay
                swung.append(time + swing_offset)
            else:
                swung.append(time)
        
        return swung
    
    def generate_velocity_curve(self, length: int, 
                               dynamics: str = 'medium') -> List[float]:
        """
        Generate musical velocity/dynamics curve
        
        Args:
            length: Number of velocity values
            dynamics: Dynamic style (soft, medium, loud, varied)
        
        Returns:
            List of velocity values (0-1)
        """
        base_levels = {
            'soft': 0.5,
            'medium': 0.7,
            'loud': 0.9,
            'varied': 0.7,
        }
        
        base = base_levels.get(dynamics, 0.7)
        velocities = []
        
        for i in range(length):
            # Add musical phrasing (crescendo/diminuendo)
            phrase_position = (i % 8) / 8  # 8-note phrases
            
            if dynamics == 'varied':
                # Create dynamic contour
                if phrase_position < 0.5:
                    # Crescendo
                    dynamic_curve = base + 0.2 * phrase_position * 2
                else:
                    # Diminuendo
                    dynamic_curve = base + 0.2 * (1 - (phrase_position - 0.5) * 2)
            else:
                dynamic_curve = base
            
            # Add micro-variations for humanization
            variation = random.uniform(-0.05, 0.05)
            velocity = max(0.1, min(1.0, dynamic_curve + variation))
            
            # Accent strong beats
            if i % 4 == 0:
                velocity = min(1.0, velocity * 1.15)
            
            velocities.append(velocity)
        
        return velocities
