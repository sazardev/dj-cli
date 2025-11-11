# Sample Audio Files

This directory contains sample audio files generated for testing and demos.

## Generated Samples

When you run `dj-cli demo`, the following files will be created:
- `demo_kick.wav` - Kick drum sample
- `demo_beat.wav` - Complete beat pattern

## Creating Your Own Samples

Use the following commands to generate your own samples:

```bash
# Generate individual sounds
dj-cli generate kick -o samples/kick.wav
dj-cli generate snare -o samples/snare.wav
dj-cli generate hihat -o samples/hihat.wav
dj-cli generate bass --freq 80 -o samples/bass.wav

# Create beats
dj-cli beat --bpm 140 --pattern trap -o samples/trap_beat.wav
dj-cli beat --bpm 128 --pattern house -o samples/house_beat.wav
```

## Sample Usage

Test effects with your samples:
```bash
dj-cli effect samples/kick.wav reverb --mix 0.5 -o samples/kick_reverb.wav
dj-cli effect samples/beat.wav distortion --intensity 0.7 -o samples/beat_distorted.wav
```
