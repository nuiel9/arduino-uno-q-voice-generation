#!/usr/bin/env python3
"""
Neural TTS using Piper (offline) for Arduino UNO Q
- Uses en_US-amy-medium by default
- Plays through PulseAudio/PipeWire via paplay
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_DIR = os.path.join(PROJECT_DIR, "voices", "en_US-amy-medium")
DEFAULT_MODEL = os.path.join(DEFAULT_MODEL_DIR, "en_US-amy-medium.onnx")
DEFAULT_CONFIG = os.path.join(DEFAULT_MODEL_DIR, "en_US-amy-medium.onnx.json")

# Locate piper binary (supports both bin/piper and bin/piper/piper layouts)
BIN_CANDIDATES = [
    os.path.join(PROJECT_DIR, "bin", "piper"),
    os.path.join(PROJECT_DIR, "bin", "piper", "piper"),
]
PIPER_BIN = next((p for p in BIN_CANDIDATES if os.path.isfile(p) and os.access(p, os.X_OK)), None)

if PIPER_BIN is None:
    print("Error: Piper binary not found. Expected at bin/piper or bin/piper/piper.")
    sys.exit(1)


def synthesize(text: str, output_file: str, model: str = DEFAULT_MODEL, config: str = DEFAULT_CONFIG,
               length_scale: float = 1.0, noise_scale: float = 0.667, noise_w: float = 0.8):
    """
    Run Piper to synthesize speech to a WAV file.
    length_scale: <1.0 faster, >1.0 slower
    noise_scale/noise_w: prosody variation (defaults from Piper CLI)
    """
    env = os.environ.copy()
    cmd = [
        PIPER_BIN,
        "--model", model,
        "--config", config,
        "--length-scale", str(length_scale),
        "--noise-scale", str(noise_scale),
        "--noise-w", str(noise_w),
        "--output_file", output_file,
    ]
    try:
        subprocess.run(cmd, input=text, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Piper synthesis failed: {e}")
        sys.exit(1)


def play_wav(path: str):
    """Play WAV via paplay (fallback to aplay)."""
    player = shutil.which("paplay") or shutil.which("aplay")
    if not player:
        print(f"Audio file saved to: {path}. Install paplay or aplay to play.")
        return
    try:
        subprocess.run([player, path], check=True)
    except subprocess.CalledProcessError:
        print(f"Audio file saved to: {path}. Player failed.")


def main():
    ap = argparse.ArgumentParser(description="Piper TTS wrapper")
    ap.add_argument("text", nargs="*", help="text to speak")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="path to .onnx model")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="path to model .json")
    ap.add_argument("--length-scale", type=float, default=1.0, help="<1 faster, >1 slower")
    ap.add_argument("--noise-scale", type=float, default=0.667)
    ap.add_argument("--noise-w", type=float, default=0.8)
    ap.add_argument("--no-play", action="store_true", help="do not play, only synthesize")
    ap.add_argument("--output", default=os.path.join(tempfile.gettempdir(), "piper.wav"))
    args = ap.parse_args()

    text = " ".join(args.text) if args.text else "Hello from Piper neural TTS on Arduino UNO Q."
    synthesize(text, args.output, model=args.model, config=args.config,
               length_scale=args.length_scale, noise_scale=args.noise_scale, noise_w=args.noise_w)
    if not args.no_play:
        play_wav(args.output)
    else:
        print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
