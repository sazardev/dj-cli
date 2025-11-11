# DJ CLI - Advanced Features Examples

## 🎼 Automatic Music Generation Examples

### Quick Lofi Track
```bash
python src/main.py compose --genre lofi --bars 8 --key C -o samples/lofi_short.wav
```

### Full Electro Track
```bash
python src/main.py auto --genre electro --duration 60 --key D -o samples/electro_full.wav
```

### Ambient Meditation
```bash
python src/main.py compose --genre ambient --bars 32 --key A -o samples/ambient.wav
```

### Funk Groove
```bash
python src/main.py compose --genre funk --bars 16 --key G -o samples/funk.wav
```

### Synthwave Track
```bash
python src/main.py compose --genre synthwave --bars 24 --key Fm -o samples/synthwave.wav
```

## 🎚️ Mixtape Generation

### Chill Mixtape
```bash
python src/main.py mixtape "lofi,relax,ambient" --bars 12 -o samples/chill_mixtape.wav
```

### Energy Mix
```bash
python src/main.py mixtape "electro,funk,synthwave" --bars 16 -o samples/energy_mix.wav
```

### Study Session
```bash
python src/main.py mixtape "lofi,ambient,lofi" --bars 20 --no-transitions -o samples/study_session.wav
```

## 🎵 Advanced Composition

### Custom Structure
```bash
python src/main.py auto --genre funk \
  --structure "intro:2,verse:8,chorus:8,break:4,verse:8,chorus:8,outro:4" \
  -o samples/structured_funk.wav
```

### Long Format Track (5 minutes)
```bash
python src/main.py auto --genre lofi --duration 300 --key C -o samples/lofi_long.wav
```

## 📊 Testing All Genres

Run this to test all genres:

```bash
# Test all genres
for genre in lofi electro funk relax ambient synthwave; do
  echo "Generating $genre..."
  python src/main.py compose --genre $genre --bars 8 -o "samples/${genre}_test.wav"
done
```

## 🎼 Music Theory Showcase

### Different Keys
```bash
# Major keys
python src/main.py compose --genre relax --key C --bars 8 -o samples/key_c.wav
python src/main.py compose --genre relax --key G --bars 8 -o samples/key_g.wav
python src/main.py compose --genre relax --key D --bars 8 -o samples/key_d.wav

# Minor feel
python src/main.py compose --genre lofi --key A --bars 8 -o samples/key_a_minor.wav
python src/main.py compose --genre lofi --key E --bars 8 -o samples/key_e_minor.wav
```

## 🎧 Post-Processing

### Add Effects to Generated Music
```bash
# Generate base track
python src/main.py compose --genre electro --bars 16 -o samples/base.wav

# Add reverb
python src/main.py effect samples/base.wav reverb --mix 0.5 -o samples/base_reverb.wav

# Add delay
python src/main.py effect samples/base.wav delay --mix 0.3 -o samples/base_delay.wav

# Add distortion for grit
python src/main.py effect samples/base.wav distortion --intensity 0.6 -o samples/base_distorted.wav
```

## 🚀 Performance Tips

### Quick Tests (8 bars)
For quick testing, use 8 bars:
```bash
python src/main.py compose --genre lofi --bars 8 -o test.wav
```

### Medium Tracks (16-32 bars)
For complete sections:
```bash
python src/main.py compose --genre electro --bars 32 -o track.wav
```

### Long Tracks (60+ bars)
For full songs, use the `auto` command:
```bash
python src/main.py auto --genre funk --duration 180 -o long_track.wav
```

## 🎪 Creative Workflow

### 1. Generate Multiple Variations
```bash
# Create 3 variations of the same genre
python src/main.py compose --genre lofi --bars 16 -o samples/lofi_v1.wav
python src/main.py compose --genre lofi --bars 16 -o samples/lofi_v2.wav
python src/main.py compose --genre lofi --bars 16 -o samples/lofi_v3.wav
```

### 2. Mix and Layer
```bash
# Generate rhythm section
python src/main.py beat --pattern trap --bpm 140 --bars 16 -o samples/drums.wav

# Auto-compose melody
python src/main.py compose --genre synthwave --bars 16 -o samples/melody.wav

# Mix together
python src/main.py mix samples/drums.wav samples/melody.wav -o samples/layered.wav
```

### 3. Build a Production
```bash
# Intro
python src/main.py compose --genre ambient --bars 8 -o samples/intro.wav

# Main section
python src/main.py compose --genre electro --bars 32 -o samples/main.wav

# Outro
python src/main.py compose --genre ambient --bars 8 -o samples/outro.wav

# Combine (would need crossfading)
python src/main.py mix samples/intro.wav samples/main.wav samples/outro.wav -o samples/production.wav
```
