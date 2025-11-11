# 🎵 DJ CLI - Advanced Music Generator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An **advanced command-line music generator** that automatically composes complete tracks with drums, bass, chords, and melodies. Generate continuous, evolving music in multiple genres directly from your terminal!

## ✨ Features

### 🎼 Automatic Composition
- **Auto-Compose Complete Tracks**: Generate full songs with drums, bass, chords, and melody
- **Multiple Genres**: lofi, electro, funk, relax, ambient, synthwave, and more
- **Music Theory Engine**: Chord progressions, scales, and harmonic structures
- **Continuous Generation**: Create evolving, non-repetitive music of any length
- **Mixtapes**: Generate multi-genre mixes with smooth transitions

### 🎹 Manual Sound Design
- **Sound Generation**: Create synthesized sounds (kick, snare, hi-hat, bass, synth)
- **Beat Making**: Generate drum patterns (trap, house, techno, DnB, and more)
- **Audio Effects**: Apply professional effects (reverb, delay, distortion, chorus, filters)
- **Audio Mixing**: Mix and crossfade multiple audio files
- **Audio Analysis**: Analyze BPM, key, duration, and more

## 📦 Installation

### Prerequisites

Make sure you have the following installed on Arch Linux:

```bash
# Install system dependencies
sudo pacman -S ffmpeg portaudio jack2 python python-pip
```

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/dj-cli.git
cd dj-cli
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate.fish  # For fish shell
# or
source venv/bin/activate       # For bash/zsh
```

3. **Install dependencies**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Quick Start

### 🎼 Automatic Music Generation (NEW!)

```bash
# Auto-compose a lofi track
python src/main.py compose --genre lofi --bars 16 --key C -o lofi_track.wav

# Generate continuous music (60 seconds)
python src/main.py auto --genre electro --duration 60 -o electro.wav

# Create a multi-genre mixtape
python src/main.py mixtape "lofi,electro,funk" --bars 16 -o mixtape.wav

# List available genres
python src/main.py genres
```

### Available Genres

| Genre         | BPM Range | Style                   | Best For                 |
| ------------- | --------- | ----------------------- | ------------------------ |
| **lofi**      | 70-90     | Chill, jazzy, laid-back | Study, relax, background |
| **electro**   | 125-135   | Electronic, energetic   | Dancing, workout         |
| **funk**      | 100-120   | Groovy, syncopated      | Upbeat vibes             |
| **relax**     | 60-80     | Calm, peaceful          | Meditation, sleep        |
| **ambient**   | 60-90     | Atmospheric, spacious   | Background, focus        |
| **synthwave** | 125-135   | Retro, 80s inspired     | Driving, nostalgia       |

### 🎹 Manual Sound Design

```bash
# Generate a kick drum
python src/main.py generate kick -o kick.wav

# Generate a snare with custom duration
python src/main.py generate snare --duration 0.2 -o snare.wav

# Generate a bass tone at 80Hz
python src/main.py generate bass --freq 80 -d 2.0 -o bass.wav

# Generate a synth tone at 440Hz (A4)
python src/main.py generate synth --freq 440 -d 1.5 -o synth.wav
```

### Create Beats

```bash
# Create a basic 4/4 beat at 120 BPM
python src/main.py beat --bpm 120 --bars 4 -o beat.wav

# Create a trap beat at 140 BPM
python src/main.py beat --bpm 140 --pattern trap --bars 8 -o trap.wav

# Create a house beat
python src/main.py beat --bpm 128 --pattern house --bars 4 -o house.wav

# Create a drum and bass beat
python src/main.py beat --bpm 174 --pattern dnb --bars 4 -o dnb.wav
```

### Apply Effects

```bash
# Apply reverb
python src/main.py effect track.wav reverb --mix 0.5 -o track_reverb.wav

# Apply delay
python src/main.py effect track.wav delay --mix 0.3 --intensity 0.7 -o track_delay.wav

# Apply distortion
python src/main.py effect track.wav distortion --intensity 0.8 -o track_distorted.wav

# Apply chorus
python src/main.py effect track.wav chorus --mix 0.4 -o track_chorus.wav

# Apply filter
python src/main.py effect track.wav filter --intensity 0.3 -o track_filtered.wav
```

### Mix Audio Files

```bash
# Mix multiple files together
python src/main.py mix track1.wav track2.wav track3.wav -o final_mix.wav

# Mix with crossfade (500ms)
python src/main.py mix track1.wav track2.wav --crossfade 500 -o crossfaded.wav
```

### Analyze Audio

```bash
# Analyze an audio file (BPM, key, duration, etc.)
python src/main.py analyze track.wav
```

### Play Audio

```bash
# Play an audio file
python src/main.py play track.wav

# Play with custom volume
python src/main.py play track.wav --volume 0.8

# Loop playback (Ctrl+C to stop)
python src/main.py play track.wav --loop
```

## 📚 Available Commands

### 🎼 Auto-Composition Commands

| Command   | Description                                                        |
| --------- | ------------------------------------------------------------------ |
| `compose` | Auto-compose a complete track with drums, bass, chords, and melody |
| `auto`    | Generate continuous, evolving music with song structure            |
| `mixtape` | Create multi-genre mixtapes with transitions                       |
| `genres`  | List all available genres and their characteristics                |

### 🎹 Manual Creation Commands

| Command    | Description                                                          |
| ---------- | -------------------------------------------------------------------- |
| `generate` | Generate synthesized sounds (kick, snare, hihat, bass, synth, noise) |
| `beat`     | Create drum beats with various patterns                              |
| `effect`   | Apply audio effects (reverb, delay, distortion, chorus, filter)      |
| `mix`      | Mix multiple audio files together                                    |
| `analyze`  | Analyze audio properties (BPM, key, duration)                        |
| `play`     | Play audio files                                                     |
| `sounds`   | List all available sounds and beat patterns                          |

## 🎼 Available Sounds

- **kick**: Deep bass drum
- **snare**: Sharp snare hit
- **hihat**: High-hat cymbal
- **bass**: Sub bass tone
- **synth**: Synthesizer tone
- **noise**: White noise

## 🥁 Beat Patterns

- **basic**: Simple 4/4 beat (60-140 BPM)
- **trap**: Modern trap with hi-hat rolls (130-170 BPM)
- **dnb**: Drum and bass (160-180 BPM)
- **house**: Four-on-the-floor (120-130 BPM)
- **techno**: Driving techno (125-145 BPM)

## 🎚️ Available Effects

- **reverb**: Room/hall reverb
- **delay**: Echo effect
- **distortion**: Overdrive/distortion
- **chorus**: Chorus effect
- **filter**: Lowpass filter
- **phaser**: Phaser effect
- **bitcrush**: Lo-fi bit reduction

## 🧪 Examples

### 🎼 Auto-Generate Complete Tracks

```bash
# Generate a 30-second lofi study track
python src/main.py auto --genre lofi --duration 30 -o lofi_study.wav

# Create an electro workout mix (2 minutes)
python src/main.py auto --genre electro --duration 120 -o workout.wav

# Generate ambient meditation music (5 minutes)
python src/main.py auto --genre ambient --duration 300 -o meditation.wav

# Create a multi-genre mixtape
python src/main.py mixtape "lofi,relax,ambient" --bars 16 -o chill_mix.wav
```

### 🎵 Auto-Composition with Custom Structure

```bash
# Compose with specific song structure
python src/main.py auto --genre funk \
  --structure "intro:4,verse:8,chorus:8,verse:8,outro:4" \
  -o funk_song.wav

# Generate in a specific musical key
python src/main.py compose --genre synthwave --key F --bars 32 -o synthwave.wav
```

### 🎹 Manual Track Creation

```bash
# 1. Auto-compose a base track
python src/main.py compose --genre electro --bars 16 -o base.wav

# 2. Apply effects
python src/main.py effect base.wav reverb --mix 0.4 -o base_reverb.wav

# 3. Analyze the result
python src/main.py analyze base_reverb.wav
```

## 📁 Project Structure

```
dj-cli/
├── src/
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── audio_engine.py   # Audio playback and processing
│   ├── music_theory.py   # Music theory (scales, chords, progressions)
│   ├── composer.py       # Automatic composition engine
│   ├── continuous.py     # Continuous music generation
│   ├── sounds.py         # Sound synthesis
│   ├── beat_maker.py     # Beat/rhythm creation
│   └── effects.py        # Audio effects processor
├── samples/              # Generated samples
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## 🛠️ Development

### Running Tests

```bash
# Install pytest
pip install pytest

# Run tests
pytest tests/
```

### Adding New Features

1. Create your feature in the appropriate module (`src/`)
2. Add commands to `src/main.py`
3. Update the README with examples
4. Write tests in `tests/`

## 🐛 Troubleshooting

### Fish Shell Activation Issue

If you get an error with `source venv/bin/activate`, use:
```bash
source venv/bin/activate.fish
```

### Audio Playback Issues

Make sure you have `ffmpeg` and `portaudio` installed:
```bash
sudo pacman -S ffmpeg portaudio
```

### JACK Audio Issues

If you encounter JACK-related errors:
```bash
sudo pacman -S jack2
```

## 📝 License

MIT License - feel free to use this project for any purpose!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Pydub](https://github.com/jiaaro/pydub) - Audio manipulation
- [Librosa](https://librosa.org/) - Audio analysis
- [Pedalboard](https://github.com/spotify/pedalboard) - Audio effects
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

## 📧 Contact

Questions? Issues? Open an issue on GitHub or contact the maintainers.

---

**Made with ❤️ and Python** 🐍🎵
