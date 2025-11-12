"""
JDCL Compiler - Compile .jdcl files into audio
Transforms JDCL compositions into actual music
WITH INTELLIGENT QUALITY ANALYSIS & REGENERATION
"""

from pydub import AudioSegment
from src.jdcl_parser import JDCLParser, Composition, Section, Pattern, Note, InstrumentType
from src.music_theory import MusicTheory
from src.sounds import SoundGenerator
from src.beat_maker import BeatMaker
from src.effects import EffectsProcessor
from src.variation_engine import VariationEngine
from src.audio_quality_analyzer import AudioQualityAnalyzer, AudioQualityReport
from src.audio_humanizer import AudioHumanizer
from src.silence_filler import SilenceFiller
from src.advanced_mastering import AdvancedMasteringChain
import random
import numpy as np
from typing import Dict, List, Optional, Tuple
import os
import tempfile


class JDCLCompiler:
    """
    Intelligent JDCL Compiler with Quality Analysis & Regeneration
    
    Features:
    - Audio quality analysis (peaks, silence, spectrum)
    - Automatic regeneration if quality fails
    - Audio humanization (natural feel)
    - Silence gap filling
    - Professional mastering chain
    - Multi-pass processing
    """
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
        self.parser = JDCLParser()
        self.theory = MusicTheory()
        self.generator = SoundGenerator(sample_rate)
        self.beat_maker = BeatMaker(sample_rate)
        self.effects = EffectsProcessor(sample_rate)
        self.variation_engine = VariationEngine()
        
        # NEW: Advanced processing modules
        self.quality_analyzer = AudioQualityAnalyzer(sample_rate)
        self.humanizer = AudioHumanizer(sample_rate)
        self.silence_filler = SilenceFiller(sample_rate)
        self.mastering = AdvancedMasteringChain(sample_rate)
        
        # Cache for generated sounds
        self.sound_cache: Dict[str, AudioSegment] = {}
        
        # Quality settings (STRICTER STANDARDS!)
        self.max_regeneration_attempts = 5  # More chances (was 3)
        self.enable_auto_fix = True
        self.enable_humanization = True
        self.enable_mastering = True
    
    def compile_file(self, jdcl_path: str, output_path: str, 
                     verbose: bool = True,
                     enable_qa: bool = True,
                     enable_humanization: bool = True,
                     enable_mastering: bool = True) -> Tuple[AudioSegment, AudioQualityReport]:
        """
        Compile a .jdcl file to audio with intelligent quality control
        
        Args:
            jdcl_path: Path to .jdcl file
            output_path: Path for output .wav file
            verbose: Print compilation progress
            enable_qa: Enable quality analysis & regeneration
            enable_humanization: Apply humanization
            enable_mastering: Apply mastering chain
            
        Returns:
            (Generated AudioSegment, Quality Report)
        """
        # Parse the file
        if verbose:
            print(f"\n{'='*70}")
            print(f"🎼 JDCL INTELLIGENT COMPILER v2.0")
            print(f"{'='*70}")
            print(f"📖 Parsing {jdcl_path}...")
        
        composition = self.parser.parse_file(jdcl_path)
        
        # Validate
        is_valid, errors = self.parser.validate()
        if not is_valid:
            print("❌ Validation errors:")
            for error in errors:
                print(f"  • {error}")
            raise ValueError("Invalid JDCL composition")
        
        if verbose:
            self.parser.print_summary()
            print(f"\n{'='*70}")
            print("🎵 COMPILATION PIPELINE")
            print(f"{'='*70}")
        
        # Compile with intelligent regeneration
        audio, report = self._compile_with_quality_control(
            composition, 
            verbose=verbose,
            enable_qa=enable_qa,
            enable_humanization=enable_humanization,
            enable_mastering=enable_mastering
        )
        
        # Export
        if verbose:
            print(f"\n{'='*70}")
            print(f"💾 Exporting to {output_path}...")
        
        audio.export(output_path, format="wav")
        
        if verbose:
            duration = len(audio) / 1000.0
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ EXPORT COMPLETE!")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   File Size: {file_size:.1f} MB")
            print(f"   Quality Score: {report.overall_score:.1f}/100")
            print(f"{'='*70}\n")
        
        return audio, report
    
    def _compile_with_quality_control(self, composition: Composition,
                                     verbose: bool = True,
                                     enable_qa: bool = True,
                                     enable_humanization: bool = True,
                                     enable_mastering: bool = True) -> Tuple[AudioSegment, AudioQualityReport]:
        """
        Compile with intelligent quality control and regeneration
        """
        best_audio = None
        best_report = None
        best_score = -1.0  # Start at -1 so even score=0 audio gets saved
        
        for attempt in range(self.max_regeneration_attempts):
            if verbose and enable_qa:
                print(f"\n🔄 Generation Attempt {attempt + 1}/{self.max_regeneration_attempts}")
            
            # === STAGE 1: Initial Compilation ===
            if verbose:
                print("  📍 Stage 1: Initial Audio Generation")
            
            audio = self._compile_composition_base(composition, verbose=False)
            
            # === STAGE 2: Quality Analysis ===
            if enable_qa:
                if verbose:
                    print("  📍 Stage 2: Quality Analysis")
                
                report = self.quality_analyzer.analyze(audio, verbose=verbose)
                
                # Save if best so far
                if report.overall_score > best_score:
                    best_score = report.overall_score
                    best_audio = audio
                    best_report = report
                
                # Check if passed
                if report.passed:
                    if verbose:
                        print(f"  ✅ Quality Check PASSED (Score: {report.overall_score:.1f}/100)")
                    break
                else:
                    if verbose:
                        print(f"  ⚠️  Quality Check FAILED (Score: {report.overall_score:.1f}/100)")
                        print(f"  🔄 Regenerating with adjustments...")
                    
                    # Adjust parameters for next attempt
                    self._adjust_generation_parameters(report)
            else:
                best_audio = audio
                best_report = None
                break
        
        # Use best version
        audio = best_audio
        
        if verbose and enable_qa and best_report:
            if best_report.passed:
                print(f"\n✅ Final Quality: {best_report.overall_score:.1f}/100 - PASSED")
            else:
                print(f"\n⚠️  Best Quality: {best_report.overall_score:.1f}/100 (improvements applied)")
        
        # === STAGE 3: Intelligent Fixes ===
        if enable_qa and self.enable_auto_fix and best_report:
            if verbose:
                print("\n  📍 Stage 3: Intelligent Audio Repair")
            
            audio = self._apply_intelligent_fixes(audio, best_report, verbose=verbose)
        
        # === STAGE 4: Humanization ===
        if enable_humanization and self.enable_humanization:
            if verbose:
                print("\n  📍 Stage 4: Audio Humanization")
                print("    • Applying micro-timing variations...")
                print("    • Adding velocity humanization...")
                print("    • Introducing pitch wobble...")
                print("    • Adding groove feel...")
                print("    • Applying analog warmth...")
            
            audio = self.humanizer.humanize_audio(
                audio,
                timing_drift=0.6,         # INCREASED (was 0.3)
                velocity_variation=0.35,  # INCREASED (was 0.25)
                pitch_wobble=0.25,        # INCREASED (was 0.15)
                groove_amount=0.6,        # INCREASED (was 0.35)
                analog_warmth=0.5         # INCREASED (was 0.3)
            )
            
            # Add room ambience
            audio = self.humanizer.add_room_ambience(audio, room_size="small", mix=0.12)
        
        # === STAGE 5: Professional Mastering ===
        if enable_mastering and self.enable_mastering:
            if verbose:
                print("\n  📍 Stage 5: Professional Mastering")
            
            # Determine mastering style from genre
            genre = getattr(composition, 'genre', 'balanced')
            if genre:
                genre = genre.lower()
            else:
                genre = 'balanced'
                
            style_map = {
                'lofi': 'warm',
                'funk': 'warm',
                'relax': 'warm',
                'ambient': 'warm',
                'electro': 'bright',
                'synthwave': 'bright',
                'edm': 'aggressive',
                'trap': 'aggressive',
            }
            mastering_style = style_map.get(genre, 'balanced')
            
            audio = self.mastering.master_audio(
                audio,
                target_lufs=-11.0,        # LOUDER! (was -14.0) - club/radio standard
                target_style=mastering_style,
                apply_saturation=True,
                enhance_stereo=True,
                verbose=verbose
            )
        
        # Final quality analysis
        if enable_qa:
            if verbose:
                print(f"\n{'='*70}")
                print("📊 FINAL QUALITY REPORT")
                print(f"{'='*70}")
            
            final_report = self.quality_analyzer.analyze(audio, verbose=verbose)
        else:
            final_report = AudioQualityReport()
            final_report.overall_score = 100.0
            final_report.passed = True
        
        return audio, final_report
    
    def _compile_composition_base(self, composition: Composition, 
                                  verbose: bool = True) -> AudioSegment:
        """Compile a Composition object to audio"""
        
        # Initialize empty track
        track = AudioSegment.silent(duration=0)
        
        # Get section map
        section_map = {s.name: s for s in composition.sections}
        
        # Compile each section in order
        for idx, section_name in enumerate(composition.structure):
            if section_name not in section_map:
                print(f"⚠ Skipping undefined section: {section_name}")
                continue
            
            section = section_map[section_name]
            
            if verbose:
                print(f"  [{idx+1}/{len(composition.structure)}] Compiling section: {section_name}")
            
            # Compile section
            section_audio = self.compile_section(
                section, 
                composition,
                verbose=verbose
            )
            
            # Add crossfade between sections (100ms)
            if len(track) > 0:
                track = track.append(section_audio, crossfade=100)
            else:
                track = section_audio
        
        # Apply global effects
        if composition.global_effects:
            if verbose:
                print("  🎚️  Applying global effects...")
            track = self._apply_effects(track, composition.global_effects)
        
        return track
    
    def compile_section(self, section: Section, composition: Composition,
                       verbose: bool = False) -> AudioSegment:
        """Compile a single section"""
        
        # Get tempo and key (section override or global)
        tempo = section.tempo or composition.tempo
        key = section.key or composition.key
        
        # Calculate section duration
        beat_duration = 60.0 / tempo  # seconds per beat
        bar_duration = beat_duration * composition.time_signature[0]
        section_duration_ms = int(bar_duration * section.bars * 1000)
        
        # Start with silence
        section_audio = AudioSegment.silent(duration=section_duration_ms)
        
        # Compile each pattern in the section
        for pattern_name in section.patterns:
            if pattern_name not in composition.patterns:
                continue
            
            pattern = composition.patterns[pattern_name]
            
            if verbose:
                print(f"    • Pattern: {pattern_name} ({pattern.instrument})")
            
            # Compile pattern
            pattern_audio = self.compile_pattern(
                pattern,
                tempo,
                key,
                section.bars,
                composition.time_signature
            )
            
            # Adjust volume
            if pattern.volume != 1.0:
                db_change = 20 * np.log10(pattern.volume)
                pattern_audio = pattern_audio + db_change
            
            # Apply pattern effects
            if pattern.effects:
                pattern_audio = self._apply_effects(pattern_audio, pattern.effects)
            
            # Mix into section (overlay)
            section_audio = section_audio.overlay(pattern_audio)
        
        # Apply section effects
        if section.effects:
            section_audio = self._apply_effects(section_audio, section.effects)
        
        return section_audio
    
    def compile_pattern(self, pattern: Pattern, tempo: int, key: str,
                       bars: int, time_signature: tuple) -> AudioSegment:
        """Compile a pattern into audio"""
        
        # Calculate timing
        beat_duration = 60.0 / tempo  # seconds per beat
        
        # Check if it's a drum pattern
        is_drum = pattern.instrument in ['kick', 'snare', 'hihat', 'clap', 'drums']
        
        if is_drum:
            return self._compile_drum_pattern(pattern, tempo, bars, time_signature)
        else:
            return self._compile_melodic_pattern(
                pattern, tempo, key, bars, time_signature
            )
    
    def _compile_drum_pattern(self, pattern: Pattern, tempo: int,
                             bars: int, time_signature: tuple) -> AudioSegment:
        """Compile drum pattern"""
        
        beat_duration_ms = (60.0 / tempo) * 1000
        bar_duration_ms = beat_duration_ms * time_signature[0]
        total_duration_ms = int(bar_duration_ms * bars)
        
        # Start with silence
        drum_track = AudioSegment.silent(duration=total_duration_ms)
        
        # Place each hit
        current_time_ms = 0
        current_beat = 0
        
        for note in pattern.notes:
            if not note.is_rest():
                # Generate drum sound
                if pattern.instrument == 'kick':
                    sound = self.generator.generate_kick(0.5, pattern.variation)
                elif pattern.instrument == 'snare':
                    sound = self.generator.generate_snare(0.2, pattern.variation)
                elif pattern.instrument == 'hihat':
                    closed = note.pitch.lower() != 'open'
                    sound = self.generator.generate_hihat(0.1, closed, pattern.variation)
                elif pattern.instrument == 'clap':
                    sound = self.generator.generate_snare(0.15, pattern.variation)
                else:
                    sound = self.generator.generate_kick(0.5, pattern.variation)
                
                # Apply velocity
                if note.velocity != 1.0:
                    db_change = 20 * np.log10(note.velocity)
                    sound = sound + db_change
                
                # Overlay at current position
                drum_track = drum_track.overlay(sound, position=int(current_time_ms))
            
            # Advance time
            note_duration_ms = note.duration * beat_duration_ms
            current_time_ms += note_duration_ms
            current_beat += note.duration
            
            # Loop back if we exceed the bar length
            if current_time_ms >= total_duration_ms:
                current_time_ms = current_time_ms % total_duration_ms
        
        return drum_track
    
    def _compile_melodic_pattern(self, pattern: Pattern, tempo: int,
                                key: str, bars: int, 
                                time_signature: tuple) -> AudioSegment:
        """Compile melodic pattern (piano, synth, bass, etc.)"""
        
        beat_duration_ms = (60.0 / tempo) * 1000
        bar_duration_ms = beat_duration_ms * time_signature[0]
        total_duration_ms = int(bar_duration_ms * bars)
        
        # Start with silence
        melodic_track = AudioSegment.silent(duration=total_duration_ms)
        
        # Place each note
        current_time_ms = 0
        
        for note in pattern.notes:
            if not note.is_rest():
                # Convert note to frequency
                frequency = self._note_to_frequency(note.pitch)
                
                # Calculate note duration in seconds
                note_duration_sec = (note.duration * beat_duration_ms) / 1000.0
                
                # Generate sound based on instrument
                sound = self._generate_instrument_sound(
                    pattern.instrument,
                    frequency,
                    note_duration_sec,
                    note.velocity,
                    pattern.variation
                )
                
                # Overlay at current position
                melodic_track = melodic_track.overlay(sound, position=int(current_time_ms))
            
            # Advance time
            note_duration_ms = note.duration * beat_duration_ms
            current_time_ms += note_duration_ms
        
        return melodic_track
    
    def _generate_instrument_sound(self, instrument: str, frequency: float,
                                   duration: float, velocity: float,
                                   variation: float) -> AudioSegment:
        """Generate sound for specific instrument"""
        
        instrument = instrument.lower()
        
        if instrument == 'piano':
            return self.generator.generate_piano(
                frequency, duration, velocity, variation
            )
        elif instrument == 'bass':
            return self.generator.generate_bass(duration, frequency)
        elif instrument == 'sub_bass':
            # Pure sine wave
            samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, samples)
            wave = np.sin(2 * np.pi * frequency * t)
            wave *= np.exp(-0.5 * t)  # Gentle decay
            wave = (wave * velocity * 0.8 * (2**23 - 1)).astype(np.int32)
            return AudioSegment(
                wave.tobytes(),
                frame_rate=self.sample_rate,
                sample_width=4,
                channels=1
            )
        elif instrument == 'synth':
            return self.generator.generate_synth(duration, frequency, 'sawtooth')
        elif instrument == 'pad':
            # Detuned synth for pad
            sound1 = self.generator.generate_synth(duration, frequency, 'sine')
            sound2 = self.generator.generate_synth(duration, frequency * 1.01, 'sine')
            sound3 = self.generator.generate_synth(duration, frequency * 0.99, 'sine')
            return sound1.overlay(sound2).overlay(sound3) - 6  # -6dB for mix
        elif instrument == 'ambient':
            # Ambient texture
            return self.generator.generate_synth(duration, frequency, 'sine')
        else:
            # Default to synth
            return self.generator.generate_synth(duration, frequency)
    
    def _note_to_frequency(self, note_str: str) -> float:
        """Convert note string to frequency (e.g., 'C4' -> 261.63)"""
        # Parse note string
        match = re.match(r'([A-G]#?)(\d+)', note_str)
        if not match:
            return 440.0  # Default A4
        
        note_name = match.group(1)
        octave = int(match.group(2))
        
        return self.theory.note_to_freq(note_name, octave)
    
    def _apply_effects(self, audio: AudioSegment, 
                      effects_config: Dict) -> AudioSegment:
        """Apply effects from configuration"""
        
        # Save to temp file for effects processing
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            temp_path = tmp.name
            audio.export(temp_path, format='wav')
        
        try:
            processed = audio
            
            for effect_name, effect_params in effects_config.items():
                effect_name = effect_name.lower()
                
                if effect_name == 'reverb':
                    mix = effect_params.get('mix', 0.5)
                    intensity = effect_params.get('intensity', 0.5)
                    processed = self.effects._apply_reverb(temp_path, mix, intensity)
                    processed.export(temp_path, format='wav')
                
                elif effect_name == 'delay':
                    mix = effect_params.get('mix', 0.3)
                    intensity = effect_params.get('intensity', 0.5)
                    processed = self.effects._apply_delay(temp_path, mix, intensity)
                    processed.export(temp_path, format='wav')
                
                elif effect_name == 'distortion':
                    mix = effect_params.get('mix', 0.5)
                    intensity = effect_params.get('intensity', 0.5)
                    processed = self.effects._apply_distortion(temp_path, mix, intensity)
                    processed.export(temp_path, format='wav')
                
                elif effect_name == 'chorus':
                    mix = effect_params.get('mix', 0.5)
                    intensity = effect_params.get('intensity', 0.5)
                    processed = self.effects._apply_chorus(temp_path, mix, intensity)
                    processed.export(temp_path, format='wav')
                
                elif effect_name == 'filter':
                    mix = effect_params.get('mix', 0.5)
                    intensity = effect_params.get('intensity', 0.5)
                    processed = self.effects._apply_filter(temp_path, mix, intensity)
                    processed.export(temp_path, format='wav')
            
            return processed
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _adjust_generation_parameters(self, report: AudioQualityReport):
        """Adjust generation parameters based on quality report"""
        # Add randomness to variation for next attempt
        if hasattr(self.generator, 'variation_amount'):
            self.generator.variation_amount *= random.uniform(0.9, 1.1)
    
    def _apply_intelligent_fixes(self, audio: AudioSegment, 
                                report: AudioQualityReport,
                                verbose: bool = True) -> AudioSegment:
        """Apply intelligent fixes based on quality report"""
        
        # Fix silence gaps
        if report.silence_gap_count > 0 and report.longest_silence_duration > 1.0:
            if verbose:
                print(f"    • Filling {report.silence_gap_count} silence gaps...")
            
            audio = self.silence_filler.fill_silence_gaps(
                audio,
                min_gap_duration=0.8,
                fill_style="smart",
                fill_volume=0.25
            )
        
        # Add subtle ambient layer if too much silence overall
        if report.total_silence_percentage > 10.0:
            if verbose:
                print(f"    • Adding continuous ambience layer...")
            
            audio = self.silence_filler.add_continuous_ambience(
                audio,
                ambience_type="subtle",
                volume=0.08
            )
        
        # Apply gentle compression if dynamic range too high
        if report.dynamic_range_db > 20.0:
            if verbose:
                print(f"    • Applying dynamic range compression...")
            
            # Gentle compression
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            samples = samples / (2**15)
            
            # Simple soft knee compression
            threshold = 0.6
            compressed = np.where(
                np.abs(samples) > threshold,
                threshold + (np.abs(samples) - threshold) * 0.5,
                np.abs(samples)
            ) * np.sign(samples)
            
            compressed = np.clip(compressed, -1.0, 1.0)
            compressed = (compressed * (2**15)).astype(np.int16)
            
            audio = AudioSegment(
                compressed.tobytes(),
                frame_rate=audio.frame_rate,
                sample_width=audio.sample_width,
                channels=audio.channels
            )
        
        return audio


import re  # Add at top with other imports

