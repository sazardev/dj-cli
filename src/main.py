#!/usr/bin/env python3
"""
DJ CLI - Create music using your terminal
Main entry point for the command-line interface
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
import sys
import os

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = typer.Typer(
    name="dj-cli",
    help="🎵 DJ CLI - Create music using your terminal",
    add_completion=True,
)

console = Console()


@app.command()
def play(
    file: str = typer.Argument(..., help="Audio file to play"),
    volume: float = typer.Option(1.0, "--volume", "-v", help="Volume level (0.0 to 2.0)"),
    loop: bool = typer.Option(False, "--loop", "-l", help="Loop playback"),
):
    """
    🎧 Play an audio file
    
    Example: dj-cli play sample.wav --volume 0.8
    """
    from src.audio_engine import AudioEngine
    
    console.print(f"[cyan]▶ Playing:[/cyan] {file}")
    console.print(f"[dim]Volume: {volume} | Loop: {loop}[/dim]")
    
    try:
        engine = AudioEngine()
        engine.play_file(file, volume=volume, loop=loop)
        console.print("[green]✓ Playback complete[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def generate(
    type: str = typer.Argument(..., help="Sound type: kick, snare, hihat, bass, synth"),
    duration: float = typer.Option(1.0, "--duration", "-d", help="Duration in seconds"),
    output: str = typer.Option("output.wav", "--output", "-o", help="Output file"),
    frequency: Optional[int] = typer.Option(None, "--freq", "-f", help="Frequency in Hz"),
):
    """
    🎹 Generate synthesized sounds
    
    Available types: kick, snare, hihat, bass, synth, noise
    
    Example: dj-cli generate kick --duration 0.5 -o kick.wav
    """
    from src.sounds import SoundGenerator
    
    console.print(f"[cyan]🎵 Generating {type} sound...[/cyan]")
    
    try:
        generator = SoundGenerator()
        audio = generator.generate(type, duration=duration, frequency=frequency)
        audio.export(output, format="wav")
        console.print(f"[green]✓ Saved to {output}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def beat(
    bpm: int = typer.Option(120, "--bpm", "-b", help="Beats per minute"),
    bars: int = typer.Option(4, "--bars", help="Number of bars"),
    pattern: str = typer.Option("basic", "--pattern", "-p", help="Beat pattern: basic, trap, dnb, house"),
    output: str = typer.Option("beat.wav", "--output", "-o", help="Output file"),
):
    """
    🥁 Create drum beats
    
    Patterns: basic, trap, dnb, house, techno
    
    Example: dj-cli beat --bpm 140 --pattern trap -o mybeat.wav
    """
    from src.beat_maker import BeatMaker
    
    console.print(f"[cyan]🥁 Creating {pattern} beat at {bpm} BPM...[/cyan]")
    
    try:
        maker = BeatMaker()
        beat = maker.create_beat(bpm=bpm, bars=bars, pattern=pattern)
        beat.export(output, format="wav")
        console.print(f"[green]✓ Beat saved to {output}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def effect(
    input_file: str = typer.Argument(..., help="Input audio file"),
    effect_type: str = typer.Argument(..., help="Effect: reverb, delay, distortion, chorus, filter"),
    output: str = typer.Option("output.wav", "--output", "-o", help="Output file"),
    mix: float = typer.Option(0.5, "--mix", "-m", help="Wet/dry mix (0.0 to 1.0)"),
    intensity: float = typer.Option(0.5, "--intensity", "-i", help="Effect intensity"),
):
    """
    🎚️ Apply audio effects
    
    Available effects: reverb, delay, distortion, chorus, filter, bitcrush
    
    Example: dj-cli effect track.wav reverb --mix 0.3 -o wet.wav
    """
    from src.effects import EffectsProcessor
    
    console.print(f"[cyan]🎚️ Applying {effect_type} effect...[/cyan]")
    
    try:
        processor = EffectsProcessor()
        audio = processor.apply_effect(input_file, effect_type, mix=mix, intensity=intensity)
        audio.export(output, format="wav")
        console.print(f"[green]✓ Processed audio saved to {output}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def mix(
    files: list[str] = typer.Argument(..., help="Audio files to mix"),
    output: str = typer.Option("mix.wav", "--output", "-o", help="Output file"),
    crossfade: int = typer.Option(0, "--crossfade", "-c", help="Crossfade duration in ms"),
):
    """
    🎛️ Mix multiple audio files
    
    Example: dj-cli mix track1.wav track2.wav --crossfade 500 -o final.wav
    """
    from src.audio_engine import AudioEngine
    
    console.print(f"[cyan]🎛️ Mixing {len(files)} files...[/cyan]")
    
    try:
        engine = AudioEngine()
        mixed = engine.mix_files(files, crossfade=crossfade)
        mixed.export(output, format="wav")
        console.print(f"[green]✓ Mixed audio saved to {output}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def analyze(
    file: str = typer.Argument(..., help="Audio file to analyze"),
):
    """
    📊 Analyze audio file (BPM, key, duration)
    
    Example: dj-cli analyze track.wav
    """
    from src.audio_engine import AudioEngine
    
    console.print(f"[cyan]📊 Analyzing {file}...[/cyan]\n")
    
    try:
        engine = AudioEngine()
        info = engine.analyze_file(file)
        
        table = Table(title="Audio Analysis")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in info.items():
            table.add_row(key, str(value))
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def sounds():
    """
    🎼 List available sound types and patterns
    """
    table = Table(title="🎵 Available Sounds")
    table.add_column("Type", style="cyan", width=15)
    table.add_column("Description", style="white")
    table.add_column("Example", style="dim")
    
    sounds_list = [
        ("kick", "Deep bass drum", "dj-cli generate kick -o kick.wav"),
        ("snare", "Sharp snare hit", "dj-cli generate snare -o snare.wav"),
        ("hihat", "High-hat cymbal", "dj-cli generate hihat -d 0.1"),
        ("bass", "Sub bass tone", "dj-cli generate bass --freq 80"),
        ("synth", "Synthesizer tone", "dj-cli generate synth --freq 440"),
        ("noise", "White noise", "dj-cli generate noise -d 2.0"),
    ]
    
    for sound_type, desc, example in sounds_list:
        table.add_row(sound_type, desc, example)
    
    console.print(table)
    console.print()
    
    patterns_table = Table(title="🥁 Beat Patterns")
    patterns_table.add_column("Pattern", style="cyan", width=15)
    patterns_table.add_column("Description", style="white")
    patterns_table.add_column("BPM Range", style="dim")
    
    patterns = [
        ("basic", "Simple 4/4 beat", "60-140"),
        ("trap", "Modern trap hi-hats", "130-170"),
        ("dnb", "Drum and bass", "160-180"),
        ("house", "Four-on-the-floor", "120-130"),
        ("techno", "Driving techno", "125-145"),
    ]
    
    for pattern, desc, bpm in patterns:
        patterns_table.add_row(pattern, desc, bpm)
    
    console.print(patterns_table)


@app.command()
def demo():
    """
    🎪 Run a demo showcase of DJ CLI capabilities
    """
    console.print(Panel.fit(
        "[bold cyan]🎵 DJ CLI Demo[/bold cyan]\n\n"
        "This demo will generate various sounds and beats to showcase the capabilities.\n\n"
        "[yellow]Commands to try:[/yellow]\n"
        "1. Generate a kick drum\n"
        "2. Create a trap beat\n"
        "3. Apply reverb effect\n"
        "4. Mix multiple tracks",
        border_style="cyan"
    ))
    
    if typer.confirm("Run demo?", default=True):
        from src.sounds import SoundGenerator
        from src.beat_maker import BeatMaker
        
        try:
            console.print("\n[cyan]Step 1: Generating kick drum...[/cyan]")
            generator = SoundGenerator()
            kick = generator.generate("kick", duration=0.5)
            kick.export("samples/demo_kick.wav", format="wav")
            console.print("[green]✓ Kick saved to samples/demo_kick.wav[/green]")
            
            console.print("\n[cyan]Step 2: Creating beat...[/cyan]")
            maker = BeatMaker()
            beat = maker.create_beat(bpm=140, bars=2, pattern="trap")
            beat.export("samples/demo_beat.wav", format="wav")
            console.print("[green]✓ Beat saved to samples/demo_beat.wav[/green]")
            
            console.print("\n[bold green]✓ Demo complete! Check the samples/ folder[/bold green]")
        except Exception as e:
            console.print(f"[red]✗ Demo error: {e}[/red]")
            raise typer.Exit(1)


@app.command()
def compose(
    genre: str = typer.Option("lofi", "--genre", "-g", help="Music genre: lofi, electro, funk, relax, ambient, synthwave"),
    bars: int = typer.Option(16, "--bars", "-b", help="Track length in bars"),
    key: str = typer.Option("C", "--key", "-k", help="Musical key (C, D, E, F, G, A, etc.)"),
    output: str = typer.Option("composition.wav", "--output", "-o", help="Output file"),
):
    """
    🎼 Auto-compose a complete music track
    
    Automatically generates drums, bass, chords, and melody for a complete track.
    
    Available genres: lofi, electro, funk, relax, ambient, synthwave
    
    Example: dj-cli compose --genre lofi --bars 16 --key C -o lofi_track.wav
    """
    from src.composer import AutoComposer
    
    console.print(f"[cyan]🎼 Composing {genre} track in key of {key}...[/cyan]")
    console.print(f"[dim]Length: {bars} bars | Style: {genre}[/dim]\n")
    
    try:
        composer = AutoComposer()
        
        with console.status("[bold cyan]Composing track..."):
            track = composer.compose_track(genre, bars, key)
        
        console.print("[cyan]💾 Exporting track...[/cyan]")
        track.export(output, format="wav")
        
        console.print(f"[bold green]✓ Track composed and saved to {output}[/bold green]")
        console.print(f"[dim]Duration: {len(track) / 1000:.1f} seconds[/dim]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def auto(
    genre: str = typer.Option("lofi", "--genre", "-g", help="Music genre"),
    duration: int = typer.Option(60, "--duration", "-d", help="Duration in seconds (approximate)"),
    key: Optional[str] = typer.Option(None, "--key", "-k", help="Musical key (auto if not specified)"),
    structure: Optional[str] = typer.Option(None, "--structure", "-s", help="Song structure (e.g., intro:4,verse:8,chorus:8)"),
    output: str = typer.Option("auto_track.wav", "--output", "-o", help="Output file"),
):
    """
    🎵 Generate continuous, evolving music automatically
    
    Creates a full track with intro, verses, chorus, breaks, and outro.
    
    Example: dj-cli auto --genre electro --duration 120 -o electro_track.wav
    """
    from src.continuous import ContinuousGenerator
    from src.music_theory import MusicTheory
    
    # Calculate bars from duration (approximate)
    theory = MusicTheory()
    bpm = theory.get_bpm_for_genre(genre)
    bars = int((duration * bpm) / (60 * 4))  # 4 beats per bar
    
    console.print(f"[bold cyan]🎵 Auto-generating {genre} track[/bold cyan]")
    console.print(f"[dim]Duration: ~{duration}s | BPM: ~{bpm} | Bars: {bars}[/dim]\n")
    
    try:
        generator = ContinuousGenerator()
        
        with console.status("[bold cyan]Generating continuous music..."):
            track = generator.generate_continuous(genre, bars, key, structure)
        
        console.print("[cyan]💾 Exporting track...[/cyan]")
        track.export(output, format="wav")
        
        console.print(f"[bold green]✓ Auto-generated track saved to {output}[/bold green]")
        console.print(f"[dim]Actual duration: {len(track) / 1000:.1f} seconds[/dim]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def mixtape(
    genres: str = typer.Argument(..., help="Comma-separated genres (e.g., lofi,electro,funk)"),
    bars_each: int = typer.Option(16, "--bars", "-b", help="Bars per genre"),
    transitions: bool = typer.Option(True, "--transitions/--no-transitions", help="Add crossfade transitions"),
    output: str = typer.Option("mixtape.wav", "--output", "-o", help="Output file"),
):
    """
    🎚️ Generate a mixtape with multiple genres
    
    Creates a continuous mix transitioning between different musical styles.
    
    Example: dj-cli mixtape "lofi,electro,funk" --bars 16 -o my_mixtape.wav
    """
    from src.continuous import ContinuousGenerator
    
    genre_list = [g.strip() for g in genres.split(',')]
    
    console.print(f"[bold cyan]🎚️ Creating mixtape with {len(genre_list)} genres[/bold cyan]")
    console.print(f"[dim]Genres: {', '.join(genre_list)}[/dim]")
    console.print(f"[dim]Bars per genre: {bars_each} | Transitions: {transitions}[/dim]\n")
    
    try:
        generator = ContinuousGenerator()
        
        with console.status("[bold cyan]Generating mixtape..."):
            mixtape = generator.generate_mixtape(genre_list, bars_each, transitions)
        
        console.print("[cyan]💾 Exporting mixtape...[/cyan]")
        mixtape.export(output, format="wav")
        
        console.print(f"[bold green]✓ Mixtape saved to {output}[/bold green]")
        console.print(f"[dim]Total duration: {len(mixtape) / 1000:.1f} seconds[/dim]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def genres():
    """
    🎼 List available music genres and their characteristics
    """
    table = Table(title="🎵 Available Genres")
    table.add_column("Genre", style="cyan", width=15)
    table.add_column("BPM Range", style="yellow", width=12)
    table.add_column("Style", style="white")
    table.add_column("Best For", style="dim")
    
    genre_info = [
        ("lofi", "70-90", "Chill, jazzy, laid-back", "Study, relax, background"),
        ("electro", "125-135", "Electronic, energetic", "Dancing, workout"),
        ("funk", "100-120", "Groovy, syncopated", "Upbeat vibes"),
        ("relax", "60-80", "Calm, peaceful", "Meditation, sleep"),
        ("ambient", "60-90", "Atmospheric, spacious", "Background, focus"),
        ("synthwave", "125-135", "Retro, 80s inspired", "Driving, nostalgia"),
    ]
    
    for genre, bpm, style, use in genre_info:
        table.add_row(genre, bpm, style, use)
    
    console.print(table)
    console.print()
    console.print("[yellow]💡 Tip:[/yellow] Use [cyan]dj-cli compose --genre <name>[/cyan] to create a track")


@app.command()
def compile(
    jdcli_file: str = typer.Argument(..., help=".jdcli composition file to compile"),
    output: str = typer.Option("output.wav", "--output", "-o", help="Output audio file"),
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show compilation details"),
):
    """
    🎼 Compile a .jdcli composition file into audio
    
    JDCL (JSON DJ Composition Language) allows you to write music like code!
    
    Example:
        dj-cli compile examples/lofi_sunset.jdcli -o my_song.wav
    """
    from src.jdcl_compiler import JDCLCompiler
    
    console.print(f"[cyan]🎵 DJ CLI Compiler v0.4.0[/cyan]")
    console.print()
    
    if not os.path.exists(jdcli_file):
        console.print(f"[red]❌ Error: File not found: {jdcli_file}[/red]")
        raise typer.Exit(1)
    
    if not jdcli_file.endswith('.jdcli'):
        console.print(f"[yellow]⚠ Warning: File should have .jdcli extension[/yellow]")
    
    try:
        compiler = JDCLCompiler()
        audio = compiler.compile_file(jdcli_file, output, verbose=verbose)
        
        console.print()
        console.print(f"[green]✓ Success![/green] Audio compiled to [cyan]{output}[/cyan]")
        
    except Exception as e:
        console.print(f"\n[red]❌ Compilation error: {str(e)}[/red]")
        import traceback
        if verbose:
            console.print(traceback.format_exc())
        raise typer.Exit(1)


@app.command()
def validate(
    jdcli_file: str = typer.Argument(..., help=".jdcli file to validate"),
):
    """
    ✓ Validate a .jdcli composition file
    
    Check for syntax errors and undefined references
    """
    from src.jdcl_parser import JDCLParser
    
    console.print(f"[cyan]Validating {jdcli_file}...[/cyan]")
    console.print()
    
    if not os.path.exists(jdcli_file):
        console.print(f"[red]❌ Error: File not found: {jdcli_file}[/red]")
        raise typer.Exit(1)
    
    try:
        parser = JDCLParser()
        composition = parser.parse_file(jdcli_file)
        
        # Show summary
        parser.print_summary()
        
        # Validate
        is_valid, errors = parser.validate()
        
        console.print()
        if is_valid:
            console.print("[green]✓ Validation passed! No errors found.[/green]")
        else:
            console.print("[red]❌ Validation failed with errors:[/red]")
            for error in errors:
                console.print(f"  • {error}")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Parse error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-V", help="Show version"),
):
    """
    🎵 DJ CLI - Create music using your terminal
    
    A powerful command-line tool for generating, mixing, and manipulating audio.
    """
    if version:
        from src import __version__
        console.print(f"DJ CLI version {__version__}")
        raise typer.Exit()
    
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit(
            "[bold cyan]🎵 DJ CLI - Advanced Music Generator[/bold cyan]\n\n"
            "Create music using your terminal!\n\n"
            "[yellow]🎼 JDCL Composition (NEW!):[/yellow]\n"
            "  dj-cli compile song.jdcli      - Compile .jdcli to audio\n"
            "  dj-cli validate song.jdcli     - Validate composition\n\n"
            "[yellow]🎼 Auto-Composition:[/yellow]\n"
            "  dj-cli compose --genre lofi    - Auto-compose complete tracks\n"
            "  dj-cli auto --duration 120     - Generate continuous music\n"
            "  dj-cli mixtape 'lofi,electro'  - Multi-genre mixtapes\n"
            "  dj-cli genres                  - List available genres\n\n"
            "[yellow]🎹 Manual Creation:[/yellow]\n"
            "  dj-cli generate kick           - Generate sounds\n"
            "  dj-cli beat --pattern trap     - Create beats\n"
            "  dj-cli effect track.wav reverb - Apply effects\n\n"
            "[dim]Use --help with any command for more info[/dim]",
            border_style="cyan"
        ))


if __name__ == "__main__":
    app()
