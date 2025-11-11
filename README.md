# 🎵 DJ CLI - Create Music Using Your Terminal

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful command-line tool for generating, mixing, and manipulating audio. Create beats, apply effects, and produce music directly from your terminal!

## ✨ Features

- 🎹 **Sound Generation**: Create synthesized sounds (kick, snare, hi-hat, bass, synth)
- 🥁 **Beat Making**: Generate drum patterns (trap, house, techno, DnB, and more)
- 🎚️ **Audio Effects**: Apply professional effects (reverb, delay, distortion, chorus, filters)
- 🎛️ **Audio Mixing**: Mix and crossfade multiple audio files
- 📊 **Audio Analysis**: Analyze BPM, key, duration, and more
- 🎪 **Interactive Demo**: Try out all features with built-in demos

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

### Run the CLI

```bash
# Show help
python src/main.py --help

# List available sounds and patterns
python src/main.py sounds

# Run interactive demo
python src/main.py demo
```

### Generate Sounds

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

| Command    | Description                                                                       |
| ---------- | --------------------------------------------------------------------------------- |
| `generate` | Generate synthesized sounds (kick, snare, hihat, bass, synth, noise)              |
| `beat`     | Create drum beats with various patterns                                           |
| `effect`   | Apply audio effects (reverb, delay, distortion, chorus, filter, phaser, bitcrush) |
| `mix`      | Mix multiple audio files together                                                 |
| `analyze`  | Analyze audio properties (BPM, key, duration)                                     |
| `play`     | Play audio files                                                                  |
| `sounds`   | List all available sounds and beat patterns                                       |
| `demo`     | Run an interactive demo                                                           |

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

### Create a Complete Track

```bash
# 1. Generate drum sounds
python src/main.py generate kick -o kick.wav
python src/main.py generate snare -o snare.wav

# 2. Create a beat
python src/main.py beat --bpm 140 --pattern trap --bars 8 -o beat.wav

# 3. Generate a bassline
python src/main.py generate bass --freq 80 -d 8.0 -o bass.wav

# 4. Apply effects
python src/main.py effect beat.wav reverb --mix 0.3 -o beat_reverb.wav
python src/main.py effect bass.wav filter --intensity 0.4 -o bass_filtered.wav

# 5. Mix everything together
python src/main.py mix beat_reverb.wav bass_filtered.wav -o final_track.wav

# 6. Analyze the result
python src/main.py analyze final_track.wav
```

## 📁 Project Structure

```
dj-cli/
├── src/
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── audio_engine.py   # Audio playback and processing
│   ├── sounds.py         # Sound generation
│   ├── beat_maker.py     # Beat creation
│   └── effects.py        # Audio effects
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
