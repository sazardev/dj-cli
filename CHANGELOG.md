# 🎵 DJ CLI - Changelog

## Version 0.2.0 - Audio Quality Improvements

### 🎧 Major Audio Quality Enhancements

#### Sample Rate Upgrade
- **Increased from 44.1kHz to 48kHz** - Professional studio quality
- Better frequency response and clarity
- Improved high-frequency reproduction

#### New Instruments Added

1. **🎹 Realistic Piano**
   - Additive synthesis with 8 harmonics
   - Proper ADSR envelope (Attack, Decay, Sustain, Release)
   - Velocity-sensitive dynamics
   - Used in: lofi, funk genres

2. **🌊 Ambient Pads**
   - Multi-oscillator detuned synthesis
   - Slow attack/release for atmospheric sound
   - Low-pass filtering for warmth
   - Used in: relax, ambient genres

3. **🔊 Sub-Bass Layer**
   - Pure sine wave below 100Hz
   - Adds depth and power to all tracks
   - Separate from main bassline
   - Automatically added to all compositions

4. **✨ Ambient Textures**
   - Evolving soundscapes
   - Different types: warm, dark, bright, spacey
   - LFO modulation for movement
   - Subtle background layer

#### Improved Drum Sounds

- **Better Kick Drum**
  - Frequency sweep: 200Hz → 50Hz (more punch)
  - Added harmonics for presence
  - Sharper attack transient
  - Click layer for definition

- **Enhanced Snare**
  - More realistic tone + noise blend
  - Better envelope shaping

- **Improved Hi-Hat**
  - Crisper sound with better filtering

#### Composition Improvements

- **Richer Harmonic Content**
  - Piano uses complex harmonic series
  - Pads have multiple detuned oscillators
  - Better chord voicings

- **Better Mixing**
  - Proper level balancing
  - Sub-bass sits below main bass
  - Ambient textures in background
  - Improved dynamic range

- **Genre-Specific Enhancements**
  - Lofi: Piano chords + warm ambient
  - Funk: Piano chords + tight rhythm
  - Relax: Pad chords + spacey ambient
  - Ambient: Pads + evolving textures
  - Synthwave: Synth chords + bright ambient

### 🎚️ Technical Improvements

- **Higher Bit Depth Processing**: 16-bit PCM with proper normalization
- **Better Envelopes**: ADSR implementation for natural sound
- **Advanced Filtering**: Low-pass filters using scipy
- **Harmonic Richness**: Multiple oscillators and harmonics

### 📊 Quality Comparison

| Feature     | Before (v0.1.0) | After (v0.2.0)      |
| ----------- | --------------- | ------------------- |
| Sample Rate | 44.1 kHz        | 48 kHz              |
| Instruments | 6 basic         | 10+ advanced        |
| Harmonics   | Simple          | Rich & complex      |
| Envelopes   | Basic           | ADSR with curves    |
| Bass Depth  | Single layer    | Double (bass + sub) |
| Atmosphere  | None            | Ambient textures    |
| Chords      | Synth only      | Piano/Pads/Synth    |

### 🎵 Sound Character Changes

**Before**: Basic 8-bit style, simple waveforms, flat mix
**After**: Modern production quality, layered sounds, professional depth

### 📝 Usage Notes

All existing commands work the same way, but the output quality is significantly improved:

```bash
# Same commands, better sound
python src/main.py compose --genre lofi --bars 16 -o track.wav
python src/main.py auto --genre synthwave --duration 60 -o mix.wav
```

### 🔄 Backward Compatibility

- All commands remain the same
- File formats unchanged (WAV)
- API interface identical
- Higher quality audio automatically applied

### 🎯 What's Next (v0.3.0 planned)

- [ ] More percussion instruments (claps, shakers, cymbals)
- [ ] Guitar/String synthesis
- [ ] Advanced mixing with EQ
- [ ] Compression and mastering
- [ ] Multiple output formats (MP3, FLAC)
- [ ] Real-time audio preview
- [ ] MIDI export support

---

## Version 0.1.0 - Initial Release

- Basic sound generation (kick, snare, hi-hat, bass, synth)
- Beat patterns (basic, trap, dnb, house, techno)
- Audio effects (reverb, delay, distortion, etc.)
- Automatic composition system
- 6 genres (lofi, electro, funk, relax, ambient, synthwave)
- Music theory engine
- CLI interface with Typer
