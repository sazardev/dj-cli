# 🎼 JDCL Examples

This directory contains example compositions in JDCL format.

## 📁 Available Examples

### 🎓 `tutorial_simple.jdcli`
**Difficulty**: Beginner  
**Duration**: ~11 seconds (4 bars)  
**Description**: Minimal example to learn JDCL basics
- Simple kick pattern
- Piano melody (4 notes)
- Basic reverb effect

**Compile:**
```bash
python src/main.py compile examples/tutorial_simple.jdcli -o output.wav
```

---

### 🌅 `lofi_sunset.jdcli`
**Difficulty**: Intermediate  
**Duration**: ~126 seconds (44 bars)  
**Description**: Complete lofi composition with multiple sections
- 9 patterns (kick, snare, 2x hihat, bass, 2x piano, pad, sub-bass)
- 5 sections (intro, verse, chorus, break, outro)
- Multiple effects (reverb, delay, chorus, filter)
- Tempo change in break section (85 → 70 BPM)

**Features:**
- Complete song structure
- Pattern reuse across sections
- Per-pattern and per-section effects
- Global effects
- Professional lofi sound

**Compile:**
```bash
python src/main.py compile examples/lofi_sunset.jdcli -o lofi.wav
```

---

### 🌃 `neon_nights.jdcli`
**Difficulty**: Advanced  
**Duration**: ~120 seconds (64 bars)  
**Description**: Complex electro track with buildup and drop
- 8 patterns (kick, snare, hihat, bass, 2x synth, pad, clap)
- 5 sections (intro, buildup, drop, breakdown, outro)
- Aggressive effects (distortion, heavy filtering)
- Tempo modulation (128 → 64 → 128 BPM)

**Features:**
- EDM-style structure (buildup → drop)
- 16th note hi-hats
- Distorted bass with filter sweep
- Synth stabs and lead melodies
- Dramatic tempo change in breakdown

**Compile:**
```bash
python src/main.py compile examples/neon_nights.jdcli -o electro.wav
```

---

## 🎯 Learning Path

### 1. Start with `tutorial_simple.jdcli`
- Understand basic structure
- Learn pattern notation
- See how sections work

### 2. Modify `tutorial_simple.jdcli`
- Change notes: `"C4:q E4:q G4:q C5:q"`
- Add more patterns
- Adjust tempo

### 3. Study `lofi_sunset.jdcli`
- See complete song structure
- Learn effect usage
- Understand pattern reuse

### 4. Explore `neon_nights.jdcli`
- Complex patterns
- Advanced effects
- Tempo automation

### 5. Create your own!
See `JDCL_LANGUAGE.md` for complete reference

---

## 🎵 Quick Compilation

Compile all examples at once:

```bash
# Fish shell
for file in examples/*.jdcli
    set name (basename $file .jdcli)
    python src/main.py compile $file -o "samples/$name.wav" 2>/dev/null
end

# Bash
for file in examples/*.jdcli; do
    name=$(basename "$file" .jdcli)
    python src/main.py compile "$file" -o "samples/$name.wav" 2>/dev/null
done
```

---

## 📊 Comparison Table

| Example         | Bars | Duration | Patterns | Sections | Effects | Difficulty |
| --------------- | ---- | -------- | -------- | -------- | ------- | ---------- |
| tutorial_simple | 4    | ~11s     | 2        | 1        | 1       | ⭐          |
| lofi_sunset     | 44   | ~126s    | 9        | 5        | 7       | ⭐⭐⭐        |
| neon_nights     | 64   | ~120s    | 8        | 5        | 6       | ⭐⭐⭐⭐       |

---

## 🎓 Tips for Creating Your Own

### 1. Start Simple
```json
{
  "metadata": {"title": "Test", "tempo": 120, "key": "C"},
  "patterns": {
    "kick": {"instrument": "kick", "notes": "C2:q C2:q C2:q C2:q"}
  },
  "sections": {
    "main": {"bars": 4, "patterns": ["kick"]}
  },
  "structure": ["main"]
}
```

### 2. Add Melody
```json
"melody": {
  "instrument": "piano",
  "notes": "C4:q E4:q G4:q E4:q"
}
```
Don't forget to add it to the section!

### 3. Layer Sounds
```json
"sections": {
  "main": {
    "bars": 4,
    "patterns": ["kick", "melody", "bass"]
  }
}
```

### 4. Add Effects
```json
"effects": {
  "reverb": {"mix": 0.4, "intensity": 0.6}
}
```

### 5. Create Structure
```json
"structure": ["intro", "verse", "chorus", "verse", "outro"]
```

---

## 🔍 Validation

Validate before compiling to catch errors:

```bash
python src/main.py validate examples/your_song.jdcli
```

This checks:
- ✓ All patterns exist
- ✓ All sections exist
- ✓ Structure references valid sections
- ✓ JSON syntax is correct

---

## 🎼 Need Help?

- **Language Reference**: See `JDCL_LANGUAGE.md`
- **Sound Quality**: See `PROFESSIONAL_SOUNDS.md`
- **General Usage**: See main `README.md`

---

Happy composing! 🎵✨
