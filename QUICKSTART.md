# 🎵 DJ CLI - Advanced Music Generator - Quick Start Guide

## ⚡ Inicio Rápido

### 1. Genera tu primera canción en 10 segundos

```bash
python src/main.py compose --genre lofi --bars 8 -o my_first_track.wav
```

### 2. Escucha géneros disponibles

```bash
python src/main.py genres
```

### 3. Genera música continua de 1 minuto

```bash
python src/main.py auto --genre electro --duration 60 -o electro_mix.wav
```

## 🎼 Ejemplos Prácticos

### Música para Estudiar (Lofi)
```bash
# Track corto (30 segundos)
python src/main.py auto --genre lofi --duration 30 -o study_music.wav

# Track largo (5 minutos) 
python src/main.py auto --genre lofi --duration 300 -o study_long.wav
```

### Música para Hacer Ejercicio (Electro/Funk)
```bash
# Electro energético
python src/main.py compose --genre electro --bars 32 -o workout.wav

# Funk motivador
python src/main.py compose --genre funk --bars 24 -o funk_workout.wav
```

### Música para Relajarse (Ambient/Relax)
```bash
# Ambiente tranquilo
python src/main.py compose --genre ambient --bars 32 -o meditation.wav

# Música relajante
python src/main.py compose --genre relax --bars 24 -o relax.wav
```

### Música Synthwave (Estilo Retro 80s)
```bash
python src/main.py compose --genre synthwave --bars 32 -o synthwave_track.wav
```

## 🎚️ Mixtapes (Varios Géneros)

### Mixtape Chill
```bash
python src/main.py mixtape "lofi,relax,ambient" --bars 16 -o chill_mixtape.wav
```

### Mixtape Energético
```bash
python src/main.py mixtape "electro,funk,synthwave" --bars 16 -o energy_mix.wav
```

### Mixtape Variado (Sin Transiciones)
```bash
python src/main.py mixtape "lofi,electro,ambient,funk" --bars 12 --no-transitions -o variety_mix.wav
```

## 🎹 Personalización Avanzada

### Cambiar la Tonalidad
```bash
# En tonalidad de C
python src/main.py compose --genre lofi --key C --bars 16 -o track_c.wav

# En tonalidad de G
python src/main.py compose --genre lofi --key G --bars 16 -o track_g.wav

# En tonalidad de A
python src/main.py compose --genre funk --key A --bars 16 -o track_a.wav
```

### Estructura Personalizada
```bash
# Definir estructura de la canción manualmente
python src/main.py auto --genre funk \
  --structure "intro:4,verse:8,chorus:8,break:4,chorus:8,outro:4" \
  -o structured_song.wav
```

### Diferentes Duraciones
```bash
# Corta (8 compases ≈ 15-20 segundos)
python src/main.py compose --genre lofi --bars 8 -o short.wav

# Media (16 compases ≈ 30-40 segundos)
python src/main.py compose --genre electro --bars 16 -o medium.wav

# Larga (32 compases ≈ 1-1.5 minutos)
python src/main.py compose --genre ambient --bars 32 -o long.wav

# Muy larga (usando duración en segundos)
python src/main.py auto --genre lofi --duration 300 -o very_long.wav
```

## 🎚️ Post-Procesamiento

### Agregar Efectos a Música Generada
```bash
# 1. Generar track base
python src/main.py compose --genre electro --bars 16 -o base.wav

# 2. Agregar reverb
python src/main.py effect base.wav reverb --mix 0.5 -o base_reverb.wav

# 3. Agregar delay
python src/main.py effect base.wav delay --mix 0.3 -o base_delay.wav

# 4. Agregar distorsión
python src/main.py effect base.wav distortion --intensity 0.6 -o base_distorted.wav
```

## 📊 Análisis de Audio

```bash
# Analizar una pista generada
python src/main.py analyze my_track.wav

# Resultado muestra: BPM, tonalidad, duración, energía, etc.
```

## 🎧 Reproducción

```bash
# Reproducir audio
python src/main.py play my_track.wav

# Reproducir con volumen personalizado
python src/main.py play my_track.wav --volume 0.8

# Reproducir en loop
python src/main.py play my_track.wav --loop
```

## 🔥 Trucos y Tips

### Generar Múltiples Variaciones
```bash
# Bash loop para generar 5 variaciones
for i in {1..5}; do
  python src/main.py compose --genre lofi --bars 16 -o "lofi_${i}.wav"
done
```

### Generar una Playlist Completa
```bash
# Generar varios tracks de diferentes géneros
python src/main.py compose --genre lofi --bars 32 -o "01_lofi.wav"
python src/main.py compose --genre electro --bars 32 -o "02_electro.wav"
python src/main.py compose --genre funk --bars 32 -o "03_funk.wav"
python src/main.py compose --genre ambient --bars 32 -o "04_ambient.wav"
python src/main.py compose --genre synthwave --bars 32 -o "05_synthwave.wav"
```

### Workflow Completo
```bash
# 1. Ver géneros disponibles
python src/main.py genres

# 2. Generar base musical
python src/main.py compose --genre lofi --bars 24 --key C -o base.wav

# 3. Analizar el resultado
python src/main.py analyze base.wav

# 4. Agregar efectos si es necesario
python src/main.py effect base.wav reverb --mix 0.4 -o final.wav

# 5. Reproducir
python src/main.py play final.wav
```

## ⏱️ Tiempos de Generación

- **8 bars** (corto): ~5-10 segundos
- **16 bars** (medio): ~10-20 segundos
- **32 bars** (largo): ~20-40 segundos
- **Mixtape**: depende del número de géneros y compases

## 🎯 Casos de Uso

### Para Estudiar
```bash
python src/main.py auto --genre lofi --duration 1800 -o study_session_30min.wav
```

### Para Trabajar
```bash
python src/main.py mixtape "ambient,lofi,relax" --bars 20 -o work_music.wav
```

### Para Hacer Ejercicio
```bash
python src/main.py mixtape "electro,funk,electro" --bars 24 -o workout_mix.wav
```

### Para Relajarse
```bash
python src/main.py auto --genre ambient --duration 600 -o relaxation_10min.wav
```

### Para Crear Contenido
```bash
# Música de fondo para videos
python src/main.py compose --genre relax --bars 40 -o background_music.wav
```

## 📝 Notas Importantes

- Todos los archivos se guardan como `.wav` por defecto
- Los compases (bars) determinan la longitud: 1 bar ≈ 2-4 segundos dependiendo del BPM
- El BPM se selecciona automáticamente según el género
- La tonalidad por defecto es C, pero puedes cambiarla
- Los mixtapes usan transiciones (crossfade) por defecto

## 🚀 Siguiente Nivel

Una vez que domines lo básico, prueba:

1. **Experimentar con diferentes tonalidades**: C, D, E, F, G, A
2. **Mezclar géneros**: Crear mixtapes únicos
3. **Estructuras personalizadas**: Definir intro, verse, chorus, etc.
4. **Post-procesamiento**: Agregar efectos y mezclar tracks
5. **Análisis**: Entender el BPM y tonalidad de tus tracks

¡Diviértete creando música! 🎵
