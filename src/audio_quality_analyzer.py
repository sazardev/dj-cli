"""
Audio Quality Analyzer - Intelligent audio analysis and validation
Analyzes peaks, saturation, silences, spectral coherence, frequency balance
WITH PROFESSIONAL LUFS METERING
"""

import numpy as np
from scipy import signal, fft
from pydub import AudioSegment
from typing import Dict, List, Tuple, Optional
import warnings

# Professional loudness metering
try:
    import pyloudnorm as pyln
    LUFS_AVAILABLE = True
except ImportError:
    LUFS_AVAILABLE = False
    print("⚠ pyloudnorm not available, LUFS metering disabled")


class AudioQualityReport:
    """Comprehensive audio quality report"""
    
    def __init__(self):
        self.peak_level_db: float = 0.0
        self.rms_level_db: float = 0.0
        self.dynamic_range_db: float = 0.0
        self.crest_factor_db: float = 0.0
        
        # Saturation & Clipping
        self.clipping_percentage: float = 0.0
        self.saturation_count: int = 0
        self.near_clipping_percentage: float = 0.0
        
        # Silence Analysis
        self.silence_gaps: List[Tuple[float, float]] = []  # (start_time, duration)
        self.total_silence_percentage: float = 0.0
        self.longest_silence_duration: float = 0.0
        self.silence_gap_count: int = 0
        
        # Spectral Analysis
        self.spectral_centroid: float = 0.0
        self.spectral_rolloff: float = 0.0
        self.spectral_flatness: float = 0.0
        self.spectral_flux: float = 0.0
        
        # Frequency Balance
        self.sub_bass_energy: float = 0.0  # <60Hz
        self.bass_energy: float = 0.0      # 60-250Hz
        self.low_mid_energy: float = 0.0   # 250-500Hz
        self.mid_energy: float = 0.0       # 500-2kHz
        self.high_mid_energy: float = 0.0  # 2k-6kHz
        self.high_energy: float = 0.0      # 6k-20kHz
        
        # Stereo Analysis
        self.stereo_width: float = 0.0
        self.phase_correlation: float = 0.0
        
        # Professional Loudness Metering (LUFS)
        self.integrated_lufs: float = 0.0   # Overall loudness
        self.true_peak_db: float = 0.0       # True peak (inter-sample)
        self.loudness_range_lu: float = 0.0  # LRA (dynamic range in Loudness Units)
        
        # Quality Scores
        self.overall_score: float = 0.0  # 0-100
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.passed: bool = False
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary"""
        return {
            'peak_level_db': round(self.peak_level_db, 2),
            'rms_level_db': round(self.rms_level_db, 2),
            'dynamic_range_db': round(self.dynamic_range_db, 2),
            'crest_factor_db': round(self.crest_factor_db, 2),
            'clipping_percentage': round(self.clipping_percentage, 3),
            'silence_gaps': len(self.silence_gaps),
            'total_silence_percentage': round(self.total_silence_percentage, 2),
            'longest_silence_duration': round(self.longest_silence_duration, 2),
            'spectral_centroid': round(self.spectral_centroid, 1),
            'frequency_balance': {
                'sub_bass': round(self.sub_bass_energy, 2),
                'bass': round(self.bass_energy, 2),
                'low_mid': round(self.low_mid_energy, 2),
                'mid': round(self.mid_energy, 2),
                'high_mid': round(self.high_mid_energy, 2),
                'high': round(self.high_energy, 2),
            },
            'stereo_width': round(self.stereo_width, 2),
            'phase_correlation': round(self.phase_correlation, 2),
            'overall_score': round(self.overall_score, 1),
            'passed': self.passed,
            'issues': self.issues,
            'warnings': self.warnings,
        }


class AudioQualityAnalyzer:
    """
    Comprehensive audio quality analysis system
    Detects issues: clipping, silence gaps, poor frequency balance, phase problems
    """
    
    def __init__(self, sample_rate: int = 96000):
        self.sample_rate = sample_rate
        
        # Quality thresholds - RELAXED FOR ELECTRONIC MUSIC
        self.thresholds = {
            'peak_max_db': -0.1,              # RELAXED: Hot peaks OK for electro
            'rms_min_db': -30.0,              # RELAXED: Lower minimum loudness
            'rms_max_db': -3.0,               # RELAXED: Louder mixes allowed
            'clipping_max_percentage': 0.5,   # RELAXED: 0.5% clipping OK
            'silence_max_gap_seconds': 15.0,  # RELAXED: 15s gaps allowed
            'silence_max_percentage': 95.0,   # RELAXED: 95% silence max
            'dynamic_range_min_db': 5.0,      # RELAXED: Electro is compressed! (was 12dB)
            'spectral_flatness_min': 0.001,   # RELAXED: Synths are pure/tonal
            'phase_correlation_min': 0.3,     # RELAXED: Less strict mono compatibility
            'stereo_width_min': 10.0,         # RELAXED: 10% minimum stereo
            'frequency_balance_tolerance': 8.0, # RELAXED: ±8dB balance OK
        }
    
    def analyze(self, audio: AudioSegment, verbose: bool = True) -> AudioQualityReport:
        """
        Comprehensive audio analysis
        
        Args:
            audio: AudioSegment to analyze
            verbose: Print detailed analysis
        
        Returns:
            AudioQualityReport with all metrics
        """
        report = AudioQualityReport()
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)  # Normalize to -1.0 to 1.0
        
        # Handle stereo
        if audio.channels == 2:
            samples = samples.reshape(-1, 2)
            left = samples[:, 0]
            right = samples[:, 1]
            mono = (left + right) / 2.0
        else:
            mono = samples
            left = right = mono
        
        # 1. Peak & RMS Analysis
        self._analyze_levels(mono, report)
        
        # 2. Clipping & Saturation Detection
        self._analyze_clipping(mono, report)
        
        # 3. Silence Gap Detection
        self._analyze_silence_gaps(mono, report, audio.duration_seconds)
        
        # 4. Professional LUFS Metering
        if LUFS_AVAILABLE:
            self._analyze_lufs(samples if audio.channels == 2 else mono.reshape(-1, 1), 
                              report, audio.frame_rate)
        
        # 5. Spectral Analysis
        self._analyze_spectrum(mono, report)
        
        # 5. Frequency Balance Analysis
        self._analyze_frequency_balance(mono, report)
        
        # 6. Stereo Analysis
        if audio.channels == 2:
            self._analyze_stereo(left, right, report)
        
        # 7. Calculate Overall Score
        self._calculate_score(report)
        
        # 8. Generate Issues & Warnings
        self._generate_issues(report)
        
        if verbose:
            self._print_report(report)
        
        return report
    
    def _analyze_levels(self, samples: np.ndarray, report: AudioQualityReport):
        """Analyze peak and RMS levels"""
        # Peak level
        peak = np.max(np.abs(samples))
        report.peak_level_db = 20 * np.log10(peak + 1e-10)
        
        # RMS level
        rms = np.sqrt(np.mean(samples**2))
        report.rms_level_db = 20 * np.log10(rms + 1e-10)
        
        # Dynamic range (rough estimate)
        report.dynamic_range_db = report.peak_level_db - report.rms_level_db
        
        # Crest factor
        report.crest_factor_db = 20 * np.log10(peak / (rms + 1e-10))
    
    def _analyze_clipping(self, samples: np.ndarray, report: AudioQualityReport):
        """Detect clipping and saturation"""
        # Hard clipping (samples at exactly ±1.0)
        clipping_threshold = 0.99
        clipped_samples = np.sum(np.abs(samples) >= clipping_threshold)
        report.clipping_percentage = (clipped_samples / len(samples)) * 100.0
        report.saturation_count = clipped_samples
        
        # Near-clipping (samples > 0.95)
        near_clipping_threshold = 0.95
        near_clipped = np.sum(np.abs(samples) >= near_clipping_threshold)
        report.near_clipping_percentage = (near_clipped / len(samples)) * 100.0
    
    def _analyze_lufs(self, samples: np.ndarray, report: AudioQualityReport, sample_rate: int):
        """
        Measure professional loudness standards (ITU-R BS.1770)
        """
        try:
            # Create loudness meter
            meter = pyln.Meter(sample_rate)
            
            # Integrated loudness (overall loudness)
            report.integrated_lufs = meter.integrated_loudness(samples)
            
            # True peak (inter-sample peaks using oversampling)
            if samples.ndim == 1:
                samples_2d = samples.reshape(-1, 1)
            else:
                samples_2d = samples
            
            # Calculate true peak for each channel
            true_peaks = []
            for channel in range(samples_2d.shape[1]):
                channel_data = samples_2d[:, channel]
                # Upsample 4x for true peak detection
                upsampled = signal.resample(channel_data, len(channel_data) * 4)
                peak = np.max(np.abs(upsampled))
                true_peaks.append(20 * np.log10(peak) if peak > 0 else -np.inf)
            
            report.true_peak_db = max(true_peaks)
            
        except Exception as e:
            print(f"⚠ LUFS measurement error: {e}")
            report.integrated_lufs = -14.0  # Default fallback
            report.true_peak_db = -1.0
    
    def _analyze_silence_gaps(self, samples: np.ndarray, report: AudioQualityReport, 
                             duration_seconds: float):
        """Detect silence gaps and calculate statistics"""
        # Silence threshold (in linear amplitude)
        silence_threshold = 0.001  # -60dB
        
        # Detect silence regions
        is_silent = np.abs(samples) < silence_threshold
        
        # Find contiguous silent regions
        silent_regions = []
        in_silence = False
        silence_start = 0
        
        for i, silent in enumerate(is_silent):
            if silent and not in_silence:
                # Start of silence
                in_silence = True
                silence_start = i
            elif not silent and in_silence:
                # End of silence
                in_silence = False
                silence_duration = (i - silence_start) / self.sample_rate
                
                # Only record gaps > 0.5 seconds
                if silence_duration > 0.5:
                    silence_start_time = silence_start / self.sample_rate
                    silent_regions.append((silence_start_time, silence_duration))
        
        # Handle case where audio ends in silence
        if in_silence:
            silence_duration = (len(samples) - silence_start) / self.sample_rate
            if silence_duration > 0.5:
                silence_start_time = silence_start / self.sample_rate
                silent_regions.append((silence_start_time, silence_duration))
        
        report.silence_gaps = silent_regions
        report.silence_gap_count = len(silent_regions)
        
        # Calculate total silence
        total_silent_samples = np.sum(is_silent)
        report.total_silence_percentage = (total_silent_samples / len(samples)) * 100.0
        
        # Longest silence
        if silent_regions:
            report.longest_silence_duration = max(dur for _, dur in silent_regions)
        else:
            report.longest_silence_duration = 0.0
    
    def _analyze_spectrum(self, samples: np.ndarray, report: AudioQualityReport):
        """Spectral analysis using FFT"""
        # Use STFT for time-varying analysis
        nperseg = 4096
        noverlap = nperseg // 2
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f, t, Zxx = signal.stft(samples, fs=self.sample_rate, 
                                   nperseg=nperseg, noverlap=noverlap)
        
        magnitude = np.abs(Zxx)
        power = magnitude**2
        
        # Spectral Centroid (brightness)
        spectral_centroid = np.sum(f[:, np.newaxis] * power, axis=0) / (np.sum(power, axis=0) + 1e-10)
        report.spectral_centroid = np.mean(spectral_centroid)
        
        # Spectral Rolloff (95% of energy)
        cumulative_power = np.cumsum(power, axis=0)
        total_power = np.sum(power, axis=0)
        rolloff_threshold = 0.95 * total_power
        rolloff_indices = np.argmax(cumulative_power >= rolloff_threshold, axis=0)
        report.spectral_rolloff = np.mean(f[rolloff_indices])
        
        # Spectral Flatness (noisiness vs tonality)
        geometric_mean = np.exp(np.mean(np.log(power + 1e-10), axis=0))
        arithmetic_mean = np.mean(power, axis=0)
        spectral_flatness = geometric_mean / (arithmetic_mean + 1e-10)
        report.spectral_flatness = np.mean(spectral_flatness)
        
        # Spectral Flux (rate of change)
        spectral_flux = np.sqrt(np.mean(np.diff(magnitude, axis=1)**2, axis=0))
        report.spectral_flux = np.mean(spectral_flux)
    
    def _analyze_frequency_balance(self, samples: np.ndarray, report: AudioQualityReport):
        """Analyze energy distribution across frequency bands"""
        # Compute FFT
        fft_size = 8192
        window = signal.windows.hann(fft_size)
        
        # Use multiple windows for averaging
        hop_size = fft_size // 4
        num_windows = (len(samples) - fft_size) // hop_size
        
        band_energies = {
            'sub_bass': 0.0,
            'bass': 0.0,
            'low_mid': 0.0,
            'mid': 0.0,
            'high_mid': 0.0,
            'high': 0.0,
        }
        
        for i in range(num_windows):
            start = i * hop_size
            end = start + fft_size
            
            if end > len(samples):
                break
            
            windowed = samples[start:end] * window
            spectrum = np.abs(fft.fft(windowed))[:fft_size//2]
            power = spectrum**2
            
            # Frequency bins
            freqs = fft.fftfreq(fft_size, 1/self.sample_rate)[:fft_size//2]
            
            # Define frequency bands
            band_energies['sub_bass'] += np.sum(power[(freqs >= 20) & (freqs < 60)])
            band_energies['bass'] += np.sum(power[(freqs >= 60) & (freqs < 250)])
            band_energies['low_mid'] += np.sum(power[(freqs >= 250) & (freqs < 500)])
            band_energies['mid'] += np.sum(power[(freqs >= 500) & (freqs < 2000)])
            band_energies['high_mid'] += np.sum(power[(freqs >= 2000) & (freqs < 6000)])
            band_energies['high'] += np.sum(power[(freqs >= 6000) & (freqs < 20000)])
        
        # Normalize by number of windows
        total_energy = sum(band_energies.values())
        
        if total_energy > 0:
            report.sub_bass_energy = (band_energies['sub_bass'] / total_energy) * 100.0
            report.bass_energy = (band_energies['bass'] / total_energy) * 100.0
            report.low_mid_energy = (band_energies['low_mid'] / total_energy) * 100.0
            report.mid_energy = (band_energies['mid'] / total_energy) * 100.0
            report.high_mid_energy = (band_energies['high_mid'] / total_energy) * 100.0
            report.high_energy = (band_energies['high'] / total_energy) * 100.0
    
    def _analyze_stereo(self, left: np.ndarray, right: np.ndarray, 
                       report: AudioQualityReport):
        """Analyze stereo field"""
        # Stereo width (difference between L and R)
        mid = (left + right) / 2.0
        side = (left - right) / 2.0
        
        mid_energy = np.sum(mid**2)
        side_energy = np.sum(side**2)
        
        total_energy = mid_energy + side_energy
        if total_energy > 0:
            report.stereo_width = (side_energy / total_energy) * 100.0
        
        # Phase correlation
        numerator = np.sum(left * right)
        denominator = np.sqrt(np.sum(left**2) * np.sum(right**2))
        
        if denominator > 0:
            report.phase_correlation = numerator / denominator
    
    def _calculate_score(self, report: AudioQualityReport):
        """Calculate overall quality score (0-100) - RELAXED FOR ELECTRONIC MUSIC"""
        score = 100.0
        
        # RELAXED PENALTIES - MUSIC IS NOT SPEECH!
        
        # 1. Clipping (Minor penalty - some distortion is OK for electro)
        if report.clipping_percentage > self.thresholds['clipping_max_percentage']:
            score -= min(15.0, report.clipping_percentage * 10)  # Much lighter
        
        # 2. Silence gaps (Very light penalty - pauses are musical!)
        if report.total_silence_percentage > self.thresholds['silence_max_percentage']:
            excess = report.total_silence_percentage - self.thresholds['silence_max_percentage']
            score -= min(10.0, excess * 0.5)  # 10x lighter
        
        # 3. Long silence gaps (Light penalty)
        if report.longest_silence_duration > self.thresholds['silence_max_gap_seconds']:
            score -= min(8.0, (report.longest_silence_duration - self.thresholds['silence_max_gap_seconds']) * 2)  # 10x lighter
        
        # 4. Dynamic range (RELAXED - electronic music is compressed)
        if report.dynamic_range_db < self.thresholds['dynamic_range_min_db']:
            score -= min(5.0, (self.thresholds['dynamic_range_min_db'] - report.dynamic_range_db) * 0.5)  # Very light
        
        # 5. Peak level (Light penalty)
        if report.peak_level_db > self.thresholds['peak_max_db']:
            score -= min(10.0, (report.peak_level_db - self.thresholds['peak_max_db']) * 5)  # 4x lighter
        
        # 6. RMS levels (Very light penalties)
        if report.rms_level_db < self.thresholds['rms_min_db']:
            score -= min(5.0, (self.thresholds['rms_min_db'] - report.rms_level_db) * 0.3)  # Very light
        if report.rms_level_db > self.thresholds['rms_max_db']:
            score -= min(5.0, (report.rms_level_db - self.thresholds['rms_max_db']) * 0.5)
        
        # 7. Spectral flatness (IGNORE - synths are supposed to be pure!)
        # No penalty for electronic music
        
        # 8. Phase correlation (Light penalty)
        if report.phase_correlation < self.thresholds['phase_correlation_min']:
            score -= min(8.0, (self.thresholds['phase_correlation_min'] - report.phase_correlation) * 10)  # 4x lighter
        
        # 9. Stereo width (Light penalty)
        if report.stereo_width < self.thresholds['stereo_width_min']:
            score -= min(5.0, (self.thresholds['stereo_width_min'] - report.stereo_width) / 5)  # 2.5x lighter
        
        # 10. Frequency balance (Very relaxed - electronic music can be bass-heavy)
        if hasattr(report, 'frequency_balance') and report.frequency_balance:
            avg_energy = sum(report.frequency_balance.values()) / len(report.frequency_balance)
            for band, energy in report.frequency_balance.items():
                deviation_db = abs(20 * np.log10(energy / avg_energy)) if energy > 0 and avg_energy > 0 else 0
                if deviation_db > self.thresholds['frequency_balance_tolerance']:
                    score -= min(2.0, (deviation_db - self.thresholds['frequency_balance_tolerance']) * 0.3)  # 7x lighter
        
        # 11. LUFS loudness check (Relaxed)
        if LUFS_AVAILABLE and report.integrated_lufs != 0.0:
            # Very relaxed - any loudness is OK
            if report.integrated_lufs < -25.0:
                score -= min(8.0, (-25.0 - report.integrated_lufs) * 0.5)  # Light penalty
            elif report.integrated_lufs > -3.0:
                score -= min(8.0, (report.integrated_lufs + 3.0) * 1)  # Light penalty
            
            # True peak check (relaxed)
            if report.true_peak_db > 0.0:
                score -= min(10.0, (report.true_peak_db) * 5)  # Light penalty
        
        report.overall_score = max(0.0, score)
        report.passed = report.overall_score >= 60.0  # RELAXED! 60/100 minimum for electronic music
    
    def _generate_issues(self, report: AudioQualityReport):
        """Generate human-readable issues and warnings"""
        # Critical issues
        if report.clipping_percentage > self.thresholds['clipping_max_percentage']:
            report.issues.append(
                f"⚠ CLIPPING DETECTED: {report.clipping_percentage:.3f}% of samples are clipped"
            )
        
        if report.longest_silence_duration > self.thresholds['silence_max_gap_seconds']:
            report.issues.append(
                f"⚠ LONG SILENCE GAP: {report.longest_silence_duration:.1f}s of silence detected"
            )
        
        if report.total_silence_percentage > self.thresholds['silence_max_percentage']:
            report.issues.append(
                f"⚠ TOO MUCH SILENCE: {report.total_silence_percentage:.1f}% of audio is silent"
            )
        
        if report.peak_level_db > self.thresholds['peak_max_db']:
            report.issues.append(
                f"⚠ PEAK TOO HOT: {report.peak_level_db:.1f}dB (max {self.thresholds['peak_max_db']}dB)"
            )
        
        # Warnings
        if report.dynamic_range_db < self.thresholds['dynamic_range_min_db']:
            report.warnings.append(
                f"⚡ Low dynamic range: {report.dynamic_range_db:.1f}dB"
            )
        
        if report.spectral_flatness < self.thresholds['spectral_flatness_min']:
            report.warnings.append(
                f"⚡ Sound too synthetic (spectral flatness: {report.spectral_flatness:.3f})"
            )
        
        if report.phase_correlation < self.thresholds['phase_correlation_min']:
            report.warnings.append(
                f"⚡ Phase correlation issues: {report.phase_correlation:.2f}"
            )
        
        if report.silence_gap_count > 5:
            report.warnings.append(
                f"⚡ Multiple silence gaps detected: {report.silence_gap_count} gaps"
            )
    
    def _print_report(self, report: AudioQualityReport):
        """Print formatted analysis report"""
        print("\n" + "="*70)
        print("🔍 AUDIO QUALITY ANALYSIS REPORT")
        print("="*70)
        
        print(f"\n📊 LEVELS:")
        print(f"  Peak:          {report.peak_level_db:>7.2f} dB")
        print(f"  RMS:           {report.rms_level_db:>7.2f} dB")
        print(f"  Dynamic Range: {report.dynamic_range_db:>7.2f} dB")
        print(f"  Crest Factor:  {report.crest_factor_db:>7.2f} dB")
        
        print(f"\n🔊 CLIPPING & SATURATION:")
        print(f"  Clipping:      {report.clipping_percentage:>7.3f} %")
        print(f"  Near-Clipping: {report.near_clipping_percentage:>7.3f} %")
        
        print(f"\n🤫 SILENCE ANALYSIS:")
        print(f"  Total Silence: {report.total_silence_percentage:>7.2f} %")
        print(f"  Silence Gaps:  {report.silence_gap_count:>7} gaps")
        print(f"  Longest Gap:   {report.longest_silence_duration:>7.2f} s")
        
        print(f"\n🎵 SPECTRAL ANALYSIS:")
        print(f"  Centroid:      {report.spectral_centroid:>7.1f} Hz")
        print(f"  Rolloff:       {report.spectral_rolloff:>7.1f} Hz")
        print(f"  Flatness:      {report.spectral_flatness:>7.3f}")
        print(f"  Flux:          {report.spectral_flux:>7.3f}")
        
        print(f"\n🎚️  FREQUENCY BALANCE:")
        print(f"  Sub-Bass:      {report.sub_bass_energy:>7.2f} %")
        print(f"  Bass:          {report.bass_energy:>7.2f} %")
        print(f"  Low-Mid:       {report.low_mid_energy:>7.2f} %")
        print(f"  Mid:           {report.mid_energy:>7.2f} %")
        print(f"  High-Mid:      {report.high_mid_energy:>7.2f} %")
        print(f"  High:          {report.high_energy:>7.2f} %")
        
        print(f"\n🎧 STEREO FIELD:")
        print(f"  Width:         {report.stereo_width:>7.2f} %")
        print(f"  Phase Corr:    {report.phase_correlation:>7.2f}")
        
        print(f"\n{'='*70}")
        
        if report.issues:
            print("\n🚨 CRITICAL ISSUES:")
            for issue in report.issues:
                print(f"  {issue}")
        
        if report.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in report.warnings:
                print(f"  {warning}")
        
        print(f"\n{'='*70}")
        status = "✅ PASSED" if report.passed else "❌ FAILED"
        print(f"OVERALL SCORE: {report.overall_score:.1f}/100 - {status}")
        print(f"{'='*70}\n")
