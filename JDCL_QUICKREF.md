# 🎼 JDCL Quick Reference Card

## Compilar
```bash
python src/main.py compile song.jdcli -o output.wav
python src/main.py validate song.jdcli
```

## Estructura Mínima
```json
{
  "metadata": {"title": "Song", "tempo": 120, "key": "C"},
  "patterns": {"p": {"instrument": "kick", "notes": "C2:q"}},
  "sections": {"s": {"bars": 4, "patterns": ["p"]}},
  "structure": ["s"]
}
```

## Notación de Notas
```
"C4:q E4:e G4:h -:q"
 │  │  │  │  │  │  └─ Silencio quarter
 │  │  │  │  │  └──── Sol half
 │  │  │  └────────── Mi eighth  
 │  │  └───────────── Do quarter
 │  └──────────────── Duración
 └─────────────────── Nota + Octava
```

## Duraciones
- `w` = whole (4 beats)
- `h` = half (2 beats)
- `q` = quarter (1 beat)
- `e` = eighth (0.5)
- `s` = sixteenth (0.25)
- `q.` = dotted (1.5)

## Instrumentos
**Melódicos**: piano, synth, pad, bass, sub_bass, ambient  
**Drums**: kick, snare, hihat, clap

## Efectos
```json
"effects": {
  "reverb": {"mix": 0.5, "intensity": 0.6},
  "delay": {"mix": 0.3, "intensity": 0.5},
  "distortion": {"mix": 0.4, "intensity": 0.6},
  "chorus": {"mix": 0.5, "intensity": 0.5},
  "filter": {"mix": 0.6, "intensity": 0.7}
}
```

## Pattern Completo
```json
"piano_melody": {
  "instrument": "piano",
  "notes": "C4:q E4:q G4:h E4:q",
  "volume": 0.8,
  "variation": 0.5,
  "effects": {
    "reverb": {"mix": 0.4, "intensity": 0.6}
  }
}
```

## Sección Completa
```json
"chorus": {
  "bars": 8,
  "patterns": ["kick", "snare", "bass", "melody"],
  "tempo": 128,
  "key": "C",
  "effects": {
    "chorus": {"mix": 0.5, "intensity": 0.6}
  }
}
```

## Volúmenes Típicos
- Kick: 1.0-1.2
- Snare: 0.8-1.0
- Hi-hat: 0.5-0.7
- Bass: 0.9-1.1
- Melodía: 0.7-0.9
- Pads: 0.3-0.5

## Estructura Típica
```json
"structure": [
  "intro",
  "verse", 
  "chorus",
  "verse",
  "break",
  "chorus",
  "outro"
]
```

## Ver Documentación Completa
```bash
cat JDCL_LANGUAGE.md
cat examples/README.md
```
