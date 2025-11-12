# 🎼 JDCL - JSON DJ Composition Language

## ¿Qué es JDCL?

**JDCL** (JSON DJ Composition Language) es un lenguaje de composición musical basado en JSON que te permite **programar música** usando texto. Es como escribir código, pero el resultado es una canción completa.

### ¿Por qué JDCL?

✅ **Control Total**: Define cada nota, cada patrón, cada sección  
✅ **Reutilizable**: Crea patrones y úsalos múltiples veces  
✅ **Versionable**: Guarda tus composiciones en Git  
✅ **Compartible**: Comparte archivos .jdcli con otros músicos  
✅ **Profesional**: Efectos, mezcla, automatización  
✅ **Legible**: Lenguaje casi humano, fácil de entender

---

## 🚀 Quick Start

### 1. Crear tu primera composición

Crea un archivo `my_song.jdcli`:

```json
{
  "metadata": {
    "title": "Mi Primera Canción",
    "artist": "Tu Nombre",
    "genre": "lofi",
    "tempo": 90,
    "key": "C",
    "time_signature": "4/4"
  },

  "patterns": {
    "kick": {
      "instrument": "kick",
      "notes": "C2:q C2:q C2:q C2:q",
      "volume": 1.0
    },
    
    "melody": {
      "instrument": "piano",
      "notes": "C4:q E4:q G4:q E4:q",
      "volume": 0.8
    }
  },

  "sections": {
    "main": {
      "bars": 4,
      "patterns": ["kick", "melody"]
    }
  },

  "structure": ["main"]
}
```

### 2. Compilar a audio

```bash
python src/main.py compile my_song.jdcli -o my_song.wav
```

### 3. ¡Escuchar!

Tu música está lista en `my_song.wav` 🎵

---

## 📖 Estructura de un archivo .jdcli

### Secciones principales

```json
{
  "metadata": { ... },       // Información de la canción
  "patterns": { ... },       // Patrones musicales (loops)
  "sections": { ... },       // Secciones de la canción
  "structure": [ ... ],      // Orden de las secciones
  "global_effects": { ... }  // Efectos globales
}
```

---

## 🎹 1. Metadata (Información de la canción)

```json
"metadata": {
  "title": "Nombre de la canción",
  "artist": "Tu nombre o alias",
  "genre": "lofi",           // lofi, electro, funk, etc.
  "tempo": 120,              // BPM (beats por minuto)
  "key": "C",                // Tonalidad: C, Dm, F#, etc.
  "time_signature": "4/4"    // Compás: 4/4, 3/4, 6/8, etc.
}
```

### Géneros disponibles
- `lofi` - Chill, relajado
- `electro` - Electrónico, energético
- `funk` - Groovy, bailable
- `relax` - Ambient, tranquilo
- `ambient` - Atmosférico
- `synthwave` - Retro, 80s

---

## 🎵 2. Patterns (Patrones musicales)

Un pattern es un **loop musical** - una secuencia de notas que se repite.

### Estructura básica

```json
"patterns": {
  "nombre_del_pattern": {
    "instrument": "piano",    // Instrumento
    "notes": "...",           // Notas (ver notación abajo)
    "volume": 1.0,            // Volumen (0.0 a 2.0)
    "variation": 0.5,         // Variación humanizada (0-1)
    "effects": { ... }        // Efectos del pattern
  }
}
```

### Instrumentos disponibles

#### Melódicos
- `piano` - Piano realista (soundfont o modelado físico)
- `synth` - Sintetizador (sawtooth, square, sine)
- `pad` - Pad atmosférico (synth detuned)
- `bass` - Bajo sintético
- `sub_bass` - Sub-bass (sine puro <100Hz)
- `ambient` - Textura ambient

#### Percusión
- `kick` - Bombo (5 capas físicas)
- `snare` - Caja/Tarola (4 capas)
- `hihat` - Hi-hat (cerrado/abierto)
- `clap` - Palmada/Clap

---

## 📝 3. Notación de Notas

### Formato compacto (string)

```
"nota:duración:velocidad"
```

**Ejemplos:**
```json
"notes": "C4:q E4:q G4:h -:q"
```

- `C4:q` = Nota C en octava 4, duración quarter (negra)
- `E4:e` = Nota E en octava 4, duración eighth (corchea)
- `G4:h` = Nota G en octava 4, duración half (blanca)
- `-:q` = Silencio de quarter note

### Notas disponibles

```
C, C#, D, D#, E, F, F#, G, G#, A, A#, B
```

**Con octavas:** `C2`, `A4`, `G#5`, etc.
- `C1` - Muy grave (sub-bass)
- `C2` - Grave (bass)
- `C3` - Medio-grave
- `C4` - Do central
- `C5` - Agudo
- `C6+` - Muy agudo

### Duraciones

| Código | Nombre         | Duración   | Uso            |
| ------ | -------------- | ---------- | -------------- |
| `w`    | whole          | 4 beats    | Nota muy larga |
| `h`    | half           | 2 beats    | Nota larga     |
| `q`    | quarter        | 1 beat     | Nota normal    |
| `e`    | eighth         | 0.5 beats  | Nota corta     |
| `s`    | sixteenth      | 0.25 beats | Nota muy corta |
| `q.`   | dotted quarter | 1.5 beats  | Puntillo       |
| `e.`   | dotted eighth  | 0.75 beats | Puntillo       |

### Velocidad (opcional)

```json
"C4:q:0.8"  // Velocidad 0.8 (80%)
```

Rango: `0.0` (silencio) a `1.0` (máximo)

### Silencios

```json
"-:q"      // Silencio de quarter
"-:h"      // Silencio de half
"rest:e"   // También funciona
```

---

## 🎼 Notación extendida (array de objetos)

Para mayor control:

```json
"notes": [
  {
    "pitch": "C4",
    "duration": "quarter",
    "velocity": 0.8
  },
  {
    "pitch": "E4",
    "duration": 0.5,
    "velocity": 0.9
  },
  {
    "pitch": "rest",
    "duration": "eighth"
  }
]
```

---

## 🎛️ 4. Effects (Efectos)

### Efectos disponibles

```json
"effects": {
  "reverb": {
    "mix": 0.5,        // 0-1: wet/dry mix
    "intensity": 0.6   // 0-1: intensidad
  },
  
  "delay": {
    "mix": 0.3,
    "intensity": 0.5
  },
  
  "distortion": {
    "mix": 0.4,
    "intensity": 0.6
  },
  
  "chorus": {
    "mix": 0.5,
    "intensity": 0.5
  },
  
  "filter": {
    "mix": 0.6,
    "intensity": 0.7
  }
}
```

### Aplicación de efectos

**1. Por pattern:**
```json
"piano_melody": {
  "instrument": "piano",
  "notes": "...",
  "effects": {
    "reverb": {"mix": 0.4, "intensity": 0.6}
  }
}
```

**2. Por sección:**
```json
"sections": {
  "chorus": {
    "bars": 8,
    "patterns": ["..."],
    "effects": {
      "chorus": {"mix": 0.5, "intensity": 0.6}
    }
  }
}
```

**3. Global:**
```json
"global_effects": {
  "reverb": {"mix": 0.2, "intensity": 0.3}
}
```

---

## 📂 5. Sections (Secciones)

Una sección agrupa múltiples patterns que suenan juntos.

```json
"sections": {
  "intro": {
    "bars": 4,                    // Duración en compases
    "patterns": [                 // Patterns que suenan
      "kick",
      "melody",
      "pad"
    ],
    "tempo": 90,                  // Override tempo (opcional)
    "key": "C",                   // Override key (opcional)
    "effects": { ... }            // Efectos de sección
  }
}
```

### Ejemplos de secciones típicas

```json
"sections": {
  "intro": {
    "bars": 4,
    "patterns": ["ambient", "melody"]
  },
  
  "verse": {
    "bars": 8,
    "patterns": ["kick", "snare", "hihat", "bass", "chords"]
  },
  
  "chorus": {
    "bars": 8,
    "patterns": ["kick", "snare", "hihat", "bass", "melody", "pad"]
  },
  
  "break": {
    "bars": 4,
    "patterns": ["hihat", "melody"],
    "tempo": 70
  },
  
  "outro": {
    "bars": 4,
    "patterns": ["ambient", "pad"]
  }
}
```

---

## 🏗️ 6. Structure (Estructura de la canción)

Define el orden de las secciones:

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

Las secciones se pueden repetir cuantas veces quieras.

---

## 🎯 Ejemplos Completos

### Ejemplo 1: Lofi Simple

```json
{
  "metadata": {
    "title": "Chill Vibes",
    "artist": "DJ CLI",
    "genre": "lofi",
    "tempo": 85,
    "key": "C",
    "time_signature": "4/4"
  },

  "patterns": {
    "kick": {
      "instrument": "kick",
      "notes": "C2:q -:q C2:q -:q",
      "volume": 1.0
    },
    
    "snare": {
      "instrument": "snare",
      "notes": "-:q C2:q -:q C2:q",
      "volume": 0.8
    },
    
    "hihat": {
      "instrument": "hihat",
      "notes": "C2:e C2:e C2:e C2:e C2:e C2:e C2:e C2:e",
      "volume": 0.6
    },
    
    "piano": {
      "instrument": "piano",
      "notes": "C4:h E4:h G4:h C5:h",
      "volume": 0.7,
      "effects": {
        "reverb": {"mix": 0.4, "intensity": 0.6}
      }
    }
  },

  "sections": {
    "main": {
      "bars": 8,
      "patterns": ["kick", "snare", "hihat", "piano"]
    }
  },

  "structure": ["main", "main"]
}
```

### Ejemplo 2: Electro con Buildup

```json
{
  "metadata": {
    "title": "Energy Drop",
    "tempo": 128,
    "key": "Am"
  },

  "patterns": {
    "kick_4x4": {
      "instrument": "kick",
      "notes": "C2:q C2:q C2:q C2:q",
      "volume": 1.2
    },
    
    "bass": {
      "instrument": "bass",
      "notes": "A1:e A1:e C2:e C2:e G1:e G1:e F1:e F1:e",
      "volume": 1.1,
      "effects": {
        "distortion": {"mix": 0.4, "intensity": 0.5}
      }
    },
    
    "lead": {
      "instrument": "synth",
      "notes": "A4:e C5:e E5:e A5:q",
      "effects": {
        "delay": {"mix": 0.5, "intensity": 0.6}
      }
    }
  },

  "sections": {
    "buildup": {
      "bars": 8,
      "patterns": ["kick_4x4"],
      "effects": {
        "filter": {"mix": 0.8, "intensity": 0.9}
      }
    },
    
    "drop": {
      "bars": 16,
      "patterns": ["kick_4x4", "bass", "lead"]
    }
  },

  "structure": ["buildup", "drop"]
}
```

---

## 🎓 Tips y Mejores Prácticas

### 1. Organización

```json
// ✅ Buen nombre
"kick_main": { ... }
"piano_verse_chords": { ... }

// ❌ Mal nombre
"pattern1": { ... }
"asdf": { ... }
```

### 2. Volúmenes

- **Kick**: `1.0 - 1.2`
- **Snare**: `0.8 - 1.0`
- **Hi-hat**: `0.5 - 0.7`
- **Bass**: `0.9 - 1.1`
- **Melodía**: `0.7 - 0.9`
- **Pads/Ambient**: `0.3 - 0.5`

### 3. Efectos

**Reverb para:**
- Piano
- Pads
- Melodías
- Intros/Outros

**Delay para:**
- Melodías principales
- Efectos especiales
- Builds

**Distortion para:**
- Bass
- Synth leads
- Drums (snare)

### 4. Estructura típica

```
intro → verse → chorus → verse → break → chorus → outro
```

Duración típica en bars:
- Intro: 2-4
- Verse: 8-16
- Chorus: 8-16
- Break: 4-8
- Outro: 2-4

---

## 🔧 Comandos

### Compilar

```bash
python src/main.py compile song.jdcli -o output.wav
```

### Validar (sin compilar)

```bash
python src/main.py validate song.jdcli
```

### Opciones

```bash
# Compilación silenciosa
python src/main.py compile song.jdcli -o out.wav --quiet

# Con detalles
python src/main.py compile song.jdcli -o out.wav --verbose
```

---

## 📚 Recursos

### Archivos de ejemplo

- `examples/lofi_sunset.jdcli` - Composición lofi completa
- `examples/neon_nights.jdcli` - Track electro avanzado

### Teoría musical

- [Music Theory](https://www.musictheory.net/)
- [Note Frequencies](https://pages.mtu.edu/~suits/notefreqs.html)
- [Chord Progressions](https://www.hooktheory.com/)

---

## 🎼 Cheat Sheet

### Notas rápidas
```
C4:q  = Do central, negra
E4:e  = Mi, corchea  
G4:h  = Sol, blanca
-:q   = Silencio de negra
```

### Patterns mínimos
```json
"kick": {
  "instrument": "kick",
  "notes": "C2:q C2:q C2:q C2:q"
}
```

### Sección mínima
```json
"main": {
  "bars": 4,
  "patterns": ["kick"]
}
```

### Composición mínima
```json
{
  "metadata": {"title": "Song", "tempo": 120, "key": "C"},
  "patterns": {"k": {"instrument": "kick", "notes": "C2:q"}},
  "sections": {"m": {"bars": 4, "patterns": ["k"]}},
  "structure": ["m"]
}
```

---

¡Ahora estás listo para crear música programando! 🚀🎵
